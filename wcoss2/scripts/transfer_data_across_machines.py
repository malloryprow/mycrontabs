"""
About:
	This script runs on WCOSS2.
        It transfers files across WCOSS dev and prod machines
	and across various NOAA machines.
History Log:
	November 2021 - Port from WCOSS to WCOSS2
Command Line Agruments: 
	1 - CDATE, date to run for in YYYYMMDD,
            default: today
Input Files:
Output Files:
Condition codes: 0 for success, 1 for failure
"""

# Load modules
import os
import sys
import re
import subprocess
import datetime
import shutil
import glob

print("BEGIN: "+sys.argv[0]+" at "+str(datetime.datetime.today()))

# Command line agruments
if len(sys.argv) == 2:
    PDY = sys.argv[1]
    PDY_dt = datetime.datetime.strptime(PDY, '%Y%m%d')
elif len(sys.argv) == 1:
    PDY_dt = datetime.datetime.today()
    PDY = PDY_dt.strftime('%Y%m%d')
else:
    print("Too many agruements passed")
    exit(1)

# WCOSS2 information
wcoss2_user = os.getenv('USER', os.environ['LOGNAME'])
base_working_dir = '/lfs/h2/emc/stmp/'+wcoss2_user
wcoss2_base_user_dir = '/lfs/h2/emc/vpppg/noscrub/'+wcoss2_user
COMROOT = os.getenv('COMROOT', '/lfs/h1/ops/prod/com')

# Hera information
hera_user = 'Mallory.Row'
hera_client = 'dtn-hera.fairmont.rdhpcs.noaa.gov'
hera_base_user_dir = '/scratch1/NCEPDEV/global/'+hera_user

# Jet information
jet_user = 'Mallory.Row'
jet_client = 'dtn-jet.boulder.rdhpcs.noaa.gov'
jet_base_user_dir = '/mnt/lfs4/HFIP/hfv3gfs/'+jet_user

# Shared storage backups
dfs_dir = '/dfs/write/emc/vpppg/'+wcoss2_user

# Set up WCOSS2 dictionary
wcoss2_dict = {}
hostname = os.environ['HOSTNAME']
cactus_match = re.match(re.compile(r"^clogin[0-9]{2}$"), hostname)
dogwood_match = re.match(re.compile(r"^dlogin[0-9]{2}$"), hostname)
if cactus_match:
    wcoss2_dict['CURRENT'] = 'cactus'
    wcoss2_dict['OTHER'] = 'dogwood'
    wcoss2_dict['OTHER_TRANSFER'] = 'ddxfer.wcoss2.ncep.noaa.gov'
elif dogwood_match:
    wcoss2_dict['CURRENT'] = 'dogwood'
    wcoss2_dict['OTHER'] = 'cactus'
    wcoss2_dict['OTHER_TRANSFER'] = 'cdxfer.wcoss2.ncep.noaa.gov'
wcoss2_config_machine_output = subprocess.run(
    ['cat', '/lfs/h1/ops/prod/config/prodmachinefile'],
    capture_output=True
).stdout.decode('utf-8').rstrip().split('\n')
for config_machine in wcoss2_config_machine_output:
    config = config_machine.split(':')[0]
    machine = config_machine.split(':')[1]
    if config == 'primary':
        wcoss2_dict['PROD'] = machine
        if machine == 'cactus':
            wcoss2_dict['PROD_TRANSFER'] = 'cdxfer.wcoss2.ncep.noaa.gov'
        elif machine == 'dogwood':
            wcoss2_dict['PROD_TRANSFER'] = 'ddxfer.wcoss2.ncep.noaa.gov'
    elif config == 'backup':
        wcoss2_dict['DEV'] = machine
        if machine == 'cactus':
            wcoss2_dict['DEV_TRANSFER'] = 'ddxfer.wcoss2.ncep.noaa.gov'
        elif machine == 'dogwood':
            wcoss2_dict['DEV_TRANSFER'] = 'ddxfer.wcoss2.ncep.noaa.gov'
