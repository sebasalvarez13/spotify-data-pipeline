#!/usr/bin/env python3

import pandas as pd
from IPython.display import HTML
from topartists import topartists
from recent_songs import recentsongs

def table_display(df1, df2):
    """Takes a dataframe as parameter and displays content as a responsive table in html page"""
    
    df1 = df1
    df2 = df2
    
    html1 = df1.to_html()
    html2 = df2.to_html()

    output_file = "templates/output.html"

    try:
        with open(output_file, 'w') as outputtable:
            outputtable.write(
            """
            <!DOCTYPE html>
            <html>
            <head>
                <link rel="stylesheet" href="/static/tables.css?v=1.1" type="text/css"></link>
                <style>
                    tr:nth-child(even) {background-color: #f2f2f2;}
                </style>
            </head>
            
            <body>
                <h2>Recent Played Songs Table</h2>
                <p>Take a look at your latest songs</p>
                <div class = container1>
            """
            )
            outputtable.write(html1)
            outputtable.write(
            """
                </div>
            """
            )
            outputtable.write(
            """
                <div class = container2>
            """    
            )
            outputtable.write(html2)
            outputtable.write(
            """
                </div>
            """
            )
            outputtable.write(
            """      
            </body>
            </html>
            """
            )
            
    except IOError as e:
        print(e)


if __name__ == "__main__":
    df1 = recentsongs()
    df2 = topartists()
    table_display(df1, df2)