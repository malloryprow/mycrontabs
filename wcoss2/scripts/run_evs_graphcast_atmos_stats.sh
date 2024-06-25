#!/bin/bash
set -x

PDYm3=$(date -d "72 hours ago" '+%Y%m%d')
rm -r /lfs/h2/emc/vpppg/noscrub/mallory.row/verification/global/verify_graphcastgfs/evs/v1.0/stats/global_det/atmos.${PDYm3}

cd /lfs/h2/emc/vpppg/noscrub/mallory.row/verification/global/verify_graphcastgfs/EVS/dev/drivers/scripts/stats/global_det
rm -f jevs_global_det_atmos_*_grid2*_stats_00.o*

#qsub jevs_global_det_atmos_graphcastgfs37_grid2grid_stats.sh
#qsub jevs_global_det_atmos_graphcastgfs37_grid2obs_stats.sh
#sleep 180
qsub jevs_global_det_atmos_graphcastgfs13_grid2grid_stats.sh
qsub jevs_global_det_atmos_graphcastgfs13_grid2obs_stats.sh
