from com.DigiLearn.DigitalBackpack.REST.Interpreters import GDriveInterpreter
from com.DigiLearn.DigitalBackpack.Server.Django import AuthenticationManager as am



cred = 'webClientSecret.json'
fileid = '1ZBc6zCt0uPDl2YVC16E0aLWik1I5PzBWxgzO_XdhMDw'

meta = GDriveInterpreter.get_file_list(cred, "my-drive")

print(meta)
