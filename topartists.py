#!/usr/bin/env python3

import sqlite3
import sqlalchemy
import requests
import pandas as pd
import pymysql
from pymysql import connections

from aws_config import *

def topartists(table_name):
    conn = connections.Connection(
        host = custom_host,
        port = 3306,
        user = custom_user,
        password = custom_pass,
        db = custom_db
    )

    cursor = conn.cursor()

    sql_query = "SELECT artist_name, COUNT(*) AS 'occurence' FROM katie_zimmerman_songs_05132021T1512 GROUP BY artist_name ORDER BY occurence DESC LIMIT 5;"

    cursor.execute(sql_query)
    print("Results fetched")

    results = pd.read_sql_query(sql_query, conn) 

    conn.close()
    print("Close database successfully")

    return(results)

if __name__ == "__main__":
    artists = topartists()
    print(artists["artist_name"])
