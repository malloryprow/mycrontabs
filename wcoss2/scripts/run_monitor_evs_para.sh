#!/bin/sh
set -x 
##################################################
# This script checks the EVS parallel output
##################################################

export PDY=$(date '+%Y%m%d')

python /u/$USER/cron_jobs/scripts/monitor_evs_para.py

report_file="/lfs/h2/emc/stmp/$USER/monitor_evs_para_reports/report_${PDY}.txt"
maillist='mallory.row@noaa.gov'
subject="EVS Parallel Monitoring Report ${PDY}"
cat $report_file | mail -s "$subject" $maillist
