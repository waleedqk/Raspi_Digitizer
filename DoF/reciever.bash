#!/bin/bash

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

MYHOME="/home/${SUDO_USER}"
PAYLOAD_DIR="${MYHOME}/Downloads/payload"

OPTS=`getopt -o c:l:h --long config:,load:,help -n 'parse-options' -- "$@"`

usage() { echo "Error - Usage: $0 [-c || --config <1-4>] [-l || --load <1-4>] [-h || --help]" 1>&2; exit 1; }


if [ $? != 0 ] ; then echo "Failed parsing options." usage >&2 ; exit 1 ; fi

echo "$OPTS"
eval set -- "$OPTS"

CONFIG_VAL=false
LOAD_VAL=false

while true; do
  case "$1" in
    -c | --config )         CONFIG=true;    CONFIG_VAL="$2";    shift; shift ;;
    -l | --load )           LOAD=true;      LOAD_VAL="$2";      shift; shift ;;
    -h | --help )           HELP=true;          shift ;;
    -- ) shift; break ;;
    * ) break ;;
  esac
done
# echo "HELP = ${HELP}"


payload_dir()
{
    echo "Creating local payload directory: ${PAYLOAD_DIR}"
    sudo -u ${SUDO_USER} mkdir -p $PAYLOAD_DIR
    echo "Clean out old payload files from directory"
    sudo -u ${SUDO_USER} rm  -f $PAYLOAD_DIR/*.dat
}

apt_update()
{
    echo "update..."
    apt-get update
}


process_load()
{
    if ! [[ "$LOAD_VAL" =~ ^[0-9]+$ ]]
        then
            # Load values can be integers only
            echo 0
            return 
    fi

    if [ "$LOAD_VAL" -ge 1 ] && [ "$LOAD_VAL" -le 4 ]; then
        echo $LOAD_VAL
    else
        # Load values can be interger vlaues between 1 - 4
        # Consult the README to find out the experimental layout
        echo 0
    fi

}

process_config()
{
    if ! [[ "$CONFIG_VAL" =~ ^[0-9]+$ ]]
        then
            # config values can be integers only
            echo 0
            return 
    fi

    if [ "$CONFIG_VAL" -ge 1 ] && [ "$CONFIG_VAL" -le 4 ]; then
        echo $CONFIG_VAL
    else
        # Load values can be interger vlaues between 1 - 4
        # Consult the README to find out the experimental layout
        echo 0
    fi  
}

run_experiment()
{
     echo "Initializing experiment..." 
     echo "CONFIG_VAL = ${CONFIG_VAL} and LOAD_VAL = ${LOAD_VAL}"

    payload_dir
    local PAYLOAD_DAT=""

    case "$LOAD_VAL" in
        1)  echo  "All devices need to be connected - No transmission required"
            ;;
        2)  echo  "51kb file to be created"
            PAYLOAD_DAT="payload51kb.dat"
            $(sudo -u ${SUDO_USER} dd if=/dev/urandom of=${PAYLOAD_DIR}/${PAYLOAD_DAT} bs=51k count=1)
            ;;
        3)  echo  "1MB file to be created"
            PAYLOAD_DAT="payload1MB.dat"
            $(sudo -u ${SUDO_USER} dd if=/dev/urandom of=${PAYLOAD_DIR}/${PAYLOAD_DAT}  bs=1M count=1)
            ;;
        4)  echo  "10MB file to be created"
            PAYLOAD_DAT="payload10MB.dat"
            $(sudo -u ${SUDO_USER} dd if=/dev/urandom of=${PAYLOAD_DIR}/${PAYLOAD_DAT}  bs=1M count=10)
            ;;
        0|*)  
            echo "Invalid input supplied for network load"
            return
            ;;
    esac

    case "$CONFIG_VAL" in
        1)  echo  "Copy payload file to single sender"
            $(scp -r -i ~/.ssh/id_ras_pi ${PAYLOAD_DIR}/*.dat pi@raspiDigitizer3.local:Downloads/payload)
            # get the sender to send the file
            $(ssh -i ~/.ssh/id_ras_pi pi@raspiDigitizer3.local "while [ 1 ]; do sleep 0.1; netcat -N raspiDigitizer1 8888 < /home/pi/Downloads/payload/payload51kb.dat ; done")
            # get the reciever to listen at the specified port for the payload

            ;;
        2)  echo  "Sending SIGINT signal"
            ;;
        3)  echo  "Sending SIGQUIT signal"
            ;;
        4) echo  "Sending SIGKILL signal"
            ;;
        0|*)  
            echo "Invalid input supplied for network load"
            return
            ;;
    esac

}


main()
{
   

    # -z string True if the string is null (an empty string)
    if [ ! -z "${HELP}" ]; then
        echo "Requesting help: "
        usage
    fi

    
    # both the config and the load option need to be specified
    if [ ! -z "${CONFIG}" ] && [ ! -z "${LOAD}" ]; then
        echo "CONFIG = ${CONFIG} and CONFIG_VAL = ${CONFIG_VAL}"
        echo "LOAD = ${LOAD} and LOAD_VAL = ${LOAD_VAL}"

        LOAD_VAL=$( process_load )        
        CONFIG_VAL=$( process_config )        

        run_experiment

    else
        echo "Both the config and the load option need to be specified"
        usage
    fi

}

main