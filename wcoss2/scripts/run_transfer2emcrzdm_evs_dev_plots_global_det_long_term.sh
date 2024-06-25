#!/bin/sh
set -x

##################################################
# This submit jobs to dev_transfer for
# EVS dev global_det long_term plots tar file
##################################################

qsub /u/mallory.row/cron_jobs/scripts/transfer2emcrzdm_evs_dev_plots_global_det_long_term.sh 
