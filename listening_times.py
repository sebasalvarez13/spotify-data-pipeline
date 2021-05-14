#!/usr/bin/env python3

import sqlalchemy
import requests
import datetime
import re
import pandas as pd
from main import CreatePlaylist
import pymysql
from pymysql import connections
from aws_config import *

def listen_times(table_name):
    conn = connections.Connection(
        host = custom_host,
        port = 3306,
        user = custom_user,
        password = custom_pass,
        db = custom_db
    )
    cursor = conn.cursor()

    sql_query = "SELECT song_name, played_at, COUNT(*) AS 'occurence' FROM {} GROUP BY song_name ORDER BY 'occurence' DESC".format(table_name)

    cursor.execute(sql_query)
    print("Getting listening times for {}".format(table_name))

    results = pd.read_sql_query(sql_query, conn)
    times = results["played_at"]

    conn.close()
    print("Close database successfully")

    return(times)


def filter_times(table_name):
    times = listen_times(table_name)
    commute = range(5,9)
    work = range(9,17)
    unwine = range(17,22)

    commute_list = []
    work_list = []
    unwine_list = []
    sleep_list = []

    print("Filtering listening times for {}".format(table_name))

    for i in range(0,times.size):
        match = re.search("([0-9]*):", times[i])
        hour_of_day = int(match.group(1))

        if hour_of_day in commute:
            commute_list.append(times[i])
        elif hour_of_day in work:
            work_list.append(times[i])
        elif hour_of_day in unwine:
            unwine_list.append(times[i])
        else:
            sleep_list.append(times[i])

    songs_recurrence = [len(commute_list), len(work_list), len(unwine_list), len(sleep_list)]
    print("Times filtered for {}".format(table_name))
    return(songs_recurrence)

