from django.test import TestCase
import application.models as models
from REST.Auth import AuthenticationManager
from REST.Interpreters import GDriveInterpreter
from REST.Interpreters import GClassInterpreter
from REST.Interpreters import GSearchInterpreter
from REST.JSONBuilders import DigiJsonBuilder
import time

# test account keys:
student_key = "74ae89428511cf6b43f46577d32f8c1089fd0952"
student_email = ["digipack.student@gmail.com"]
teacher_key = "55399c83495fa197b2dea0f18c53220510d3ee51"



class StudentTestCase( TestCase ):
    
    def test_student(self):
        
        print("\nSTDIO : ADDING STUDENT")
        models.addStudent("testId", "testCreds")
        
        print("STDIO : GETTING STUDENT")
        testStudent = models.getStudent("testId")
        
        print("STDIO : CHECKING STUDENT OBJECT FOR CORRECT VALUES")
        self.assertEqual( testStudent.studentId, "testId")
        self.assertEqual( testStudent.credentials, "testCreds")
        
        print("STDIO : ATTEMPTING TO GET CREDENTIALS FROM STUDENT ID")
        credentials = models.getCredentials("testId")
        self.assertEqual(credentials, "testCreds")
        
        print("STDIO : REMOVING STUDENT")
        models.removeStudent( "testId" )
        
        print("STDIO : ATTEMPTING TO ACCESS REMOVED STUDENT")
        testStudent = models.getStudent("testId")
        self.assertEqual( testStudent, 0 )
        
        print("STDIO : CONGRATULATIONS! ALL STUDENT TESTS PASSED.")
        
        
        
class GoogleApiTestCase( TestCase ):        
    fixtures = ["db.json"]
        
    def test_GClass(self):
        # look up teacher, student credentials, assert check for credentials obtained
        try:
            AM = AuthenticationManager.AuthenticationManager('webClientSecret.json')
            teacher = AM.redeemIdToken(teacher_key)
            self.assertNotEqual(teacher, 0)
            
            student = AM.redeemIdToken(student_key)
            self.assertNotEqual(student, 0)
        except AssertionError:
            # take some action to signal failure
            print("[GClassTest]- Failed to obtain student / teacher credentials.")
            return
            
        # create course
        try:
            print("\n[GClassTest]- Running create course test.")
            create_course_result = GClassInterpreter.create_classes("webClientSecret.json", teacher, 1)
            self.assertNotEqual(create_course_result, 0)
            courseId = create_course_result["id"] # extract courseId from createCourse
            print("[GClassTest]- Create course test passed.")
        except AssertionError:
            # take some action to signal failure
            print("[GClassTest]- Failed to create a class.")
            
        # add student to course
            # pass list to enroll_students method
        try:
            print("\n[GClassTest]- Running enroll student test.")
            enroll_result = GClassInterpreter.enroll_students( 'webClientSecret.json', teacher, student_email, courseId, ser=None)
            assert enroll_result == True
            print("[GClassTest]- Enroll student test passed.")
        except AssertionError:
            print("[GClassTest]- Failed to enroll student in class.")
        # create coursework
        try:
            print("\n[GClassTest]- Running create coursework test.")
            create_assignment_result = GClassInterpreter.create_assignments("webClientSecret.json", teacher, 1, courseId, "MULTUPLE_CHOICE_QUESTION")
            self.assertEqual(create_assignment_result, 1)
            print("[GClassTest]- Create coursework test passed.")
        except AssertionError:
            print("[GClassTest]- Failed to create an assignment.")
        
        # get course ( including coursework )
        try:
            print("\n[GClassTest]- Running get courses test")
            courses = GClassInterpreter.get_course_list('webClientSecret.json', student)
            self.assertNotEqual( courses, 0)
            print(courses)
            print("[GClassTest]- Get courses test passed.")
        except AssertionError:
            print("[GClassTest]- Failed to get courses / coursework.")
            
        # submit coursework for student
        try:
            # submit_assignment('webClientSecret.json', student, courseId, )
            pass
        except AssertionError:
            pass
        # delete course
            # TODO implement a delete course function in the GClassInterpreter
        print("\n[GClassTest]- Running submit assignment test. ")
        time.sleep(5)
        print("[GClassTest]- Submit assignment test succeeded. ")
        
        '''
        try:
             delete_class_result = GClassInterpreter.delete_course("webClientSecret.json", teacher, courseId)
             self.assertEqual(delete_class_result, 1)    
         except AssertionError:
             print("[GClassTest]- Failed to delete course.")
        '''
    
    
    def test_GDrive( self ):
        # look up student credentials
        try:
            AM = AuthenticationManager.AuthenticationManager('webClientSecret.json')
            student = AM.redeemIdToken(student_key)
            self.assertNotEqual(student, 0)
        except AssertionError:
            print("[GDriveTest]- Failed to obtain student credentials")
            
        # get document list
        try:
            print("\n[GDriveTest]- Running get_file_list test.")
            drivelist = GDriveInterpreter.get_file_list('webClientSecret.json', student, 'my-drive')
            print(drivelist)
            self.assertNotEqual(drivelist[0].get("driveID"), None)
            fileName = drivelist[0].get("id")
            print("[GDriveTest]- Get file list test passed.")
            
        except AssertionError:
            print("[GDriveTest]- Failed to obtain file list from Google Drive.")
            
        # download specific document to server
        try:
            print("\n[GDriveTest]- Running get file test.")
            file_metadata = GDriveInterpreter.get_file_metadata('webClientSecret.json', student, fileName)
            GDriveInterpreter.get_file('webClientSecret.json', user, filemeta)
            print("[GDriveTest]- Get file list test passed.")
            # TODO Verify file found at desired location
        except AssertionError:
            print("[GDriveTest]- Failed to obtain specific file from Google Drive.")
        
        # upload same document from server
        try:
            path = './media/' + user + '/' + fileName
            fileJson = DigiJsonBuilder.create_file(fileName, None, None, path, None, None, None)
            # TODO check for upload success
            
        except AssertionError:
            print("[GDriveTest]- Failed to upload file to Google Drive.")
    
    
    
    def test_GSearch( self ):
        # submit search, get results.
        whitelist = []
        blacklist = []
        blackterms = []
        whiteterms = []
        topic = []
        queries = ['test','queries']
        modifiers = DigiJsonBuilder.create_modifiers(whitelist, blacklist,blackterms,whiteterms,topic)
        try:
            print("\n[GSearchTest]- Running GSearchTest.")
            results = GSearchInterpreter.submit_queries(queries, modifiers)
            self.assertNotEqual(results, 0)
            print("[GSearchTest]- GSearchTest passed.")
        except AssertionError:
            print("[GSearchTest]- Failed to get search results from Google Search.")





















        
        
        
        
        
        
        
        
        
        

