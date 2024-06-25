#!/bin/sh
set -x 
##################################################
# This submit jobs to dev_transfer for EVS para
# plot tar files
##################################################

qsub /u/mallory.row/cron_jobs/scripts/transfer_rzdm_emc_para_global_det_atmos_plots.sh
qsub /u/mallory.row/cron_jobs/scripts/transfer_rzdm_emc_para_global_det_wave_plots.sh

dd=$(date '+%d')
if [ $dd = 03 ]; then
    qsub /u/mallory.row/cron_jobs/scripts/transfer_rzdm_emc_para_global_det_atmos_plots_long_term.sh
fi
