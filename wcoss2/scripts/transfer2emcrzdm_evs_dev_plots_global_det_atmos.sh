#PBS -N transfer2emcrzdm_evs_dev_plots_global_det_atmos
#PBS -o /u/mallory.row/cron_jobs/logs/log_transfer2emcrzdm_evs_dev_plots_global_det_atmos.out
#PBS -e /u/mallory.row/cron_jobs/logs/log_transfer2emcrzdm_evs_dev_plots_global_det_atmos.out
#PBS -S /bin/bash
#PBS -q dev_transfer
#PBS -A VERF-DEV
#PBS -l walltime=02:00:00
#PBS -l place=shared,select=1:ncpus=1
#PBS -l debug=true
#PBS -V

export PDYm1=$(date -d "24 hours ago" '+%Y%m%d')
rsync -ahr -P /lfs/h2/emc/ptmp/emc.vpppg/evs/v2.0/plots/global_det/atmos.${PDYm1}/*.tar mrow@emcrzdm.ncep.noaa.gov:/home/people/emc/www/htdocs/users/verification/global/gfs/dev/atmos/tar_files/.
