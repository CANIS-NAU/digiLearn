
'''
in this file, server_auth(), user_auth() are placeholder functions for
create_service() calls from the GoogleInterface

server_*() methods are calls using the server's (projects) credentials

user_*() methods are call using the requesting users credentials
'''



### to create a class
server = server_auth()
user = user_auth()

fileid = '<file id as generated by google>'  # this can be found using the GDriveInterpreter

classJSON = {
    'name': '<class Name>',
    'section': '<any string, typically a number>',
    'descriptionHeading': '<Title of Course Desciption>',
    'description': """A course about the history of cars.""",  # triple quotes are required for this value
    'room': '<272>',
    'ownerId': 'me',  # 'me' is a string literal used by google to signify a pointer to the userid of the user passed into create_service()
    'courseState': 'PROVISIONED',  # initializing a course requires the PROVISIONED value because teachers have to manually accept the position before the course can be set to ACTIVE
                                    # the change to ACTIVE happens internally through google, no change needs to be done here once the teacher accepts the class
    'courseMaterialSets': [
                             {
                                 'materials': [
                                     {
                                         'driveFile': {
                                             'id': fileid,
                                             'title': '<title of the material>'
                                         }
                                     }
                                 ],
                                 'title': '<material set title>'
                             }
                         ],
}

# call to Google Classroom API to creat the course using the projects credentials
cresp = server.courses().create(body=classJSON).execute()
print(cresp)

### responds with dictionary (JSON) containing relevant values populated by the above call and by Google upon creation of the course
### below is an example of a class that was created during the initial development stages of the Digital Backpack application

cresp = { 'id': '316143603555', # the courses id number
          'name': 'History', 'section': '1', 'descriptionHeading': 'Welcome To History Class!',
          'description': 'A course about the history of cars.', 'room': '272',
          'ownerId': '<ownerId number>', # redacted for obvious reasons, if you are still using the team.digilearn@gmail address then you can access this easily
          'creationTime': '2021-04-15T04:19:39.188Z', 'updateTime': '2021-04-15T04:19:38.191Z',
          'enrollmentCode': '26ssscz', # the code used to enroll students in the course
          'courseState': 'PROVISIONED',
          'alternateLink': 'https://classroom.google.com/c/MzE2MTQzNjAzNTU1',
          'teacherGroupEmail': 'History_1_teachers_b4b62c75@classroom.google.com',
          'courseGroupEmail': 'History_1_ef02565c@classroom.google.com',
          'teacherFolder': {'id': '<google drive object ID>'},
            # when a teacher accepts a course, a folder shared between all teachers for the class is created
            # this folder is used for student submission attachments, explained below
          'guardiansEnabled': False # this value can be changed at any time, indicates whether or not students need parental permission to enroll in the course
            # when set to True, students are required to provide a parents or gaurdians email address upon enrolling in the class
  }



### creating course work for class
cw = {
    'dueDate': {
        'year': 2021, # integer values, bounds provided in the Google Classroom PyDocs
        'day': 30,
        'month': 12
    },
    'state': 'PUBLISHED', # PUBLISHED signifies that
    'dueTime': {
        'seconds': 0, # integer values, bounds provided in the Google Classroom PyDocs
        'hours': 23,
        'minutes': 58,
        'nanos': 0
    },
    'description': '<description of the assignment>',
        ######################################################################################################################################
        #                                                   EXTREMELY IMPORTANT!!!!!                                                         #
        #                                                   ------------------------                                                         #
        # this value below, 'associatedWithDeveloper', is the key to this whole thing working, with out it google provides no way to access  #
        # assignments, even if you created the class in the same way as above                                                                #
        # ALL assignments must be created this way or students will not be able to submit assignments.                                       #
        # if set to false or not set at all, the server will be unable to access the assignment and therefore not show it to the user        #
        # at the time of writing this (4/28/2021) i believe it also would break the interpreter because google would simply return an error  #
        ######################################################################################################################################
    'associatedWithDeveloper': True,
    'maxPoints': 100, # total points possible for an assignment
    'workType': 'ASSIGNMENT', # there are a few different possible values for this, see the Google Documentation for others
    'title': '<title of the assignment>',
}

# call to the google api to create the coursework object within a class indicated by COURSE_ID
cwresp = server.courseWork().create(courseId=COURSE_ID, body=cw).execute()
print(cwresp)

## Example response
x = {'courseId': '316143603555', # ID of the course that this assignment is associated with
     'id': '316147105855', # ID of the assignment itself
     'title': 'Pick a Car Project',
     'description': 'Pick your favorite car and write a 3 paragraph essay', 'state': 'PUBLISHED',
     'alternateLink': 'https://classroom.google.com/c/MzE2MTQzNjAzNTU1/a/MzE2MTQ3MTA1ODU1/details',
     'creationTime': '2021-04-15T04:35:58.580Z', 'updateTime': '2021-04-15T04:35:58.525Z',
     'dueDate': {'year': 2021, 'month': 12, 'day': 30}, 'dueTime': {'hours': 23, 'minutes': 58},
     'maxPoints': 100, 'workType': 'ASSIGNMENT', 'submissionModificationMode': 'MODIFIABLE_UNTIL_TURNED_IN',
     'associatedWithDeveloper': True, 'assigneeMode': 'ALL_STUDENTS', 'creatorUserId': '<project owner id>'
 }