print("\nWCOSS2 machine information...")
for status in list(wcoss2_dict.keys()):
    print(status+' -> '+wcoss2_dict[status])

# Set up date dictionary
print("\nDate information...")
print("PDY -> "+PDY)
PDYm_dict = {
    'PDYm1': (PDY_dt - datetime.timedelta(days=1)).strftime('%Y%m%d'),
    'PDYm2': (PDY_dt - datetime.timedelta(days=2)).strftime('%Y%m%d'),
    'PDYm3': (PDY_dt - datetime.timedelta(days=3)).strftime('%Y%m%d'),
    #'PDYm4': (PDY_dt - datetime.timedelta(days=4)).strftime('%Y%m%d'),
    #'PDYm5': (PDY_dt - datetime.timedelta(days=5)).strftime('%Y%m%d'),
    #'PDYm6': (PDY_dt - datetime.timedelta(days=6)).strftime('%Y%m%d'),
    #'PDYm7': (PDY_dt - datetime.timedelta(days=7)).strftime('%Y%m%d')
}
for PDYm in list(PDYm_dict.keys()):
    print(PDYm+" -> "+PDYm_dict[PDYm])
PDYp_dict = {
    'PDYp1': (PDY_dt + datetime.timedelta(days=1)).strftime('%Y%m%d'),
    'PDYp2': (PDY_dt + datetime.timedelta(days=2)).strftime('%Y%m%d'),
    'PDYp3': (PDY_dt + datetime.timedelta(days=3)).strftime('%Y%m%d'),
    'PDYp4': (PDY_dt + datetime.timedelta(days=4)).strftime('%Y%m%d'),
    'PDYp5': (PDY_dt + datetime.timedelta(days=5)).strftime('%Y%m%d'),
    'PDYp6': (PDY_dt + datetime.timedelta(days=6)).strftime('%Y%m%d'),
    'PDYp7': (PDY_dt + datetime.timedelta(days=7)).strftime('%Y%m%d')
}
for PDYp in list(PDYp_dict.keys()):
    print(PDYp+" -> "+PDYp_dict[PDYp])

# Set up model version dictionary
model_ver_dict = {
    'gfs': os.getenv('gfs_ver', 'v16.3'),
    'obsproc': os.getenv('obsproc_ver', 'v1.2'),
}
print("\nModel version information...")
for model_ver in model_ver_dict:
    print(model_ver+" -> "+model_ver_dict[model_ver])

# Definitions
def rsync_cmd(source, destination):
    """! Executed rsync command from source to destination
        
         Args:
             source      - string of source information
             destination - string of destination information
         Returns:
    """
    if '*' in source:
        rsync_cmd = subprocess.run(
            ' '.join(['rsync', '-ahr', '-P', source, destination]),
            shell=True, capture_output=True
        )
    else:
        rsync_cmd = subprocess.run(
            ['rsync', '-ahr', '-P', source, destination],
            capture_output=True
        )
    if rsync_cmd.returncode != 0:
        print("***ERROR*** Could not rsync "+source+" to "+destination)
        print(rsync_cmd.stderr.decode('utf-8'))
    print(' '.join(['rsync', '-ahr', '-P', source, destination]))

