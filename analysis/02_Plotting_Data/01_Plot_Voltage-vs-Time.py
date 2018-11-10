"""

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

CSVDATA_DIR = COMPUTE1_HOME + "/Documents/Experiment-Data-Dump/wqkhan_Raspi_Digitizer/dataLogstoCSV"
PLOT_DIR = COMPUTE1_HOME + "/Documents/Experiment-Data-Dump/wqkhan_Raspi_Digitizer/plots"


def plot_time_vs_voltage(dataFolder, plotFolder):
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
                         nrows=samplesToPlot,
                         usecols=['Voltage(mV)'],
                         )

        (row, col) = df.shape
        print("Number of Rows: {} and Col: {}".format(row, col))
        columnNames = list(df.columns.values)
        print("Data has columns: {}".format(columnNames))

        # Time column
        df.insert(0, 'Time(s)',[float(x)*sample_period for x in range(len(df))])


        time = df['Time(s)']
        signal = df['Voltage(mV)']

        max_signal = signal.max()
        min_signal = signal.min()
        print("The signle goes from: {} - {}".format(min_signal, max_signal))


        # # Option 1: Using matplotlib to generate a static plot
        print("Plot static image using matplotlib")

        plt.plot(time, signal, c='r', label='Voltage(mV)')
        plt.xlabel('Time(s)')
        plt.xticks(rotation='vertical')
        plt.ylabel('Voltage(mV)')
        plt.title('Digitizer DAQ\nTime vs Voltage')
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
            name='Voltage'
        )

        data = [trace]

        layout = dict(
            title='Power Tracing at {} SPS with Voltage max peak: {}'.format(1 / sample_period, voltageRange),
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

    plot_time_vs_voltage(dataFolder=CSVDATA_DIR, plotFolder=PLOT_DIR)