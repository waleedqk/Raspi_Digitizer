#!/bin/bash

# This script copies the local git repo from the laptop
# to the rasp_pi's. The Pi's do not have an internet connection
# as of yet so this helper script keeps the repo updated on them

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PAR_DIR="$(dirname "$SCRIPT_DIR")"

MYHOME="/home/${SUDO_USER}"
REPO_DIR="${MYHOME}/Documents/git/Raspi_Digitizer"


RASPI_LIST=(
    "raspiDigitizer1"
    # "raspiDigitizer2"
    "raspiDigitizer3"
    # "raspiDigitizer4"
    # "raspiDigitizer5"
    "raspiDigitizer6"
)

for i in "${RASPI_LIST[@]}"
do

    # delete exiting repo from the pi
    echo "Processing: ${i}"
    $(ssh -i ~/.ssh/id_ras_pi pi@${i}.local "rm -rf /home/pi/Documents/git/Raspi_Digitizer")
    # scp repo from laptop to the pi
    $(scp -r -i ~/.ssh/id_ras_pi ${REPO_DIR} pi@${i}.local:Documents/git)

done