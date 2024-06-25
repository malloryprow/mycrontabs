#!/bin/bash
set -x

PDYm3=$(date -d "72 hours ago" '+%Y%m%d')

cd /lfs/h2/emc/vpppg/noscrub/$USER/EVS/dev/drivers/scripts/stats/global_det
rm -f jevs_global_det_atmos_*_stats_00.o*
rm -r /lfs/h2/emc/vpppg/noscrub/$USER/evs/v2.0/stats/global_det/atmos.${PDYm3}
qsub jevs_global_det_gfs_atmos_grid2grid_stats.sh
qsub jevs_global_det_gfs_atmos_grid2obs_stats.sh
qsub jevs_global_det_gfs_atmos_wmo_daily_stats.sh
sleep 10m
qsub jevs_global_det_cfs_atmos_grid2grid_stats.sh
qsub jevs_global_det_cfs_atmos_grid2obs_stats.sh
qsub jevs_global_det_cmc_atmos_grid2grid_stats.sh
qsub jevs_global_det_cmc_atmos_grid2obs_stats.sh
qsub jevs_global_det_cmc_regional_atmos_grid2grid_stats.sh
qsub jevs_global_det_dwd_atmos_grid2grid_stats.sh
qsub jevs_global_det_ecmwf_atmos_grid2grid_stats.sh
qsub jevs_global_det_ecmwf_atmos_grid2obs_stats.sh
qsub jevs_global_det_fnmoc_atmos_grid2grid_stats.sh
qsub jevs_global_det_fnmoc_atmos_grid2obs_stats.sh
qsub jevs_global_det_imd_atmos_grid2grid_stats.sh
qsub jevs_global_det_imd_atmos_grid2obs_stats.sh
qsub jevs_global_det_jma_atmos_grid2obs_stats.sh
qsub jevs_global_det_jma_atmos_grid2grid_stats.sh
qsub jevs_global_det_metfra_atmos_grid2grid_stats.sh
qsub jevs_global_det_ukmet_atmos_grid2obs_stats.sh
qsub jevs_global_det_ukmet_atmos_grid2grid_stats.sh
