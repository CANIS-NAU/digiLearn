# local dependencies
from com.DigiLearn.DigitalBackpack.REST.JSONBuilders import DigiJsonBuilder
from com.DigiLearn.DigitalBackpack.REST.Interfaces.GDriveInterface import create_service
from com.DigiLearn.DigitalBackpack.Auth.AuthenticationManager import get_gdrive_auth
from com.DigiLearn.DigitalBackpack.src.DataManagers.DataManager import store_file
from com.DigiLearn.DigitalBackpack.err import DigiExceptions
# python dependencies
import io
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
def get_file_metadata(user_auth: dict, file_id: str):
    # initialize "service"
    #   do some auth, probably need to mess w/ this in GDriveInterface
    gdrive_auth = user_auth  # get_gdrive_auth(user_auth['user_id'])
    service = create_service(gdrive_auth, _API_NAME, _API_VERSION, _SCOPES)
    # make request for file metadata
    request = service.files().get(fileId=file_id, fields=_FILE_FIELDS).execute()
    # if the file hasn't been moved to trash by the user
    if not request['trashed']:
        # build the file object with no local_file_path, can be added with a second call to get_file
        try:
            filemeta = DigiJsonBuilder.create_file(name=request['name'], drive_id=request['id'], class_id=None,
                                                   local_file_path=None, drive_path=request['parents'], classpath=None,
                                                   size=request['size'])
        except KeyError as k:
            if k == 'size':
                filemeta = DigiJsonBuilder.create_file(name=request['name'], drive_id=request['id'], class_id=None,
                                                       local_file_path=None, drive_path=request['parents'],
                                                       classpath=None,
                                                       size=None)
        # add the other stuff we get from gdrive to the object, don't necessarily need it but might be useful eventually
        filemeta.update({'mimeType': request['mimeType'], 'capabilities': request['capabilities']})
        # return metadata
        return filemeta
    else:
        # throw an error here
        raise DigiExceptions.TrashedFileError(file_id, '%s file has been moved to trash by user and cannot be accessed'
                                              % file_id)


# gets a singular file from google drive, for multiple files call in a loop.
def get_file(user_auth, file_dict):
    # do auth and create service
    gdrive_auth = get_gdrive_auth(user_auth['user_id'])
    service = create_service(gdrive_auth, _API_NAME, _API_VERSION, _SCOPES)
    # get the file itself
    request = service.files().get_media(fileID=file_dict['drive_id'])
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)

    done = False

    while not done:
        status, done = downloader.next_chunk()
        # log the progress somewhere
        print('download progress {0}'.format(status.progress() * 100))

    fh.seek(0)
    # store it on the server somewhere
    #   this will be done by the datamanager
    #   pass the recieved string of bits to the datamanager with location,
    #   driveid(just gonna use these for naming ease), and ya well figure that out when we get there
    file_path = store_file(user_auth, file_dict, fh, "drive_storage")
    file_dict['localpath'] = file_path
    return file_dict


# because of the way that the gdrive API works, this only returns the shared drives for a user
#   my guess is that this is because every user is assumed to (and required to) have their own drive at drive#my-drive
#   //might be drive#mydrive idrk
def get_drive_list(user_auth):
    # do auth and create service
    gdrive_auth = get_gdrive_auth(user_auth['user_id'])
    service = create_service(gdrive_auth, _API_NAME, _API_VERSION, _SCOPES)
    # get list of drive objects (this is like, mydrive, shared drives, etc. no files)
    # with all list getters, there is a list_next(prev_req, prev_resp) that can be used, gonna need a while loop
    # for those in the future but for now well just do one page of results
    gdrive_list = service.drives().list()
    mydrive = get_file_list(user_auth, 'my-drive')
    drivelist = [mydrive]
    for drive in gdrive_list['drives']:
        driveobj = DigiJsonBuilder.create_drive(drive['id'], get_file_list(user_auth, drive['id']),
                                                drive['capabilities'])
        driveobj = _get_drive_permissions(driveobj, drive)
        drivelist.append(driveobj)
    # convert to digijson
    return drivelist


def get_file_list(user_auth, driveid):
    filelist = []
    # get list of files in the specified drive
    gdrive_auth = user_auth  # get_gdrive_auth(user_auth['user_id'])
    service = create_service(gdrive_auth, _API_NAME, _API_VERSION, _SCOPES)
    # see get_drive_list
    if driveid == 'my-drive':
        gdrive_list = service.files().list(fields="files(" + _FILE_FIELDS + ")").execute()
    else:
        gdrive_list = service.files().list(fields="files(" + _FILE_FIELDS + ")", driveId=driveid,
                                           supportsAllDrives=True, includeItemsFromAllDrives=True, corpora='drive'
                                           ).execute()

    for file in gdrive_list['files']:
        if not file['trashed']:
            try:
                filemeta = DigiJsonBuilder.create_file(name=file['name'], drive_id=file['id'], class_id=None,
                                                       local_file_path=None, drive_path=file['parents'], classpath=None,
                                                       size=file['size'])
            except KeyError as k:
                if k == 'size':
                    filemeta = DigiJsonBuilder.create_file(name=file['name'], drive_id=file['id'], class_id=None,
                                                           local_file_path=None, drive_path=file['parents'],
                                                           classpath=None, size=None)
                else:
                    # throw an error
                    return k
            try:
                filemeta.update({'mimeType': file['mimeType']})
                filemeta.update({'capabilities': file['capabilities']})
            except KeyError as k:
                if k == 'mimeType':
                    try:
                        filemeta.update({'capabilities': file['capabilities']})
                    except KeyError as k1:
                        # throw an error? or just log?
                        return None
                if k == 'capabilities':
                    filemeta.update({'capabilities': None})
                    # should probably do some logging here...
            filelist.append(filemeta)
    # convert to digijson
    return filelist


def get_file_comments(user_auth, fileid):
    comments = []
    # do auth and create service
    gdrive_auth = get_gdrive_auth(user_auth['user_id'])
    service = create_service(gdrive_auth, _API_NAME, _API_VERSION, _SCOPES)
    # get comments on the file
    file_comm_list = service.comments.list(fileId=fileid)
    # just create a (python)json object
    # because json i can just slap that shit in there and not care about it lol
    comm = {
        "comments": file_comm_list['comments']
    }
    return comm


def upload_file(user_auth, file_dict, fileobj, drivepath):
    uploadjson = None
    gdrive_auth = get_gdrive_auth(user_auth['user_id'])
    service = create_service(gdrive_auth, _API_NAME, _API_VERSION, _SCOPES)
    # get the (local) file and needed data to upload to drive
    # create drive json
    # make sure file got uploaded correctly/completely
    uploadsuccess = service.files().create(body='json object', media_body='filepath')
    return uploadsuccess


def _get_drive_permissions(drive, gdrive):
    # get the permissions that the user has for the drive
    permissions = {
        "restrictions": gdrive['restrictions'],
        "capabilities": gdrive['capabilities']
    }
    drive.update(permissions)  # works like append
    return drive


def _beforeanything(user_auth):
    interpretername = "Google Drive Interpreter"

    # i need to figure out more testing to do here and how to properly handle errors
    if type(user_auth) != dict:
        errstr = "Incorrect Data Type for Google Drive Interpreter User Authentication variable"
        # throw an error about this
        return False
    if "installed" not in user_auth:
        errstr = "User Authentication has no value 'installed', no Google Drive authentication values for this user"
        # throw an error about this
        return False
    if type(user_auth["installed"]) != dict:
        errstr = "User Authentication values either not set, or set incorrectly for Google Drive Interpreter"
        # throw
        return False
    return True
