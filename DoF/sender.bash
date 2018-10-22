#!/bin/bash

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

PIHOME="/home/${SUDO_USER}"
PI_PAYLOAD_DIR="${MYHOME}/Downloads/payload"

OPTS=`getopt -o p:d:h --long port:,device:,help -n 'parse-options' -- "$@"`

usage() { echo "Error - Usage: $0 [-p || --port] [-d || --device] [-h || --help]" 1>&2; exit 1; }


if [ $? != 0 ] ; then echo "Failed parsing options." usage >&2 ; exit 1 ; fi

echo "$OPTS"
eval set -- "$OPTS"

PORT_VAL=false
DEVICE_VAL=false

while true; do
  case "$1" in
    -p | --port )       PORT=true;      PORT_VAL="$2";      shift; shift ;;
    -d | --device )     DEVICE=true;    DEVICE_VAL="$2";     shift; shift ;;
    -h | --help )       HELP=true;      shift ;;
    -- ) shift; break ;;
    * ) break ;;
  esac
done



main()
{
    echo "My home: ${HOME}"
    echo "Sudo user: ${SUDO_USER}"
    # -z string True if the string is null (an empty string)
    if [ ! -z "${HELP}" ]; then
        echo "Requesting help: "
        usage
    fi

    # Both the port and device option need to be specified
    if [ ! -z "${PORT}" ] && [ ! -z "${DEVICE}" ]; then
        echo "PORT = ${PORT} and PORT_VAL = ${PORT_VAL}"
        echo "DEVICE = ${DEVICE} and DEVICE_VAL = ${DEVICE_VAL}"

        while [ 1 ];  do  sleep 0.1;  netcat -N ${DEVICE_VAL} ${PORT_VAL} < /home/pi/Downloads/payload/payload51kb.dat ;  done

    else
        echo "Both the port and device option need to be specified"
        usage
    fi


}


main