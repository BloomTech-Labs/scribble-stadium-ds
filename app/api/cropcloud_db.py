import pymysql
import os
import csv
from dotenv import load_dotenv
import boto3
from pymysql.cursors import DictCursor

load_dotenv()

class CropData:
    
    HOST_NAME = os.getenv('MY_SQL_HOSTNAME')
    USER_NAME = os.getenv('MY_SQL_USERNAME')
    PASSWORD = os.getenv('MY_SQL_PASSWORD')
    
    def __init__(self):
        self.HOST_NAME = self.HOST_NAME
        self.USER_NAME = self.USER_NAME
        self.PASSWORD = self.PASSWORD
        self.CONNECTION = pymysql.connect(host = self.HOST_NAME, user = self.USER_NAME, password = self.PASSWORD, cursorclass=DictCursor)
        self.CURSOR = self.CONNECTION.cursor()

    def GetImage(self, id):
        """Function to retrieve file name from RDS database

        Args:
            id (INT): id of user entry

        Returns:
            STR: File name in S3 bucket 
        """
        db_query = "USE cropcloud"
        image_query = 'SELECT id, image_url FROM cropcloud'
        self.CURSOR.execute(db_query)
        self.CURSOR.execute(image_query)
        records = self.CURSOR.fetchall()
        for row in records:
            if row['id'] == id:
                return row['image_url']
    
    def GetTranscript(self, id):
        """Function to retrieve transcript from id

        Args:
            id (INT): id of user entry

        Returns:
            STR: Transcript in S3 bucket
        """
        db_query = "USE cropcloud"
        transcript_query = "SELECT id, transcript FROM cropcloud"
        self.CURSOR.execute(db_query)
        self.CURSOR.execute(transcript_query)
        records = self.CURSOR.fetchall()
        for row in records:
            if row['id'] == id:
                return row['transcript']
    
    def GetSubmissionDateTime(self, id):
        """Function to retreive submission date time

        Args:
            id (INT): id of user entry

        Returns:
            STR: Submission Date and Time
        """
        db_query = "USE cropcloud"
        datetime_query = "SELECT id, submission_datetime FROM cropcloud"
        self.CURSOR.execute(db_query)
        self.CURSOR.execute(datetime_query)
        records = self.CURSOR.fetchall()
        for row in records:
            if row['id'] == id:
                return row['submission_datetime']

# Tests

db = CropData()

print(db.GetImage(3))
print(db.GetTranscript(3))
print(db.GetSubmissionDateTime(3))