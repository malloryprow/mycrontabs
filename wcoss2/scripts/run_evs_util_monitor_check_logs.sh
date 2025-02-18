#!/bin/sh
set -x 
##################################################
# This script checks the EVS parallel output
##################################################

export PDYm1=$(date -d "-1 days" +"%Y%m%d")

mkdir -p /lfs/h2/emc/stmp/mallory.row/monitor_evs
cd /lfs/h2/emc/stmp/mallory.row/monitor_evs
qsub /lfs/h2/emc/vpppg/noscrub/mallory.row/EVS-util/monitor/drive_check_logs.sh

sleep 1800
report_file="/lfs/h2/emc/stmp/mallory.row/monitor_evs/report_${PDYm1}.txt"
maillist='mallory.row@noaa.gov'
subject="emc.vpppg EVS Parallel Monitoring Report for ${PDYm1}"
cat $report_file | mail -s "$subject" $maillist
