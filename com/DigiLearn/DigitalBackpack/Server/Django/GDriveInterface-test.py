from REST.Interpreters import GDriveInterpreter
import AuthenticationManager as am


#instantiate AuthenticationManager
am = am.AuthenticationManager('webClientSecret.json')

#create new student with given credentials
credentials = am.getCredentialsFromFileOrString(True, 'Oauth2Credentials.json')
am.insertCredentialsToDatabase(credentials)

cred = 'webClientSecret.json'
fileid = '1ZBc6zCt0uPDl2YVC16E0aLWik1I5PzBWxgzO_XdhMDw'

meta = GDriveInterpreter.get_file_list(cred, 'team.digilearn@gmail.com',"my-drive")


print(meta)
