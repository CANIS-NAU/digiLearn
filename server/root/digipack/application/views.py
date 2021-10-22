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
import json
import os
from Utilities.Logger import accessLog



#initial authentication
@api_view(['POST'])
@parser_classes([JSONParser])
@ensure_csrf_cookie
def MobileAuth(request):
    #pass webclientsecret to auth manager
    AM = AuthenticationManager.AuthenticationManager('webClientSecret.json')

    #load the json data
    auth_json = request.data

    #pass access token to the auth manager
    credentials = AM.redeemAuthCode(auth_json["authToken"])

    return JsonResponse({'Result' : 'ACK'})




#initial authentication
@api_view(['POST'])
@parser_classes([JSONParser])
@ensure_csrf_cookie
def GetClasses(request):
    # unpack request data
    request_data = request.data    
    id_token = request_data["id_token"]
    
    print("[GetClasses]- id_token: " + str(id_token) )
    
    # authenticate teacher id_token
    AM = AuthenticationManager.AuthenticationManager('webClientSecret.json')

    #idToken passed for user; needs to be validated
    user = AM.redeemIdToken(id_token)

    #if user is 0, id token failed to redeem
    if user == 0:
        print("[GetClasses]- Id Token failed to redeem.")
        #return some fail message
        return JsonResponse({"response":"ID_ERROR"})
    #else, id token redeemed for user id.
    
    #get courses
    courses = GClassInterpreter.get_courses('webClientSecret.json', user)
    print(str(courses))
    accessLog("User got Google Classroom data.", user)
    return JsonResponse(courses)


#get file list
@api_view(['GET'])
def InitDrive(request, user):
    AM = AuthenticationManager.AuthenticationManager('webClientSecret.json')
    secretFile = open("webClientSecret.json", "r")
    secretText = secretFile.read()

    print("[GetFileList]- Request received with Id Token  " + user)


    #idToken passed for user; needs to be validated
    user = AM.redeemIdToken(user)

    #if user is 0, id token failed to redeem
    if user == 0:
        print("[GetFileList]- Id Token failed to redeem.")
        #return some fail message
        return JsonResponse({"Result":"noACK"})
    #else, id token redeemed for user id.

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
    accessLog("User retrieved Google Drive file list.", user)
    # spit the file name list back
    return JsonResponse({"Files" : filedata})


#get file
@api_view(['GET'])
def DriveServerDownload(request, user, fileid):

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


    return JsonResponse({'File Metadata' : filemeta})

#@api_view(['GET'])
def DriveClientDownload(request, filename):

    #use mimetype to determine the file type
    file_path = './DriveStorage/' + filename
    file_to_download = open(file_path, 'rb')
    content_type = mimetypes.guess_type(filename)[0]
    response = FileResponse(file_to_download, content_type=content_type)
    response['Content-Disposition'] = "attachment ; filename=%s" % filename
    accessLog("User downloaded file " + filename + "from Google Drive.", "noUser")
    return response


#@api_view(['GET'])
# downloads a webpaged saved on the server to the client
def SearchClientDownload(request, filename):
    
    html = filename + '.html'

    file_path = './sitearchives/' + html
    file_to_download = open(file_path, 'rb')
    content_type = mimetypes.guess_type(filename)[0]
    response = FileResponse(file_to_download, content_type=content_type)
    response['Content-Disposition'] = "attachment ; filename=%s" % html

    return response


@api_view(['POST'])
def ArchiveUrl(request):
    url = request.data["link"]
    filename = request.data["filename"]

    command = 'wget ' + url + ' -m -E -Q1m -O ./sitearchives/' + filename + '.html'

    proc = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = proc.communicate()

    return JsonResponse({'Result' : 'ACK'})


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
    accessLog("User downloaded file " + str(filename) + " from Google Drive.", user)
    return response


