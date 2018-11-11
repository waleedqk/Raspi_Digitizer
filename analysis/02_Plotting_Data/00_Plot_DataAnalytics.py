import os, sys, time
import re
import glob
import argparse

import numpy as np
from scipy.fftpack import fft, fftfreq, ifft
import pandas as pd


import pickle # For Saving interactive Matplotlib figures
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import plotly
import plotly.plotly as py
import plotly.graph_objs as go

"""
REFERENCES: 
https://plot.ly/python/range-slider/#basic-range-slider-and-range-selectors
https://plot.ly/python/axes/
https://plot.ly/python/subplots/
https://matplotlib.org/gallery/subplots_axes_and_figures/figure_title.html
https://stackoverflow.com/questions/20906474/import-multiple-csv-files-into-pandas-and-concatenate-into-one-dataframe

"""

SCRIPT_DIR = sys.path[0]
SCRIPT_NAME = str(sys.argv[0]).split("/")[-1]
FILE_NAME =  os.path.basename(sys.argv[0])
HOME = os.environ['HOME']
COMPUTE1_HOME = "/rhome/wqkhan"

# HOME = COMPUTE1_HOME

# Location of where the csv data is - the file has a single column with a header
CSVDATA_DIR = HOME + "/Documents/Experiment-Data-Dump/wqkhan_Raspi_Digitizer/dataLogstoCSV"

# Location of where the csv data is - the file has 3 columns for time, voltage and mean with a header row
CSVDECIMATEDATA_DIR = HOME + "/Documents/Experiment-Data-Dump/wqkhan_Raspi_Digitizer/dataLogstoCSV_decimate"

# Location of where the csv data is - the file has 3 columns for time, voltage and mean with a header row
CSVMEANDATA_DIR = HOME + "/Documents/Experiment-Data-Dump/wqkhan_Raspi_Digitizer/dataLogstoCSVmean"

# Location of where the plots are being stored
PLOT_DIR = HOME + "/Documents/Experiment-Data-Dump/wqkhan_Raspi_Digitizer/plots"

def plot_voltage(dataFolder, plotFolder):
    '''

    :param dataFolder: The location of the csv files that have a column for voltage value recorded by the digitizer
    :param plotFolder: The location of where the plots are to be saved
    :return:
    '''

    csvFiles = sorted(glob.glob(dataFolder + "/*.csv"))

    for csvFile in csvFiles:

        # the number of samples used in drawing the plot
        samplesToPlot = 10000000

        base = os.path.basename(csvFile)
        file_name, file_ext = os.path.splitext(base)

        MSPS = int(re.search(r'\d+', base.split("--")[1]).group())
        voltageRange = int(re.search(r'\d+', base.split("--")[2]).group())
        sample_period=(1/(MSPS*10**6))

        print("Processing: {} with: \tMSPS={} & VoltageRange={}".format(base, MSPS, voltageRange))

        df = pd.read_csv(csvFile, sep=",",
                         nrows=samplesToPlot,
                         skiprows=range(1, 3), # after decimate the first two readings are rampimg up to the actual value so to avoid seeing the spike in the splot, those values are omitted
                         usecols=['Voltage(mV)'],
                         )

        # 100147201 lines on decimated files
        samplesToPlot = len(df)

        (row, col) = df.shape
        print("Number of Rows: {} and Col: {}".format(row, col))
        columnNames = list(df.columns.values)
        print("Data has columns: {}".format(columnNames))

        # df.insert(0, 'Sample', [x for x in range(samplesToPlot)])


        # plot only a subset of the data points
        # the plots files are very large in size and cannot be loaded properly to view the full signal
        df = df[:int(samplesToPlot/3)]

        index = df.index
        signal = df['Voltage(mV)']

        print("Plot interactive web graph using plotly")

        # Create a trace
        trace = go.Scatter(
            x=index,
            y=signal,
            mode='lines',
            name='Voltage'
        )

        data = [trace]

        layout = dict(
            title='Power Tracing {} Data Points \nwith Voltage max peak: {}'.format(samplesToPlot, voltageRange),
            xaxis=dict(
                title='Index',
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
                # range=[min_signal - (abs(min_signal)*0.1), max_signal + (max_signal*0.1)],
            )
        )

        fig = dict(data=data, layout=layout)

        plotly.offline.plot(
            fig,
            filename=plotFolder + '/' + file_name + '_Voltage_Plot.html',
            auto_open=False)


