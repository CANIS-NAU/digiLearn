from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import parser_classes
from REST.Interpreters import GDriveInterpreter
from REST.Interpreters import GClassInterpreter
from REST.Interpreters import GSearchInterpreter
from REST.JSONBuilders import DigiJsonBuilder
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http import HttpResponseRedirect
from REST.Auth import AuthenticationManager
from django.http import FileResponse
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpRequest
from django.shortcuts import render
import subprocess
import mimetypes
import pathlib
import pandas
import json
import os
from Utilities.Logger import accessLog

#@login_required(login_url='/login')
def index(request):
    # check for session token
    try:
        token = request.session['token']
        return render(request, 'index.html', token)
    except:
        return render(request, 'index.html')

   
def teacherconsole(request):
    try:
        token = request.session['token']
        return render(request, 'teacherconsole.html', token)
    except:
        return render(teacherlogin, 'teacherlogin.html', token)


def login(request):
    return render(request, 'login.html')


def teacherlogin(request):
    return render(request, 'teacherlogin.html')


#initial authentication
@api_view(['POST'])
@parser_classes([JSONParser])
@ensure_csrf_cookie
def WebAuth(request):
    #pass webclientsecret to auth manager
    AM = AuthenticationManager.AuthenticationManager('webClientSecret.json')

    #load the json data
    auth_data = request.data

    print(" the request data: " + str(auth_data))

    # get auth json and token json
    auth_json = json.loads(auth_data["authCodeString"])
    token_json = json.loads(auth_data["token_data"])

    # get access token and id token
    access_token = auth_json["googleAccessToken"]
    id_token = token_json["token"]

    #pass access token to the auth manager, ID token returned.
    token_key = AM.redeemAuthCodeWeb(access_token)
    
    # if registration was successful
    if token_key != 0:
        # store the token key as the idtoken in the  session to be passed to other views
        token_json["token"] = token_key
        request.session['token'] = token_json
        
    #idToken passed for user; needs to be validated
    user = AM.redeemIdToken(token_key)
    accessLog("User registered/logged in as student.", user)

    return JsonResponse({'token' : token_key})



#initial authentication
@api_view(['POST'])
@parser_classes([JSONParser])
@ensure_csrf_cookie
def CreateClass(request):
    # unpack request data
    request_data = request.data    
    id_token = request_data["id_token"]
    num = int(request_data["numClasses"])
    
    print("[CreateClass]- id_token: " + str(id_token) + "   numClasses: " + str(num))
    
    # authenticate teacher id_token
    AM = AuthenticationManager.AuthenticationManager('webClientSecret.json')

    #idToken passed for user; needs to be validated
    user = AM.redeemIdToken(id_token)

    #if user is 0, id token failed to redeem
    if user == 0:
        print("[CreateClass]- Id Token failed to redeem.")
        #return some fail message
        return JsonResponse({"response":"ID_ERROR"})
    #else, id token redeemed for user id.
    
    print("[CreateClass]- Id Token redeemed.")
    GClassInterpreter.create_classes('webClientSecret.json', user, num)
    accessLog("User created " + str(num) + " classes.")
    return JsonResponse({'response' : 'success'})


#initial authentication
@api_view(['POST'])
@parser_classes([JSONParser])
@ensure_csrf_cookie
def CreateAssignment(request):
    # unpack request data
    request_data = request.data    
    id_token = request_data["id_token"]
    courseId = request_data["courseId"]
    numAssignments = request_data["numAssignments"]
    assignmentType = request_data["assignmentType"]
    
    # print("[CreateAssignment]- id_token: " + str(id_token) + "   courseId: " +  str(courseId) + "   
    #  numAssignments: " + str(numAssignments))
    
    # authenticate teacher id_token
    AM = AuthenticationManager.AuthenticationManager('webClientSecret.json')
    
     #idToken passed for user; needs to be validated
    user = AM.redeemIdToken(id_token)

    #if user is 0, id token failed to redeem
    if user == 0:
        print("[CreateAssignment]- Id Token failed to redeem.")
        #return some fail message
        return JsonResponse({"response":"ID_ERROR"})
    #else, id token redeemed for user id.
    
    print("[CreateAssignment]- Id Token redeemed.")
    
    GClassInterpreter.create_assignments("webClientSecret.json", user, numAssignments, courseId, assignmentType)
    accessLog("User created " + str(numAssignments) + " assignments of type " + str(assignmentType) + " for course " + str(courseId) + ".", user)
    return JsonResponse({'response' : 'success'})


