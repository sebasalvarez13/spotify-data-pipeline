#!/usr/bin/env python3

import pymysql
import requests
import pandas as pd
import sqlalchemy

from pymysql import connections
from aws_config import *

def recentsongs(name, last_name):
    #DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
    #conn = sqlite3.connect('my_played_tracks.sqlite')

    engine = sqlalchemy.create_engine("mysql+pymysql://{}:{}@{}:3306/recent_played_songs".format(custom_user, custom_pass, custom_host))
    conn = connections.Connection(
       host = custom_host,
       port = 3306,
       user = custom_user,
       password = custom_pass,
       db = custom_db
    )

    cursor = conn.cursor()

    table_name = "{}_{}_songs".format(name, last_name)
    table_name = table_name.replace(" ", "")
    sql_query = "SELECT * FROM {}".format(table_name)

    cursor.execute(sql_query)
    print("Results fetched")

    results = pd.read_sql_query(sql_query, conn) 

    conn.close()
    print("Close database successfully")

    return(results)

if __name__ == "__main__":
    recent = recentsongs()
    print(recent)

