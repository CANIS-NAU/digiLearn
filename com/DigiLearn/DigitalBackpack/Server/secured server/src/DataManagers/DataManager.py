import os

_STORAGE_MEDIUMS = {'drive_storage': 'DriveStorage'}
_DATABASES = None
_STORAGE_MANAGER = None
_DATABASE_MANAGER = None
_MAX_STORAGE_TIME = None


def run():
    _beforeanything()
    # run through all storage mediums and remove stuff thats too old
    # remove all those entries from the database
    # handle errors
    # return a log message if successful or not


# i believe the file will always come in as a bytes-like object
# not sure tho, gonna need testing for this
def store_file(user_obj: dict, fileobj: dict, file: bytes, storage_medium_key: str):
    # make sure all the parameters are filled correctly
    # file obj has all the parameters needed to store this
    #       mostly name, size, type
    # store on the server
    # *****this (or possibly whatever is sending the request to store something)
    # also needs to check if the file json associated has a drive id, and if not get one from google so we can upload
    # if necessary
    # so its currently saving stuff to
    filepath = './' + _STORAGE_MEDIUMS[storage_medium_key] + '/' #+ user_obj #["auth"]["digilearn"]["userid"]

    try:
        with open(os.path.join(filepath, fileobj["name"]), 'wb') as f:
            f.write(file.read())  # this doesnt work this way, need to fix
            f.close()
            return True
    except:
        # handle exception(s), need multiple of these
        print("an exception occured")
        return False


def _beforeanything():
    # make sure all of the global variables are filled in correctly
    # throw errors if not
    return None