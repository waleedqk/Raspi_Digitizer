"""
The code takes in a csv file that has a column for voltage value recorded by the digitizer
The function asks for two such files and loads the values fro them
The function takes in the csv file and plots it both as a png and as an interactive html file
"""
import os, sys, time
import re
import glob
import argparse

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import plotly
import plotly.plotly as py
import plotly.graph_objs as go

"""
Plot the voltage recorded from the digitizer from a no-data send trace and a heavy data send trace to see the difference in power consumption

Example run:
python3 03_Plot_Normal_vs_Heavy_Load.py -n 2018-10-23-1016--50MSPS--800mV--Raspi_Digitizer_l1_c1_zeroTrans_allConnected_voltage-mV.csv -c 2018-10-23-1029--50MSPS--800mV--Raspi_Digitizer_l4_c2_10MBmaxFlow_dualSender_voltage-mV.csv -s 10000

REFERENCES
https://plot.ly/python/axes/
https://plot.ly/python/subplots/
https://stackoverflow.com/questions/20906474/import-multiple-csv-files-into-pandas-and-concatenate-into-one-dataframe
"""

SCRIPT_DIR = sys.path[0]
SCRIPT_NAME = str(sys.argv[0]).split("/")[-1]
FILE_NAME =  os.path.basename(sys.argv[0])
HOME = os.environ['HOME']
COMPUTE1_HOME = "/rhome/wqkhan"

CSVDATA_DIR = HOME + "/Documents/Experiment-Data-Dump/wqkhan_Raspi_Digitizer/dataLogstoCSV"
PLOT_DIR = HOME + "/Documents/Experiment-Data-Dump/wqkhan_Raspi_Digitizer/plots"

def plot_normal_vs_heavy_load(normalData, CompareData, plotFolder, sampleSize=1000):


    normalData = CSVDATA_DIR + "/" + os.path.basename(normalData)
    CompareData = CSVDATA_DIR + "/" + os.path.basename(CompareData)

    # if either of the files do not exist - exit the function
    if (not os.path.isfile(normalData)) or (not os.path.isfile(CompareData)):
        print("A file specified by the parameters does on exists - Exiting the function")
        exit(1)

    # Compute the digitizer parameters for each input file

    baseNormal = os.path.basename(normalData)
    file_nameNormal, file_extCompare = os.path.splitext(baseNormal)
    MSPSNormal = int(re.search(r'\d+', baseNormal.split("--")[1]).group())
    voltageRangeNormal = int(re.search(r'\d+', baseNormal.split("--")[2]).group())
    sample_periodNormal = (1 / (MSPSNormal * 10 ** 6))

    baseCompare = os.path.basename(CompareData)
    file_nameCompare, file_extCompare = os.path.splitext(baseCompare)
    MSPSCompare = int(re.search(r'\d+', baseCompare.split("--")[1]).group())
    voltageRangeCompare = int(re.search(r'\d+', baseCompare.split("--")[2]).group())
    sample_periodCompare = (1 / (MSPSCompare * 10 ** 6))

    # Number of rows to skip to see viable data
    skiprows = 100000000

    # Initialize a dataframe
    df = pd.DataFrame()

    # load the respective voltage column for each of the signals

    dff_a = pd.read_csv(normalData, sep=",",
                        nrows=sampleSize,
                        skiprows=range(1, skiprows),  # to keep the header row but skip the next n rows
                        usecols=['Voltage(mV)'],
                     )
    dff_b = pd.read_csv(CompareData, sep=",",
                        nrows=sampleSize,
                        skiprows=range(1, skiprows),  # to keep the header row but skip the next n rows
                        usecols=['Voltage(mV)'],
                     )

    df['mV_Normal'] = dff_a['Voltage(mV)']
    df['mV_Compare'] = dff_b['Voltage(mV)']

    del dff_a, dff_b

    # Add the time column associated with each signal trace
    df['mV_Normal_Time_s'] = [float(x) * sample_periodNormal for x in range(sampleSize)]
    df['mV_Compare_Time_s'] = [float(x) * sample_periodCompare for x in range(sampleSize)]


    # Stacked Subplots with a Shared X-Axis
    print("Plot interactive web graph using plotly")

    trace1 = go.Scatter(
        x=df['mV_Normal_Time_s'],
        y=df['mV_Normal'],
        mode='lines',
        name='Voltage Normal Trace (mV)',
        # yaxis = 'y1'
    )

    trace2 = go.Scatter(
        x=df['mV_Compare_Time_s'],
        y=df['mV_Compare'],
        mode='lines',
        name='Voltage Heavy Trace (mV)',
        # yaxis='y2'
    )

    data = [trace1, trace2]


    layout = dict(
        title='Normal Power Trace to Heavy Load Trace',
        legend=dict(
            traceorder='reversed'
        ),
        xaxis=dict(
            title='Time(s)',
            showticklabels=True,
            tickangle=45,
            rangeslider=dict(
                visible=True
            ),
        ),

        yaxis=dict(
            title='Voltage (mV)',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            ),
            # range=[min_signal - (abs(min_signal) * 0.1), max_signal + (max_signal * 0.1)],
        )
    )

    fig = dict(data=data, layout=layout)

    plotly.offline.plot(
        fig,
        filename=plotFolder + '/Normal_vs_Heavy_Load_Trace.html',
        auto_open=False)


def init_parser():
    parser = argparse.ArgumentParser(description="Plot Normal Power Load vs Comparative Use Power Load")

    parser.add_argument('-n', '--normal-data', type=str, required=True,
                        help="Name of normal data csv file")
    parser.add_argument('-c', '--compare-data', type=str, required=True,
                        help="Name of comparison data csv file")
    parser.add_argument('-s', '--sample-size', type=int, required=True,
                        help="How many rows to take for the plot")

    return parser


if __name__ == '__main__':

    print("Starting script {}".format(FILE_NAME))

    parser = init_parser()
    args = parser.parse_args()

    plot_normal_vs_heavy_load(normalData=args.normal_data, CompareData=args.compare_data, sampleSize=args.sample_size, plotFolder=PLOT_DIR)