def format_filler(file_format, date_time, string_sub_dict):
    """! This creates a file name based on a given file
         format
         
         Args:
             file_format        - string of file naming
                                  convention
             date_time          - string of the date and
                                  time in YYYYmmddHHMMSS
             string_sub_dict    - dictionary of other strings
                                  to use
          
         Returns:
             filled_file_format - string of file_format
                                  filled in with verifying
                                  time information
    """
    # Fill date and time information
    date_time_dt = datetime.datetime.strptime(date_time, '%Y%m%d%H%M%S')
    for file_format_chunk in file_format.split('/'):
        d, t = 1, 1
        filled_file_chunk = file_format_chunk
        if '{date?fmt=' in file_format_chunk:
            date_fmt_count = file_format_chunk.count('{date?fmt=')
            while d <= date_fmt_count:
                date_fmt = (filled_file_chunk \
                    .partition('{date?fmt=')[2].partition('}')[0]
                )
                filled_file_chunk = filled_file_chunk.replace(
                    '{date?fmt='+date_fmt+'}', date_time_dt.strftime(date_fmt)
                )
                d+=1
        if '{time?fmt=' in file_format_chunk:
            time_fmt_count = file_format_chunk.count('{time?fmt=')
            while t <= time_fmt_count:
                time_fmt = (filled_file_chunk \
                    .partition('{time?fmt=')[2].partition('}')[0]
                )
                filled_file_chunk = filled_file_chunk.replace(
                    '{time?fmt='+time_fmt+'}', date_time_dt.strftime(time_fmt)
                )
                t+=1
        for string_sub in list(string_sub_dict.keys()):
            s = 1
            if '{'+string_sub+'?fmt=%str}' in file_format_chunk:
                string_sub_fmt_count = (
                    file_format_chunk.count('{'+string_sub+'?fmt=%str}')
                )
                while s <= string_sub_fmt_count:
                    filled_file_chunk = filled_file_chunk.replace(
                        '{'+string_sub+'?fmt=%str}',
                        string_sub_dict[string_sub]
                    )
                    s+=1
        if 'filled_file_format' not in vars():
            filled_file_format = filled_file_chunk
        else:
            filled_file_format = filled_file_format+'/'+filled_file_chunk
    return filled_file_format

def rsync_to_machines(source, hera_dest, jet_dest):
    if '*' in source:
        if len(glob.glob(source)) != 0:
            source_exists = True
        else:
            source_exists = False
            print("***ERROR*** number of files for '"+source+"' is 0")
    else:
        if os.path.exists(source):
           source_exists = True
        else:
           source_exists = False
           print("***ERROR*** "+source+" does not exist")
    if source_exists:
        print("---- Copying to Hera: "+hera_dest)
        hera_client_dest = hera_user+'@'+hera_client+':'+hera_dest
        rsync_cmd(source, hera_client_dest)
        print("---- Copying to Jet: "+jet_dest)
        jet_client_dest = jet_user+'@'+jet_client+':'+jet_dest
        rsync_cmd(source, jet_client_dest)

