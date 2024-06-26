#!/bin/bash
set -x

PDYm3=$(date -d "72 hours ago" '+%Y%m%d')
rm -r /lfs/h2/emc/ptmp/mallory.row/evs/v1.0/plots/global_det/atmos.${PDYm3}

cd /lfs/h2/emc/vpppg/noscrub/mallory.row/verification/global/verify_graphcastgfs/EVS/dev/drivers/scripts/plots/global_det
rm -f jevs_global_det_graphcastgfs_atmos_grid2*_*_plots_*days_00.o*
qsub jevs_global_det_graphcastgfs_atmos_grid2grid_means_plots_31days.sh
qsub jevs_global_det_graphcastgfs_atmos_grid2grid_means_plots_90days.sh
qsub jevs_global_det_graphcastgfs_atmos_grid2grid_precip_plots_31days.sh
qsub jevs_global_det_graphcastgfs_atmos_grid2grid_precip_plots_90days.sh
qsub jevs_global_det_graphcastgfs_atmos_grid2grid_pres_levs_plots_31days.sh
qsub jevs_global_det_graphcastgfs_atmos_grid2grid_pres_levs_plots_90days.sh
qsub jevs_global_det_graphcastgfs_atmos_grid2obs_pres_levs_plots_31days.sh
qsub jevs_global_det_graphcastgfs_atmos_grid2obs_pres_levs_plots_90days.sh
qsub jevs_global_det_graphcastgfs_atmos_grid2obs_sfc_plots_31days.sh
qsub jevs_global_det_graphcastgfs_atmos_grid2obs_sfc_plots_90days.sh
