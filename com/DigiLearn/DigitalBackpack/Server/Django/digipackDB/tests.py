from django.test import TestCase
import digipackDB.models as models
import digipackDB.DatabaseManager as dbm

# Create your tests here.

class StudentTestCase( TestCase ):
    
    def test_student(self):
        
        print("\nSTDIO : ADDING STUDENT")
        dbm.addStudent("testId", "testCreds")
        
        print("STDIO : GETTING STUDENT")
        testStudent = dbm.getStudent("testId")
        
        print("STDIO : CHECKING STUDENT OBJECT FOR CORRECT VALUES")
        self.assertEqual( testStudent.studentId, "testId")
        self.assertEqual( testStudent.credentials, "testCreds")
        
        print("STDIO : ATTEMPTING TO GET CREDENTIALS FROM STUDENT ID")
        credentials = dbm.getCredentials("testId")
        self.assertEqual(credentials, "testCreds")
        
        print("STDIO : REMOVING STUDENT")
        dbm.removeStudent( "testId" )
        
        print("STDIO : ATTEMPTING TO ACCESS REMOVED STUDENT")
        testStudent = dbm.getStudent("testId")
        self.assertEqual( testStudent, 0 )
        
        print("STDIO : CONGRATULATIONS! ALL STUDENT TESTS PASSED.")
        
        
        
        
        

        
        
        
        
        
        
        
        
        
        

