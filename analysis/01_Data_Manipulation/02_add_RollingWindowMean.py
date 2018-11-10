'''
Compute the rolling window mean of the signal data
'''


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

SCRIPT_DIR = sys.path[0]
SCRIPT_NAME = str(sys.argv[0]).split("/")[-1]
FILE_NAME =  os.path.basename(sys.argv[0])
HOME = os.environ['HOME']
COMPUTE1_HOME = "/rhome/wqkhan"

CSVDATA_DIR = COMPUTE1_HOME + "/Documents/Experiment-Data-Dump/wqkhan_Raspi_Digitizer/dataLogstoCSV"
MEANDATA_DIR = COMPUTE1_HOME + "/Documents/Experiment-Data-Dump/wqkhan_Raspi_Digitizer/dataLogstoCSVmean"


def RollingWindoe_Mean(dataFolder, outputFolder):
    '''

    :param dataFolder:
    :param outputFolder:
    :return:
    '''


    csvFiles = sorted(glob.glob(dataFolder + "/*.csv"))

    for csvFile in csvFiles:

        base = os.path.basename(csvFile)
        file_name, file_ext = os.path.splitext(base)

        MSPS = int(re.search(r'\d+', base.split("--")[1]).group())
        voltageRange = int(re.search(r'\d+', base.split("--")[2]).group())
        sample_period=(1/(MSPS*10**6))

        print("Processing: {} with: \tMSPS={} & VoltageRange={}".format(base, MSPS, voltageRange))

        df = pd.read_csv(csvFile, sep=",",
                         # nrows=1000000,
                         # usecols=['Voltage(mV)'],
                         )

        (row, col) = df.shape
        print("Number of Rows: {} and Col: {}".format(row, col))
        columnNames = list(df.columns.values)
        print("Data has columns: {}".format(columnNames))

        # Calculate the mean
        df['MA_100'] = df['Voltage(mV)'].rolling(100, center=True).mean()

        # Time column
        df.insert(0, 'Time(s)',[float(x)*sample_period for x in range(len(df))])

        # Write data to CSV
        df.to_csv(outputFolder + "/" + file_name + "_voltage-mV_mean.csv", index=False, header=True)


if __name__ == '__main__':

    print("Starting script {}".format(FILE_NAME))

    RollingWindoe_Mean(dataFolder=CSVDATA_DIR, outputFolder=MEANDATA_DIR)