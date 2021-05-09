#!/usr/bin/env python3
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import boto3
from listening_times import filter_times
from aws_config import *


def piechart(name, last_name):
    songs_recurrence = filter_times(name, last_name)
    labels = ["Commute", "Work", "Unwind", "Sleep"]

    fig = plt.figure(1, figsize=(6,6))
    ax = fig.add_subplot(111)
    colors=('b', 'g', 'r', 'y')
    ax.pie(songs_recurrence, colors = colors , labels = labels, autopct = '%1.1f%%', textprops = {'fontsize': 14})
    plt.title("Times of activity", fontsize = 22)
    plt.legend(["5-9am", "9-5pm", "5-10pm", "10-5am"])

    chart_name = "{}_{}_chart.png".format(name, last_name)
    chart_name = chart_name.replace(" ", "")

    plt.savefig("static/{}".format(chart_name))

    #return(chart_name, fig)


if __name__ == "__main__":
    piechart()    