### Set up information
## CCPA
ccpa_accum24hr_time_list = ['120000']
ccpa_accum24hr_prod_file_format = os.path.join(
    '/lfs/h2/emc/vpppg/noscrub/emc.vpppg/verification/global/archive/obs_data',
    'ccpa_accum24hr',
    'ccpa.{date?fmt=%Y%m%d}{time?fmt=%H}.24h'
)
hera_ccpa_accum24hr_file_format = os.path.join(
    hera_base_user_dir, 'obdata', 'ccpa_accum24hr',
    'ccpa.{date?fmt=%Y%m%d}{time?fmt=%H}.24h'
)
jet_ccpa_accum24hr_file_format = os.path.join(
    jet_base_user_dir, 'obdata', 'ccpa_accum24hr',
    'ccpa.{date?fmt=%Y%m%d}{time?fmt=%H}.24h'
)
ccpa_accum24hr_string_sub_dict = {}
## Prepbufr GDAS
prepbufr_gdas_time_list = ['000000', '060000', '120000', '180000']
prepbufr_gdas_prod_file_format = os.path.join(
    COMROOT, 'obsproc', model_ver_dict['obsproc'], 'gdas.{date?fmt=%Y%m%d}',
    '{time?fmt=%H}', 'atmos', 'gdas.t{time?fmt=%H}z.prepbufr'
)
hera_prepbufr_gdas_file_format = os.path.join(
    hera_base_user_dir, 'prepbufr', 'gdas',
    'prepbufr.gdas.{date?fmt=%Y%m%d}{time?fmt=%H}'
)
jet_prepbufr_gdas_file_format = os.path.join(
    jet_base_user_dir, 'prepbufr', 'gdas',
    'prepbufr.gdas.{date?fmt=%Y%m%d}{time?fmt=%H}'
)
prepbufr_gdas_string_sub_dict = {}
## Prebufr NAM
prepbufr_nam_time_list = ['000000', '060000', '120000', '180000']
prepbufr_nam_offset_list = ['00', '03']
prepbufr_nam_prod_file_format = os.path.join(
    COMROOT, 'obsproc', model_ver_dict['obsproc'], 'nam.{date?fmt=%Y%m%d}',
    'nam.t{time?fmt=%H}z.prepbufr.tm{offset?fmt=%str}'
)
hera_prepbufr_nam_file_format = os.path.join(
    hera_base_user_dir, 'prepbufr', 'nam',
    'nam.{date?fmt=%Y%m%d}',
    'nam.t{time?fmt=%H}z.prepbufr.tm{offset?fmt=%str}'
)
jet_prepbufr_nam_file_format = os.path.join(
    jet_base_user_dir, 'prepbufr', 'nam',
    'nam.{date?fmt=%Y%m%d}',
    'nam.t{time?fmt=%H}z.prepbufr.tm{offset?fmt=%str}'
)
prepbufr_nam_string_sub_dict = {}
### GFS archive
wcoss2_gfs_archive = os.path.join(
    '/lfs', 'h2', 'emc', 'vpppg', 'noscrub', 'emc.vpppg',
    'verification', 'global', 'archive', 'model_data', 'gfs'
)
hera_gfs_archive = os.path.join(
    hera_base_user_dir, 'archive', 'gfs'
)
jet_gfs_archive = os.path.join(
    jet_base_user_dir, 'archive', 'gfs'
)
### Fit2Obs archive
wcoss2_fit2obs_fnl_archive = os.path.join(
    '/lfs', 'h2', 'emc', 'vpppg', 'noscrub', 'emc.vpppg',
    'verification', 'global', 'archive', 'fit2obs_data', 'fnl'
)
hera_fit2obs_fnl_archive = os.path.join(
    hera_base_user_dir, 'archive', 'fit2obs', 'fnl'
)
jet_fit2obs_fnl_archive = os.path.join(
    jet_base_user_dir, 'archive', 'fit2obs', 'fnl'
)
### MET stat files
metplus_data_dict = {
    'gfs': {'time_list': ['000000', '060000', '120000', '180000'],
            'verif_case_type_dict': {'grid2grid': ['anom', 'pres', 'sfc'],
                                     'grid2obs': ['upper_air', 'conus_sfc'],
                                     'precip': ['ccpa_accum24hr']}},
}
wcoss2_metplus_data_file_format = os.path.join(
    '/lfs', 'h2', 'emc', 'vpppg', 'noscrub', 'emc.vpppg',
    'verification', 'global', 'archive', 'metplus_data',
    'by_VSDB', '{verif_case?fmt=%str}', '{verif_type?fmt=%str}',
    '{time?fmt=%H}Z', '{model?fmt=%str}',
     '{model?fmt=%str}_{date?fmt=%Y%m%d}.stat'
)
hera_metplus_data_file_format = os.path.join(
    hera_base_user_dir, 'archive', 'metplus_data',
    'by_VSDB', '{verif_case?fmt=%str}', '{verif_type?fmt=%str}',
    '{time?fmt=%H}Z', '{model?fmt=%str}',
     '{model?fmt=%str}_{date?fmt=%Y%m%d}.stat'
)
jet_metplus_data_file_format = os.path.join(
    jet_base_user_dir, 'archive', 'metplus_data',
    'by_VSDB', '{verif_case?fmt=%str}', '{verif_type?fmt=%str}',
    '{time?fmt=%H}Z', '{model?fmt=%str}',
     '{model?fmt=%str}_{date?fmt=%Y%m%d}.stat'
)

