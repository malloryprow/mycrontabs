import os
import datetime
import subprocess
import glob
import time

today = datetime.date.today()

monitor_reports_dir = '/lfs/h2/emc/stmp/mallory.row/monitor_evs_para_reports'
evs_para_base_dir = '/lfs/h2/emc/vpppg/noscrub/emc.vpppg/evs/v2.0'
evs_para_log_dir = '/lfs/h2/emc/ptmp/emc.vpppg/output'

### Set up report file
if not os.path.exists(monitor_reports_dir):
    os.makedirs(monitor_reports_dir)
today_report_file = os.path.join(monitor_reports_dir,
                                 f"report_{today:%Y%m%d}.txt")
print(f"Report File: {today_report_file}")
if os.path.exists(today_report_file):
    os.remove(today_report_file)
trf = open(today_report_file, 'w')

### Check global_det atmos prep
PREP_CHECKDATE = f"{today - datetime.timedelta(days=2):%Y%m%d}"
evs_para_prep_global_det_atmos_dir = os.path.join( 
    evs_para_base_dir, 'prep', 'global_det', f"atmos.{PREP_CHECKDATE}"
)
trf.write("GLOBAL_DET ATMOS - PREP\n")
for prep_dir in os.listdir(evs_para_prep_global_det_atmos_dir):
    if len(
        os.listdir(os.path.join(evs_para_prep_global_det_atmos_dir,
                                prep_dir))
    ) == 0:
        trf.write("EMPTY "
                  +os.path.join(evs_para_prep_global_det_atmos_dir,prep_dir)
                  +'\n')
    else:
        trf.write(os.path.join(evs_para_prep_global_det_atmos_dir,prep_dir)
                  +":"
                  +str(len(os.path.join(evs_para_prep_global_det_atmos_dir,prep_dir)))
                  +" files\n")
trf.write("\n")

### Check global_det wave prep
PREP_CHECKDATE = f"{today - datetime.timedelta(days=2):%Y%m%d}"
evs_para_prep_global_det_wave_dir = os.path.join(
    evs_para_base_dir, 'prep', 'global_det', f"wave.{PREP_CHECKDATE}"
)
trf.write("GLOBAL_DET WAVE - PREP\n")
for prep_dir in os.listdir(evs_para_prep_global_det_wave_dir):
    if len(
        os.listdir(os.path.join(evs_para_prep_global_det_wave_dir,
                                prep_dir))
    ) == 0:
        trf.write("EMPTY "
                  +os.path.join(evs_para_prep_global_det_wave_dir,prep_dir)
                  +'\n')
    else:
        trf.write(os.path.join(evs_para_prep_global_det_wave_dir,prep_dir)
                  +":"
                  +str(len(os.path.join(evs_para_prep_global_det_wave_dir,prep_dir)))
                  +" files\n")
trf.write("\n")


### Check global_det atmos stats
trf.write("GLOBAL_DET ATMOS - STATS\n")
STAT_CHECKDATE = f"{today - datetime.timedelta(days=2):%Y%m%d}"
evs_para_stats_global_det_dir = os.path.join(
    evs_para_base_dir, 'stats', 'global_det'
)
verif_case_model_dict = {
    'grid2grid': ['cfs', 'cmc', 'cmc_regional', 'dwd',
                  'ecmwf', 'fnmoc', 'gfs', 'imd', 'jma',
                  'metfra', 'ukmet'],
    'grid2obs': ['cfs', 'cmc', 'ecmwf', 'fnmoc', 'gfs',
                 'imd', 'jma', 'ukmet']
}
for verif_case in list(verif_case_model_dict.keys()):
    for model in verif_case_model_dict[verif_case]:
        stat_file = os.path.join(
            evs_para_stats_global_det_dir, f"{model}.{STAT_CHECKDATE}",
            f"evs.stats.{model}.atmos.{verif_case}.v{STAT_CHECKDATE}.stat"
        )
        if not os.path.exists(stat_file):
            trf.write(f"DOES NOT EXIST {stat_file}\n")
        else:
            with open(stat_file, 'r') as fp:
                stat_file_nlines = len(fp.readlines())
                trf.write(f"{stat_file}: {stat_file_nlines} lines\n")
trf.write("\n")

