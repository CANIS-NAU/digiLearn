# local dependencies
from REST.JSONBuilders import DigiJsonBuilder
from REST.JSONBuilders import GDriveJsonBuilder
from REST.Interfaces.GoogleInterface import create_service
from REST.Auth.AuthenticationManager import get_gdrive_auth
from REST.src.DataManagers.DataManager import store_file
from REST.err import DigiExceptions

# python dependencies
import io
import os
import mimetypes
# google dependencies
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload

_API_NAME = 'drive'
_API_VERSION = 'v3'
_SCOPES = ['https://www.googleapis.com/auth/drive']
# this might need more eventually but for now this is all i need
_FILE_FIELDS = 'name, id, parents, mimeType, description, trashed, size, capabilities'
_DRIVE_FIELDS = ''


# this needs some work with the user_auth stuff but other than that (and some error checking stuff)
# its done
def get_file_metadata(user_auth: dict, user_email, file_id: str):
    # initialize "service"
    #   do some auth, probably need to mess w/ this in GDriveInterface
    gdrive_auth = user_auth  # get_gdrive_auth(user_auth['user_id'])
    service = create_service(gdrive_auth, _API_NAME, _API_VERSION, _SCOPES, user_email=user_email)
    # make request for file metadata
    request = service.files().get(fileId=file_id, fields=_FILE_FIELDS).execute()
    fname = request["name"] if "name" in request else "<No File Name>"
    did = request["id"] if "id" in request else "<No Drive ID>"
    cid = None
    lfp = None
    dpath = request["parents"] if "parents" in request else "<No Drive Path>"
    cpath = None
    size = request["size"] if "size" in request else "<No Size>"
    mtp = request["mimeType"] if "mimeType" in request else None
    cap = request["capabilities"] if "capabilities" in request else None

    filemeta = DigiJsonBuilder.create_file(fname, did, cid, lfp, dpath, cpath, size)
    filemeta.update({'mimeType': mtp, 'capabilities': cap})

    return filemeta


# gets a singular file from google drive, for multiple files call in a loop.
def get_file(user_auth: dict, user_email, file_dict):
    # do auth and create service
    gdrive_auth = user_auth #get_gdrive_auth(user_auth['user_id'])
    service = create_service(gdrive_auth, _API_NAME, _API_VERSION, _SCOPES, user_email=user_email)
    # get the file itself
    try:
        request = service.files().get_media(fileId=file_dict['driveID'])
    except Exception:
        request = service.files().export_media(fileId=file_dict['driveID'], mimeType = file_dict["mimeType"])

     #.get_media(fileId=file_dict['id'])
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)

    done = False

    while not done:
        status, done = downloader.next_chunk()
        # log the progress somewhere
        #print('download progress {0}'.format(status.progress() * 100))

    fh.seek(0)
    # store it on the server somewhere
    #   this will be done by the datamanager
    #   pass the recieved string of bits to the datamanager with location,
    #   driveid(just gonna use these for naming ease), and ya well figure that out when we get there
    sfres = store_file(user_auth, file_dict, fh, "drive_storage")
    if sfres:
        file_path = './DriveStorage/' + file_dict["name"]
        file_dict['localpath'] = file_path
        file_dict['filesize'] = os.path.getsize(file_path)
        mt = mimetypes.guess_type(file_path, strict=True)
        file_dict.update({"mimetype": mt[0]})
    return file_dict


# because of the way that the gdrive API works, this only returns the shared drives for a user
#   my guess is that this is because every user is assumed to (and required to) have their own drive at drive#my-drive
#   //might be drive#mydrive idrk
def get_drive_list(user_auth, user_email):
    # do auth and create service
    gdrive_auth = user_auth  # get_gdrive_auth(user_auth['user_id'])
    service = create_service(gdrive_auth, _API_NAME, _API_VERSION, _SCOPES, user_email=user_email)

    # get list of drive objects (this is like, mydrive, shared drives, etc. no files)
    # with all list getters, there is a list_next(prev_req, prev_resp) that can be used, gonna need a while loop
    # for those in the future but for now well just do one page of results
    gdrive_list = service.drives().list()
    mydrive = get_file_list(user_auth, user_email, 'my-drive')
    drivelist = [mydrive]
    for drive in gdrive_list['drives']:
        did = drive['id'] if 'id' in drive else None
        cap = drive['capabilities'] if 'capabilities' in drive else None
        fl = get_file_list(user_auth, did)
        driveobj = DigiJsonBuilder.create_drive(did, fl, cap)
        driveobj = _get_drive_permissions(driveobj, drive)
        drivelist.append(driveobj)
    # convert to digijson
    return drivelist


