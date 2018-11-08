"""
The code takes in a csv file that has two columns, comma seperated
One column is time the second is the voltage value recorded by the digitizer

The function takes in the csv file and plots it both as a png and as an interactive html file
"""
import os, sys, time
import re
import glob

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import plotly
import plotly.plotly as py
import plotly.graph_objs as go

"""
REFERENCES: 
https://plot.ly/python/range-slider/#basic-range-slider-and-range-selectors
"""

SCRIPT_DIR = sys.path[0]
SCRIPT_NAME = str(sys.argv[0]).split("/")[-1]
FILE_NAME =  os.path.basename(sys.argv[0])
HOME = os.environ['HOME']
COMPUTE1_HOME = "/rhome/wqkhan"

CSVDATA_DIR = COMPUTE1_HOME + "/Documents/Experiment-Data-Dump/wqkhan_Raspi_Digitizer/dataLogstoCSVmean"
PLOT_DIR = COMPUTE1_HOME + "/Documents/Experiment-Data-Dump/wqkhan_Raspi_Digitizer/plots"


def plot_time_vs_mean(dataFolder, plotFolder):
    '''

    :param dataFolder:
    :param plotFolder:
    :return:
    '''

    # the number of samples used in drawing the plot
    samplesToPlot = 10000000


    csvFiles = sorted(glob.glob(dataFolder + "/*.csv"))

    for csvFile in csvFiles:

        base = os.path.basename(csvFile)
        file_name, file_ext = os.path.splitext(base)

        MSPS = int(re.search(r'\d+', base.split("--")[1]).group())
        voltageRange = int(re.search(r'\d+', base.split("--")[2]).group())
        sample_period=(1/(MSPS*10**6))

        print("Processing: {} with: \tMSPS={} & VoltageRange={}".format(base, MSPS, voltageRange))

        df = pd.read_csv(csvFile, sep=",",
                         skiprows=range(1, 100), # to keep the header row but skip the next n rows
                         nrows=samplesToPlot,
                         usecols=['Time(s)', 'MA_100'],
                         )

        (row, col) = df.shape
        print("Number of Rows: {} and Col: {}".format(row, col))
        columnNames = list(df.columns.values)
        print("Data has columns: {}".format(columnNames))


        time = df['Time(s)']
        signal = df['MA_100']

        max_signal = signal.max()
        min_signal = signal.min()
        print("The signle goes from: {} - {}".format(min_signal, max_signal))


        # # Option 1: Using matplotlib to generate a static plot
        print("Plot static image using matplotlib")

        plt.plot(time, signal, c='r', label='MEAN_100')
        plt.xlabel('Time(s)')
        plt.xticks(rotation='vertical')
        plt.ylabel('Mean (mV) per 100 samples')
        plt.title('Digitizer DAQ\nTime vs Mean Voltage per 100 samples')
        plt.legend()
        plt.tight_layout()
        # plt.show()
        plt.savefig(plotFolder + '/' + file_name + '.png')




        # # Option 2: Using plotly to create a web-based interactive plot
        print("Plot interactive web graph using plotly")

        # Create a trace
        trace = go.Scatter(
            x=time,
            y=signal,
            mode='lines',
            name='Mean (mV)'
        )

        data = [trace]

        layout = dict(
            title='Mean 100 sample Power Tracing \n{} SPS with Voltage max peak: {}'.format(1 / sample_period, voltageRange),
            xaxis=dict(
                title='Time(s)',
                showticklabels=True,
                tickangle=45,
                rangeslider=dict(
                    visible=True
                ),
            ),
            yaxis = dict(
                title='Voltage (mV)',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                ),
                range=[min_signal - (abs(min_signal)*0.1), max_signal + (max_signal*0.1)],
            )
        )

        fig = dict(data=data, layout=layout)

        plotly.offline.plot(
            fig,
            filename=plotFolder + '/' + file_name + '.html',
            auto_open=False)


if __name__ == '__main__':

    print("Starting script {}".format(FILE_NAME))

    plot_time_vs_mean(dataFolder=CSVDATA_DIR, plotFolder=PLOT_DIR)