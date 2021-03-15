
#
import django

django.setup()


#import statements
from googleapiclient import discovery
import httplib2
from oauth2client import client
import DatabaseManager as dbm
 

'''
Class Name: AuthenticationManager
Description: Manages the exchange of Auth codes for Oauth2 credentials objects, 
             which can then be used to make api requests on the behalf of the user.
             Also manages the conversion from credentials json to the OAuth2Credentials
             object for database management.
Constructor: Constructor takes in the path to the web server's client secret file.
'''
class AuthenticationManager:
    
    
    webClientSecretPath = ""
    
    
    def __init__( self, webClientSecretPath ):
        self.webClientSecretPath = webClientSecretPath
        
    
    
    
    def redeemAuthCode( self,   authCode ):
        try:
            credentials = client.credentials_from_clientsecrets_and_code(
                self.webClientSecretPath,
                ['https://www.googleapis.com/auth/drive'],
                authCode,
                redirect_uri = "https://127.0.0.1:8080/")

            return credentials
        
        except client.FlowExchangeError:
            return 0
        
        
        

    def getCredentialsFromFileOrString(self, pathFlag, filePath="", fileString="" ):
        
        if( pathFlag == True ):
            credentialsFile = open(filePath, mode='r')
            credentialsString = credentialsFile.read()
            credentialsFile.close()
        
        else:
            credentialsString = fileString
            
        #convert json to credentials object
        credentialsObject = client.OAuth2Credentials.from_json(credentialsString)
        
        #return credentials object
        return credentialsObject
    
    
    
    def insertCredentialsToDatabase(self, credentials):
        #get student email from credentials
        email = credentials.id_token['email']
        jsonString = client.OAuth2Credentials.to_json(credentials)
        dbm.addStudent(email, jsonString)
    
    
    
    def getCredentialsFromDatabase(self, studentGmail):
        credentialsString = dbm.getCredentials(studentGmail)
        credentialsObject = self.getCredentialsFromFileOrString(False, fileString=credentialsString)
        return credentialsObject
    
    

    #takes in Oauth2Credentials object and return GoogleCredentials object
    def convertOAuth2Creds( self, credentials ):
        credentialsString = client.OAuth2Credentials.to_json(credentials)
        return client.GoogleCredentials.from_json(credentialsString)





'''


am = AuthenticationManager('/home/matrian/Desktop/django/digipack/digipackDB/client_secret_867834249770-gqs8vn9kq50u4o99im41eoa5odto9hfu.apps.googleusercontent.com.json')

#get credentials from file
credentials = am.getCredentialsFromFileOrString(True, filePath = '/home/matrian/Desktop/django//digipack/digipackDB/credentials.json')

print("From File: ")
print(credentials.access_token)



#get credentials from string
credentialsFile = open('/home/matrian/Desktop/django/digipack/digipackDB/credentials.json', mode='r')
credentialsString = credentialsFile.read()
credentialsFile.close()

credentials = am.getCredentialsFromFileOrString(False, fileString = credentialsString)
print("\nFrom String: ")
print(credentials.access_token)



#insertCredentialsToDatabase test
am.insertCredentialsToDatabase(credentials)


#getCredentialsFromDatabase test
credentials = am.getCredentialsFromDatabase("team.digilearn@gmail.com")
print("\nFrom Database: ")
print(credentials.access_token)




#convert to google credentials
googleCredentials = am.convertOAuth2Creds( credentials )


print("\nFrom Google Credentials: ")
print(client.GoogleCredentials.to_json(googleCredentials))





'''











