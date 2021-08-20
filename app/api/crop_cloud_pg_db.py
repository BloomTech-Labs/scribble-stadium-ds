import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME', default='Check env variables')
DB_USER = os.getenv('DB_USER', default='Check env variables')
DB_PASSWORD = os.getenv('DB_PASSWORD', default='Check env variables')
DB_HOST = os.getenv('DB_HOST', default='Check env variables')


conn = psycopg2.connect(dbname = DB_NAME, user = DB_USER,
                                password = DB_PASSWORD, host = DB_HOST)

print("CONNECTION:", conn)

cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

print("CURSOR:", cur)

image_query = "SELECT id, image_url FROM cropcloud"

data = cur.execute(image_query)

records = cur.fetchall()

for row in records:
    if row['id'] ==1:
        print(row['image_url'])
