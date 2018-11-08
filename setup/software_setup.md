
# GUI Reader

AlazarFrontPanel 

    ls /usr/local/bin

    acquire_to_disk

Sample at 50MSPS 
    voltage highest range to check 800mV
    for 20 seconds

    acquire_to_disk 50 800mv 20 <file-name>

Files are always stored under:

    /Digitizer/captured-data/<file-name>

## Bin to actual Voltage values

The encoding is as 16-bit values.
So firstly load as unit16 to so it maps all values from 0 - 65535

alsazar documentation require the subtraction of 2**15 = 32768 from the recorded values

    value = binData_uint16 - (2**15)

**Note** Make sure this arethimatic does not cause an overflow or the output values will be wrong
now the data is scaled from 32767 - -32768

do a liner approximation based on what the recorded voltage scale was
if data was collected at 800 mV range then multiplying by 800 will give voltage in mV
to get value in V, multiple by 0.8
then divide the value by the scale (2**15) to get the final output

    value_in_mV = (value * 800.0) / (2**15)

# Split files:

Only use if capturing more than one channels:

    split-channels 

# 

It will split the files if more channels 

Will create a <file-name>.txt with two columns

    bin2txt 1 /Digitizer/captured-data/<file-name> 50 800mv

Get time and value in mV


# IMPORTANT

If the AlazarFrontPanel GUI and acquire_to_disk run at the same time the machine will hang. Will have to be ```Reset```. 

So do no tdo that. 

alias rm='rm -i'