@api_view(['POST'])
def FileUpload(request):
    print(str(request.POST))
    user = request.POST.get('idTok', 'noIdTok')
    fileName = request.POST.get('file_name', 'noFileName.txt')

    print("[FileUpload]- User ID is " + user)

    #init authentication manager
    AM = AuthenticationManager.AuthenticationManager('webClientSecret.json')

    #redeem id token
    user = AM.redeemIdToken(user)

    #if user is 0, id token failed to redeem
    if user == 0:
        print("[GetFileList]- Id Token failed to redeem.")
        #return some fail message
        return HttpResponse('HTTP 403 Forbidden')
    #else, id token redeemed for user id.

    #user verified, save the file.
    path = './media/' + user + '/'

    #make the directory
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == 17:
            # Dir already exists
            pass

    #append filename to oath
    path = path + fileName

    print('This is the path: ' + path)

    with open(path, 'wb+') as destination:
        for chunk in request.FILES['uploaded_file'].chunks():
            destination.write(chunk)

    #assemble file json
    fileJson = DigiJsonBuilder.create_file(fileName, None, None, path, None, None, None )

    #upload to drive
    GDriveInterpreter.upload_file("webClientSecret.json", user, fileJson)
    accessLog("User uploaded file " + str(filename) + " to Google Drive", user)
    return HttpResponse('the file is saved')



@api_view(['POST'])
def FileSubmit(request):
    user = request.POST.get('idTok', 'noIdTok')
    fileName = request.POST.get('file_name', 'noFileName.txt')
    courseId = request.POST.get('courseId', 'noCourseId')
    courseworkId = request.POST.get('courseworkId','courseworkId')

    #init authentication manager
    AM = AuthenticationManager.AuthenticationManager('webClientSecret.json')

    #redeem id token
    user = AM.redeemIdToken(user)

    #if user is 0, id token failed to redeem
    if user == 0:
        print("[GetFileList]- Id Token failed to redeem.")
        #return some fail message
        return HttpResponse('HTTP 403 Forbidden')
    #else, id token redeemed for user id.

    #user verified, save the file.
    path = './media/' + user + '/'

    #make the directory
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == 17:
            # Dir already exists
            pass

    #append filename to oath
    path = path + fileName

    print('This is the path: ' + path)
    with open(path, 'wb+') as destination:
        for chunk in request.FILES['file'].chunks():
            destination.write(chunk)
    accessLog("User submitted assignment to course " + str(courseId) + ".", user)

    #assemble file json
    fileJson = DigiJsonBuilder.create_file(fileName, None, None, path, None, None, None )

    #upload to drive
    submission = GDriveInterpreter.upload_file("webClientSecret.json", user, fileJson)

    #submit the assignment submit_assignment(user_auth, user_email, course_id, submission, coursework_id, ser=None):
    GClassInterpreter.submit_assignment("webClientSecret.json", user, courseId, submission, courseworkId)

    messages.success(request, 'Form submission successful')
    



#get GClass
@api_view(['GET'])
def InitGClass(request, user):
    AM = AuthenticationManager.AuthenticationManager('webClientSecret.json')

    #idToken passed for user; needs to be validated
    user = AM.redeemIdToken(user)

    #if user is 0, id token failed to redeem
    if user == 0:
        print("[GetClassList]- Id Token failed to redeem.")
        #return some fail message
        return JsonResponse({"Result":"noACK"})
    #else, id token redeemed for user id.

    # get class info
    courses = GClassInterpreter.get_course_list('webClientSecret.json', user)
    accessLog("User accessed Google Drive document list.", user)
    # spit the file name list back
    return JsonResponse({"Courses" : courses})




@api_view(['POST'])
def RetrieveQueries(request):
    whitelist = []
    blacklist = []
    blackterms = []
    whiteterms = []
    topic = []

    queries = request.data["queries"]
    print("Queries: " + str(queries))
    modifiers = DigiJsonBuilder.create_modifiers(whitelist, blacklist,blackterms,whiteterms,topic)

    results = GSearchInterpreter.submit_queries(queries, modifiers)

    print("results of retrieve queries: " + str(results))

    return JsonResponse({"resultslist" : results})


