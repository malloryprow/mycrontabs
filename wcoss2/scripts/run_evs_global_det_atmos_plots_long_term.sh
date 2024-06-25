#!/bin/bash
set -x

cd /lfs/h2/emc/vpppg/noscrub/$USER/EVS/dev/drivers/scripts/plots/global_det
rm -f jevs_global_det_atmos_long_term_plots_00.o*

qsub jevs_global_det_atmos_long_term_plots.sh
