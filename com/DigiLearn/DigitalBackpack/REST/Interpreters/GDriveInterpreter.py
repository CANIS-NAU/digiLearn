import json
from DigiLearn.DigitalBackpack.REST.JSONBuilders import DigiJsonBuilder
from DigiLearn.DigitalBackpack.REST import GDriveInterface


_API_NAME = 'drive'
_API_VERSION = 'v3'
_GOOGLE_URI = 'https://www.googleapis.com/'
_SCOPES = 'https://www.googleapis.com/auth/drive'
# this might need more eventually but for now this is all i need
_FILE_FIELDS = 'name, id, parents, mimeType, description, trashed, size, contentRestrictions'
_GDRIVE_INTERFACE = None


# this needs some work with the user_auth stuff but other than that (and some error checking stuff)
# its done
def getfilemetadata(user_auth: dict, fileid: str):
    # make sure we have everything we need to fulfil the request
    _beforeanything(user_auth)

    #   get keys from user auth for GET building
    api_key = user_auth["installed"]["something else idk need to figure this out"]  # see: client_secret.json somewhere
    access_token = user_auth["installed"]["see above"]  # **********************

    # build request  # i believe the Accept: application/json only gets the metadata here
    request = "GET %s/%s/%s/files/%s?fields=%s&key=%s HTTP/1.1\r\n\r\nAuthorization: %s\nAccept: application/json" \
              % (_GOOGLE_URI, _API_NAME, _API_VERSION, fileid, _FILE_FIELDS, api_key, access_token)
    #               scopes here is the wrong liink
    # send the metadata request
    # get file from drive
    response = GDriveInterface.getrequest(request)

    # socket.recv() returns a bytes object
    # bytes.decode() converts to str, defaults to ASCII
    http_response = response.decode()
    http_response_len = len(http_response)

    # if the response went through and we got what we wanted
    #       this is now handled by the GDriveInterface

    # parse http_response for the metadata we want
    i = 0
    # while the next three characters arent {\r\n (start of json) and we haven't reached the end of the file
    while i+2 < http_response_len and http_response[i:i+2] != "{\r\n":
        i += 1  # iterate
    # hit the first instance of {\n and so now we load the rest of the response to a dict/json
    drive_response = json.loads(http_response[i:])

    if drive_response["trashed"] != "true":
        # well have whatever is calling this ask for the actual file in a separate call, this just gets metadata
        local_file_path = None
        # take the metadata about the file and create digijson
        name = drive_response["name"]
        driveid = drive_response["id"]
        classid = None
        drivepath = drive_response["parents"]
        classpath = None
        size = drive_response["size"]
        fileobj = DigiJsonBuilder.createfile(name, driveid, classid, local_file_path, drivepath, classpath, size)
        # the things added below are not a part of the official "digilearn" json structure but could be useful
        fileobj.update(drive_response["mimeType"])
        fileobj.update(drive_response["description"])
        fileobj.update(drive_response["contentRestrictions"])
        return fileobj
    else:
        # throw an error here about the file being deleted by the user and return none
        return None


def getfile(user_auth, filedict):
    _beforeanything(user_auth)
    # then for the actual file? i think?
    #   the API says you can GET files content buuut im gonna have to test that
    #   cause currently i cant figure that out w/ just the documentation (through a GET request, their api does it tho)
    #   but assume we have to send a separate request for the actual file
    #       for now (unless caitlin and i can figure this out) i think we might have to use the Google libraries
    #       to do this
    # store it on the server somewhere
    #   this will be done by the datamanager
    #   pass the recieved string of bits to the datamanager with location,
    #   driveid(just gonna use these for naming ease), and ya well figure that out when we get there
    return None


def getdrivelist(userauth):
    drivelist = None
    # get list of drive objects (this is like, mydrive, shared drives, etc. no files)
    #   ?fields=files(_FILE_FIELDS)
    # convert to digijson
    return drivelist


def getfilelist(userauth, driveid):
    filelist = None
    # get list of files in the specified drive
    # convert to digijson
    return filelist


def getfilecomments(userauth, fileid):
    comments = None
    # get comments on the file
    # just create a (python)json object
    # because json i can just slap that shit in there and not care about it lol
    comm = {
        "comments": comments
    }
    return comm


def uploadfile(userauth, fileobj, drivepath):
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


def _getdrivepermissions(drive, userauth):
    permissions = None
    # get the permissions that the user has for the drive
    drive.update(permissions)  # works like append
    return drive


def _beforeanything(user_auth):
    interpretername = "Google Drive Interpreter"

    # i need to figure out how the  imma do this

    if type(_DATA_MANAGER) != type():  # fill this out when data manager is built
        errstr = "No Data Manager set for Google Drive Interpreter"
        # throw an error about this
        return False
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
