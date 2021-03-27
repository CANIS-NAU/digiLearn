from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse
from django.http import HttpRequest
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from Auth import AuthenticationManager #TODO: add am to folder and change pathing on this import?
import json
from REST.Interpreters import GDriveInterpreter
from digipackDB import DatabaseManager
import pathlib
from django.http import FileResponse
import mimetypes
import os

#@login_required(login_url='/login')
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

@api_view(['POST'])
@parser_classes([JSONParser])
@ensure_csrf_cookie
def MobileAuth(request):
    #pass webclientsecret to auth manager
    AM = AuthenticationManager.AuthenticationManager('webClientSecret.json')

    #load the json data
    auth_json = request.data

    #pass access token to the auth manager
    credentials = AM.redeemAuthCode(auth_json["googleAccessToken"])

    return JsonResponse({'Result' : 'ACK'})

#TODO: add a restriction that only allows a user to access their own url
@api_view(['GET'])
def InitDrive(request, user):
    #pass webclientsecret to auth manager
    #AM = AuthenticationManager.AuthenticationManager('webClientSecret.json')

    #retrieve database creds
    #credentials = AM.getCredentialsFromDatabase(user)

    secretFile = open("webClientSecret.json", "r")
    secretText = secretFile.read()

    #print("webClientSecret" + secretText)

    # get file list // next try with drive list
    drivelist = GDriveInterpreter.get_file_list('webClientSecret.json', user, 'my-drive')

    # extract the file names & file ids
    # begin creating JSON object to pass to client
    filedata = "[ "

    #iterate through each dictionary
    for d in drivelist:
        keylist = d.keys()
        if d.get("name") != None:

            filedata =  filedata + "{"

            # add the 'filename' as key
            filedata =  filedata + "\"fileName\""

            # separate key/value pairs with a colon
            filedata = filedata + ":"

            # add the file name as the value
            filedata = filedata + "\"" + str(d.get("name"))  + "\""

            # add comma
            filedata = filedata + ", "

            # add 'fileid' as key
            filedata =  filedata + "\"fileid\""

            # separate key/value pairs with a colon
            filedata = filedata + ":"

            # add the file id as the value
            filedata = filedata + "\"" + str(d.get("driveID")) + "\""

            filedata =  filedata + "}"

            # add comma after except for last element
            if d != drivelist[-1]:
                filedata = filedata + ", "

    # ending brace for JSON object
    filedata = filedata + " ]"

    # spit the file name list back
    return JsonResponse({"Files" : filedata})

#TODO: make the url for this one, probably needs to pass in user and fileid
#TODO: add restriction on this one too
@api_view(['GET'])
def DriveServerDownload(request, user, fileid):

    #pass webclientsecret to auth manager
    AM = AuthenticationManager.AuthenticationManager('webClientSecret.json')

    #get credentials
    credentials = AM.getCredentialsFromDatabase(user)

    filemeta = GDriveInterpreter.get_file_metadata(credentials, user, fileid) 
    GDriveInterpreter.get_file('webClientSecret.json', user, filemeta)
    
    print (filemeta)

    return JsonResponse({'File Metadata' : filemeta})

#@api_view(['GET'])
def DriveClientDownload(request, filename):

    #use mimetype to determine the file type
    file_path = './DriveStorage/' + filename
    file_to_download = open(file_path, 'rb')
    content_type = mimetypes.guess_type(filename)[0]
    response = FileResponse(file_to_download, content_type=content_type)
    response['Content-Disposition'] = "attachment ; filename=%s" % filename

    return response
