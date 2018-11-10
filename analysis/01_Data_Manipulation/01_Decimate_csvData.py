import os, sys, time
import re
import glob
import argparse

import numpy as np
import scipy.signal 
from scipy.fftpack import fft, fftfreq, ifft
import pandas as pd


import pickle # For Saving interactive Matplotlib figures
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

# Location of where the csv data is - the file has a single column with a header
CSVDATA_DIR = HOME + "/Documents/Experiment-Data-Dump/wqkhan_Raspi_Digitizer/dataLogstoCSV"

# Location of where the csv data is - the file has 3 columns for time, voltage and mean with a header row
CSVDECIMATEDATA_DIR = HOME + "/Documents/Experiment-Data-Dump/wqkhan_Raspi_Digitizer/dataLogstoCSV_decimate"



def decimatedata(dataFolder, outputFolder):
    """

    :param log_folder:
    :param outputFolder:
    :return:
    """

    # The downsampling factor
    q = 10

    csvFiles = sorted(glob.glob(dataFolder + "/*.csv"))

    for csvFile in csvFiles:

        # the number of samples used in drawing the plot
        samplesToPlot = 100

        base = os.path.basename(csvFile)
        file_name, file_ext = os.path.splitext(base)

        MSPS = int(re.search(r'\d+', base.split("--")[1]).group())
        voltageRange = int(re.search(r'\d+', base.split("--")[2]).group())
        sample_period=(1/(MSPS*10**6))

        print("Processing: {} with: \tMSPS={} & VoltageRange={}".format(base, MSPS, voltageRange))

        df = pd.read_csv(csvFile,
                         sep=",",
                         # nrows=samplesToPlot,
                         usecols=['Voltage(mV)'],
                         )

        samplesToPlot = len(df)

        # decimate the column values with the specified factor
        # the return value is a numpy.array
        # cast it to a pandas dataframe
        dff = pd.DataFrame(data=scipy.signal.decimate(df['Voltage(mV)'].values, q, ftype='fir'),
                           columns=['Voltage(mV)'],
                           )

        # print(df['Voltage(mV)'].mean())
        # print(dff.mean())
        del df
        # print(dff)
        # print(type(dff))

        dff.to_csv(outputFolder + "/" + file_name + "_voltage-mV_decimate_{}.csv".format(q), index=False, header=True)



if __name__ == '__main__':

    print("Starting script {}".format(FILE_NAME))

    decimatedata(dataFolder=CSVDATA_DIR, outputFolder=CSVDECIMATEDATA_DIR)