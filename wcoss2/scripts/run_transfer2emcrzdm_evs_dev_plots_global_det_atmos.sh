#!/bin/sh
set -x 
##################################################
# This submit jobs to dev_transfer for
# EVS dev global_det atmos plots tar files
##################################################

qsub /u/mallory.row/cron_jobs/scripts/transfer2emcrzdm_evs_dev_plots_global_det_atmos.sh
