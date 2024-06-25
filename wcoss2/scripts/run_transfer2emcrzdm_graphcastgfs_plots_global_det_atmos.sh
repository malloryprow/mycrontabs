#!/bin/sh
set -x 
##################################################
# This submit jobs to dev_transfer for
# EVS GraphcastGFS global_det atmos plots tar files
##################################################

qsub /u/mallory.row/cron_jobs/scripts/transfer2emcrzdm_graphcastgfs_plots_global_det_atmos.sh
