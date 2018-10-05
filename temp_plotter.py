import matplotlib as mpl
mpl.use('Agg')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import argparse

def plotTemperature(secondsToPlot, data):
    e=np.array(data['epoch'])
    last = e[-1]
    start = last - secondsToPlot
    idx = e>start
    minTemp = np.array(data['min'])[idx]
    meanTemp = np.array(data['mean'])[idx]
    maxTemp = np.array(data['max'])[idx]
    dt = mdates.epoch2num(e)

    plt.plot_date(dt, meanTemp, xdate=True, linestyle='-', marker='.', label='mean')
    plt.plot_date(dt, minTemp, xdate=True, linestyle='-', marker='.', label='max')
    plt.plot_date(dt, maxTemp, xdate=True, linestyle='-', marker='.', label='min')
    plt.grid()
    plt.title('Last weeks temperature')
    plt.xlabel('Date')
    plt.ylabel('Temperature [degF]')
    plt.legend()
    plt.savefig('lastweek.png', dpi=600)
    #plt.show()

parser = argparse.ArgumentParser(description='Temperature Plotter.')
parser.add_argument('-f-', '--file', type=str, help='File to plot')

args = parser.parse_args()
print(args.file)

x = pd.read_csv(args.file)

# plot the last week of data
one_week = 7 * 24 * 3600
one_month = one_week * 4

plotTemperature(one_week, x)
