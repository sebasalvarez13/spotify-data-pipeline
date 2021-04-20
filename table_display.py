#!/usr/bin/env python3

import pandas as pd
from IPython.display import HTML
from main import CreatePlaylist

def songdisplay(df):
    #cp = CreatePlaylist(1)
    #df = cp.get_spotify_songs()
    df = df

    html = df.to_html()

    output_file = "templates/output.html"
    # write html to file
    try:
        with open(output_file, 'w') as outputtable:
            outputtable.write(
         """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        .container{
        display: inline-block;
        width: 1000px;
        height: 700px;
        border: 1px solid black;
        overflow: auto;
        }
        table {
        border-collapse: collapse;
        width: 100%;
        }
        td {
        text-align: left;
        padding: 8px;
        }
        th {
        text-align: left;
        padding: 8px;
        height: 10px;
        }
        tr:nth-child(even) {background-color: #f2f2f2;}
        </style>
        </head>
        <body>
        <h2>Recent Played Songs Table</h2>
        <p>A responsive table will display a horizontal scroll bar if the screen is too 
        small to display the full content. Resize the browser window to see the effect:</p>
        <div class = container>
        """
            )
            outputtable.write(html)
            outputtable.write(
        """
        </div>
        </body>
        </html>
        """
            )
    except IOError as e:
        print(e)

