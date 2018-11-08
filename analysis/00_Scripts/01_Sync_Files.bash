#! /bin/bash

MYHOME="/home/${USER}"

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PAR_DIR="$(dirname "$SCRIPT_DIR")"

OPTS=`getopt -o rth --long receive,transmit,help -n 'parse-options' -- "$@"`

usage() { echo "Error - Usage: $0 [-r || --receive] [-t || --transmit] [-h || --help]" 1>&2; exit 1; }


if [ $? != 0 ] ; then echo "Failed parsing options." usage >&2 ; exit 1 ; fi

echo "$OPTS"
eval set -- "$OPTS"

while true; do
  case "$1" in
    -r | --receive )         RECEIVE=true;       shift ;;
    -t | --transmit )        TRANSMIT=true;      shift ;;
    -h | --help )            HELP=true;          shift ;;
    -- ) shift; break ;;
    * ) break ;;
  esac
done



main()
{
    # -z string True if the string is null (an empty string)
    if [ ! -z "${HELP}" ]; then
        echo "Requesting help: "
        usage
    fi

    if [ ! -z "${TRANSMIT}" ]; then
        echo "Transmit Files to Remote System: "
        scp -r ${MYHOME}/Documents/git/Raspi_Digitizer wqkhan@compute1.esg.uwaterloo.ca:/rhome/wqkhan/Documents/Experiment-Data-Dump/wqkhan_Raspi_Digitizer
    fi

    if [ ! -z "${RECEIVE}" ]; then
        echo "Receive Files to Remote System: "
        scp -r wqkhan@compute1.esg.uwaterloo.ca:/rhome/wqkhan/Documents/Experiment-Data-Dump/wqkhan_Raspi_Digitizer/plots/* ${MYHOME}/Documents/Experiment-Data-Dump/wqkhan_Raspi_Digitizer/plots
    fi

}

main
