import pickle
import os
import mysql.connector as connector

UPDATE_SQL = "UPDATE docs_leidos SET leido = %s WHERE path_to_file = %s"

mydb = connector.connect(
  host="host",
  user="user",
  passwd="pass",
  database="db"
)

def update_database(ORIG_PICKLE):
    try:
        with open(ORIG_PICKLE, 'rb') as f:
            orig_read_file, orig_read_text, orig_read_type = pickle.load(f)
    except:
        orig_read_file, orig_read_text, orig_read_type = [], [], []
        print('tripla orig no abrio')

    orig_read_file = [(1,'/run/user/1000/gvfs/smb-share:server=10.20.135.21,share=archivos'+x.split('/archivos')[1].strip()) for x in orig_read_file]
    cursor = mydb.cursor()

    cursor.executemany(UPDATE_SQL, orig_read_file)

    mydb.commit()
    print(len(orig_read_file))