##creating an announcement for a course
annou = {
        'text': '<announcement text>',
        'state': 'PUBLISHED', # indicates that the announcement should be immediately pushed to students by Google
                                # other values available in the Google Classroom Documentation
}

annouresp = server.announcements().create(courseId=COURSE_ID, body=annou).execute()
print(annouresp)

# example response
x = {'courseId': '316126885315',
     'id': '316131136259', # the id of the announcement in relation to the course
     'text': 'Welcome to Language Arts!', 'state': 'PUBLISHED',
     'alternateLink': 'https://classroom.google.com/c/MzE2MTI2ODg1MzE1/p/MzE2MTMxMTM2MjU5',
     'creationTime': '2021-04-15T05:20:02.050Z', 'updateTime': '2021-04-15T05:20:02.044Z',
     'assigneeMode': 'ALL_STUDENTS', 'creatorUserId': '<project owner ID>'
 }





############################
# STUDENT ENROLLMENT
# ------------------
# this can be handled in the typical manner through classroom.google.com by sharing the enrollment code and or link
# with a student who then uses it to enroll in a course
# at this time we do not have an example of how to do this using the Google Classroom API
############################





###
# ASSIGNMENT SUBMISSION
##

# with the users credentials, find the student submission object
    # call to the google api
usl = user.courseWork().studentSubmissions().list(courseId=COURSE_ID, courseWorkId=COURSEWORK_ID, userId='me').execute()

print(str(usl))

# example of student submission object
x={'studentSubmissions': [
    {'courseId': '316143603555',
     'courseWorkId': '316147105855',
     'id': 'Cg4Ih6flsYQJEL-A2N6ZCQ', # submission ID
     'userId': '<users google ID>',
     'creationTime': '2021-04-15T06:38:15.884Z',
     'updateTime': '2021-04-15T06:38:13.301Z',
     'state': 'CREATED',
     'alternateLink': 'https://classroom.google.com/c/MzE2MTQzNjAzNTU1/a/MzE2MTQ3MTA1ODU1/submissions/by-status/and-sort-last-name/student/MzEwNDE1ODA3MzY3',
     'courseWorkType': 'ASSIGNMENT',
     'assignmentSubmission':
         {'attachments':
              [{'driveFile':
                    {'id': '1SML1QNgHzt-iUPTjfmV__UzPdg7xGErq',
                     'title': 'techFeasDoc.docx',
                     'alternateLink': 'https://drive.google.com/open?id=1SML1QNgHzt-iUPTjfmV__UzPdg7xGErq',
                     'thumbnailUrl': 'https://drive.google.com/thumbnail?id=1SML1QNgHzt-iUPTjfmV__UzPdg7xGErq&sz=s200'}}]},
     'associatedWithDeveloper': True}]}

# adding students attachments
sub = {
        'addAttachments':[
            {
                'driveFile': {
                    'id': '<drive file id>'  # string pointer to a google drive file
                }
            }
        ]
}

us = usl['studentSubmissions'][0]  # there *should* only ever be one value in the response array for a user
subid = us['id']

# modify attachments as user
umod = user.courses().courseWork().studentSubmissions().modifyAttachments(
    courseId=COURSE_ID, courseWorkId=COURSEWORK_ID, id=subid,
    body=sub
).execute()
print(umod)

# example response
# example response
x = {'courseId': '316143603555', 'courseWorkId': '316147105855', 'id': '<submission ID>',
       'userId': '<users google ID>', 'state': 'CREATED',
       'alternateLink': 'https://classroom.google.com/c/MzE2MTQzNjAzNTU1/a/MzE2MTQ3MTA1ODU1/submissions/by-status/and-sort-last-name/student/MzEwNDE1ODA3MzY3',
       'courseWorkType': 'ASSIGNMENT', 'assignmentSubmission': {'attachments': [
            {'driveFile': {'id': '1SML1QNgHzt-iUPTjfmV__UzPdg7xGErq', 'title': 'techFeasDoc.docx',
                           'alternateLink': 'https://drive.google.com/open?id=1SML1QNgHzt-iUPTjfmV__UzPdg7xGErq',
                           'thumbnailUrl': 'https://drive.google.com/thumbnail?id=1SML1QNgHzt-iUPTjfmV__UzPdg7xGErq&sz=s200'}}]
        }, 'associatedWithDeveloper': True}


# as user, turn in submission
usub = user.courseWork().studentSubmissions().turnIn(courseId=COURSE_ID, courseWorkId=COURSEWORK_ID, id=subid).execute()
print(usub)

# example response
x = {'courseId': '316143603555', 'courseWorkId': '316147105855', 'id': '<submission ID>',
       'userId': '<users google ID>', 'state': 'TURNED_IN',
       'alternateLink': 'https://classroom.google.com/c/MzE2MTQzNjAzNTU1/a/MzE2MTQ3MTA1ODU1/submissions/by-status/and-sort-last-name/student/MzEwNDE1ODA3MzY3',
       'courseWorkType': 'ASSIGNMENT', 'assignmentSubmission': {'attachments': [
            {'driveFile': {'id': '1SML1QNgHzt-iUPTjfmV__UzPdg7xGErq', 'title': 'techFeasDoc.docx',
                           'alternateLink': 'https://drive.google.com/open?id=1SML1QNgHzt-iUPTjfmV__UzPdg7xGErq',
                           'thumbnailUrl': 'https://drive.google.com/thumbnail?id=1SML1QNgHzt-iUPTjfmV__UzPdg7xGErq&sz=s200'}}]
        }, 'associatedWithDeveloper': True}