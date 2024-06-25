#!/bin/bash
set -x

cd /lfs/h2/emc/vpppg/noscrub/$USER/EVS/dev/drivers/scripts/plots/global_det
rm -f jevs_global_det_wave_grid2obs_plots_*days_00.o*

qsub jevs_global_det_wave_grid2obs_plots_last31days.sh
qsub jevs_global_det_wave_grid2obs_plots_last90days.sh
