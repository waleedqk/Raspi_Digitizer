

## Listing the connected devices

The laptop is connected to the same switch/router as the rasp_pi. Figure out which device is active on the network:

    sudo arp-scan -l -I enp0s25

## Connect to the devices

SSH into the required devices:

    ssh -i ~/.ssh/id_ras_pi pi@raspiDigitizer1.local


## On the Digitizer PC

    acquire_to_disk 50 800mv 20 <file-name>