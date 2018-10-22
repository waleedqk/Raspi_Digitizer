



## Process incoming data

Listen to data coming in and output the lines from word count via ```wc -l```:

    while [ 1 ]; do (netcat -l 8888 | wc -l ); done

## Process incoming data with counter

Listen to data coming in and output the lines from word count via ```wc -l``` and add a counter value to the text:

    i=0; while [ 1 ]; do i=$((i+1)); echo $i: $(netcat -l 8888 | wc -l ); done

## Process incoming data with counter and date

Listen to data coming in and output the lines from word count via ```wc -l``` and add a counter value to the text and date:

    i=0; while [ 1 ]; do i=$((i+1)); echo $(date) $i: $(netcat -l 8888 | wc -l ); done


## Listen to port

    netcat -l 8888

## Keep listening to port

Infinite recursive loop:

    while [ 1 ]; do netcat -l 8888; done