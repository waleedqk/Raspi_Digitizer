
import os, sys
import pickle

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

"""
REFERENCES
http://fredborg-braedstrup.dk/blog/2014/10/10/saving-mpl-figures-using-pickle/
"""

SCRIPT_DIR = sys.path[0]
SCRIPT_NAME = str(sys.argv[0]).split("/")[-1]
FILE_NAME =  os.path.basename(sys.argv[0])
HOME = os.environ['HOME']
COMPUTE1_HOME = "/rhome/wqkhan"

# Location of where the plots are being stored
PLOT_DIR = HOME + "/Documents/Experiment-Data-Dump/wqkhan_Raspi_Digitizer/plots"


if __name__ == '__main__':

    print("Starting script {}".format(FILE_NAME))

    fig_handle = pickle.load(open(PLOT_DIR + '/FigureObject.fig.pickle', 'rb'))

    plt.show()  # Show the figure, edit it, etc.!