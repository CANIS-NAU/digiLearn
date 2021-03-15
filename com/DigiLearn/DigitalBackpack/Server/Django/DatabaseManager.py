#django setup
import django

django.setup()


#import DB models
from digipackDB.models import Student

import allauth.models.User as User



'''
NOTE: Whenever you update the value of an object, that object must be reobtained
      to contain updated values.
      
TODO: All update functions should therefore return the updated instance of their
      #modified object on success
'''



'''
=====================
BEGIN STUDENT SECTION
=====================
'''




'''
Function Name: addStudent
Algorithm: creates a student object, saves it to the student table in the 
           database
Preconditions: valid studentId and hashedPassword provided
Postconditions: student object created and stored in database. 1 Returned to
                report success.
Excaptions: in the case of invalid data, no student created and 0 returned for
            faliure.
'''
def addStudent( studentId, jsonString ):
    #create student
    newStudent = Student( studentId=studentId, credentials=jsonString )
    
    #TODO
    #check for student it already in use
    
    #save student
    newStudent.save()
    return 1



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
    



def getCredentials (studentId ):
    try:
        requestedStudent = Student.objects.get( pk= studentId )
    
    except Student.DoesNotExist:
        #report failure
        return 0
        
    return requestedStudent.credentials




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
        return 0
        
    return requestedStudent





def getSocialLoginCredentials(user_email):
	user = aas.User.objects.get(email=user_email)
	social = user.social_auth.get(provider='google-oauth2')
	print(social.extradata['access_token'])



getSocialLoginCredentials('team.digilearn@gmail.com')





































































































