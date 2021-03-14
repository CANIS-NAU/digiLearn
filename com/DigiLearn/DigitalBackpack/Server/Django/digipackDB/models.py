#imports
from django.db import models


'''
Model Name:  Student
Description: Abstracts a single student in the Digital Backpack system

Fields:
    studentId = Student's gmail address
    credentials: OAuth2 Credentials JSON file
'''
class Student( models.Model ):
    studentId = models.CharField( max_length=100, primary_key=True )
    credentials = models.JSONField(default="")
