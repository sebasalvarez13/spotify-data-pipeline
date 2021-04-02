#!usr/bin/env python3

from flask import Flask, render_template, request, redirect
from main import CreatePlaylist

app = Flask(__name__)

output = {}
table = 'my_songs_played'


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route("/about", methods=["GET"])
def about():
    return redirect("https://www.spotify.com/us/")


@app.route("/getdays", methods=['POST'])
def load_to_table():
    name = request.form["name"]
    user_name = request.form["user_name"]
    days_ago = request.form["days_ago"]

    #pass days_ago to spotify_pipeline_aws script
    cp = CreatePlaylist(int(days_ago))
    cp.load_to_table()

    print("all modification done...")
    return render_template('RecentPlayedSongsOutput.html', name = "Hey {}, here are your songs from {} days ago".format(name, days_ago))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
