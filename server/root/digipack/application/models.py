
#django setup
from django.db import models
import django
import traceback
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
#django.setup()


'''
Model Name:  Student
Description: Abstracts a single student in the Digital Backpack system

Fields:
    studentId = Student's gmail address
    credentials: OAuth2 Credentials JSON file
    
Each student instance is created alongside a User instance. The student's
studentId becoems the User's username. In this way, access to the Student
gives unique access to the User and vice-versa. This is used to manage
Django tokens and keep those tokens associated with the student.
'''
class Student( models.Model ):
    studentId = models.CharField( max_length=1000, primary_key=True )
    credentials = models.JSONField(default=str)

'''
NOTE: Whenever you update the value of an object, that object must be reobtained
      to contain updated values.
      

'''



'''
Student Section
'''




'''
Function Name: addStudent
Algorithm: creates a student object, saves it to the student table in the 
           database. Also creates the associated User object which has the student's id
           as a username.
Preconditions: valid studentId and hashedPassword provided
Postconditions: student  and user objects created and stored in database. Returns the token
                key associated with the student.
Excaptions: in the case of invalid data, no student created and 0 returned for
            faliure.
'''
def addStudent( userId, jsonString ):
    #create student
    
    print("[addStudent]- userId is: " + str(userId))
    #check for student id already in use
    try:
        student = Student.objects.get(pk=userId)
        
        print("[addStudent]- userId " + str(userId) + " already in use, no action.")

        # student already exists, get and return token key
        fetchUser = User.objects.get(username =userId)
        token = Token.objects.get(user=fetchUser)
        tokenKey = str(token.key)
        
        print("[addStudent]- Token retrieved with key " + tokenKey)

        return tokenKey

    except Student.DoesNotExist:    
    # create and save student
        newStudent = Student( studentId=userId, credentials=jsonString )
        newStudent.save()
        print("[addStudent]- New student created with userId " + str(userId))
        
        # create User associated with student
        newUser = User.objects.create_user(userId)
        print("[addStudent]- New User created with username " + str(newUser.get_username()))
        
        # create token for new user 
        token = Token.objects.create(user=newUser)
        
        print("[addStudent]- New token created with key " + str(token.key))
        return token.key








'''
Function Name: removeStudent
Algorithm: retrieves student associated with given ID, deletes student.
Preconditions: valid studentId provided.
Postconditions: specified student is deleted from the database
Exceptions: in the case that the student is not found, no action taken and 0
            reported for failure.
'''
def removeStudent( studentId ):
    try:
        #retrieve student
        studentToRemove = Student.objects.get(pk=studentId)
        
        #remove student
        studentToRemove.delete()
       
        #report success
        return 1
    
    #except student not found
    except Student.DoesNotExist:
        #report failure
        return 0
    



def getCredentials (email ):
    print("[getCredentials]- userId is: " + str(email))
    try:
        requested = Student.objects.get( studentId=email )
    
    except Student.DoesNotExist:
        #report failure
        print("[getCredentials]- No student with userId " + str(email) + ", checking for teacher.")
        try:
            requested = Teacher.objects.get( teacherId=email )
        
        except Teacher.DoesNotExist:
            #report failure
            print("[getCredentials]- No teacher with userId " + str(email) + ", returning failure.")
            traceback.print_exc()
            return 0
        
    return requested.credentials




'''
Function Name: getStudent
Algorithm: standard getter retrieves student with specified ID if such a student
           exists, otherwise returns 0 for failure
'''
def getStudent( studentId ):
    try:
        requestedStudent = Student.objects.get( pk= studentId )
    
    except Student.DoesNotExist:
        #report failure
        traceback.print_exc()
        return 0
        
    return requestedStudent


'''
Teacher Section
'''


class Teacher( models.Model ):
    teacherId = models.CharField( max_length=1000, primary_key=True )
    credentials = models.JSONField(default=str)


def addTeacher( userId, jsonString ):
    #create student
    
    print("[addTeacher]- userId is: " + str(userId))
    #check for student id already in use
    try:
        teacher = Teacher.objects.get(pk=userId)
        
        print("[addTeacher]- userId " + str(userId) + " already in use, no action.")

        # student already exists, get and return token key
        fetchUser = User.objects.get(username =userId)
        token = Token.objects.get(user=fetchUser)
        tokenKey = str(token.key)
        
        print("[addTeacher]- Token retrieved with key " + tokenKey)

        return tokenKey

    except Teacher.DoesNotExist:    
    # create and save student
        newTeacher = Teacher( teacherId=userId, credentials=jsonString )
        newTeacher.save()
        print("[addTeacher]- New teacher created with userId " + str(userId))
        
        # create User associated with student
        newUser = User.objects.create_user(userId)
        print("[addTeacher]- New User created with username " + str(newUser.get_username()))
        
        # create token for new user 
        token = Token.objects.create(user=newUser)
        
        print("[addTeacher]- New token created with key " + str(token.key))
        return token.key
    
    
def removeTeacher( teacherId ):
    try:
        #retrieve student
        teacherToRemove = Teacher.objects.get(pk=studentId)
        
        #remove student
        teacherToRemove.delete()
       
        #report success
        return 1
    
    #except student not found
    except Teacher.DoesNotExist:
        #report failure
        return 0


def getTeacherCredentials (userId ):
    print("GET CREDENTIALS DBM METHOD ENTERED")
    print("[getTeacherCredentials]- userId is: " + userId)
    try:
        requestedTeacher = Teacher.objects.get( teacherId=userId )
    
    except Teacher.DoesNotExist:
        #report failure
        print("[getCredentials]- No teacher with userId " + userId + ", returning failure.")
        traceback.print_exc()
        return 0
        
    return requestedTeacher.credentials


def getTeacher( teacherId ):
    try:
        requestedTeacher = Teacher.objects.get( pk= teacherId )
    
    except Teacher.DoesNotExist:
        #report failure
        traceback.print_exc()
        return 0
        
    return requestedTeacher





































