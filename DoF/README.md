# Desgn of Experiment

The experiment is being carried out for the data acquisition of the voltage reading of the router as devices connect and disconnect and as they transmit the data.

## Experimental Hardware

The hardware is outlined as follows:

    1) 1x Netgear Router
    2) 1x Raspi acting as the reciever
    3) 2x Raspi acting as the sender
    4) 1x Laptop to ssh into the devices and run the jobs

## Factore and Levels

There are two factors in the experiment:

    1) Load of data transfer
    2) Configuration of the hardware

### Levels of Loads - l<index>

    1) Zero transmission - All devices connected
    2) 512 kb/s
    3) 1MB/100ms
    4) Max throuput - no sleep

### Levels of Configurations - c<index>

    1) Only one sender
    2) 2 Sending devices
    3) Start Trace; Plug Reciever only; Wait 10 sec; Stop Trace
    4) Start Trace; Unplug Reciever; Wait 10 sec; Stop Trace

During **3 and 4** none of the senders are connected to the router and hence no data is being transmitted.

## Data Capture

On the digitizer side, the plan is to capture 20 seconds of data per experiment at the 50MSPS (Mega Samples Per Second) and 800mV as the upper limit of the readout of the scale:

    acquire_to_disk 50 800mv 20 <file-name>

To see how the digitzer is run and how to access and manipulate the data look at ```software_setup.md``` readme


## Experimental Results

After the experiments have been carried out we now have the following log files:

    2018-10-23-1016--50MSPS--800mV--Raspi_Digitizer_l1_c1_zeroTrans_allConnected
    2018-10-23-1020--50MSPS--800mV--Raspi_Digitizer_l2_c1_512KbPS_singleSender
    2018-10-23-1022--50MSPS--800mV--Raspi_Digitizer_l3_c1_10MBPS_singleSender
    2018-10-23-1023--50MSPS--800mV--Raspi_Digitizer_l4_c1_10MBmaxFlow_singleSender
    2018-10-23-1025--50MSPS--800mV--Raspi_Digitizer_l2_c2_512KbPS_dualSender
    2018-10-23-1028--50MSPS--800mV--Raspi_Digitizer_l3_c2_10MBPS_dualSender
    2018-10-23-1029--50MSPS--800mV--Raspi_Digitizer_l4_c2_10MBmaxFlow_dualSender
    2018-10-23-1032--50MSPS--800mV--Raspi_Digitizer_l1_c3_zeroTrans_plugReciever
    2018-10-23-1033--50MSPS--800mV--Raspi_Digitizer_l1_c4_zeroTrans_unplugReciever

Each trace was run to collect 20 seconds of data.

The file ```2018-10-23-1023--50MSPS--800mV--Raspi_Digitizer_l4_c1_10MBmaxFlow_singleSender``` was run on 2018-10-23 at 10:23 am, collection reading at 50MSPS with peak to peak check of 800mV, while the load **l4** was set for max throughput, and the configuration **c1** denotes that there was only one sender node.