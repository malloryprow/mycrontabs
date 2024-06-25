#!/bin/bash
set -x

PDYm19=$(date -d "456 hours ago" '+%Y%m%d')

cd /lfs/h2/emc/vpppg/noscrub/$USER/EVS/dev/drivers/scripts/prep/global_det
rm -f jevs_global_det_wave_prep_00.o*
rm -r /lfs/h2/emc/vpppg/noscrub/mallory.row/evs/v2.0/prep/global_det/wave.${PDYm19}
qsub jevs_global_det_wave_prep.sh