### Check global_det wave stats
trf.write("GLOBAL_DET WAVE - STATS\n")
STAT_CHECKDATE = f"{today - datetime.timedelta(days=2):%Y%m%d}"
evs_para_stats_global_det_dir = os.path.join(
    evs_para_base_dir, 'stats', 'global_det'
)
verif_case_model_dict = {
    'grid2obs': ['gfs']
}
for verif_case in list(verif_case_model_dict.keys()):
    for model in verif_case_model_dict[verif_case]:
        stat_file = os.path.join(
            evs_para_stats_global_det_dir, f"{model}.{STAT_CHECKDATE}",
            f"evs.stats.{model}.wave.{verif_case}.v{STAT_CHECKDATE}.stat"
        )
        if not os.path.exists(stat_file):
            trf.write(f"DOES NOT EXIST {stat_file}\n")
        else:
            with open(stat_file, 'r') as fp:
                stat_file_nlines = len(fp.readlines())
                trf.write(f"{stat_file}: {stat_file_nlines} lines\n")
trf.write("\n")

### Check global_det atmos plots
trf.write("GLOBAL_DET ATMOS - PLOTS\n")
PLOT_CHECKDATE = f"{today - datetime.timedelta(days=2):%Y%m%d}"
evs_para_plots_global_det_atmos_dir = os.path.join(
    '/lfs/h2/emc/ptmp/emc.vpppg/evs/v2.0', 'plots', 'global_det',
    f"atmos.{PLOT_CHECKDATE}"
)
verif_case_type_list = ['grid2grid_means', 'grid2grid_precip', 'grid2grid_pres_levs',
                        'grid2grid_sea_ice', 'grid2grid_snow', 'grid2grid_sst',
                        'grid2obs_pres_levs', 'grid2obs_ptype', 'grid2obs_sfc']
ndays_list = ['31', '90']
for verif_case_type in verif_case_type_list:
    for ndays in ndays_list:
        tar_file = os.path.join(
            evs_para_plots_global_det_atmos_dir,
            f"evs.plots.global_det.atmos.{verif_case_type}."
            +f"last{ndays}days.v{PLOT_CHECKDATE}.tar"
        )
        if not os.path.exists(tar_file):
            trf.write(f"DOES NOT EXIST {tar_file}\n")
        else:
            trf.write(f"{tar_file}: {round(os.path.getsize(tar_file) * 1e-9,2)}GB\n")

evs_para_plots_global_det_headline_dir = os.path.join(
    '/lfs/h2/emc/ptmp/emc.vpppg/evs/v2.0', 'plots', 'global_det',
    f"headline.{PLOT_CHECKDATE}"
)
tar_file = os.path.join(
    evs_para_plots_global_det_headline_dir,
    f"evs.plots.global_det.atmos.headline.v{PLOT_CHECKDATE}.tar"
)
if not os.path.exists(tar_file):
    trf.write(f"DOES NOT EXIST {tar_file}\n")
else:
    trf.write(f"{tar_file}: {round(os.path.getsize(tar_file) * 0.01,2)}MB\n")
trf.write("\n")

### Check global_det wave plots
trf.write("GLOBAL_DET WAVE - PLOTS\n")
PLOT_CHECKDATE = f"{today - datetime.timedelta(days=2):%Y%m%d}"
evs_para_plots_global_det_wave_dir = os.path.join( 
    '/lfs/h2/emc/ptmp/emc.vpppg/evs/v2.0', 'plots', 'global_det',
    f"wave.{PLOT_CHECKDATE}"
)
verif_case_type_list = ['grid2obs']
ndays_list = ['31', '90']
for verif_case_type in verif_case_type_list:
    for ndays in ndays_list:
        tar_file = os.path.join(
            evs_para_plots_global_det_wave_dir,
            f"evs.plots.global_det.wave.{verif_case_type}."
            +f"last{ndays}days.v{PLOT_CHECKDATE}.tar"
        )
        if not os.path.exists(tar_file):
            trf.write(f"DOES NOT EXIST {tar_file}\n")
        else:
            trf.write(f"{tar_file}: {round(os.path.getsize(tar_file) * 1e-9,2)}GB\n")
trf.write("\n")