@api_view(['POST'])
def DemoQueries(request):
    results = [{'query': 'math', 'imagebool': False, 'numresults': 10, 'results': [{'title': 'Math Games | Math Playground | Fun for Kids', 'link': 'https://www.mathplayground.com/', 'displaylink': 'www.mathplayground.com', 'snippet': 'Free, online math games and more at MathPlayground.com! Problem solving, \nlogic games and number puzzles kids love to play.', 'mimetype': None, 'fileformat': 'No File Format'}, {'title': 'Math.com - World of Math Online', 'link': 'http://www.math.com/', 'displaylink': 'www.math.com', 'snippet': 'Free math lessons and math homework help from basic math to algebra, \ngeometry and beyond. Students, teachers, parents, and everyone can find \nsolutions to\xa0...', 'mimetype': None, 'fileformat': 'No File Format'}, {'title': 'Math is Fun', 'link': 'https://www.mathsisfun.com/', 'displaylink': 'www.mathsisfun.com', 'snippet': 'Math explained in easy language, plus puzzles, games, worksheets and an \nillustrated dictionary. For K-12 kids, teachers and parents.', 'mimetype': None, 'fileformat': 'No File Format'}, {'title': 'Khan Academy Math', 'link': 'https://www.khanacademy.org/math', 'displaylink': 'www.khanacademy.org', 'snippet': 'Learn fourth grade math—arithmetic, measurement, geometry, fractions, and \nmore. This course is aligned with Common Core standards.', 'mimetype': None, 'fileformat': 'No File Format'}, {'title': 'Math - JavaScript | MDN', 'link': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math', 'displaylink': 'developer.mozilla.org', 'snippet': "5 days ago ... Math is a built-in object that has properties and methods for mathematical \nconstants and functions. It's not a function object.", 'mimetype': None, 'fileformat': 'No File Format'}, {'title': 'Mathway | Algebra Problem Solver', 'link': 'https://www.mathway.com/', 'displaylink': 'www.mathway.com', 'snippet': 'Free math problem solver answers your algebra homework questions with step-\nby-step explanations.', 'mimetype': None, 'fileformat': 'No File Format'}, {'title': 'Learn math online - IXL Math', 'link': 'https://www.ixl.com/math/', 'displaylink': 'www.ixl.com', 'snippet': "Discover thousands of math skills covering pre-K to 12th grade, from counting to \ncalculus, with infinite questions that adapt to each student's level.", 'mimetype': None, 'fileformat': 'No File Format'}, {'title': 'math — Mathematical functions — Python 3.9.4 documentation', 'link': 'https://docs.python.org/3/library/math.html', 'displaylink': 'docs.python.org', 'snippet': 'This module provides access to the mathematical functions defined by the C \nstandard. These functions cannot be used with complex numbers; use the \nfunctions\xa0...', 'mimetype': None, 'fileformat': 'No File Format'}, {'title': 'IXL | Math, Language Arts, Science, Social Studies, and Spanish', 'link': 'https://www.ixl.com/', 'displaylink': 'www.ixl.com', 'snippet': "IXL is the world's most popular subscription-based learning site for K–12. Used \nby over 12 million students, IXL provides personalized learning in more than\xa0...", 'mimetype': None, 'fileformat': 'No File Format'}, {'title': 'The ACT Test Math Practice Test Questions | ACT', 'link': 'https://www.act.org/content/act/en/products-and-services/the-act/test-preparation/math-practice-test-questions.html', 'displaylink': 'www.act.org', 'snippet': 'Math. Test Tips. An actual ACT Mathematics Test contains 60 questions to be \nanswered in 60 minutes. Read each question carefully to make\xa0...', 'mimetype': None, 'fileformat': 'No File Format'}]}]

    return JsonResponse({"resultslist" : results})
