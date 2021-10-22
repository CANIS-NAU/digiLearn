import json
import traceback
from REST.Interfaces.GoogleInterface import create_service
from REST.JSONBuilders import DigiJsonBuilder
from REST.JSONBuilders import GDriveJsonBuilder

_API_NAME = 'classroom'
_API_VERSION = 'v1'
_GOOGLE_URI = 'https://www.googleapis.com/'
_SCOPES = ['https://www.googleapis.com/auth/classroom.courses',
          'https://www.googleapis.com/auth/classroom.coursework.me',
          'https://www.googleapis.com/auth/classroom.announcements',
          'https://www.googleapis.com/auth/classroom.guardianlinks.me.readonly'
          ]

_TEACHERSCOPES = ['https://www.googleapis.com/auth/classroom.courses',
          'https://www.googleapis.com/auth/classroom.coursework.me',
          'https://www.googleapis.com/auth/classroom.announcements',
          'https://www.googleapis.com/auth/classroom.guardianlinks.me.readonly',
          'https://www.googleapis.com/auth/classroom.coursework.students',
          'https://www.googleapis.com/auth/classroom.rosters'
          ]


def create_classes(user_auth, user_email, numClasses):
    try:
        print("[create_classes]- Creating GClass service...")
        service = create_service(user_auth, _API_NAME, _API_VERSION, _SCOPES, user_email=user_email)
        
        classJSON = {"name":"New DigiPack Class",
                    "ownerId":"me",
                    "courseState":"PROVISIONED"}
        
        index = 1
        while index < numClasses + 1:
            print("[create_classes]- Creating classroom " + str(index))
            cresp = service.courses().create(body=classJSON).execute()
            index = index + 1
            
        print("[create_classes]- All classes created.")
            
        return cresp   # returns most recently created class on success
    
    except:
        return 0       # returns 0 (false) for failure


def create_assignments(user_auth, user_email, numAssignments, courseId, assignmentType):
    try:
        print("[create_assignments]- Creating GClass service...")
        service = create_service(user_auth, _API_NAME, _API_VERSION, _TEACHERSCOPES, user_email=user_email)
        
        assignmentJSON = {"title":assignmentType,
                    "courseId": courseId,
                    "associatedWithDeveloper":"True",
                    "workType":assignmentType}

        if assignmentType == "MULTIPLE_CHOICE_QUESTION":
            print("if conditional entered")
            list = ["choice"]
            choiceJSON = {"choices":list}
            assignmentJSON = {"title":assignmentType,
                    "courseId": courseId,
                    "associatedWithDeveloper":"True",
                    "workType":assignmentType,
                    "multipleChoiceQuestion":""}
            assignmentJSON["multipleChoiceQuestion"] = choiceJSON
            print(assignmentJSON)

        index = 1
        while index < int(numAssignments) + 1:
            print("[create_assignments]- Creating assignments " + str(index))
            cwresp = service.courses().courseWork().create(courseId=courseId, body=assignmentJSON).execute()
            index = index + 1
            
        print("[create_assignments]- All assignments created.")
            
        return 1
    except:
        return 0

def get_course_list(user_auth, user_email):
    courselist = []
    service = create_service(user_auth, _API_NAME, _API_VERSION, _SCOPES, user_email=user_email)
    res = service.courses().list().execute()
    #print(res.toString())
    if 'courses' in res:
        for course in res['courses']:
            cw = get_coursework_list(user_auth, user_email, course['id'], ser=service)
            annou = get_announcements(user_auth, user_email, course['id'], ser=service)
            coursejson = DigiJsonBuilder.create_course(course['name'], course['id'], [user_email], announcements=annou,
                                                       coursework=cw)
            courselist.append(coursejson)
    return courselist

 
'''
Unlike the above get_course_list, this function only returns a list of courses. It does not get coursework or announcements
'''
def get_courses(user_auth, user_email):
    courselist = []
    service = create_service(user_auth, _API_NAME, _API_VERSION, _SCOPES, user_email=user_email)
    res = service.courses().list().execute()
    return res
    

def get_announcements(user_auth, user_email, course_id, ser=None):
    service = create_service(user_auth, _API_NAME, _API_VERSION, _SCOPES, user_email=user_email) if ser == None else ser
    gannoulist = service.courses().announcements().list(courseId=course_id, announcementStates='PUBLISHED').execute()
    anlist = []
    mode = None
    if 'announcements' in gannoulist:
        for gan in gannoulist["announcements"]:
            anid = gan['id']
            antext = gan['text'] if 'text' in gan else None
            anmats = _get_materials_from_json(gan) if 'materials' in gan else None
            anctime = gan['creationTime'] if 'creationTime' in gan else None
            anstu = [user_email]
            anou = DigiJsonBuilder.create_announcement(anid, antext, anmats, anctime, mode, anstu)
            anlist.append(anou)
    return anlist


def get_course(user_auth, user_email, course_id, ser=None):
    service = create_service(user_auth, _API_NAME, _API_VERSION, _SCOPES, user_email=user_email) if ser == None else ser
    course = service.courses().get(id=course_id).execute()
    coursejson = DigiJsonBuilder.create_course(course['name'], course_id, [user_email], announcements=[], coursework=[])
    otherfromgoogle = {
        'section': course['section'] if 'section' in course else None,
        'room': course['room'] if 'room' in course else None,
        'courseState': course['courseState'] if 'courseState' else None,
        'teacherGroupEmail': course['teacherGroupEmail'] if 'teacherGroupEmail' in course else None,
        'courseDescription': course['descriptionHeading'] if 'descriptionHeading' in course else None
    }
    coursejson.update(otherfromgoogle)
    mats = _get_materials_from_json(course['courseMaterialSets'] if 'courseMaterialSets' in course else None)
    coursejson.update({'materialSets': mats})
    return coursejson