def get_file_list(user_auth, user_email, driveid):
    filelist = []
    # get list of files in the specified drive
    gdrive_auth = user_auth  # get_gdrive_auth(user_auth['user_id'])
    service = create_service(gdrive_auth, _API_NAME, _API_VERSION, _SCOPES, user_email=user_email)

    # see get_drive_list
    if driveid == 'my-drive':
        gdrive_list = service.files().list(fields="files(" + _FILE_FIELDS + ")").execute()
    else:
        gdrive_list = service.files().list(fields="files(" + _FILE_FIELDS + ")", driveId=driveid,
                                           supportsAllDrives=True, includeItemsFromAllDrives=True, corpora='drive'
                                           ).execute()
    for file in gdrive_list['files']:
        if "mimeType" in file and file["mimeType"] != 'application/vnd.google-apps.folder':
            if not file["trashed"]:
                fname = file['name'] if 'name' in file else "<No File Name>"
                fid = file['id'] if 'id' in file else "<No File ID>"
                cid = None
                lfp = None
                dpath = file["parents"] if "parents" in file else "<No Drive Path>"
                cpath = None
                size = file["size"] if "size" in file else "<No Size>"
                cap = file["capabilities"] if "capabilities" in file else None
                mtp = file["mimeType"] if "mimeType" in file else None

                filemeta = DigiJsonBuilder.create_file(fname, fid, cid, lfp, dpath, cpath, size)
                filemeta.update({'mimeType': mtp})
                filemeta.update({'capabilities': cap})

                filelist.append(filemeta)
    # convert to digijson
    return filelist


def get_file_comments(user_auth, user_email, fileid):
    comments = []
    # do auth and create service
    gdrive_auth = user_auth  # get_gdrive_auth(user_auth['user_id'])
    service = create_service(gdrive_auth, _API_NAME, _API_VERSION, _SCOPES, user_email=user_email)
    # get comments on the file
    file_comm_list = service.comments.list(fileId=fileid)
    # just create a (python)json object
    # because json i can just slap that shit in there and not care about it lol
    comm = {
        "comments": file_comm_list['comments'] if 'comments' in file_comm_list else None
    }
    return comm


def upload_file(user_auth, user_email, file_dict, drivepath=None):
    uploadjson = None
    gdrive_auth = user_auth  # get_gdrive_auth(user_auth['user_id'])
    service = create_service(gdrive_auth, _API_NAME, _API_VERSION, _SCOPES, user_email=user_email)
    # get the (local) file and needed data to upload to drive
    filepath = file_dict["localpath"]
    # create drive json
    gdrivejson = GDriveJsonBuilder.createfilejson(file_dict)
    mt = file_dict['mimetype'] if 'mimetype' in file_dict else mimetypes.guess_type(filepath, strict=True)[0]
    if 'mimetype' not in file_dict:
        file_dict.update({"mimetype": mt})
    # create media file upload
    media = MediaFileUpload(filepath, mimetype=mt)
    # upload file
    fid = service.files().create(body=gdrivejson, media_body=media, fields='id').execute()
    file_dict["driveID"] = fid['id'] if 'id' in fid else None
    if file_dict["driveID"] != None:
        return file_dict
    return None


def _get_drive_permissions(drive, gdrive):
    # get the permissions that the user has for the drive
    permissions = {
        "restrictions": gdrive['restrictions'] if 'restrictions' in gdrive else None,
        "capabilities": gdrive['capabilities'] if 'capabilities' in gdrive else None
    }
    drive.update(permissions)  # works like append
    return drive
