'''
Compute the rolling window mean of the signal data
'''


import os, sys, time
import re
import glob
import random

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

CSVDATA_DIR = HOME + "/Documents/Experiment-Data-Dump/wqkhan_Raspi_Digitizer/dataLogstoCSV"
MEANDATA_DIR = HOME + "/Documents/Experiment-Data-Dump/wqkhan_Raspi_Digitizer/dataLogstoCSVmean"


def RollingWindoe_Mean(dataFolder, outputFolder):
    '''

    :param dataFolder:
    :param outputFolder:
    :return:
    '''
    d = {'Time': random.sample(range(100), 25)}
    df = pd.DataFrame(data=d)


    df['mean'] = df.Time.rolling(5, center=True).mean()

    print(df.head(25))

if __name__ == '__main__':

    print("Starting script {}".format(FILE_NAME))

    RollingWindoe_Mean(dataFolder=CSVDATA_DIR, outputFolder=MEANDATA_DIR)