def get_coursework_list(user_auth, user_email, course_id, ser=None):
    service = create_service(user_auth, _API_NAME, _API_VERSION, _SCOPES, user_email=user_email) if ser == None else ser
    gcwlist = service.courses().courseWork().list(courseId=course_id).execute()
    cwlist = []
    if 'courseWork' in gcwlist:
        for coursework in gcwlist['courseWork']:
            cwid = coursework['id']
            cwjson = get_coursework(user_auth, user_email, course_id, cwid, service)
            cwlist.append(cwjson)
    return cwlist


def get_coursework(user_auth, user_email, course_id, coursework_id, ser=None):
    service = create_service(user_auth, _API_NAME, _API_VERSION, _SCOPES, user_email=user_email) if ser == None else ser
    cw = service.courses().courseWork().get(courseId=course_id, id=coursework_id).execute()
    cwid = cw['id']
    title = cw['title']
    desc = cw['description'] if 'description' in cw else None
    mats = get_materials(user_auth, user_email, course_id, cwid, service)
    ctime = cw['creationTime']
    ddate = cw['dueDate'] if 'dueDate' in cw else None
    dtime = cw['dueTime'] if 'dueTime' in cw else None
    wtype = cw['workType'] if 'workType' in cw else None
    dets = cw['multipleChoiceQuestion'] if 'multipleChoiceQuestion' in cw else None
    pts = cw['maxPoints'] if 'maxPoints' in cw else None
    cwjson = DigiJsonBuilder.create_coursework(cwid, title, desc, mats, ctime, ddate, dtime, wtype, None, [user_email], dets)
    if pts != None:
        cwjson.update({"maxPoints": pts})
    return cwjson


def get_materials(user_auth, user_email, course_id, coursework_id, ser=None):
    service = create_service(user_auth, _API_NAME, _API_VERSION, _SCOPES, user_email=user_email) if ser == None else ser
    cw = service.courses().courseWork().get(courseId=course_id, id=coursework_id).execute()
    matlist = _get_materials_from_json(cw)
    return matlist

def submit_assignment(user_auth, user_email, course_id, submission, coursework_id, ser=None):
    # assumes submission is json object from DigiJsonBuilder.create_file()
    service = create_service(user_auth, _API_NAME, _API_VERSION, _SCOPES, user_email=user_email) if ser == None else ser
    # user_email is their ID

    # as user find the student submission object
    usl = service.courses().courseWork().studentSubmissions().list(courseId=course_id, courseWorkId=coursework_id, userId='me').execute()
    us = usl['studentSubmissions'][0]
    subid = us['id']

    # as user attach submission
    attach = GDriveJsonBuilder.add_file_attachment(submission['driveID'])
    umod = service.courses().courseWork().studentSubmissions().modifyAttachments(
        courseId=course_id, courseWorkId=coursework_id, id=subid, body=attach
    ).execute()

    # if attachment was successful (we just assume this cause digilearn babyy)
    # submit assignment
    sub = service.courseWork().studentSubmissions().turnIn( courseId=course_id, courseWorkId=coursework_id,
                                                            id=subid).execute()
    return sub




def _get_materials_from_json(mat):
    if mat is not None:
        cm = []
        if 'materials' in mat:
            df = mat['driveFile'] if "driveFile" in mat else None
            yt = mat['youtubeVideo'] if "youtubeVideo" in mat else None
            lnk = mat['link'] if "link" in mat else None
            form = mat['form'] if "form" in mat else None
            # at this point we arent storing these files
            material = DigiJsonBuilder.create_material(df, yt, lnk, form, None)
            cm.append(material)
        return cm
    # this will be similar to get materials loop
    return None


'''
Function Name: enroll_students
Algorithm: gets the specified course via courseId, adds all students in the studentEmailList to said course. If no
            service is provided, creates one.
Arguments: user_auth - server secret
           teacherId - Google userId string for the owner of the classroom
           studentEmailList - python-style list containing the emails of all students to be added
           courseId - google ID for the course for students to be added to
           ser - service object connected with Google servers
'''
def enroll_students( user_auth, teacherId, studentEmailList, courseId, ser=None):
    # get service if none
    service = create_service(user_auth, _API_NAME, _API_VERSION, _SCOPES, user_email=teacherId) if ser == None else ser
    allStudentsEnrolled = True
    # get all courses for the requesting teacher
    courses = get_courses('webClientSecret.json', teacherId)
    course_list = courses['courses']
    # get enrollment code for requested course
    foundCourse = False
    for course in course_list:
        if course["id"] == courseId:
            foundCourse = course
            break
    # check for course foundCourse
    if not foundCourse:
        print("[enroll_students]- Failed to find requested course.")
        allStudentsEnrolled = False
        return allStudentsEnrolled
    foundCourseEnrollCode = foundCourse["enrollmentCode"]
    print("[enroll_students]- " + str(foundCourseEnrollCode))
    # enroll each student in studentEmailList to class
    for studentEmail in studentEmailList:
        try:
            invitation = {"userId":studentEmail, "courseId": courseId, "role":"STUDENT"}
            student = service.invitations().create(
                body=invitation).execute()
            print("[enroll_students]- Student " + studentEmail + " successfully enrolled.")
        except:
            print("[enroll_students]- Student " + studentEmail + " failed to  enroll.")
            allStudentsEnrolled = False
            traceback.print_exc()
    return allStudentsEnrolled





