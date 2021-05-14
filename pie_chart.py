#!/usr/bin/env python3
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import boto3
import logging
from botocore.exceptions import ClientError
from listening_times import filter_times
from aws_config import *


def piechart(table_name, chart_name, file_extension):
    songs_recurrence = filter_times(table_name)
    labels = ["Commute", "Work", "Unwind", "Sleep"]

    fig = plt.figure(1, figsize=(6,6))
    ax = fig.add_subplot(111)
    colors=('b', 'g', 'r', 'y')
    ax.pie(songs_recurrence, colors = colors , labels = labels, autopct = '%1.1f%%', textprops = {'fontsize': 14})
    plt.title("Times of activity", fontsize = 22)
    plt.legend(["5-9am", "9-5pm", "5-10pm", "10-5am"])

    print("Saving chart {} locally".format(chart_name))
    plt.savefig("/var/www/html/spotiSights/static/charts/{}.{}".format(chart_name, file_extension))
    print("Chart {} saved".format(chart_name))

    chart_path = "/var/www/html/spotiSights/static/charts/{}.{}".format(chart_name, file_extension)
    s3_bucket = custom_bucket
    s3_chart_name = chart_name

    #call upload to S3 method
    upload_to_s3(chart_path, s3_bucket, s3_chart_name)


def upload_to_s3(chart_path, s3_bucket, s3_chart_name):
    """Upload the chart to S3 bucket"""
    s3 = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_key)

    try:
       print("Uploading image to S3")
       s3.upload_file(chart_path, s3_bucket, s3_chart_name)
       print("Upload Successful")
       return True
    except FileNotFoundError:
       print("The file was not found")
       return False
    except NoCredentialsError:
       print("Credentials not available")
       return False

