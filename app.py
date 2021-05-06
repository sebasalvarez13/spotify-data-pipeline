#!usr/bin/env python3

from flask import Flask, render_template, request, redirect
from main import CreatePlaylist
from authorization import get_authorization, get_token
from output_display import output_display
from topartists import topartists
from recent_songs import recentsongs
from pie_chart import piechart

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

    #pass code to obtain token
    response_json = get_token(code)
    print(response_json)
    token = response_json["access_token"]

    #pass name, last name and token to obtain Spotify played songs
    cp = CreatePlaylist(name, last_name, token)
    cp.load_to_table()

    #show recent songs and top artists tables
    df1 = recentsongs(name, last_name)
    df2 = topartists(name, last_name)

    #create pie chart
    piechart(user_name)

    output_display(df1, df2)


    return render_template('output.html')


@app.route("/about", methods=["GET"])
def about():
    return redirect("https://www.spotify.com/us/")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
