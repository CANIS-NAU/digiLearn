from com.DigiLearn.DigitalBackpack.REST.Interpreters import GDriveInterpreter

cred = 'credentials.json'
fileid = '1SML1QNgHzt-iUPTjfmV__UzPdg7xGErq'

meta = GDriveInterpreter.get_file_list(cred, "my-drive")

print(meta)
