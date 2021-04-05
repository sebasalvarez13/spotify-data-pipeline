#!/usr/bin/env python3

import sqlite3
import sqlalchemy
import requests
import pandas as pd
from table_display import songdisplay

def topartist():
    DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
    #song_df = self.get_spotify_songs()
    #engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('my_played_tracks.sqlite')
    cursor = conn.cursor()

    sql_query = """
    SELECT "artist_name",
        COUNT("artist_name") AS "value_occurence"
        FROM "my_played_tracks"
        GROUP BY "artist_name"
        ORDER BY "value_occurence" DESC
        LIMIT 3;

    """
    cursor.execute(sql_query)
    print("Results fetched")

    results = pd.read_sql_query(sql_query, conn) 

    conn.close()
    print("Close database successfully")

    return(results)
