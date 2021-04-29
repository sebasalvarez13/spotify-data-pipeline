#!/usr/bin/env python3
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from listening_times import filter_times

def piechart(user_name):
    songs_recurrence = filter_times()
    #y = np.array(songs_recurrence)
    labels = ["Commute", "Work", "Unwine", "Sleep"]

    fig = plt.figure(1, figsize=(6,6))
    ax = fig.add_subplot(111)
    colors=('b', 'g', 'r', 'y')
    ax.pie(songs_recurrence, colors = colors , labels = labels, autopct = '%1.1f%%', textprops = {'fontsize': 14})
    plt.title("Times of most activity", fontsize = 22)
    plt.legend(["5-9am", "9-5pm", "5-10pm", "10-5am"])

    plt.savefig("static/{}_spotichart.png".format(user_name))



if __name__ == "__main__":
    piechart()    