#initial authentication
@api_view(['POST'])
@parser_classes([JSONParser])
@ensure_csrf_cookie
def teacherAuth(request):
    #pass webclientsecret to auth manager
    AM = AuthenticationManager.AuthenticationManager('webClientSecret.json')

    #load the json data
    auth_data = request.data

    # print(" the request data: " + str(auth_data))

    # get auth json and token json
    auth_json = json.loads(auth_data["authCodeString"])
    token_json = json.loads(auth_data["token_data"])

    # get access token and id token
    access_token = auth_json["googleAccessToken"]
    id_token = token_json["token"]

    #pass access token to the auth manager, ID token returned.
    token_key = AM.redeemAuthCodeTeacher(access_token)

    token_json["token"] = token_key
    request.session['token'] = token_json

    #idToken passed for user; needs to be validated
    user = AM.redeemIdToken(token_key)
    accessLog("User registered/logged in as teacher.", user)

    return JsonResponse({'token' : token_key})


@api_view(['GET'])
def DrivePWADownload(request, user, fileid, filename):
    #pass webclientsecret to auth manager
    AM = AuthenticationManager.AuthenticationManager('webClientSecret.json')

    #idToken passed for user; needs to be validated
    user = AM.redeemIdToken(user)

    #if user is 0, id token failed to redeem
    if user == 0:
        print("[GetFileList]- Id Token failed to redeem.")
        #return some fail message
        return JsonResponse({"Result":"NoACK"})
    #else, id token redeemed for user id.

    #get file metadata and
    filemeta = GDriveInterpreter.get_file_metadata('webClientSecret.json', user, fileid)
    GDriveInterpreter.get_file('webClientSecret.json', user, filemeta)

    #use mimetype to determine the file type
    file_path = './DriveStorage/' + filename
    file_to_download = open(file_path, 'rb')
    content_type = mimetypes.guess_type(filename)[0]
    response = FileResponse(file_to_download, content_type=content_type)
    response['Content-Disposition'] = "attachment ; filename=%s" % filename
    accessLog("User downloaded " + str(filename) + " from Google Drive.", user)
    return response


@api_view(['POST'])
def EnrollStudents(request):
    # unpack request data
    request_data = request.data
    column = request_data["colSelect"]
    courseId = request_data["classSelectEnroll"]
    user = request_data["uploadIdTok"]
    print(user)
    print(column)
    print(courseId)
    # check for roster upload
    try:
        roster = request.FILES['roster']
    
    except:
        print('[EnrollStudents]- No roster uploaded.')
        return JsonResponse({"Error":"NoRoster"})
    
    # verify id
    AM = AuthenticationManager.AuthenticationManager('webClientSecret.json')
    user = AM.redeemIdToken(user)
    #if user is 0, id token failed to redeem
    if user == 0:
        print("[EnrollStudents]- Id Token failed to redeem.")
        #return some fail message
        return JsonResponse({"Result":"badId"})
    
    # parse roster
    filename = roster.name
    # write the file to the server
    with open(filename, 'wb+') as destination:
        for chunk in request.FILES['roster'].chunks():
            destination.write(chunk)
    print('[EnrollStudents]- Column:' + column + " Class:" + courseId + " ID Token:" + user)
    #process column character to index
    columnNum = ord(column) - ord ('A')
    print(str(ord(column)) + " " + str(ord('A')) + " " + str(columnNum))

    # open spreadsheet
    roster = pandas.read_excel(filename)
    print(roster)
    # extract info from specified column
    studentList = roster.iloc[:, columnNum].tolist()
    print(studentList)
    
    # enroll students
    enrollResult = GClassInterpreter.enroll_students( "webClientSecret.json", user, studentList, courseId )
    # delete roster file
    os.remove(filename)
    
    if enrollResult:
        accessLog("User successfully enrolled students via roster.", user)
    else:
        accessLog("User failed to enroll students via roster.", user)
    
    # return success()
    return JsonResponse({'response' : 'success'})


























