#!/bin/sh
set -x
##################################################
# This script runs transfer_data_across_machines.py
# which transfers between WCOSS2 dev and prod
# and other NOAA machines
##################################################

module load rsync/3.2.2

source ~/models.ver
export CDATE=${1:-$(date +%Y%m%d)}

python /u/$USER/cron_jobs/scripts/transfer_data_across_machines.py ${CDATE}
