#PBS -N transfer2emcrzdm_evs_para_plots_global_det_long_term
#PBS -o /u/mallory.row/cron_jobs/logs/log_transfer2emcrzdm_evs_para_plots_global_det_long_term.out
#PBS -e /u/mallory.row/cron_jobs/logs/log_transfer2emcrzdm_evs_para_plots_global_det_long_term.out
#PBS -S /bin/bash
#PBS -q dev_transfer
#PBS -A VERF-DEV
#PBS -l walltime=00:05:00
#PBS -l place=shared,select=1:ncpus=1
#PBS -l debug=true
#PBS -V

VDATEYYYY=$(date -d "1 month ago" '+%Y')
VDATEmm=$(date -d "1 month ago" '+%m')
rsync -ahr -P /lfs/h1/ops/para/com/evs/v1.0/plots/global_det/long_term/evs.plots.global_det.atmos.long_term.v${VDATEYYYY}${VDATEmm}.tar mrow@emcrzdm.ncep.noaa.gov:/home/people/emc/www/htdocs/users/verification/global/gfs/para/atmos/tar_files/.
