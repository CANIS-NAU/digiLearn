from REST.Interpreters import GDriveInterpreter

def GetDriveList():

    cred = 'credentials.json'

    file_list = GDriveInterpreter.get_file_list(cred, "my-drive")

    return file_list

