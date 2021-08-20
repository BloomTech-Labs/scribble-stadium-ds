import pymysql
import os
import csv
from dotenv import load_dotenv
import boto3
from pymysql.cursors import DictCursor

load_dotenv()

HOST_NAME = os.getenv('MY_SQL_HOSTNAME')
USER_NAME = os.getenv('MY_SQL_USERNAME')
PASSWORD = os.getenv('MY_SQL_PASSWORD')

# DB Connection
crop_db_conn = pymysql.connect(host = HOST_NAME, user = USER_NAME, password = PASSWORD, cursorclass=DictCursor)
print("CONNECTION: ", crop_db_conn)

# DB Cursor
cursor = crop_db_conn.cursor()
print("CURSOR: ", cursor)

# SQL Queries
create_db_query = 'CREATE DATABASE cropcloud'
select_db_query = 'USE cropcloud'
create_table_query = 'CREATE TABLE IF NOT EXISTS cropcloud (id INTEGER, username VARCHAR(100), submission_datetime VARCHAR(100), transcript VARCHAR(10000), image_url VARCHAR(1000), PRIMARY KEY (id))'
insertion_query = 'INSERT INTO cropcloud (id, username, submission_datetime, transcript, image_url) VALUES (%s, %s, %s, %s, %s)'

# Creating DB - Run only once
# cursor.execute(create_db_query)
# cursor.connection.commit()

# Selecting DB
cursor.execute(select_db_query)
cursor.connection.commit()

# # Creating Table
# cursor.execute(create_table_query)
# cursor.connection.commit()

# # Inserting data
# with open('37 stories.csv', 'r') as f:
#     reader = csv.reader(f)
#     next(reader)
#     for row in reader:
#         cursor.execute(insertion_query, row)

# cursor.connection.commit()

## Testing if Table is created and populated
# cursor.execute("SELECT * FROM cropcloud")
# print(cursor.fetchone())

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', default = 'Check env variables')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', default = 'Check env variables')

s3 = boto3.client('s3', aws_access_key_id='AWS_ACCESS_KEY_ID', aws_secret_access_key='AWS_SECRET_ACCESS_KEY')

# Functions
def s3_GetImage(id):
    """Function to retrieve file name from RDS database

    Args:
        id (INT): id of user entry

    Returns:
        STR: File name in S3 bucket 
    """
    image_query = 'SELECT id, image_url FROM cropcloud'
    cursor.execute(image_query)
    records = cursor.fetchall()
    for row in records:
        if row['id'] == id:
            return row['image_url']

def s3_GetTranscript(id):
    """Function to retrieve transcript from id

    Args:
        id (INT): id of user entry

    Returns:
        STR: Transcript in S3 bucket
    """
    transcript_query = "SELECT id, transcript FROM cropcloud"
    cursor.execute(transcript_query)
    records = cursor.fetchall()
    for row in records:
        if row['id'] == id:
            return row['transcript']

print(s3_GetTranscript(1))













