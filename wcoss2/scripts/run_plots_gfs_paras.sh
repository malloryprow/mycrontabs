#!/bin/sh

set -x

cd /lfs/h2/emc/vpppg/noscrub/mallory.row/verification/global/EMC_verif-global/ush
 
### gfseval_a
rm -r /lfs/h2/emc/stmp/$USER/verif_global_gfseval_a_plots
./run_verif_global.sh ../parm/config/gfseval_a/config.vrfy.plots

### gfs_wcoss2_para
rm -r /lfs/h2/emc/stmp/$USER/verif_global_gfs_wcoss2_para_plots
./run_verif_global.sh ../parm/config/gfs_wcoss2_para/config.vrfy.plots
