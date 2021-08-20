import os
import csv
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME', default='Check env variables')
DB_USER = os.getenv('DB_USER', default='Check env variables')
DB_PASSWORD = os.getenv('DB_PASSWORD', default='Check env variables')
DB_HOST = os.getenv('DB_HOST', default='Check env variables')

conn = psycopg2.connect(dbname = DB_NAME, user = DB_USER,
                                password = DB_PASSWORD, host = DB_HOST)

print("CONNECTION:", conn)

cur = conn.cursor()

sql_query = "INSERT INTO cropcloud (id, username, submission_datetime, transcript, image_url) VALUES (%s, %s, %s, %s, %s)"

# Getting data from .csv
with open('37 stories.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cur.execute(sql_query, row)

conn.commit()