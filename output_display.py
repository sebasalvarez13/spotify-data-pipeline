#!/usr/bin/env python3

import pandas as pd
from IPython.display import HTML
from topartists import topartists
from recent_songs import recentsongs

#def output_display(df1, df2, name, last_name):
def output_display(df1, df2):
    """Takes a dataframe as parameter and displays content as a responsive table in html page"""

    html1 = df1.to_html()
    html2 = df2.to_html()

    output_file = "/var/www/html/spotiSights/templates/output.html"
    #chart_name = "{}_{}_chart.png".format(name, last_name)

    str1 = """
            <!DOCTYPE html>
            <html lang="es">
            <head>
            <meta charset="utf-8"/>
                <link rel="stylesheet" href="/static/tables.css?v=1.1" type="text/css"></link>
                <link rel="stylesheet" href="/static/images.css?v=1.1" type="text/css"></link>
                <style>
                    tr:nth-child(even) {background-color: #f2f2f2;}
                </style>
            </head>

            <body>
                <h2>Spotify Insights</h2>
                <p>Take a look at your recent Spotify playing history, top listened artists and
                listening activity during your day.</p>
            """

    try:
        with open(output_file, "wb") as outputtable:
            outputtable.write(str1.encode(encoding = "UTF-8",errors = "strict"))
            outputtable.write("<div class = container1>\n".encode(encoding = "UTF-8",errors = "strict"))
            outputtable.write(html1.encode(encoding = "UTF-8", errors = "strict"))
            outputtable.write("</div>\n".encode(encoding = "UTF-8",errors = "strict"))
            outputtable.write("<div class = container2>\n".encode(encoding = "UTF-8",errors = "strict"))
            outputtable.write(html2.encode(encoding = "UTF-8",errors = "strict"))
            outputtable.write("</div>\n".encode(encoding = "UTF-8",errors = "strict"))
            #outputtable.write("<div class = img>")
            #outputtable.write("<img src='static/{}' alt='spotichart'>".format(table_name)
            #outputtable.write("<\div>")
            outputtable.write("</body>\n</html>".encode(encoding = "UTF-8",errors = "strict"))

    except Exception as e:
        print(e)


if __name__ == "__main__":
    output_display()