def plot_time_vs_voltage(dataFolder, plotFolder):
    '''
    The function takes in the csv file and plots it (Time vs the Voltage Value) both as a png and as an interactive html file and saves it to the plot folder

    :param dataFolder: The location of the csv files that have a column for voltage value recorded by the digitizer
    :param plotFolder: The location of where the plots are to be saved
    :return:
    '''


    csvFiles = sorted(glob.glob(dataFolder + "/*.csv"))

    for csvFile in csvFiles:

        # the number of samples used in drawing the plot
        samplesToPlot = 10000000

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

        samplesToPlot = len(df)

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

def plot_time_vs_mean(dataFolder, plotFolder):
    '''
    The function takes in the csv file and plots it (Time vs the Mean Value) both as a png and as an interactive html file and saves it to the plot folder

    :param dataFolder: The location of the csv files that have 3 columns for time, voltage and mean with a header row
    :param plotFolder: The location of where the plots are to be saved
    :return:
    '''

    csvFiles = sorted(glob.glob(dataFolder + "/*.csv"))

    for csvFile in csvFiles:

        # the number of samples used in drawing the plot
        samplesToPlot = 10000000

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

        samplesToPlot = len(df)

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


def plot_fft_signal(dataFolder, plotFolder):
    """
    The function takes in the csv file and plots it (Fast Fourier Transforms - FFT and IFFT) both as a png and as an interactive html file and saves it to the plot folder

    :param dataFolder: The location of the csv files that have a column for voltage value recorded by the digitizer
    :param plotFolder: The location of where the plots are to be saved
    :return:
    """

    csvFiles = sorted(glob.glob(dataFolder + "/*.csv"))

    for csvFile in csvFiles:

        # the number of samples used in drawing the plot
        samplesToPlot = 10000000

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

        samplesToPlot = len(df)

        (row, col) = df.shape
        print("Number of Rows: {} and Col: {}".format(row, col))
        columnNames = list(df.columns.values)
        print("Data has columns: {}".format(columnNames))

        # Time column
        df.insert(0, 'Time(s)',[float(x)*sample_period for x in range(len(df))])


        x = df['Time(s)']
        y = df['Voltage(mV)']

        # Create all the fequencies that are necessary
        freqs = fftfreq(samplesToPlot)

        # mask array to be used for power spectra
        # ignoring half of the values, as they are complex conjugates of the other
        mask = freqs > 0

        # fft values
        y_fft = fft(y)

        # true throratical fit
        fft_theo = 2.0*np.abs(y_fft/samplesToPlot)

        fig, axs = plt.subplots(3, 1, constrained_layout=True)

        fig.suptitle('Fast Fourier Transforms - FFT', fontsize=16)

        axs[0].plot(x, y, '-')
        axs[0].set_title('Original Signal')
        axs[0].set_xlabel('Time(s)')
        axs[0].set_ylabel('Voltage(mV)')

        axs[1].plot(freqs, y_fft, '-')
        axs[1].set_title('Raw FFT values')
        # axs[1].set_xlabel('Time(s)')
        # axs[1].set_ylabel('Voltage(mV)')

        axs[2].plot(freqs[mask], fft_theo[mask], '-')
        axs[2].set_title('True FFT values')
        # axs[2].set_xlabel('Time(s)')
        # axs[2].set_ylabel('Voltage(mV)')

        plt.show()
        # pickle.dump(fig, open(plotFolder + '/FigureObject.fig.pickle', 'wb'))


if __name__ == '__main__':

    print("Starting script {}".format(FILE_NAME))

    plot_voltage(dataFolder=CSVDECIMATEDATA_DIR, plotFolder=PLOT_DIR)

    # plot_time_vs_voltage(dataFolder=CSVDATA_DIR, plotFolder=PLOT_DIR)

    # plot_time_vs_mean(dataFolder=CSVMEANDATA_DIR, plotFolder=PLOT_DIR)

    # plot_fft_signal(dataFolder=CSVDATA_DIR, plotFolder=PLOT_DIR)
