#!/usr/bin/env python3

"""Create a script to automate creation of Spotify playlist from liked Youtube videos"""

import json
import requests
import os
import re
import pandas as pd
import datetime
from datetime import timezone
import sqlite3
import sqlalchemy
import pymysql
from pymysql import connections



from secrets import user_id, client_id, client_secret
from rds_connection import rds_connect
from aws_config import *

class CreatePlaylist:
    def __init__(self, days_ago, spotify_token):
        self.days_ago = days_ago
        self.user_id = user_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.spotify_token = spotify_token

    def set_time_period(self):
        today = datetime.datetime.now()
        days_difference = datetime.timedelta(days = self.days_ago)
        starting_day = today - days_difference
        starting_day_unix_timestamp = int(starting_day.timestamp()) * 1000

        return(starting_day_unix_timestamp)

    def utc_to_local(utc_dt):
        return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

    def get_spotify_songs(self):
        time = self.set_time_period()
        limit = 50 #max number of items that can be returned
        
        query = "https://api.spotify.com/v1/me/player/recently-played?limit={}&after={}".format(limit, time)

        response = requests.get(
            query,
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)}
        )

        data = response.json()
        
        song_names = []
        artist_names = []
        song_played_at = []
        date_played = []

        for song in data["items"]:
            #spotify returns time as a string in UTC.
            spotify_time_str = song["played_at"]
            #filter string from  ".xxxZ" element
            spotify_time_str_fltrd = re.search("[0-9]+\-[0-9]+\-[0-9]+T[0-9]+\:[0-9]+\:[0-9]+", spotify_time_str)
            print(spotify_time_str_fltrd.group())
            #convert time string to datetime object
            try:
                spotify_time_obj = datetime.datetime.strptime(spotify_time_str_fltrd.group(), "%Y-%m-%dT%H:%M:%S")
                break
            except ValueError as ve:
                print(ve)
            #convert datetime object in UTC to local time
            local_time_obj = spotify_time_obj.replace(tzinfo=timezone.utc).astimezone(tz=None)

            #strip datetime object in local time into time and date
            time = local_time_obj.strftime("%H:%M:%S")
            date = local_time_obj.strftime("%m-%d-%Y")

            #append the values of the returned songs into their respective lists
            song_names.append(song["track"]["name"])
            artist_names.append(song["track"]["album"]["artists"][0]["name"])
            song_played_at.append(time)
            date_played.append(date)

        #create a dictionary with the lists 
        song_dict = {
            "song_name" : song_names,
            "artist_name": artist_names,
            "played_at": song_played_at,
            "date": date_played
        }

        #create a dataframe object using the previous dictionary as input parameter
        song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "date"])
        
        return(song_df)

    def delete_repeated_songs(self):
        song_dict = self.get_spotify_songs()
        songs_list = []
        for name in song_dict.get("song_name"):
            if name not in songs_list:
                songs_list.append(name)

        songs_names = pd.DataFrame(songs_list)
        return(songs_names)
        
    def load_to_table(self):
        #DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
        song_df = self.get_spotify_songs()
        engine = sqlalchemy.create_engine("mysql+pymysql://{}:{}@{}:3306/recent_played_songs".format(custom_user, custom_pass, custom_host))
        #conn = sqlite3.connect('my_played_tracks.sqlite')
        conn = connections.Connection(
           host = custom_host,
           port = 3306,
           user = custom_user,
           password = custom_pass,
           db = custom_db
        )
        cursor = conn.cursor()

        sql_query = """
        CREATE TABLE IF NOT EXISTS my_played_tracks(
            song_name VARCHAR(200),
            artist_name VARCHAR(200),
            played_at VARCHAR(200),
            date VARCHAR(200)
        )
        """

        cursor.execute(sql_query)
        print(song_df)
        print("this is the engine type: {}".format(type(engine)))
        print("Opened database successfully")

        try:
            song_df.to_sql(name = "my_played_tracks", con = engine, index=False, if_exists="replace")
        except Exception as e:
            print(e)

        conn.close()
        print("Close database successfully")

if __name__ == "__main__":
    cp = CreatePlaylist(1)
    cp.load_to_table()
