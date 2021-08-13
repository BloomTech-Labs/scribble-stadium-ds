'''
Notebook used to load the demo data into a local database.
Demo data is 167 transcribed anonymous student story submissions.
Database will be hosted on AWS to be used as demo data
for the word cloud feature for the parent dashboard.
'''

import sqlite3
from sqlite3 import Error
from zipfile import ZipFile


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_data(conn, story):
    '''
    Insert the demo data into the table
    '''
    sql = '''INSERT INTO stories(story)
             VALUES(?)'''
    cur = conn.cursor()
    cur.execute(sql, story)
    conn.commit()
    return cur.lastrowid

def ingest_zip():
    '''opens the zip file of the submissions'''
    z = ZipFile(r'C:\Users\temsy\Downloads\story transcripts.zip', 'r')
    text_files = z.infolist()

    return z, text_files

def main():
    database = r"C:\Users\temsy\Documents\GitHub\ebtest\test_data.db"

    '''Creates the table'''
    sql_create_table = """ CREATE TABLE IF NOT EXISTS stories (
                            story text
                            );"""

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_table)
    
    else:
        print("Error, cannot create the database connection")

    '''ingest zipfile of demo data'''
    z, text_files = ingest_zip()


    '''Inserts the data into the table'''
    for file in text_files:
        text = z.read(file)
        insert_data(conn, [text])
 
if __name__ == '__main__':
    main()