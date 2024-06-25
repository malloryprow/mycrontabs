#!/bin/bash
set -x

cd /lfs/h2/emc/vpppg/noscrub/$USER/EVS/dev/drivers/scripts/stats/global_det
rm -f jevs_global_det_atmos_long_term_stats_00.o*

qsub jevs_global_det_atmos_long_term_stats.sh

#cd /lfs/h2/emc/vpppg/noscrub/$USER/evs/v2.0/stats/global_det/long_term
#python copy_rename_long_term_files.py
