import json
from REST.Interfaces.GoogleInterface import create_service
from REST.JSONBuilders import DigiJsonBuilder

_API_NAME = 'classroom'
_API_VERSION = 'v1'
_GOOGLE_URI = 'https://www.googleapis.com/'
_SCOPES = ['https://www.googleapis.com/auth/classroom.courses',
          'https://www.googleapis.com/auth/classroom.coursework.me',
          'https://www.googleapis.com/auth/classroom.announcements',
          'https://www.googleapis.com/auth/classroom.guardianlinks.me.readonly'
          ]

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

