
import django

django.setup()

#import statements
from googleapiclient import discovery
import httplib2
from oauth2client import client
from digipackDB import DatabaseManager as dbm
 

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
        
    
    
    '''
    Function Name: redeemAuthCode
    Descripion: takes in authCode from mobile app then redeems for credentials. Thenn attempts to
    		 create new student with said credentials using studentId as primary key. In the
    		 case that the student already exists, updates credentials. Returns 1 on success, 0
    		 on failure.
    '''
    def redeemAuthCode( self,   authCode ):
        print("Redeem authcode method entered")
        print("receemAuthCode says authCode is: " + authCode)
        try:
            credentials = client.credentials_from_clientsecrets_and_code(
                self.webClientSecretPath,
                ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/classroom.courses', 'https://www.googleapis.com/auth/classroom.coursework.me', 'https://www.googleapis.com/auth/classroom.announcements', 'https://www.googleapis.com/auth/classroom.guardianlinks.me.readonly'],
                authCode,
                redirect_uri = "https://127.0.0.1:8000/")
            insertResult = self.insertCredentialsToDatabase( credentials )
	    

            return insertResult
        
        except client.FlowExchangeError:
            print("FlowExchangeError caught in redeemAuthCode")
            return 0
        
        
        
    '''
    pathFlag - set to true if credentials are to be taken from file, false for
                string.
    filePath - only needed if pathFlag is true. path to credentials json.
    fileStirng - only needed if pathFlag is false. String containing credentials
                json.
    Returns OAuth2Credentials object.
    '''
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
    
    
    
    
    #Extracts email from credentials for use as primary key, then creates new student row
    def insertCredentialsToDatabase(self, credentials):
        #get student email from credentials
        print("insertCredentials says credentials are " + str(credentials))
        email = credentials.id_token['email']
        jsonString = client.OAuth2Credentials.to_json(credentials)
        result = dbm.addStudent(email, jsonString)
        return result
    
    
    
    
    #pass in student id as primary key, returns credentials JSON as a string
    def getCredentialsFromDatabase(self, studentGmail):
        try:
            credentialsString = dbm.getCredentials(studentGmail)
        except:
            print("AUTH MANAGER GET CREDENTIALS RETURNED FAILURE")
            return 0
        return credentialsString
    
    
    
    

    #takes in Oauth2Credentials object and return GoogleCredentials object
    def convertOAuth2Creds( self, credentials ):
        credentialsString = client.OAuth2Credentials.to_json(credentials)
        return client.GoogleCredentials.from_json(credentialsString)

    '''
    Function Name: redeemIdToken
    Algorithm: Takes in a user's ID token then validates it against Google's authentication
               servers. In the case that the ID token is valid, returns the associated 
               gmail address. Otherwise, returns 0 for failure.
    '''
    def redeemIdToken(self, idToken):
        pass




def get_gdrive_auth(userid):
    return userid
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
