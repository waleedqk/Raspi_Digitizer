

## Send file

Keep sending 1MB file at 500ms interval

    while [ 1 ]; do sleep 0.5; netcat -N raspiDigitizer6 8888 < payload1MB.dat ; done

Keep sending 10MB file at 100ms interval

    while [ 1 ]; do sleep 0.1; netcat -N raspiDigitizer6 8888 < payload10MB.dat ; done


## Netcat send and close

Close netcat once the command has ended

Call netcat -N <ip> <port> <  <what_file_to_send>

    netcat -N raspiDigitizer6 8888 < payload.dat


## Netcat send

Call netcat <ip> <port> <  <what_file_to_send>

    netcat raspiDigitizer6 8888 < payload.dat