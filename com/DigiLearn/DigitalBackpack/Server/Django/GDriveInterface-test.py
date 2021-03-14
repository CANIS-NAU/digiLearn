from REST.Interpreters import GDriveInterpreter
import AuthenticationManager as am


file_id = '1a3RBXtm9P1LnnIboyUIKGQOjYvzLXkhG'
user_email = 'team.digilearn@gmail.com'
#instantiate AuthenticationManager
am = am.AuthenticationManager('webClientSecret.json')

#create new student with given credentials
credentials = am.getCredentialsFromFileOrString(True, 'Oauth2Credentials.json')
am.insertCredentialsToDatabase(credentials)

cred = 'webClientSecret.json'
fileid = '1ZBc6zCt0uPDl2YVC16E0aLWik1I5PzBWxgzO_XdhMDw'



meta = GDriveInterpreter.get_file_list(cred, user_email,"my-drive")
print(meta)


meta = GDriveInterpreter.get_file_metadata(cred, user_email, file_id)
print("\n\n" + str(meta))













