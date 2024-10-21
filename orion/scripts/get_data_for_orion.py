import os
import sys
import subprocess
import datetime
import shutil

print("BEGIN: "+sys.argv[0]+" at "+str(datetime.datetime.today())+"\n")

########## Set up information
##### Paths
working_dir = '/home/'+os.environ['USER']+'/mycronjobs/out'
base_user_dir = '/work/noaa/ovp/'+os.environ['USER']
prepbufr_archive_base_dir = os.path.join(base_user_dir, 'prepbufr')
prepbufr_rstprod_archive_base_dir = '/work/noaa/rstprod/verif/prepbufr'
ccpa_archive_base_dir = os.path.join(base_user_dir, 'obdata')
metplus_archive_base_dir = os.path.join(base_user_dir, 'archive',
                                        'metplus_data', 'by_VSDB')
model_data_archive_base_dir = os.path.join(base_user_dir, 'archive')
model_archive_base_dir = os.path.join(base_user_dir, 'archive')
hwrf_trak_archive_base_dir = os.path.join(base_user_dir, 'trak', 'abdeck')
NOMADS_web_path = 'https://nomads.ncep.noaa.gov/pub/data/nccf/com'
##### Hera
hera_base_user_dir = '/scratch1/NCEPDEV/global/Mallory.Row'
hera_client = 'dtn-hera.fairmont.rdhpcs.noaa.gov'
hera_user = 'Mallory.Row'
##### Environment variables
CP = os.environ['CP']
WGET = os.environ['WGET']
RSYNC = os.environ['RSYNC']