### Log File Check
trf.write("LOG CHECK\n")
log_file_list = [
    'jevs_global_det_atmos_prep_00',
    'jevs_global_det_wave_prep_00',
    'jevs_global_det_atmos_cfs_grid2grid_stats_00',
    'jevs_global_det_atmos_cfs_grid2obs_stats_00',
    'jevs_global_det_atmos_cmc_grid2grid_stats_00',
    'jevs_global_det_atmos_cmc_grid2obs_stats_00',
    'jevs_global_det_atmos_cmc_regional_grid2grid_stats_00',
    'jevs_global_det_atmos_dwd_grid2grid_stats_00',
    'jevs_global_det_atmos_ecmwf_grid2grid_stats_00',
    'jevs_global_det_atmos_ecmwf_grid2obs_stats_00',
    'jevs_global_det_atmos_fnmoc_grid2grid_stats_00',
    'jevs_global_det_atmos_fnmoc_grid2obs_stats_00',
    'jevs_global_det_atmos_gfs_grid2grid_stats_00',
    'jevs_global_det_atmos_gfs_grid2obs_stats_00',
    'jevs_global_det_atmos_imd_grid2grid_stats_00',
    'jevs_global_det_atmos_imd_grid2obs_stats_00',
    'jevs_global_det_atmos_jma_grid2grid_stats_00',
    'jevs_global_det_atmos_jma_grid2obs_stats_00',
    'jevs_global_det_atmos_metfra_grid2grid_stats_00',
    'jevs_global_det_atmos_ukmet_grid2grid_stats_00',
    'jevs_global_det_atmos_ukmet_grid2obs_stats_00',
    'jevs_global_det_wave_gfs_grid2obs_stats_00',
    'jevs_global_det_atmos_headline_plots_00',
    'jevs_global_det_atmos_grid2grid_means_plots_31days_00',
    'jevs_global_det_atmos_grid2grid_means_plots_90days_00',
    'jevs_global_det_atmos_grid2grid_precip_plots_31days_00',
    'jevs_global_det_atmos_grid2grid_precip_plots_90days_00',
    'jevs_global_det_atmos_grid2grid_pres_levs_plots_31days_00',
    'jevs_global_det_atmos_grid2grid_pres_levs_plots_90days_00',
    'jevs_global_det_atmos_grid2grid_sea_ice_plots_31days_00',
    'jevs_global_det_atmos_grid2grid_sea_ice_plots_90days_00',
    'jevs_global_det_atmos_grid2grid_snow_plots_31days_00',
    'jevs_global_det_atmos_grid2grid_snow_plots_90days_00',
    'jevs_global_det_atmos_grid2grid_sst_plots_31days_00',
    'jevs_global_det_atmos_grid2grid_sst_plots_90days_00',
    'jevs_global_det_atmos_grid2obs_pres_levs_plots_31days_00',
    'jevs_global_det_atmos_grid2obs_pres_levs_plots_90days_00',
    'jevs_global_det_atmos_grid2obs_ptype_plots_31days_00',
    'jevs_global_det_atmos_grid2obs_ptype_plots_90days_00',
    'jevs_global_det_atmos_grid2obs_sfc_plots_31days_00',
    'jevs_global_det_atmos_grid2obs_sfc_plots_90days_00',
    'jevs_global_det_wave_grid2obs_plots_31days_00',
    'jevs_global_det_wave_grid2obs_plots_90days_00',
]
grep_keyword_list = ['failed', 'FAILED', 'exceeded']
for log_file in log_file_list:
    if len(glob.glob(os.path.join(evs_para_log_dir, log_file+'.o*'))) == 0:
        trf.write(f"NO LOG FILE MATCHING {os.path.join(evs_para_log_dir, log_file+'.o*')}\n")
    else:
        LOG_CHECKDATE = f"{today - datetime.timedelta(days=1):%Y%m%d}"
        for check_date_log_file in glob.glob(os.path.join(evs_para_log_dir, log_file+'.o*')):
            date_log_file_dt = datetime.datetime.strptime(
                time.ctime(os.path.getctime(check_date_log_file)),
                '%a %b %d %H:%M:%S %Y'
            )
            if f"{date_log_file_dt:%Y%m%d}" == LOG_CHECKDATE:
                LOG_CHECKDATE_file = check_date_log_file
                for grep_keyword in grep_keyword_list:
                    ps = subprocess.Popen(
                        'grep -r "'+grep_keyword+'" '+LOG_CHECKDATE_file,
                        shell=True, stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT, encoding='UTF-8'
                    )
                    grep_keyword_log_output = ps.communicate()[0]
                    grep_keyword_log_output_write = []
                    for grep_grep_keyword_log_line in grep_keyword_log_output.split('\n'):
                        if 'LNet' not in grep_grep_keyword_log_line:
                            grep_keyword_log_output_write.append(grep_grep_keyword_log_line)
                    if len(grep_keyword_log_output_write) == 0:
                        trf.write(f"{LOG_CHECKDATE_file} has no '"+grep_keyword+"'\n")
                    else:
                        trf.write(f"{LOG_CHECKDATE_file} ({grep_keyword}): "
                                  +'|'.join(grep_keyword_log_output_write)
                                  +"\n")
trf.close()
