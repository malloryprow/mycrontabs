#PBS -N transfer2emcrzdm_evs_para_plots_global_det_headline
#PBS -o /u/mallory.row/cron_jobs/logs/log_transfer2emcrzdm_evs_para_plots_global_det_headline.out
#PBS -e /u/mallory.row/cron_jobs/logs/log_transfer2emcrzdm_evs_para_plots_global_det_headline.out
#PBS -S /bin/bash
#PBS -q dev_transfer
#PBS -A VERF-DEV
#PBS -l walltime=00:05:00
#PBS -l place=shared,select=1:ncpus=1
#PBS -l debug=true
#PBS -V

export PDYm1=$(date -d "24 hours ago" '+%Y%m%d')
rsync -ahr -P /lfs/h1/ops/para/com/evs/v1.0/plots/global_det/headline.${PDYm1}/*.tar mrow@emcrzdm.ncep.noaa.gov:/home/people/emc/www/htdocs/users/verification/global/gfs/para/atmos/tar_files/.
