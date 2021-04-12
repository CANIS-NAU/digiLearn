from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import parser_classes
from REST.Interpreters import GDriveInterpreter
from REST.Interpreters import GClassInterpreter
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http import HttpResponseRedirect
from digipackDB import DatabaseManager
from Auth import AuthenticationManager 
from django.http import FileResponse
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpRequest
from django.shortcuts import render
from .forms import UploadFileForm
import mimetypes
import pathlib
import json
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
    
    
@api_view(['POST'])
@parser_classes([JSONParser])
@ensure_csrf_cookie
def WebAuth(request):
    #pass webclientsecret to auth manager
    AM = AuthenticationManager.AuthenticationManager('webClientSecret.json')

    #load the json data
    auth_json = request.data

    #pass access token to the auth manager
    credentials = AM.redeemAuthCodeWeb(auth_json["googleAccessToken"])

    return JsonResponse({'Result' : 'ACK'})    
    

#TODO: add a restriction that only allows a user to access their own url
@api_view(['GET'])
def InitDrive(request, user):

    secretFile = open("webClientSecret.json", "r")
    secretText = secretFile.read()

    # get file list // next try with drive list
    drivelist = GDriveInterpreter.get_file_list('webClientSecret.json', user, 'my-drive')

    filedata = []

    for d in drivelist:
        if d.get("name") != None:

            val = {
                "fileName": d["name"],
                "fileid": d["driveID"]
            }
            filedata.append(val)

    # spit the file name list back
    return JsonResponse({"Files" : filedata})

#TODO: add restriction on this one too
@api_view(['GET'])
def DriveServerDownload(request, user, fileid):

    #pass webclientsecret to auth manager
    AM = AuthenticationManager.AuthenticationManager('webClientSecret.json')

    #get credentials
    credentials = AM.getCredentialsFromDatabase(user)

    #get file metadata and
    filemeta = GDriveInterpreter.get_file_metadata(credentials, user, fileid) 
    GDriveInterpreter.get_file('webClientSecret.json', user, filemeta)
    
    #print (filemeta)

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

@api_view(['GET'])
def DrivePWADownload(request, user, fileid, filename):
    #pass webclientsecret to auth manager
    AM = AuthenticationManager.AuthenticationManager('webClientSecret.json')

    #get credentials
    credentials = AM.getCredentialsFromDatabase(user)

    #get file metadata and
    filemeta = GDriveInterpreter.get_file_metadata(credentials, user, fileid) 
    GDriveInterpreter.get_file('webClientSecret.json', user, filemeta)

    #use mimetype to determine the file type
    file_path = './DriveStorage/' + filename
    file_to_download = open(file_path, 'rb')
    content_type = mimetypes.guess_type(filename)[0]
    response = FileResponse(file_to_download, content_type=content_type)
    response['Content-Disposition'] = "attachment ; filename=%s" % filename

    return response

@api_view(['POST'])
def FileUpload(request):

    path = './media/' + request.FILES[fileName]
    print('This is the path: ' + path)
    with open(path, 'wb+') as destination:
        for chunk in request.FILES['uploaded_file'].chunks():
            destination.write(chunk)
    return HttpResponse('the file is saved')

#TODO: add a restriction that only allows a user to access their own url
@api_view(['GET'])
def InitGClass(request, user):

    # get class info
    courses = GClassInterpreter.get_course_list('webClientSecret.json', user)

    # spit the file name list back
    return JsonResponse({"Courses" : courses})
