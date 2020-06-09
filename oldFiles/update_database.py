import re
import os
import pickle
import numpy as np
import pandas as pd
import mysql.connector as connector

SELECT_QUERY  = "SELECT * FROM docs_leidos where grupo = %s"
INSERT_QUERY =  "INSERT INTO docs_leidos (path_to_file, leido, exist, grupo) VALUES (%s, %s, %s, %s)"
DELETE_QUERY = "DELETE FROM docs_leidos where grupo = %s"

mydb = connector.connect(
  host="host",
  user="user",
  passwd="pass",
  database="db"
)



def update_database(directory,typ):
    list_current_data = []

    cursor = mydb.cursor()
    cursor.execute(SELECT_QUERY,(typ,))
    list_data = cursor.fetchall()
    set_names_data = set([x[1].strip() for x in list_data])
    print(len(set_names_data))


    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.pdf'):
                  list_current_data.append(str(os.path.join(root,file_name)).strip())

            if file_name.endswith(".docx") or file_name.endswith(".doc"):
              if file_name.startswith("~"):
                  continue
              elif file_name.startswith("."):
                  continue
              list_current_data.append(str(os.path.join(root,file_name)).strip())

    set_current_data =  set(list_current_data)

    insert_data = [(x,0,1,typ) for x in list(set_current_data.difference(set_names_data))]
    print(len(insert_data))

    list_exist = list(set_names_data.intersection(set_current_data))
    for x in list_data:
        if x[1].strip() in list_exist:
            insert_data.append((x[1],x[2],x[3],x[4]))


    cursor.execute(DELETE_QUERY,(typ,))
    print(len(insert_data))
    cursor.executemany(INSERT_QUERY, insert_data)

    mydb.commit()

    print(cursor.rowcount, "was inserted.")
