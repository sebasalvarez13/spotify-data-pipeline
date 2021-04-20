#!usr/bin/env python3

from flask import Flask, render_template, request, redirect
from main import CreatePlaylist
from authorization import get_authorization, get_token
from table_display import songdisplay

app = Flask(__name__)

output = {}
table = 'my_songs_played'


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('authorization.html')

@app.route("/callback", methods=["GET", 'POST'])
def callback():
    print(get_authorization())
    return render_template("callback.html") 

@app.route("/getsongs", methods=["GET", 'POST'])
def load_to_table():
    code = request.form["code"] 
    user_name = request.form["user_name"]
    days_ago = request.form["days_ago"]

    #pass code to obtain toke
    response_json = get_token(code)
    token = response_json["access_token"]
    print(token)

    #pass days_ago to spotify_pipeline_aws script
    cp = CreatePlaylist(int(days_ago), token)
    cp.load_to_table()

    songdisplay(cp.get_spotify_songs())
    
    print("all modification done...")
    return render_template('output.html')


@app.route("/about", methods=["GET"])
def about():
    return redirect("https://www.spotify.com/us/")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