## Copy to other WCOSS2 machine
rsync_cmd(os.path.join(os.environ['HOME'], 'get_hpss_data.py'),
          wcoss2_dict['OTHER_TRANSFER']+':'+os.environ['HOME']+'/.')
rsync_cmd(os.path.join(os.environ['HOME'], 'load_metplus.sh'),
          wcoss2_dict['OTHER_TRANSFER']+':'+os.environ['HOME']+'/.')
rsync_cmd(os.path.join(os.environ['HOME'], 'models.ver'),
          wcoss2_dict['OTHER_TRANSFER']+':'+os.environ['HOME']+'/.')
rsync_cmd(os.path.join(os.environ['HOME'], 'qstat.py'),
          wcoss2_dict['OTHER_TRANSFER']+':'+os.environ['HOME']+'/.')
rsync_cmd(os.path.join(os.environ['HOME'], 'run_after_prod_switch.sh'),
          wcoss2_dict['OTHER_TRANSFER']+':'+os.environ['HOME']+'/.')
rsync_cmd(os.path.join(os.environ['HOME'], 'run_get_hpss_data.sh'),
          wcoss2_dict['OTHER_TRANSFER']+':'+os.environ['HOME']+'/.')
rsync_cmd(os.path.join(os.environ['HOME'], '.bashrc'),
          wcoss2_dict['OTHER_TRANSFER']+':'+os.environ['HOME']+'/.')
rsync_cmd(os.path.join(os.environ['HOME'], 'cron_jobs', 'crontab.dev'),
          wcoss2_dict['OTHER_TRANSFER']+':'
          +os.path.join(os.environ['HOME'], 'cron_jobs', '.'))
rsync_cmd(os.path.join(os.environ['HOME'], 'cron_jobs', 'crontab.prod'),
          wcoss2_dict['OTHER_TRANSFER']+':'
          +os.path.join(os.environ['HOME'], 'cron_jobs', '.'))
rsync_cmd(os.path.join(os.environ['HOME'], 'cron_jobs', 'scripts/*'),
          wcoss2_dict['OTHER_TRANSFER']+':'
          +os.path.join(os.environ['HOME'], 'cron_jobs', 'scripts/.'))

