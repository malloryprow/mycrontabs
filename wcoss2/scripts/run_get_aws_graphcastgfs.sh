#!/bin/bash

set -x

rm /lfs/h2/emc/vpppg/noscrub/mallory.row/verification/global/verify_graphcastgfs/log_get_aws_graphcastgfs_*Z.out

PDYm15=$(date -d "360 hours ago" '+%Y%m%d')
host=$HOSTNAME
host_letter=$(echo $HOSTNAME | cut -c 1-1)
if [ $host_letter = d ]; then
    prod_host="clogin01"
elif [ $host_letter = c ]; then
    prod_host="dlogin01"
fi
rm -r /lfs/h2/emc/vpppg/noscrub/mallory.row/verification/global/verify_graphcastgfs/graphcastgfs13/graphcastgfs.${PDYm15}
rm -r /lfs/h2/emc/vpppg/noscrub/mallory.row/verification/global/verify_graphcastgfs/graphcastgfs37/graphcastgfs.${PDYm15}
ssh ${USER}@${prod_host} "rm -rf /lfs/h2/emc/vpppg/noscrub/mallory.row/verification/global/verify_graphcastgfs/graphcastgfs13/graphcastgfs.${PDYm15}"
ssh ${USER}@${prod_host} "rm -rf /lfs/h2/emc/vpppg/noscrub/mallory.row/verification/global/verify_graphcastgfs/graphcastgfs37/graphcastgfs.${PDYm15}"

PDYm1=$(date -d "24 hours ago" '+%Y%m%d')
cd /lfs/h2/emc/vpppg/noscrub/mallory.row/verification/global/verify_graphcastgfs
qsub -v PDYm1=${PDYm1} submit_get_aws_graphcastgfs_00Z.sh
qsub -v PDYm1=${PDYm1} submit_get_aws_graphcastgfs_06Z.sh
qsub -v PDYm1=${PDYm1} submit_get_aws_graphcastgfs_12Z.sh
sleep 600
qsub -v PDYm1=${PDYm1} submit_get_aws_graphcastgfs_18Z.sh
