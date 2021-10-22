
import django

django.setup()

#import statements
from googleapiclient import discovery
import httplib2
from oauth2client import client
from application import models as dbm
import traceback
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.authtoken.models import Token
 

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
        print("[redeemAuthCode]- Method entered")
        print("[redeemAuthCode]- authCode is: " + authCode)
        try:
            credentials = client.credentials_from_clientsecrets_and_code(
                self.webClientSecretPath,
                ['profile', 'email', 'https://www.googleapis.com/auth/drive',
                'https://www.googleapis.com/auth/classroom.courses', 
                'https://www.googleapis.com/auth/classroom.coursework.me',
                'https://www.googleapis.com/auth/classroom.announcements', 
                'https://www.googleapis.com/auth/classroom.guardianlinks.me.readonly'],
                authCode,
                redirect_uri = "https://127.0.0.1:8000/")
            insertResult = self.insertCredentialsToDatabase( credentials )
	    

            return insertResult
        
        except client.FlowExchangeError:
            print("[redeemAuthCode]- FlowExchangeError caught" +
                                  "-- likely because student already registered")
            traceback.print_exc()
            return 0
        
        
    '''
    Function Name: redeemAuthCode
    Descripion: takes in authCode from mobile app then redeems for credentials. Thenn attempts to
    		 create new student with said credentials using studentId as primary key. In the
    		 case that the student already exists, updates credentials. Returns 1 on success, 0
    		 on failure.
    '''
    def redeemAuthCodeWeb( self,   authCode ):
        print("[redeemAuthCode]- Method entered")
        print("[redeemAuthCode]- authCode is: " + authCode)
        try:
            credentials = client.credentials_from_clientsecrets_and_code(
                self.webClientSecretPath,
                ['profile', 'email', 'https://www.googleapis.com/auth/drive',
                'https://www.googleapis.com/auth/classroom.courses', 
                'https://www.googleapis.com/auth/classroom.coursework.me',
                'https://www.googleapis.com/auth/classroom.announcements', 
                'https://www.googleapis.com/auth/classroom.guardianlinks.me.readonly'],
                authCode)
            insertResult = self.insertCredentialsToDatabase( credentials )
	    

            return insertResult
        
        except client.FlowExchangeError:
            print("[redeemAuthCode]- FlowExchangeError caught" +
                                  "-- likely because student already registered")
            traceback.print_exc()
            return 0
        
        
    '''
    Function Name: redeemAuthCode
    Descripion: takes in authCode from mobile app then redeems for credentials. Thenn attempts to
    		 create new student with said credentials using studentId as primary key. In the
    		 case that the student already exists, updates credentials. Returns 1 on success, 0
    		 on failure.
    '''
    def redeemAuthCodeTeacher( self,   authCode ):
        print("[redeemAuthCode]- Method entered")
        print("[redeemAuthCode]- authCode is: " + authCode)
        try:
            credentials = client.credentials_from_clientsecrets_and_code(
                self.webClientSecretPath,
                ['profile', 'email', 'https://www.googleapis.com/auth/drive',
                'https://www.googleapis.com/auth/classroom.courses', 
                'https://www.googleapis.com/auth/classroom.coursework.me',
                'https://www.googleapis.com/auth/classroom.announcements', 
                'https://www.googleapis.com/auth/classroom.guardianlinks.me.readonly'],
                authCode)
            insertResult = self.insertCredentialsToDatabaseTeacher( credentials )
	    

            return insertResult
        
        except client.FlowExchangeError:
            print("[redeemAuthCode]- FlowExchangeError caught" +
                                  "-- likely because student already registered")
            traceback.print_exc()
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
        #get student id from credentials
        #print("[insertCredentialsToDatabase]- Credentials are: " + str(credentials))
        userId = credentials.id_token["sub"]
        
        print("[insertCredentialsToDatabase]- userId is: " + str(userId))
        #insert credentials + userId to database
        jsonString = client.OAuth2Credentials.to_json(credentials)
        result = dbm.addStudent(userId, jsonString)
        return result
    
    
    #Extracts email from credentials for use as primary key, then creates new student row
    def insertCredentialsToDatabaseTeacher(self, credentials):
        #get student id from credentials
        #print("[insertCredentialsToDatabase]- Credentials are: " + str(credentials))
        userId = credentials.id_token["sub"]
        
        print("[insertCredentialsToDatabaseTeacher]- userId is: " + str(userId))
        #insert credentials + userId to database
        jsonString = client.OAuth2Credentials.to_json(credentials)
        result = dbm.addTeacher(userId, jsonString)
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
    Algorithm: Takes in a user's ID Token (a simple Django token generated and 
                distriuted by this server) and uses it to obtain the user's ID. 
                Returns said ID. If the token is not found, returns 0 for failure.
    '''
    def redeemIdToken(this, idToken):
        try:
            userId = str(Token.objects.get(key=idToken).user.username)
            print("[redeemIdToken]- userId is: " + userId)
            return userId
            
        except Token.DoesNotExist:
            print("[redeemIdToken]- value error; returning failure." )
            # Invalid token, return False
            return 0
        



def get_gdrive_auth(userid):
    return userid
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
