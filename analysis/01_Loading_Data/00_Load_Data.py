import os, sys, time
import numpy as np

SCRIPT_DIR = sys.path[0]
HOME = os.environ['HOME']

'''
The data collected by the experiments is a bin file
that has 16 bit values in a sequence
'''


def load_bin_data():

    binData = np.fromfile(HOME + '/Desktop/2018-10-23-1022--50MSPS--800mV--Raspi_Digitizer_l3_c1_10MBPS_singleSender_temp', dtype=np.uint16)

    binData = binData - (2**15)

    print("{}".format(binData))


if __name__ == '__main__':

    print("Starting script")

    load_bin_data()