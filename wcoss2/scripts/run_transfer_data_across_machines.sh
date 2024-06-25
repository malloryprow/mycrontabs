#!/bin/bash

##################################################
# This script runs transfer_data_across_machines.py
# which transfers between WCOSS2 dev and prod
# and other NOAA machines
##################################################

rm /u/$USER/cron_jobs/logs/log_transfer_data_across_machines.out

qsub -S /bin/bash -N transfer_data_across_machines -q dev_transfer -A VERF-DEV -V -l walltime=04:00:00 -l debug=true -l place=shared,select=1:ncpus=1 -o /u/$USER/cron_jobs/logs/log_transfer_data_across_machines.out -e /u/$USER/cron_jobs/logs/log_transfer_data_across_machines.out /u/$USER/cron_jobs/scripts/transfer_data_across_machines.sh
