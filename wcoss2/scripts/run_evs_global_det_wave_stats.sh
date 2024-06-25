#!/bin/bash
set -x

PDYm3=$(date -d "72 hours ago" '+%Y%m%d')

cd /lfs/h2/emc/vpppg/noscrub/$USER/EVS/dev/drivers/scripts/stats/global_det
rm -f jevs_global_det_wave_gfs_grid2obs_stats_00.o*
rm -r /lfs/h2/emc/vpppg/noscrub/mallory.row/evs/v2.0/stats/global_det/wave.${PDYm3}
qsub  jevs_global_det_gfs_wave_grid2obs_stats.sh