### Copy to Hera and Jet
if wcoss2_dict['DEV'] == wcoss2_dict['CURRENT']:
     print("\nDoing dev machine daily data transfer tasks....")
     print("\n-- Copying CCPA 24 hour accumulation production files")
     for PDYm in list(PDYm_dict.keys()):
        for time in ccpa_accum24hr_time_list:
            PDYm_date_time = PDYm_dict[PDYm]+time
            ccpa_accum24hr_prod_file = format_filler(
                ccpa_accum24hr_prod_file_format,
                PDYm_date_time,
                ccpa_accum24hr_string_sub_dict
            )
            print("--- CCPA 24 hour accumulation file for "
                  +PDYm_dict[PDYm]+" "+time+"..."+ccpa_accum24hr_prod_file)
            hera_ccpa_accum24hr_file = format_filler(
                hera_ccpa_accum24hr_file_format,
                PDYm_date_time,
                ccpa_accum24hr_string_sub_dict
            )
            jet_ccpa_accum24hr_file = format_filler(
                jet_ccpa_accum24hr_file_format,
                PDYm_date_time,
                ccpa_accum24hr_string_sub_dict
            )
            rsync_to_machines(
                ccpa_accum24hr_prod_file,
                hera_ccpa_accum24hr_file,
                jet_ccpa_accum24hr_file
            )
     print("\n-- Copying GDAS prepbufr production files")
     for PDYm in list(PDYm_dict.keys()):
        for time in prepbufr_gdas_time_list:
            PDYm_date_time = PDYm_dict[PDYm]+time
            prepbufr_gdas_prod_file = format_filler(
                prepbufr_gdas_prod_file_format,
                PDYm_date_time,
                prepbufr_gdas_string_sub_dict
            )
            print("--- Prepbufr GDAS file for "
                  +PDYm_dict[PDYm]+" "+time+"..."+prepbufr_gdas_prod_file)
            hera_prepbufr_gdas_file = format_filler(
                hera_prepbufr_gdas_file_format,
                PDYm_date_time,
                prepbufr_gdas_string_sub_dict
            )
            jet_prepbufr_gdas_file = format_filler(
                jet_prepbufr_gdas_file_format,
                PDYm_date_time,
                prepbufr_gdas_string_sub_dict
            )
            rsync_to_machines(
                prepbufr_gdas_prod_file,
                hera_prepbufr_gdas_file,
                jet_prepbufr_gdas_file
            )                
     print("\n-- Copying NAM prepbufr production files")
     for PDYm in list(PDYm_dict.keys()):
        for time in prepbufr_nam_time_list:
            PDYm_date_time = PDYm_dict[PDYm]+time
            for offset in prepbufr_nam_offset_list:
                prepbufr_nam_string_sub_dict['offset'] = offset
                prepbufr_nam_prod_file = format_filler(
                    prepbufr_nam_prod_file_format,
                    PDYm_date_time,
                    prepbufr_nam_string_sub_dict
                )
                prepbufr_nam_dt = (
                    datetime.datetime.strptime(PDYm_date_time, '%Y%m%d%H%M%S')
                    - datetime.timedelta(hours=int(offset))
                )
                print("--- Prepbufr NAM file for "
                      +prepbufr_nam_dt.strftime('%Y%m%d')+" "
                      +prepbufr_nam_dt.strftime('%H%M%S')+"..."
                      +prepbufr_nam_prod_file)
                hera_prepbufr_nam_file = format_filler(
                    hera_prepbufr_nam_file_format,
                    PDYm_date_time,
                    prepbufr_nam_string_sub_dict
                )
                mkdir_hera = subprocess.run(
                    ['ssh', '-q', '-l',
                     hera_user, hera_client,
                     " mkdir -p "
                     +hera_prepbufr_nam_file.rpartition('/')[0]]
                )
                if mkdir_hera.returncode != 0:
                    print("Could not make directory on Hera "
                          +hera_prepbufr_nam_file.rpartition('/')[0])    
                jet_prepbufr_nam_file = format_filler(
                    jet_prepbufr_nam_file_format,
                    PDYm_date_time,
                    prepbufr_nam_string_sub_dict
                )
                mkdir_jet = subprocess.run(
                    ['ssh', '-q', '-l',
                     jet_user, jet_client,
                     " mkdir -p "
                     +jet_prepbufr_nam_file.rpartition('/')[0]]
                )
                if mkdir_jet.returncode != 0:
                    print("Could not make directory on Jet "
                          +jet_prepbufr_nam_file.rpartition('/')[0])
                rsync_to_machines(
                    prepbufr_nam_prod_file,
                    hera_prepbufr_nam_file,
                    jet_prepbufr_nam_file
                )
     print("\n-- Copying GFS archive files")
     for PDYm in list(PDYm_dict.keys()):
         #wcoss2_gfs_PDYm_file_wildcard = os.path.join(
         #    wcoss2_gfs_archive, 'pgb*.'+PDYm_dict[PDYm]+'*'
         #)
         #wcoss2_gfs_PDYm_file_list = glob.glob(wcoss2_gfs_PDYm_file_wildcard)
         #print("--- GFS Archive Files for "+PDYm_dict[PDYm]+"..."
         #      +wcoss2_gfs_PDYm_file_wildcard)
         print("--- GFS Archive Files for "+PDYm_dict[PDYm])
         wcoss2_gfs_PDYm_file_list = [
             'pgbanl.gfs.'+PDYm_dict[PDYm]+'00',
             'pgbanl.gfs.'+PDYm_dict[PDYm]+'06',
             'pgbanl.gfs.'+PDYm_dict[PDYm]+'12',
             'pgbanl.gfs.'+PDYm_dict[PDYm]+'18',
             'pgbanl.gdas.'+PDYm_dict[PDYm]+'00',
             'pgbanl.gdas.'+PDYm_dict[PDYm]+'06',
             'pgbanl.gdas.'+PDYm_dict[PDYm]+'12',
             'pgbanl.gdas.'+PDYm_dict[PDYm]+'18',
             'pgbf00.gfs.'+PDYm_dict[PDYm]+'00',
             'pgbf00.gfs.'+PDYm_dict[PDYm]+'06',
             'pgbf00.gfs.'+PDYm_dict[PDYm]+'12',
             'pgbf00.gfs.'+PDYm_dict[PDYm]+'18',
             'pgbf00.gdas.'+PDYm_dict[PDYm]+'00',
             'pgbf00.gdas.'+PDYm_dict[PDYm]+'06',
             'pgbf00.gdas.'+PDYm_dict[PDYm]+'12',
             'pgbf00.gdas.'+PDYm_dict[PDYm]+'18',
         ]
         for wcoss2_gfs_PDYm_file in wcoss2_gfs_PDYm_file_list:
             rsync_to_machines(
                 os.path.join(wcoss2_gfs_archive,
                              wcoss2_gfs_PDYm_file),
                 hera_gfs_archive+'/.',
                 jet_gfs_archive+'/.'
             )
     #print("\n-- Copying fit2obs files")
     #for PDYm in list(PDYm_dict.keys()):
     #    wcoss2_fit2obs_fnl_fits_PDYm_wildcard = os.path.join(
     #        wcoss2_fit2obs_fnl_archive, 'fits', '*.'+PDYm_dict[PDYm]+'*'
     #    )
     #    wcoss2_fit2obs_fnl_fits_PDYm_file_list = glob.glob(
     #        wcoss2_fit2obs_fnl_fits_PDYm_wildcard
     #    )
     #    print("--- Fit2Obs fnl fits for "+PDYm_dict[PDYm]+"..."
     #          +wcoss2_fit2obs_fnl_fits_PDYm_wildcard)
     #    hera_fit2obs_fnl_fits_archive = os.path.join(
     #        hera_fit2obs_fnl_archive, 'fits'
     #    )
     #    jet_fit2obs_fnl_fits_archive = os.path.join(
     #        jet_fit2obs_fnl_archive, 'fits'
     #    )
     #    for wcoss2_fit2obs_fnl_fits_PDYm_file \
     #            in wcoss2_fit2obs_fnl_fits_PDYm_file_list:
     #        rsync_to_machines(
     #            wcoss2_fit2obs_fnl_fits_PDYm_file,
     #            hera_fit2obs_fnl_fits_archive+'/.',
     #            jet_fit2obs_fnl_fits_archive+'/.'
     #        )
     #    wcoss2_fit2obs_fnl_horiz_anl_PDYm_wildcard = os.path.join(
     #        wcoss2_fit2obs_fnl_archive, 'horiz', 'anl',
     #        '*.'+PDYm_dict[PDYm]+'*'
     #    )
     #    wcoss2_fit2obs_fnl_horiz_anl_PDYm_file_list = glob.glob(
     #        wcoss2_fit2obs_fnl_horiz_anl_PDYm_wildcard
     #    )
     #    print("--- Fit2Obs fnl horiz anl for "+PDYm_dict[PDYm]+"..."
     #          +wcoss2_fit2obs_fnl_horiz_anl_PDYm_wildcard)
     #    hera_fit2obs_fnl_horiz_anl_archive = os.path.join(
     #        hera_fit2obs_fnl_archive, 'horiz', 'anl'
     #    )
     #    jet_fit2obs_fnl_horiz_anl_archive = os.path.join(
     #        jet_fit2obs_fnl_archive, 'horiz', 'anl'
     #    )
     #    for wcoss2_fit2obs_fnl_horiz_anl_PDYm_file \
     #           in wcoss2_fit2obs_fnl_horiz_anl_PDYm_file_list:
     #        rsync_to_machines(
     #            wcoss2_fit2obs_fnl_horiz_anl_PDYm_file,
     #            hera_fit2obs_fnl_horiz_anl_archive+'/.',
     #            jet_fit2obs_fnl_horiz_anl_archive+'/.'
     #        )
     #    wcoss2_fit2obs_fnl_horiz_fcs_PDYm_wildcard = os.path.join(
     #        wcoss2_fit2obs_fnl_archive, 'horiz', 'fcs',
     #        '*.'+PDYm_dict[PDYm]+'*'
     #    )
     #    wcoss2_fit2obs_fnl_horiz_fcs_PDYm_file_list = glob.glob(
     #        wcoss2_fit2obs_fnl_horiz_fcs_PDYm_wildcard
     #    )
     #    print("--- Fit2Obs fnl horiz fcs for "+PDYm_dict[PDYm]+"..."
     #          +wcoss2_fit2obs_fnl_horiz_fcs_PDYm_wildcard)
     #    hera_fit2obs_fnl_horiz_fcs_archive = os.path.join(
     #        hera_fit2obs_fnl_archive, 'horiz', 'fcs'
     #    )
     #    jet_fit2obs_fnl_horiz_fcs_archive = os.path.join(
     #        jet_fit2obs_fnl_archive, 'horiz', 'fcs'
     #    )
     #    for wcoss2_fit2obs_fnl_horiz_fcs_PDYm_file \
     #            in wcoss2_fit2obs_fnl_horiz_fcs_PDYm_file_list:
     #        rsync_to_machines(
     #            wcoss2_fit2obs_fnl_horiz_fcs_PDYm_file,
     #            hera_fit2obs_fnl_horiz_fcs_archive+'/.',
     #            jet_fit2obs_fnl_horiz_fcs_archive+'/.'
     #        )
     print("\n-- Copying METplus stat files")
     for model in list(metplus_data_dict.keys()):
        model_metplus_data_dict = metplus_data_dict[model]
        model_metplus_data_time_list = model_metplus_data_dict['time_list']
        model_metplus_data_verif_case_type_dict = (
            model_metplus_data_dict['verif_case_type_dict']
        )
        model_metplus_data_string_sub_dict = {
            'model': model
        }
        for PDYm in list(PDYm_dict.keys()):
            for time in model_metplus_data_time_list:
                PDYm_date_time = PDYm_dict[PDYm]+time
                for verif_case in \
                        list(model_metplus_data_verif_case_type_dict.keys()):
                    if (verif_case == 'precip' and PDYm == 'PDYm1'):
                        # Skip files for precip PDYm1, latest verification
                        # is PDYm2
                        continue
                    model_metplus_data_string_sub_dict['verif_case'] = (
                        verif_case
                    )
                    verif_type_list = (
                        model_metplus_data_verif_case_type_dict[verif_case]
                    )
                    for verif_type in verif_type_list:
                        model_metplus_data_string_sub_dict['verif_type'] = (
                            verif_type
                        )
                        wcoss2_model_metplus_data_file = format_filler(
                            wcoss2_metplus_data_file_format,
                            PDYm_date_time,
                            model_metplus_data_string_sub_dict
                        )
                        print("--- METplus verification file for "+model+" "
                               +PDYm_dict[PDYm]+" "+time+"..."
                               +wcoss2_model_metplus_data_file)
                        hera_metplus_data_file = format_filler(
                            hera_metplus_data_file_format,
                            PDYm_date_time,
                            model_metplus_data_string_sub_dict
                        )
                        jet_metplus_data_file = format_filler(
                            jet_metplus_data_file_format,
                            PDYm_date_time,
                            model_metplus_data_string_sub_dict
                        )
                        rsync_to_machines(
                            wcoss2_model_metplus_data_file,
                            hera_metplus_data_file,
                            jet_metplus_data_file
                        )

print("\nEND: "+sys.argv[0]+" at "+str(datetime.datetime.today()))
