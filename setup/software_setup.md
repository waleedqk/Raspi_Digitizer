
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

## 16-bit values 

0 - 65535

subtract 32768

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