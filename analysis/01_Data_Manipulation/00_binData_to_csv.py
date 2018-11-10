'''
REFERENCES:
https://stackoverflow.com/questions/15192847/saving-arrays-as-columns-with-np-savetxt
'''

import os, sys, time
import re
import glob

import numpy as np
import pandas as pd


SCRIPT_DIR = sys.path[0]
SCRIPT_NAME = str(sys.argv[0]).split("/")[-1]
FILE_NAME =  os.path.basename(sys.argv[0])
HOME = os.environ['HOME']
COMPUTE1_HOME = "/rhome/wqkhan"

# Location of where the bin data is stored
BINDATA_DIR = HOME + "/Documents/Experiment-Data-Dump/wqkhan_Raspi_Digitizer/dataLogs"
# Output location of where the csv data is - the file has a single column with a header
CSVDATA_DIR = HOME + "/Documents/Experiment-Data-Dump/wqkhan_Raspi_Digitizer/dataLogstoCSV"


def loadBin_savetocsv(log_folder, outputFolder):
    '''

    :param log_folder: absolute path to where the test logs are stored
    :param outputFolder:
    :return:

    The data collected by the experiments is a bin file
    that has 16 bit values in a sequence

    Loads all files in the specifed folder location "assumes they are bin files"
    processed the data and transforms them to an array with time and value
    then saves that to a text file in the output folder location
    '''

    binFiles = sorted(glob.glob(log_folder+"/*"))

    for binFile in binFiles:

        base = os.path.basename(binFile)
        file_name, file_ext = os.path.splitext(base)


        MSPS = int(re.search(r'\d+', base.split("--")[1]).group())
        voltageRange = int(re.search(r'\d+', base.split("--")[2]).group())
        sample_period=(1/(MSPS*10**6))

        print("Processing: {} with: \tMSPS={} & VoltageRange={}".format(base, MSPS, voltageRange))

        # loading the data encoded as 16bit so it maps all values from 0 - 65535
        binData_int16 = np.fromfile(binFile, dtype=np.uint16)#, count=100)
        (row, ) = binData_int16.shape
        print("Number of Rows: {}".format(row))

        # split the array into sections so we do not run out of memory
        chunk_size = 100
        split_binData_int16 = np.array_split(binData_int16, chunk_size)
        del binData_int16

        # The start time for the time column to be updated at the end of the chunks
        start_time = 0

        # Create and Add the header to the output csv file // d = {'Voltage(mV)': [], 'Time(s)': []}
        d = {'Voltage(mV)': []}
        df = pd.DataFrame(data=d)
        df.to_csv(outputFolder + "/" + base + "_voltage-mV.csv", index=False, header=True)

        # go through and process all the splits of the dataFrame
        for binData_int16 in split_binData_int16:

            df = pd.DataFrame()

            # changing the type from uint16 to int so overflow restriction is removed
            df = pd.DataFrame(data=binData_int16, dtype=int, columns=['binary'])

            # alsazar documentation require the subtraction of 2**15 = 32768 from the recorded values
            # now the data is scaled from 32767 - -32768
            df['binary'] = df['binary'].apply(lambda x: x - (2**15))

            # do a liner approximation based on what the recorded voltage scale was
            # if data was collected at 800 mV range then multiplying by 800 will give voltage in mV
            # to get value in V, multiple by 0.8
            # then divide the value by the scale (2**15) to get the final output
            df['binary'] = df['binary'].apply(lambda x: (x * float(voltageRange)) / (2**15))


            # # # Could add a time column to the data - but not adding additional data in this step
            # # Calculate the time difference between each sample by processing the MSPS value - stop=time_step*Number_of_Samples_Needed*Start_time
            # df['time'] = pd.DataFrame(data=np.linspace(start=start_time, stop=sample_period*chunk_size+start_time, num=chunk_size, endpoint=False))
            # # update the start time for the next chunk of data - based on the last value used here
            # start_time = df["time"].iloc[-1] + sample_period

            # stack multiple arrays as columns side by side
            # np.savetxt(outputFolder + "/" + base + "_time_vs_voltages.txt", np.c_[time, binData_int])

            # append the chunk to the csv file
            df.to_csv(outputFolder + "/" + file_name + "_voltage-mV.csv", index=False, mode='a', header=False)



if __name__ == '__main__':

    print("Starting script {}".format(FILE_NAME))

    loadBin_savetocsv(log_folder=BINDATA_DIR, outputFolder=CSVDATA_DIR)