

## Listing the connected devices

The laptop is connected to the same switch/router as the rasp_pi. Figure out which device is active on the network:

    sudo arp-scan -l -I enp0s25

## Connect to the devices

SSH into the required devices:

    ssh -i ~/.ssh/id_ras_pi pi@raspiDigitizer1.local

## On the Sender Rasp_pi

Create the appropriate payload to send:

    dd if=/dev/urandom of=payload1MB.dat bs=1M count=1

Send the payload to a specified pi at a designated port

    while [ 1 ]; do sleep 0.5; netcat -N raspiDigitizer6 8888 < payload1MB.dat ; done

## On the Recieving Rasp_pi

    i=0; while [ 1 ]; do i=$((i+1)); echo $(date) $i: $(netcat -l 8888 | wc -l ); done

## On the Digitizer PC

    acquire_to_disk 50 800mv 20 <file-name>