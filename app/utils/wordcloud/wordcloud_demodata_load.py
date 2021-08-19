'''
Notebook used to load the demo data into a hosted Postgres database.
Demo data is 167 transcribed anonymous student story submissions.
Database will be hosted on AWS to be used as demo data
for the word cloud feature for the parent dashboard.

Commented out. Uncomment and use it again to create a database.
'''

# import psycopg2
# import os
# from dotenv import load_dotenv
# import sqlite3
# from sqlite3 import Error
# from zipfile import ZipFile
# from psycopg2.extras import execute_values

# load_dotenv()

# def create_connection():
#     """elephantsql connection"""
#     #connect to ElephantSQL-hosted PostgreSQL
#     DB_NAME = os.getenv("DB_NAME", default="OOPS")
#     DB_USER = os.getenv("DB_USER", default="OOPS")
#     DB_PASSWORD = os.getenv("DB_PASSWORD", default="OOPS")
#     DB_HOST = os.getenv("DB_HOST", default="OOPS")

#     pg_connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    
#     return pg_connection

# def insert_data(conn, story):
#     '''
#     Insert the demo data into the table
#     '''
#     sql = f'''INSERT INTO stories (story)
#              VALUES (%s)'''
#     cur = conn.cursor()
#     cur.execute(sql, story)
#     conn.commit()
#     return cur.lastrowid

# def ingest_zip():
#     '''opens the zip file of the submissions'''
#     z = ZipFile(r'C:\Users\temsy\Downloads\story transcripts.zip', 'r')
#     text_files = z.infolist()

#     return z, text_files

# def create_table(conn, create_table_sql):
#     try:
#         c = conn.cursor()
#         c.execute(create_table_sql)
#     except Error as e:
#         print(e)

# def fetch_sqlite():
#     sql_connection = sqlite3.connect("test_data.db")
#     sql_cursor = sql_connection.cursor()

#     '''fetch all stories from db'''
#     query = """SELECT*FROM stories"""
#     all_stories = sql_cursor.execute(query).fetchall()

#     return all_stories

# def main():

#     '''Creates the table'''
#     sql_create_table = f""" DROP TABLE stories;
#                             CREATE TABLE IF NOT EXISTS stories (
#                             id SERIAL PRIMARY KEY,
#                             story text
#                             );"""

#     conn = create_connection()

#     if conn is not None:
#         create_table(conn, sql_create_table)

#     else:
#         print("Error, cannot create the database connection")

#     '''ingest zipfile of demo data'''
#     z, text_files = ingest_zip()

#     '''Inserts the data into the table'''
#     for file in text_files:
#         text = z.read(file)
#         insert_data(conn, [str(text)])

# if __name__ == '__main__':
#     main()
