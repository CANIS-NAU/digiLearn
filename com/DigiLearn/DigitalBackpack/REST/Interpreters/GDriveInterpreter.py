# local dependencies
from com.DigiLearn.DigitalBackpack.REST.JSONBuilders import DigiJsonBuilder
from com.DigiLearn.DigitalBackpack.REST.Interfaces.GDriveInterface import create_service
from com.DigiLearn.DigitalBackpack.Auth.AuthenticationManager import get_gdrive_auth
from com.DigiLearn.DigitalBackpack.src.DataManagers.DataManager import store_file
# python dependencies
import io
# google dependencies
from googleapiclient.http import MediaIoBaseDownload

_API_NAME = 'drive'
_API_VERSION = 'v3'
_SCOPES = ['https://www.googleapis.com/auth/drive']
# this might need more eventually but for now this is all i need
_FILE_FIELDS = 'name, id, parents, mimeType, description, trashed, size, contentRestrictions'


# this needs some work with the user_auth stuff but other than that (and some error checking stuff)
# its done
def get_file_metadata(user_auth: dict, file_id: str):
    # initialize "service"
    #   do some auth, probably need to mess w/ this in GDriveInterface
    gdrive_auth = get_gdrive_auth(user_auth['user_id'])
    service = create_service(gdrive_auth, _API_NAME, _API_VERSION, _SCOPES)
    # make request for file metadata
    request = service.files().get(fileId=file_id, fields=_FILE_FIELDS)
    # if the file hasn't been moved to trash by the user
    if not request['trashed']:
        # build the file object with no local_file_path, can be added with a second call to get_file
        filemeta = DigiJsonBuilder.create_file(name=request['name'], drive_id=request['id'], class_id=None,
                                               local_file_path=None, drive_path=request['parents'], classpath=None,
                                               size=request['size'])
        # add the other stuff we get from gdrive to the object, don't necessarily need it but might be useful eventually
        filemeta.update({'mimeType': request['mimeType'], 'description': request['description'],
                         'contentRestrictions': request['contentRestrictions']})
        # return metadata
        return filemeta
    else:
        # throw an error here
        return None


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
    file_path = store_file(user_auth, file_dict, fh, "need to make up a storage medium key somehwere or chage the DM")
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
    gdrive_list = service.drives().list()

    # convert to digijson
    return drivelist


def get_file_list(userauth, driveid):
    filelist = None
    # get list of files in the specified drive
    # convert to digijson
    return filelist


def get_file_comments(userauth, fileid):
    comments = None
    # get comments on the file
    # just create a (python)json object
    # because json i can just slap that shit in there and not care about it lol
    comm = {
        "comments": comments
    }
    return comm


def upload_file(userauth, fileobj, drivepath):
    uploadjson = None
    # get the (local) file and needed data to upload to drive
    # create drive json
    # create POST request
    # slap it all together
    # send it out the socket
    # probably gonna need a from Google import something up at the top
    # make sure file got uploaded correctly/completely
    uploadsuccess = None
    return uploadsuccess


def _get_drive_permissions(drive, userauth):
    permissions = None
    # get the permissions that the user has for the drive
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