########## Functions
def check_and_make_directory(dir_path):
    """! See if a directory path exists, if it does not then
         make it   
         Args:
             dir_path        - string of directory path
          
         Returns:
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def change_permissions(file_path):
    """! Adjust file permissions
         Args:
             file_path        - string of file path
          
         Returns:
    """
    os.system('chmod 755 '+file_path)

def format_filler(file_format, date_time):
    """! This creates a file name based on a given file
         format
         
         Args:
             file_format        - string of file naming
                                  convention
             date_time          - string of the date and
                                  time in YYYYmmddHHMMSS
          
         Returns:
             filled_file_format - string of file_format
                                  filled in with verifying
                                  time information
    """
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
        if 'filled_file_format' not in vars():
            filled_file_format = filled_file_chunk
        else:
            filled_file_format = filled_file_format+'/'+filled_file_chunk
    return filled_file_format

########## Set up date information
today = datetime.datetime.today()
PDY = today.strftime('%Y%m%d')
PDYm_dict = {
    'PDYm1': (today - datetime.timedelta(days=1)).strftime('%Y%m%d'),
    'PDYm2': (today - datetime.timedelta(days=2)).strftime('%Y%m%d'),
    'PDYm3': (today - datetime.timedelta(days=3)).strftime('%Y%m%d'),
    'PDYm4': (today - datetime.timedelta(days=4)).strftime('%Y%m%d'),
    'PDYm5': (today - datetime.timedelta(days=5)).strftime('%Y%m%d'),
    'PDYm6': (today - datetime.timedelta(days=6)).strftime('%Y%m%d'),
    'PDYm7': (today - datetime.timedelta(days=7)).strftime('%Y%m%d')
}
PDYp_dict = {
    'PDYp1': (today + datetime.timedelta(days=1)).strftime('%Y%m%d'),
    'PDYp2': (today + datetime.timedelta(days=2)).strftime('%Y%m%d'),
    'PDYp3': (today + datetime.timedelta(days=3)).strftime('%Y%m%d'),
    'PDYp4': (today + datetime.timedelta(days=4)).strftime('%Y%m%d'),
    'PDYp5': (today + datetime.timedelta(days=5)).strftime('%Y%m%d'),
    'PDYp6': (today + datetime.timedelta(days=6)).strftime('%Y%m%d'),
    'PDYp7': (today + datetime.timedelta(days=7)).strftime('%Y%m%d')
}
print("Using PDY as "+PDY)

########## Set up and clean up working directory
os.chdir(working_dir)
working_dir_PDY = os.path.join(working_dir, 'get_data_for_orion_run_on_'+PDY)
check_and_make_directory(working_dir_PDY)
for PDYm in list(PDYm_dict.keys()):
    working_dir_PDYm = os.path.join(working_dir,
                                    'get_data_for_orion_run_on_'
                                    +PDYm_dict[PDYm])
    if os.path.exists(working_dir_PDYm):
        shutil.rmtree(working_dir_PDYm)

########## Get from NOMADS
from_NOMADS_working_dir_PDY = os.path.join(working_dir_PDY, 'from_NOMADS')
check_and_make_directory(from_NOMADS_working_dir_PDY)
##### 1. Get GDAS and NAM non-restricted prepbufr files from NOMADS
check_and_make_directory(
    os.path.join(from_NOMADS_working_dir_PDY, 'prepbufr')
)
# Prepbufr information dictionary
prepbufr_dict = {
    'gdas': {
         'NOMADS_dir': 'obsproc/v1.2',
         'NOMADS_file_format_list': [
             'gdas.{date?fmt=%Y%m%d}'
             +'/gdas.t{time?fmt=%H}z.prepbufr.nr'
         ],
         'archive_file_format_list': [
             'prepbufr.gdas.{date?fmt=%Y%m%d}{time?fmt=%H}.nr'
         ],
         'time_list': ['000000', '060000', '120000', '180000']
     } ,
     'nam': {
         'NOMADS_dir': 'obsproc/v1.2',
         'NOMADS_file_format_list': [
             'nam.{date?fmt=%Y%m%d}/nam.t{time?fmt=%H}z.prepbufr.tm00.nr',
             'nam.{date?fmt=%Y%m%d}/nam.t{time?fmt=%H}z.prepbufr.tm03.nr'
         ],
         'archive_file_format_list': [
             'nam.{date?fmt=%Y%m%d}/nam.t{time?fmt=%H}z.prepbufr.tm00.nr',
             'nam.{date?fmt=%Y%m%d}/nam.t{time?fmt=%H}z.prepbufr.tm03.nr'
         ],
         'time_list': ['000000', '060000', '120000', '180000']
     }
}
check_and_make_directory(prepbufr_archive_base_dir)
print("\n- Checking GDAS and NAM non-restricted prepbufr archive files in "
      +prepbufr_archive_base_dir+", getting missing files from NOMADS")
for prepbufr in list(prepbufr_dict.keys()):
    # Set up information
    prepbufr_info_dict = prepbufr_dict[prepbufr]
    prepbufr_NOMADS_dir = os.path.join(NOMADS_web_path,
                                       prepbufr_info_dict['NOMADS_dir'])
    prepbufr_NOMADS_file_format_list = (
        prepbufr_info_dict['NOMADS_file_format_list']
    )
    prepbufr_archive_file_format_list = (
        prepbufr_info_dict['archive_file_format_list']
    )
    prepbufr_time_list = prepbufr_info_dict['time_list']
    # Set up directories
    prepbufr_from_NOMADS_working_dir_PDY = os.path.join(
        from_NOMADS_working_dir_PDY, 'prepbufr', prepbufr
    )
    check_and_make_directory(prepbufr_from_NOMADS_working_dir_PDY)
    prepbufr_archive_dir = os.path.join(prepbufr_archive_base_dir, prepbufr)
    check_and_make_directory(prepbufr_archive_dir)
    # Get files
    print("-- Checking "+prepbufr.upper()+" non-restricted prepbufr files")
    for PDYm in list(PDYm_dict.keys()):
        for time in prepbufr_time_list:
            PDYm_date_time = PDYm_dict[PDYm]+time
            for prepbufr_archive_file_format \
                    in prepbufr_archive_file_format_list:
                idx = prepbufr_archive_file_format_list.index(
                    prepbufr_archive_file_format
                )
                # Archive file information
                prepbufr_archive_file_name = format_filler(
                    prepbufr_archive_file_format, PDYm_date_time
                )
                prepbufr_archive_file = os.path.join(
                    prepbufr_archive_dir, prepbufr_archive_file_name
                )
                print("--- Checking for file: "+prepbufr_archive_file)
                if not os.path.exists(prepbufr_archive_file):
                    print("---- "+prepbufr_archive_file+" does not exist, "
                          +"retrieving file from NOMADS.")
                    prepbufr_archive_file_dir = (
                        prepbufr_archive_file.rpartition('/')[0]
                    )
                    check_and_make_directory(prepbufr_archive_file_dir)
                    # NOMADS file information
                    prepbufr_NOMADS_file_format = (
                       prepbufr_NOMADS_file_format_list[idx]
                    )
                    prepbufr_NOMADS_file_name = format_filler(
                        prepbufr_NOMADS_file_format, PDYm_date_time
                    )
                    prepbufr_NOMADS_file = os.path.join(
                        prepbufr_NOMADS_dir, prepbufr_NOMADS_file_name
                    )
                    # Working file information
                    prepbufr_working_file = os.path.join(
                        prepbufr_from_NOMADS_working_dir_PDY,
                        prepbufr_archive_file_name
                    )
                    prepbufr_working_file_dir = (
                        prepbufr_working_file.rpartition('/')[0]
                    )
                    check_and_make_directory(prepbufr_working_file_dir)
                    # Get file
                    WGET_cmd = subprocess.run(
                        [WGET,
                         '-O', prepbufr_working_file,
                         prepbufr_NOMADS_file]
                    )
                    if WGET_cmd.returncode == 0:
                        CP_cmd = subprocess.run(
                            [CP,
                             prepbufr_working_file,
                             prepbufr_archive_file]
                        )
                        if CP_cmd.returncode != 0:
                            print("***ERROR*** Could not cp "
                                  +prepbufr_working_file+" to "
                                  +prepbufr_archive_file)
                        else:
                            # Change permissions
                            change_permissions(prepbufr_archive_file)
                    else:
                        print("***ERROR*** Could not wget "+prepbufr_NOMADS_file)
                else:
                    print("---- "+prepbufr_archive_file+" exists ")

##### Get from hera
from_hera_working_dir_PDY = os.path.join(working_dir_PDY, 'from_hera')
check_and_make_directory(from_hera_working_dir_PDY)
##### 1. Copy prepbufr files from Hera
prepbufr_rstprod_dict = {
    'gdas': {
         'hera_dir': 'prepbufr',
         'hera_file_format_list': [
             'prepbufr.gdas.{date?fmt=%Y%m%d}{time?fmt=%H}'
         ],
         'archive_file_format_list': [
             'prepbufr.gdas.{date?fmt=%Y%m%d}{time?fmt=%H}'
         ],
         'time_list': ['000000', '060000', '120000', '180000']
     },
     'nam': {
         'hera_dir': 'prepbufr',
         'hera_file_format_list': [
             'nam.{date?fmt=%Y%m%d}/nam.t{time?fmt=%H}z.prepbufr.tm00',
             'nam.{date?fmt=%Y%m%d}/nam.t{time?fmt=%H}z.prepbufr.tm03'
         ],
         'archive_file_format_list': [
             'nam.{date?fmt=%Y%m%d}/nam.t{time?fmt=%H}z.prepbufr.tm00',
             'nam.{date?fmt=%Y%m%d}/nam.t{time?fmt=%H}z.prepbufr.tm03'
         ],
         'time_list': ['000000', '060000', '120000', '180000']
    }
}
print("\n- Checking GDAS and NAM restricted prepbufr archive files in "
      +prepbufr_rstprod_archive_base_dir+", getting missing files from Hera")
for prepbufr_rstprod in list(prepbufr_rstprod_dict.keys()):
    # Set up information
    prepbufr_rstprod_info_dict = prepbufr_rstprod_dict[prepbufr_rstprod]
    prepbufr_rstprod_hera_dir = os.path.join(
        hera_base_user_dir, prepbufr_rstprod_info_dict['hera_dir'],
        prepbufr_rstprod
    )
    prepbufr_rstprod_hera_file_format_list = (
        prepbufr_rstprod_info_dict['hera_file_format_list']
    )
    prepbufr_rstprod_archive_file_format_list = (
        prepbufr_rstprod_info_dict['archive_file_format_list']
    )
    prepbufr_rstprod_time_list = prepbufr_rstprod_info_dict['time_list']
    # Set up directories
    prepbufr_rstprod_from_hera_working_dir_PDY = os.path.join(
        from_hera_working_dir_PDY, 'prepbufr_rstprod', prepbufr_rstprod
    )
    check_and_make_directory(prepbufr_rstprod_from_hera_working_dir_PDY)
    prepbufr_rstprod_archive_dir = os.path.join(prepbufr_rstprod_archive_base_dir,
                                                prepbufr_rstprod)
    check_and_make_directory(prepbufr_rstprod_archive_dir)
    ## Get files
    print("-- Checking "+prepbufr_rstprod+" files")
    for PDYm in list(PDYm_dict.keys()):
        for time in prepbufr_rstprod_time_list:
            PDYm_date_time = PDYm_dict[PDYm]+time
            for prepbufr_rstprod_archive_file_format \
                    in prepbufr_rstprod_archive_file_format_list:
                idx = prepbufr_rstprod_archive_file_format_list.index(
                    prepbufr_rstprod_archive_file_format
                )
                 # Archive file information
                prepbufr_rstprod_archive_file_name = format_filler(
                    prepbufr_rstprod_archive_file_format, PDYm_date_time
                )
                prepbufr_rstprod_archive_file = os.path.join(
                    prepbufr_rstprod_archive_dir, prepbufr_rstprod_archive_file_name
                )
                print("--- Checking for file: "+prepbufr_rstprod_archive_file)
                if not os.path.exists(prepbufr_rstprod_archive_file):
                    print("---- "+prepbufr_rstprod_archive_file+" does not exist, "
                          +"retrieving file from Hera.")
                    prepbufr_rstprod_archive_file_dir = (
                        prepbufr_rstprod_archive_file.rpartition('/')[0]
                    )
                    check_and_make_directory(prepbufr_rstprod_archive_file_dir)
                    os.system('chmod 750 '+prepbufr_rstprod_archive_file_dir)
                    os.system('chgrp rstprod '+prepbufr_rstprod_archive_file_dir)
                    # Hera file information
                    prepbufr_rstprod_hera_file_format = (
                       prepbufr_rstprod_hera_file_format_list[idx]
                    )
                    prepbufr_rstprod_hera_file_name = format_filler(
                        prepbufr_rstprod_hera_file_format, PDYm_date_time
                    )
                    prepbufr_rstprod_hera_file = os.path.join(
                        prepbufr_rstprod_hera_dir, prepbufr_rstprod_hera_file_name
                    )
                    print(prepbufr_rstprod_hera_file)
                    # Working file information
                    prepbufr_rstprod_working_file = os.path.join(
                        prepbufr_rstprod_from_hera_working_dir_PDY,
                        prepbufr_rstprod_archive_file_name
                    )
                    prepbufr_rstprod_working_file_dir = (
                        prepbufr_rstprod_working_file.rpartition('/')[0]
                    )
                    check_and_make_directory(prepbufr_rstprod_working_file_dir)
                    # Get file
                    RSYNC_cmd = subprocess.run(
                        [RSYNC,
                         '-ahr', '-P',
                         hera_user+'@'+hera_client+':'
                         +prepbufr_rstprod_hera_file,
                         prepbufr_rstprod_working_file]
                    )
                    if RSYNC_cmd.returncode == 0:
                        CP_cmd = subprocess.run(
                            [CP,
                             prepbufr_rstprod_working_file,
                             prepbufr_rstprod_archive_file]
                        )
                        if CP_cmd.returncode != 0:
                            print("***ERROR*** Could not cp "
                                  +prepbufr_rstprod_working_file+" to "
                                  +prepbufr_rstprod_archive_file)
                        else:
                            # Change permissions
                            os.system('chmod 650 '+prepbufr_rstprod_archive_file)
                            os.system('chgrp rstprod '+prepbufr_rstprod_archive_file)
                    else:
                        print("***ERROR*** Could not rsync "+prepbufr_rstprod_hera_file)
                else:
                    print("---- "+prepbufr_archive_file+" exists ")
##### 2. Copy CCPA files from Hera
check_and_make_directory(
    os.path.join(from_hera_working_dir_PDY, 'ccpa')
)
# CCPA information dictionary
ccpa_accum_dict = {
    'ccpa_accum24hr': {
        'hera_dir': 'obdata',
        'hera_file_format_list': [
             'ccpa.{date?fmt=%Y%m%d}{time?fmt=%H}.24h'
        ],
        'archive_file_format_list': [
            'ccpa.{date?fmt=%Y%m%d}{time?fmt=%H}.24h'
        ],
        'time_list': ['120000']
    }
}
check_and_make_directory(ccpa_archive_base_dir)
print("\n- Checking CCPA archive files in "
      +ccpa_archive_base_dir+", getting missing files from Hera")
for ccpa_accum in list(ccpa_accum_dict.keys()):
    # Set up information
    ccpa_accum_info_dict = ccpa_accum_dict[ccpa_accum]
    ccpa_accum_hera_dir = os.path.join(hera_base_user_dir,
                                       ccpa_accum_info_dict['hera_dir'],
                                       ccpa_accum)
    ccpa_accum_hera_file_format_list = (
        ccpa_accum_info_dict['hera_file_format_list']
    )
    ccpa_accum_archive_file_format_list = (
        ccpa_accum_info_dict['archive_file_format_list']
    )
    ccpa_accum_time_list = ccpa_accum_info_dict['time_list']
    # Set up directories
    ccpa_accum_from_hera_working_dir_PDY = os.path.join(
        from_hera_working_dir_PDY, 'ccpa', ccpa_accum
    )
    check_and_make_directory(ccpa_accum_from_hera_working_dir_PDY)
    ccpa_accum_archive_dir = os.path.join(ccpa_archive_base_dir, ccpa_accum)
    check_and_make_directory(ccpa_accum_archive_dir)
    ## Get files
    print("-- Checking "+ccpa_accum.split('_')[0].upper()+" "
          +ccpa_accum.split('_')[1]+" files")
    for PDYm in list(PDYm_dict.keys()):
        for time in ccpa_accum_time_list:
            PDYm_date_time = PDYm_dict[PDYm]+time
            for ccpa_accum_archive_file_format \
                    in ccpa_accum_archive_file_format_list:
                idx = ccpa_accum_archive_file_format_list.index(
                    ccpa_accum_archive_file_format
                )
                # Archive file information
                ccpa_accum_archive_file_name = format_filler(
                    ccpa_accum_archive_file_format, PDYm_date_time
                )
                ccpa_accum_archive_file = os.path.join(
                    ccpa_accum_archive_dir, ccpa_accum_archive_file_name
                )
                print("--- Checking for file: "+ccpa_accum_archive_file)
                if not os.path.exists(ccpa_accum_archive_file):
                    print("---- "+ccpa_accum_archive_file+" does not exist, "
                          +"retrieving file from Hera.")
                    ccpa_accum_archive_file_dir = (
                        ccpa_accum_archive_file.rpartition('/')[0]
                    )
                    check_and_make_directory(ccpa_accum_archive_file_dir)
                    # Hera file information
                    ccpa_accum_hera_file_format = (
                       ccpa_accum_hera_file_format_list[idx]
                    )
                    ccpa_accum_hera_file_name = format_filler(
                        ccpa_accum_hera_file_format, PDYm_date_time
                    )
                    ccpa_accum_hera_file = os.path.join(
                        ccpa_accum_hera_dir, ccpa_accum_hera_file_name
                    )
                    # Working file information
                    ccpa_accum_working_file = os.path.join(
                        ccpa_accum_from_hera_working_dir_PDY,
                        ccpa_accum_archive_file_name
                    )
                    ccpa_accum_working_file_dir = (
                        ccpa_accum_working_file.rpartition('/')[0]
                    )
                    check_and_make_directory(ccpa_accum_working_file_dir)
                    # Get file
                    RSYNC_cmd = subprocess.run(
                        [RSYNC,
                         '-ahr', '-P',
                         hera_user+'@'+hera_client+':'
                         +ccpa_accum_hera_file,
                         ccpa_accum_working_file]
                    )
                    if RSYNC_cmd.returncode == 0:
                        CP_cmd = subprocess.run(
                            [CP,
                             ccpa_accum_working_file,
                             ccpa_accum_archive_file]
                        )
                        if CP_cmd.returncode != 0:
                            print("***ERROR*** Could not cp "
                                  +ccpa_accum_working_file+" to "
                                  +ccpa_accum_archive_file)
                        else:
                            # Change permissions
                            change_permissions(ccpa_accum_archive_file)
                    else:
                        print("***ERROR*** Could not rsync "+ccpa_accum_hera_file)
                else:
                    print("---- "+ccpa_accum_archive_file+" exists")
##### 3. Copy METplus archive files from Hera
check_and_make_directory(
    os.path.join(from_hera_working_dir_PDY, 'metplus_data')
)
# METplus archive information dictionary
metplus_data_dict = {
    'grid2grid': {
        'hera_dir': 'archive/metplus_data/by_VSDB',
        'hera_file_format_list': [
             'anom/{time?fmt=%H}Z/gfs/gfs_{date?fmt=%Y%m%d}.stat',
             'pres/{time?fmt=%H}Z/gfs/gfs_{date?fmt=%Y%m%d}.stat',
             'sfc/{time?fmt=%H}Z/gfs/gfs_{date?fmt=%Y%m%d}.stat'
        ],
        'archive_file_format_list': [
             'anom/{time?fmt=%H}Z/gfs/gfs_{date?fmt=%Y%m%d}.stat',
             'pres/{time?fmt=%H}Z/gfs/gfs_{date?fmt=%Y%m%d}.stat',
             'sfc/{time?fmt=%H}Z/gfs/gfs_{date?fmt=%Y%m%d}.stat'
        ],
        'time_list': ['000000', '060000', '120000', '180000']
    },
    'grid2obs': {
        'hera_dir': 'archive/metplus_data/by_VSDB',
        'hera_file_format_list': [
             'upper_air/{time?fmt=%H}Z/gfs/gfs_{date?fmt=%Y%m%d}.stat',
             'conus_sfc/{time?fmt=%H}Z/gfs/gfs_{date?fmt=%Y%m%d}.stat'
        ],
        'archive_file_format_list': [
             'upper_air/{time?fmt=%H}Z/gfs/gfs_{date?fmt=%Y%m%d}.stat',
             'conus_sfc/{time?fmt=%H}Z/gfs/gfs_{date?fmt=%Y%m%d}.stat'
        ],
        'time_list': ['000000', '060000', '120000', '180000']
    },
    'precip': {
        'hera_dir': 'archive/metplus_data/by_VSDB',
        'hera_file_format_list': [
             'ccpa_accum24hr/{time?fmt=%H}Z/gfs/gfs_{date?fmt=%Y%m%d}.stat'
        ],
        'archive_file_format_list': [
             'ccpa_accum24hr/{time?fmt=%H}Z/gfs/gfs_{date?fmt=%Y%m%d}.stat'
        ],
        'time_list': ['000000', '060000', '120000', '180000']
    }
}
check_and_make_directory(metplus_archive_base_dir)
print("\n- Checking METplus archive files in "
      +metplus_archive_base_dir+", getting missing files from Hera")
for metplus_data in list(metplus_data_dict.keys()):
    # Set up information
    metplus_data_info_dict = metplus_data_dict[metplus_data]
    metplus_data_hera_dir = os.path.join(hera_base_user_dir,
                                         metplus_data_info_dict['hera_dir'],
                                         metplus_data)
    metplus_data_hera_file_format_list = (
        metplus_data_info_dict['hera_file_format_list']
    )
    metplus_data_archive_file_format_list = (
        metplus_data_info_dict['archive_file_format_list']
    )
    metplus_data_time_list = metplus_data_info_dict['time_list']
    # Set up directories
    metplus_data_from_hera_working_dir_PDY = os.path.join(
        from_hera_working_dir_PDY, 'metplus_data', metplus_data
    )
    check_and_make_directory(metplus_data_from_hera_working_dir_PDY)
    metplus_data_archive_dir = os.path.join(
        metplus_archive_base_dir, metplus_data
    )
    check_and_make_directory(metplus_data_archive_dir)
    # Get files
    print("-- Checking METplus "+metplus_data+" archive files")
    for PDYm in list(PDYm_dict.keys()):
        for time in metplus_data_time_list:
            PDYm_date_time = PDYm_dict[PDYm]+time
            for metplus_data_archive_file_format \
                    in metplus_data_archive_file_format_list:
                idx = metplus_data_archive_file_format_list.index(
                    metplus_data_archive_file_format
                )
                # Archive file information
                metplus_data_archive_file_name = format_filler(
                    metplus_data_archive_file_format, PDYm_date_time
                )
                metplus_data_archive_file = os.path.join(
                    metplus_data_archive_dir, metplus_data_archive_file_name
                )
                if (metplus_data == 'precip' and PDYm == 'PDYm1'):
                    # Skip files for precip PDYm1, latest verification
                    # is PDYm2
                    continue
                print("--- Checking for file: "+metplus_data_archive_file)
                if not os.path.exists(metplus_data_archive_file):
                    print("---- "+metplus_data_archive_file+" "
                          +"does not exist, retrieving file from Hera.")
                    metplus_data_archive_file_dir = (
                        metplus_data_archive_file.rpartition('/')[0]
                    )
                    check_and_make_directory(metplus_data_archive_file_dir)
                    # Hera file information
                    metplus_data_hera_file_format = (
                        metplus_data_hera_file_format_list[idx]
                    )
                    metplus_data_hera_file_name = format_filler(
                        metplus_data_hera_file_format, PDYm_date_time
                    )
                    metplus_data_hera_file = os.path.join(
                        metplus_data_hera_dir, metplus_data_hera_file_name
                    )
                    # Working file information
                    metplus_data_working_file = os.path.join(
                        metplus_data_from_hera_working_dir_PDY,
                        metplus_data_archive_file_name
                    )
                    metplus_data_working_file_dir = (
                        metplus_data_working_file.rpartition('/')[0]
                    )
                    check_and_make_directory(metplus_data_working_file_dir)
                    # Get file
                    RSYNC_cmd = subprocess.run(
                        [RSYNC,
                         '-ahr', '-P',
                         hera_user+'@'+hera_client+':'
                         +metplus_data_hera_file,
                         metplus_data_working_file]
                    )
                    if RSYNC_cmd.returncode == 0:
                        CP_cmd = subprocess.run(
                            [CP,
                             metplus_data_working_file,
                             metplus_data_archive_file]
                        )
                        if CP_cmd.returncode != 0:
                            print("***ERROR*** Could not cp "
                                  +metplus_data_working_file+" to "
                                  +metplus_data_archive_file)
                        else:
                            # Change permissions
                            change_permissions(metplus_data_archive_file)
                    else:
                        print("***ERROR*** Could not rsync "
                              +metplus_data_hera_file)
                else:
                    print("---- "+metplus_data_archive_file+" exists")

##### 3. Copy model archive files from Hera
check_and_make_directory(
    os.path.join(from_hera_working_dir_PDY, 'model_data')
)
# Model archive information dictionary
model_data_dict = {
    'gfs': {
        'hera_dir': 'archive',
        'hera_file_format_list': [
            'pgbanl.gfs.{date?fmt=%Y%m%d}{time?fmt=%H}',
            'pgbf00.gfs.{date?fmt=%Y%m%d}{time?fmt=%H}' 
        ],
        'archive_file_format_list': [
            'pgbanl.gfs.{date?fmt=%Y%m%d}{time?fmt=%H}',
            'pgbf00.gfs.{date?fmt=%Y%m%d}{time?fmt=%H}'
        ],
        'time_list': ['000000', '060000', '120000', '180000']
    },

}
check_and_make_directory(model_archive_base_dir)
print("\n- Checking model archive files in "
      +model_archive_base_dir+", getting missing files from Hera")
for model_data in list(model_data_dict.keys()):
    # Set up information
    model_data_info_dict = model_data_dict[model_data]
    model_data_hera_dir = os.path.join(hera_base_user_dir,
                                         model_data_info_dict['hera_dir'],
                                         model_data)
    model_data_hera_file_format_list = (
        model_data_info_dict['hera_file_format_list']
    )
    model_data_archive_file_format_list = (
        model_data_info_dict['archive_file_format_list']
    )
    model_data_time_list = model_data_info_dict['time_list']
    # Set up directories
    model_data_from_hera_working_dir_PDY = os.path.join(
        from_hera_working_dir_PDY, 'model_data', model_data
    )
    check_and_make_directory(model_data_from_hera_working_dir_PDY)
    model_data_archive_dir = os.path.join(
        model_data_archive_base_dir, model_data
    )
    check_and_make_directory(model_data_archive_dir)
    # Get files
    print("-- Checking "+model_data+" archive files")
    for PDYm in list(PDYm_dict.keys()):
        for time in model_data_time_list:
            PDYm_date_time = PDYm_dict[PDYm]+time
            for model_data_archive_file_format \
                    in model_data_archive_file_format_list:
                idx = model_data_archive_file_format_list.index(
                    model_data_archive_file_format
                )
                # Archive file information
                model_data_archive_file_name = format_filler(
                    model_data_archive_file_format, PDYm_date_time
                )
                model_data_archive_file = os.path.join(
                    model_data_archive_dir, model_data_archive_file_name
                )
                print("--- Checking for file: "+model_data_archive_file)
                if not os.path.exists(model_data_archive_file):
                    print("---- "+model_data_archive_file+" does not exist, "
                          +"retrieving file from Hera.")
                    model_data_archive_file_dir = (
                        model_data_archive_file.rpartition('/')[0]
                    )
                    check_and_make_directory(model_data_archive_file_dir)
                    # Hera file information
                    model_data_hera_file_format = (
                       model_data_hera_file_format_list[idx]
                    )
                    model_data_hera_file_name = format_filler(
                        model_data_hera_file_format, PDYm_date_time
                    )
                    model_data_hera_file = os.path.join(
                        model_data_hera_dir, model_data_hera_file_name
                    )
                    # Working file information
                    model_data_working_file = os.path.join(
                        model_data_from_hera_working_dir_PDY,
                        model_data_archive_file_name
                    )
                    model_data_working_file_dir = (
                        model_data_working_file.rpartition('/')[0]
                    )
                    check_and_make_directory(model_data_working_file_dir)
                    # Get file
                    RSYNC_cmd = subprocess.run(
                        [RSYNC,
                         '-ahr', '-P',
                         hera_user+'@'+hera_client+':'
                         +model_data_hera_file,
                         model_data_working_file]
                    )
                    if RSYNC_cmd.returncode == 0:
                        CP_cmd = subprocess.run(
                            [CP,
                             model_data_working_file,
                             model_data_archive_file]
                        )
                        if CP_cmd.returncode != 0:
                            print("***ERROR*** Could not cp "
                                  +model_data_working_file+" to "
                                  +model_data_archive_file)
                        else:
                            # Change permissions
                            change_permissions(model_data_archive_file)
                    else:
                        print("***ERROR*** Could not rsync "+model_data_hera_file)
                else:
                    print("---- "+model_data_archive_file+" exists")
##### 4. Copy HWRF track archive
#hwrf_trak_archive_subdir_list = ['aid', 'aid_nws', 'btk']
#hwrf_trak_hera_base_dir = os.path.join(hera_base_user_dir, 'trak', 'abdeck')
#check_and_make_directory(hwrf_trak_archive_base_dir)
#print("\n- Checking hurricane track archive files in "
#      +hwrf_trak_archive_base_dir+", getting missing files from Hera")
#for hwrf_trak_archive_subdir in hwrf_trak_archive_subdir_list:
#    hwrf_trak_hera_archive_dir = os.path.join(hwrf_trak_hera_base_dir,
#                                              hwrf_trak_archive_subdir)
#    hwrf_trak_archive_dir = os.path.join(hwrf_trak_archive_base_dir,
#                                         hwrf_trak_archive_subdir)
#    # Sync directories
#    RSYNC_cmd = subprocess.run(
#        [RSYNC,
#         '-ahr', '-P',
#         hera_user+'@'+hera_client+':'
#         +hwrf_trak_hera_archive_dir+'/',
#         hwrf_trak_archive_dir+'/.']
#    )
#    if RSYNC_cmd.returncode != 0:
#        print("***ERROR*** Could not rsync "+hwrf_trak_hera_archive_dir)
#    else:
#        # Change permissions
#        change_permissions(hwrf_trak_archive_dir+'/*')

print("\nEND: "+sys.argv[0]+" at "+str(datetime.datetime.today()))
