#!usr/bin/env python3

from flask import Flask, render_template, request, redirect
from main import CreatePlaylist
from authorization import get_authorization, get_token
from output_display import output_display
from topartists import topartists
from recent_songs import recentsongs
from pie_chart import piechart
import datetime
import os

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("authorization.html")


@app.route("/callback", methods=["GET", "POST"])
def callback():
    url = get_authorization()
    if request.method == "POST":
        return redirect(url)
    return render_template("callback.html")


@app.route("/getsongs", methods=["GET", "POST"])
def load_to_table():
    code = request.form["code"]
    name = request.form["name"]
    last_name = request.form["last_name"] 
    user_name = request.form["user_name"]

    #remove white spaces and set name and last name to lower case
    name = (name.strip()).lower()
    last_name = (last_name.strip()).lower()

    #create table timestamp
    today = datetime.datetime.now()
    today_unix_timestamp = int(today.timestamp()) * 1000
    table_timestamp_str = datetime.datetime.strftime(today, "%m%d%YT%H%M")

    #create table name
    table_name = "{}_{}_songs_{}".format(name, last_name, table_timestamp_str)

    #pass code to obtain token
    response_json = get_token(code)
    token = response_json["access_token"]

    #pass name, last name and token to obtain Spotify played songs
    cp = CreatePlaylist(name, last_name, token, table_name)
    cp.load_to_table()

    #show recent songs and top artists tables
    df1 = recentsongs(table_name)
    df2 = topartists(table_name)

    #create pie chart
    #piechart(name, last_name)

    #output_display(df1, df2, name, last_name)
    output_display(df1, df2)

    return render_template('output.html')


@app.route("/about", methods=["GET"])
def about():
    return redirect("https://www.spotify.com/us/")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
