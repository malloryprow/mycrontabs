import os
import glob
import datetime
import shutil
import sys

verif_base_dir = '/home/people/emc/www/htdocs/users/verification'

def usage():
    """! How to call this script.
    """
    filename = os.path.basename(__file__)
    print ("Usage: "+filename+" arg1 arg2\n"
           +"-h|--help               Display this usage statement\n"
           +"Arguments:\n"
           +"   --date=PDY              optional, "
           +"date (format YYYYmmdd) to run for, "
           +"default: today\n"
           +"   --envir=ENVIR           required, "
           +"webpage environment")

# Print usage statement
help_args = ('-h', '--help')
for help_arg in help_args:
    if help_arg in sys.argv:
        usage()
        sys.exit(0)

# Check number of command line arguments
if len(sys.argv[1:]) > 2:
    print("ERROR: Too many agruments")
    usage()
    sys.exit(1)

# Read agruments
have_envir = False
have_date = False
for arg in sys.argv[1:]:
    if '--envir' in arg:
        have_envir = True
        arg_envir = arg.replace('--envir=', '')
    elif '--date' in arg:
        have_date = True
        arg_date = arg.replace('--date=', '')
if not have_envir:
    print("ERROR: No envir provided, exit")
    sys.exit(1)
if have_date:
    if len(arg_date) != 8:
        print("ERROR: argument date must be in YYYYmmdd, exit")
        sys.exit(1)
else:
    print("WARNING: No date provided, using today")
    arg_date =  f"{datetime.date.today():%Y%m%d}"

# Set directory
precip_spatial_map_envir_dir = os.path.join(
    verif_base_dir, 'precip', arg_envir, 'spatial_maps'
)
if os.path.exists(precip_spatial_map_envir_dir):
    print(f"Gathering images to {precip_spatial_map_envir_dir}")
else:
    print(f"ERROR: {precip_spatial_map_envir_dir} does not exists, exit")
    sys.exit(1)

# Set dates
arg_date_dt = datetime.datetime.strptime(
    arg_date, '%Y%m%d'
)
gather_date_list = [arg_date]
for mN in range(1,6,1):
    gather_date_list.append(
        f"{arg_date_dt - datetime.timedelta(days=mN):%Y%m%d}"
    )
print(f"Gathering maps for {', '.join(gather_date_list)}")

# Set paths of components' precip spatial maps
if arg_envir == 'para':
    cam_envir = 'dev'
else:
    cam_envir = arg_envir
precip_spatial_map_dir_dict = {
    'global_det': os.path.join(verif_base_dir, 'global', 'gfs', arg_envir,
                               'atmos', 'grid2grid', 'images'),
    'global_ens': os.path.join(verif_base_dir, 'global', 'gefs', arg_envir,
                               'atmos', 'grid2grid', 'images'),
    'sref': os.path.join(verif_base_dir, 'regional', 'sref', arg_envir,
                         'images', 'spatial'),
    'mesoscale': os.path.join(verif_base_dir, 'regional', 'mesoscale', arg_envir,
                              'grid2grid', 'precip_maps', 'images'),
    'cam': os.path.join(verif_base_dir, 'regional', 'cam', cam_envir,
                        'det', 'grid2grid', 'images'),
    'cam_href': os.path.join(verif_base_dir, 'regional', 'cam', cam_envir,
                             'ens', 'images', 'spatial'),
    }
# Copy files
for PDYm in gather_date_list:
    print(f"---> Getting precip maps for {PDYm}")
    precip_spatial_map_PDYm_dir = os.path.join(
        precip_spatial_map_envir_dir,
        PDYm[0:4], PDYm
    )
    if not os.path.exists(precip_spatial_map_PDYm_dir):
        print(f"Making {precip_spatial_map_PDYm_dir}")
        os.makedirs(precip_spatial_map_PDYm_dir)
    precip_spatial_map_PDYm_gif_list = []
    for component in list(precip_spatial_map_dir_dict.keys()):
        if component == 'mesoscale':
            component_precip_spatial_map_PDYm_gif_list =  glob.glob(
                os.path.join(precip_spatial_map_dir_dict[component],
                             PDYm, f"*v{PDYm}12*.gif")
            )
        else:
            component_precip_spatial_map_PDYm_gif_list =  glob.glob(
                os.path.join(precip_spatial_map_dir_dict[component],
                             f"*v{PDYm}12*.gif")
            )
        # Remove QPE from other component but global_det and cam
        # Use global_det CONUS qpe
        if component not in ['global_det', 'cam']:
            for component_precip_spatial_map_PDYm_gif \
                    in component_precip_spatial_map_PDYm_gif_list:
                if 'qpe' in component_precip_spatial_map_PDYm_gif:
                    component_precip_spatial_map_PDYm_gif_list.remove(
                        component_precip_spatial_map_PDYm_gif
                    )
        if component == 'cam':
            for component_precip_spatial_map_PDYm_gif \
                    in component_precip_spatial_map_PDYm_gif_list:
                if 'qpe' in component_precip_spatial_map_PDYm_gif \
                        and 'conus' in component_precip_spatial_map_PDYm_gif:
                    component_precip_spatial_map_PDYm_gif_list.remove(
                        component_precip_spatial_map_PDYm_gif
                    )
        precip_spatial_map_PDYm_gif_list.extend(
            component_precip_spatial_map_PDYm_gif_list
        )
    for precip_spatial_map_PDYm_gif in precip_spatial_map_PDYm_gif_list:
        source_precip_spatial_map_PDYm_gif = precip_spatial_map_PDYm_gif
        dest_precip_spatial_map_PDYm_gif = os.path.join(
            precip_spatial_map_PDYm_dir,
            precip_spatial_map_PDYm_gif.rpartition('/')[2]
        )
        if not os.path.exists(dest_precip_spatial_map_PDYm_gif):
            print(f"Copying {source_precip_spatial_map_PDYm_gif} to "
                  +f"{dest_precip_spatial_map_PDYm_gif}")
            shutil.copy(source_precip_spatial_map_PDYm_gif,
                        dest_precip_spatial_map_PDYm_gif)
            #os.system('mv '+source_precip_spatial_map_PDYm_gif+' '
            #          +precip_spatial_map_PDYm_dir+'/.')
            #os.remove(source_precip_spatial_map_PDYm_gif.replace('.gif', '.png'))
                                                                                                                                                                                                                                                                        rename_images_acc_archive.py                                                                        0000644 0006162 0005714 00000004574 14571407346 015642  0                                                                                                    ustar   mrow                            EnVeGrp                                                                                                                                                                                                                import os
import glob
import sys

old_images_dir = '/home/people/emc/www/htdocs/users/verification/global/gfs/ops/grid2grid_all_models/acc_archive/images/'
gfs_base_dir = '/home/people/emc/www/htdocs/users/verification/global/gfs'

def usage():
    """! How to call this script.
    """
    filename = os.path.basename(__file__)
    print ("Usage: "+filename+" arg1 arg2\n"
           +"-h|--help               Display this usage statement\n"
           +"Arguments:\n"
           +"   --envir=ENVIR           required, "
           +"webpage environment")

# Print usage statement
help_args = ('-h', '--help')
for help_arg in help_args:
    if help_arg in sys.argv:
        usage()
        sys.exit(0)

# Check number of command line arguments
if len(sys.argv[1:]) > 1:
    print("ERROR: Too many agruments")
    usage()
    sys.exit(1)

# Read agruments
have_envir = False
for arg in sys.argv[1:]:
    if '--envir' in arg:
        have_envir = True
        arg_envir = arg.replace('--envir=', '')
if not have_envir:
    print("ERROR: No envir provided, exit")
    sys.exit(1)

# Set directory
new_images_dir = os.path.join(
    gfs_base_dir, arg_envir, 'atmos', 'long_term', 'images'
)
if os.path.exists(new_images_dir):
    print(f"Putting images within {new_images_dir}")
else:
    print(f"ERROR: {new_images_dir} does not exists, exit")
    sys.exit(1)

# Rename images
for old_image in glob.glob(old_images_dir+'/*'):
    old_image_name = old_image.rpartition('/')[2]
    old_stat = old_image_name.split('_')[0]
    old_valid_hour = old_image_name.split('_')[1]
    old_var = old_image_name.split('_')[2]
    old_level = old_image_name.split('_')[3]
    old_fhr = old_image_name.split('_')[4]
    old_region = old_image_name.split('_')[5]
    year_mon = old_image_name.split('_')[6].replace('.png', '')
    new_image_name = 'evs.global_det.'
    new_image_name = new_image_name+old_stat+'.'+old_var+'_'+old_level+'.'+year_mon+'.'
    if old_fhr != 'fhrmean':
        new_image_name = new_image_name+'timeseries_'+old_valid_hour+'_f'+old_fhr.replace('fhr', '').zfill(3)+'.'
    elif old_fhr == 'fhrmean':
        new_image_name = new_image_name+'fhrmean_'+old_valid_hour+'_f240.'
    if old_region == 'G002NHX':
        new_image_name = new_image_name+'g004_nhem.png'
    new_image = os.path.join(new_images_dir, new_image_name.lower())
    print('cp '+old_image+' '+new_image)
    os.system('cp '+old_image+' '+new_image)
                                                                                                                                    rename_verf_precip.py                                                                               0000644 0006162 0005714 00000011057 14565453056 014366  0                                                                                                    ustar   mrow                            EnVeGrp                                                                                                                                                                                                                import os
import glob
import shutil
import datetime

start_date = '20220101'
end_date = '20220101'

verf_precip_img_base_dir = '/home/people/emc/www/htdocs/users/verification/precip/verif/daily'
evs_img_base_dir = '/home/people/emc/www/htdocs/users/verification/precip/verif/daily_para'

start_date_dt = datetime.datetime.strptime(start_date, '%Y%m%d')
end_date_dt = datetime.datetime.strptime(end_date, '%Y%m%d')

date_dt = start_date_dt
while date_dt <= end_date_dt:
    date = date_dt.strftime('%Y%m%d')
    print("Renaming verf_precip images for "+date)
    verf_precip_conus_date_dir = os.path.join(verf_precip_img_base_dir,
                                              date[0:4], date)
    verf_precip_oconus_date_dir = os.path.join(verf_precip_img_base_dir,
                                               date[0:4], f"{date}.oconus")
    evs_date_dir = os.path.join(evs_img_base_dir, date[0:4], date)
    print(f"- verf_precip CONUS image dir: {verf_precip_conus_date_dir}")
    print(f"- verf precip OCONUS image dir: {verf_precip_oconus_date_dir}")
    print(f"- EVS image dir: {evs_date_dir}")
    if not os.path.exists(evs_date_dir):
        print(f"-- Making {evs_date_dir}")
        os.makedirs(evs_date_dir)
    for verf_precip_date_dir in \
            [verf_precip_conus_date_dir, verf_precip_oconus_date_dir]:
        print(f"-- Renaming .gif in {verf_precip_date_dir}")
        for verf_precip_gif \
                in glob.glob(os.path.join(verf_precip_date_dir, '*.gif')):
            verf_precip_gif_name = verf_precip_gif.rpartition('/')[2]
            verf_precip_gif_model = verf_precip_gif_name.split('.')[0]
            if verf_precip_gif_model in ['firewxcs', 'fv3lamda', 'fv3lamdax',
                                         'fv3lam', 'gec00', 'medley', 'ndassoil',
                                         'ndas', 'nssl4arw', 'srfreqm', 'srmean','st4',
                                         'akqpe', 'st4_pr', 'cmorph']:
                continue
            verf_precip_gif_date = verf_precip_gif_name.split('.')[1]
            if 'cmorph' in verf_precip_gif_name or 'akqpe.' in verf_precip_gif_name:
                verf_precip_gif_fhr = '024h'
            else:
                verf_precip_gif_fhr = verf_precip_gif_name.split('.')[2]
            if verf_precip_gif_fhr == '24h':
                verf_precip_gif_fhr = '024h'
            if '.oconus' in verf_precip_date_dir:
                if 'akqpe.' in verf_precip_gif_name:
                    verf_precip_gif_region = 'AK'
                elif 'st4_pr.' in verf_precip_gif_name:
                    verf_precip_gif_region = 'PR'
                elif 'cmorph' in verf_precip_gif_name:
                    verf_precip_gif_region = verf_precip_gif_name.split('.')[2].upper()
                else:
                    verf_precip_gif_region = verf_precip_gif_name.split('.')[3].upper()
            else:
                verf_precip_gif_region = 'CONUS'
            if verf_precip_gif_model == 'cmcglb':
                evs_gif_model = 'cmc'
            elif verf_precip_gif_model == 'cmc':
                evs_gif_model = 'cmc_regionl'
            elif verf_precip_gif_model in ['conusarw', 'akarw', 'hiarw', 'prarw']:
                evs_gif_model = 'hireswarw'
            elif verf_precip_gif_model in ['conusarw2', 'akarw2', 'hiarw2', 'prarw2']:
                evs_gif_model = 'hireswarwmem2'
            elif verf_precip_gif_model == 'conusfv3':
                evs_gif_model = 'hireswfv3'
            elif verf_precip_gif_model in ['conusnest', 'aknest', 'hinest', 'prnest']:
                evs_gif_model = 'namnest'
            elif verf_precip_gif_model == 'hrrrak':
                evs_gif_model = 'hrrr'
            else:
                evs_gif_model = verf_precip_gif_model
            evs_gif_date = verf_precip_gif_date
            evs_gif_fhr = verf_precip_gif_fhr
            if verf_precip_gif_region == 'AK':
                evs_gif_region = 'alaska'
            elif verf_precip_gif_region == 'PR':
                evs_gif_region = 'prico'
            elif verf_precip_gif_region == 'HI':
                evs_gif_region = 'hawaii'
            else:
                evs_gif_region = verf_precip_gif_region.lower()
            evs_gif_name = f"{evs_gif_model}.{evs_gif_date}.{evs_gif_fhr}.{evs_gif_region}.gif"
            evs_gif = os.path.join(evs_date_dir, evs_gif_name)
            if not os.path.exists(evs_gif):
                print(f"Copying {verf_precip_gif} to {evs_gif}")
                shutil.copy2(verf_precip_gif, evs_gif)
            else:
                print(f"{evs_gif} exists")
    date_dt = date_dt + datetime.timedelta(days=1)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 untar_images_atmos_long_term.py                                                                     0000644 0006162 0005714 00000004332 14571406165 016454  0                                                                                                    ustar   mrow                            EnVeGrp                                                                                                                                                                                                                import os
import glob
import datetime
import sys

gfs_base_dir = '/home/people/emc/www/htdocs/users/verification/global/gfs'

def usage():
    """! How to call this script.
    """
    filename = os.path.basename(__file__)
    print ("Usage: "+filename+" arg1 arg2\n"
           +"-h|--help               Display this usage statement\n"
           +"Arguments:\n"
           +"   --date=YYYYmm           optional, "
           +"date (format YYYYmmdd) to run for, "
           +"default: today\n"
           +"   --envir=ENVIR           required, "
           +"webpage environment")

# Print usage statement
help_args = ('-h', '--help')
for help_arg in help_args:
    if help_arg in sys.argv:
        usage()
        sys.exit(0)

# Check number of command line arguments
if len(sys.argv[1:]) > 2:
    print("ERROR: Too many agruments")
    usage()
    sys.exit(1)

# Read agruments
have_envir = False
have_date = False
for arg in sys.argv[1:]:
    if '--envir' in arg:
        have_envir = True
        arg_envir = arg.replace('--envir=', '')
    elif '--date' in arg:
        have_date = True
        arg_date = arg.replace('--date=', '')
if not have_envir:
    print("ERROR: No envir provided, exit")
    sys.exit(1)
if have_date:
    if len(arg_date) != 6:
        print("ERROR: argument date must be in YYYYmm, exit")
        sys.exit(1)
else:
    print("WARNING: No date provided, using today")
    arg_date =  f"{datetime.date.today():%Y%m}"


# Set directory to check
gfs_envir_atmos_dir = os.path.join(gfs_base_dir, arg_envir, 'atmos')
if os.path.exists(gfs_envir_atmos_dir):
    print(f"Putting images within {gfs_envir_atmos_dir}")
else:
    print(f"ERROR: {gfs_envir_atmos_dir} does not exists, exit")
    sys.exit(1)

# Untar tar file
tar_file = os.path.join(gfs_envir_atmos_dir, 'tar_files',
                        f"evs.plots.global_det.atmos.long_term.v{arg_date}.tar")
image_dir = os.path.join(gfs_envir_atmos_dir, 'long_term', 'images')
if not os.path.exists(tar_file):
    print(f"ERROR: {tar_file} does not exist, exit")
    sys.exit(1)
if not os.path.exists(image_dir):
    print("Making {image_dir}")
    os.makedirs(image_dir)
print(f"Untarring {tar_file} to {image_dir}")
os.system('tar -xvf '+tar_file+' -C '+image_dir)
os.remove(tar_file)
                                                                                                                                                                                                                                                                                                      untar_images_atmos.py                                                                               0000644 0006162 0005714 00000011744 14645764501 014416  0                                                                                                    ustar   mrow                            EnVeGrp                                                                                                                                                                                                                import os
import glob
import datetime
import sys

gfs_base_dir = '/home/people/emc/www/htdocs/users/verification/global/gfs'
prod_tar_files_dir = '/common/data/model/com/evs/v1.0/global_det'

def usage():
    """! How to call this script.
    """
    filename = os.path.basename(__file__)
    print ("Usage: "+filename+" arg1 arg2\n"
           +"-h|--help               Display this usage statement\n"
           +"Arguments:\n"
           +"   --date=PDY              optional, "
           +"date (format YYYYmmdd) to run for, "
           +"default: today\n"
           +"   --envir=ENVIR           required, "
           +"webpage environment")

# Print usage statement
help_args = ('-h', '--help')
for help_arg in help_args:
    if help_arg in sys.argv:
        usage()
        sys.exit(0)

# Check number of command line arguments
if len(sys.argv[1:]) > 2:
    print("ERROR: Too many agruments")
    usage()
    sys.exit(1)

# Read agruments
have_envir = False
have_date = False
for arg in sys.argv[1:]:
    if '--envir' in arg:
        have_envir = True
        arg_envir = arg.replace('--envir=', '')
    elif '--date' in arg:
        have_date = True
        arg_date = arg.replace('--date=', '')
if not have_envir:
    print("ERROR: No envir provided, exit")
    sys.exit(1)
if have_date:
    if len(arg_date) != 8:
        print("ERROR: argument date must be in YYYYmmdd, exit")
        sys.exit(1)
else:
    print("WARNING: No date provided, using today")
    arg_date =  f"{datetime.date.today():%Y%m%d}"


# Set directory
gfs_envir_atmos_dir = os.path.join(gfs_base_dir, arg_envir, 'atmos')
if os.path.exists(gfs_envir_atmos_dir):
    print(f"Putting images within {gfs_envir_atmos_dir}")
else:
    print(f"ERROR: {gfs_envir_atmos_dir} does not exists, exit")
    sys.exit(1)

# Get tar files
if arg_envir == 'prod':
    big_tar_file_wildcard = os.path.join(
        prod_tar_files_dir, f"atmos.{arg_date}",
        f"evs.plots.global_det.atmos.*.v{arg_date}.tar"
    )
else:
    big_tar_file_wildcard = os.path.join(
        gfs_envir_atmos_dir, 'tar_files',
        f"evs.plots.global_det.atmos.*.v{arg_date}.tar"
    )
big_tar_file_list = glob.glob(big_tar_file_wildcard)
if len(big_tar_file_list) == 0:
    print(f"ERROR: No big tar files matching {big_tar_file_wildcard}, exit")
    sys.exit(1)

# Untar files
for big_tar_file in big_tar_file_list:
    print(f"Untarring big tar file {big_tar_file} to {os.path.join(gfs_envir_atmos_dir, 'tar_files')}")
    os.system('tar -xvf '+big_tar_file+' -C '+os.path.join(gfs_envir_atmos_dir, 'tar_files'))
    big_tar_file_verif_case_type = big_tar_file.rpartition('/')[2].split('.')[4]
    small_tar_file_wildcard = os.path.join(
        gfs_envir_atmos_dir, 'tar_files', big_tar_file_verif_case_type+'*.tar'
    )
    small_tar_file_list = glob.glob(small_tar_file_wildcard)
    if len(small_tar_file_list) == 0:
        print(f"WARNING: No small tar files matching {small_tar_file_wildcard}")
        continue
    for small_tar_file in small_tar_file_list:
        if big_tar_file_verif_case_type == 'grid2obs_sfc' \
                and arg_envir in ['prod', 'para', 'dev']:
            if 'cape_l0' in small_tar_file or 'cape_l90' in small_tar_file:
                image_subdir = 'cape'
            elif 'hgt_ceiling' in small_tar_file:
                image_subdir = 'ceiling'
            elif 'dpt_z2' in small_tar_file:
                image_subdir = 'dpt_2m'
            elif 'vis_z0' in small_tar_file:
                image_subdir = 'vis'
            elif 'tmp_anom_dailyavg_z2' in small_tar_file:
                image_subdir = 'tmp_anom_2m'
            elif 'hpbl_l0' in small_tar_file:
                image_subdir = 'pbl_hgt'
            elif 'rh_z2' in small_tar_file:
                image_subdir = 'rh_2m'
            elif 'prmsl_z0' in small_tar_file:
                image_subdir = 'prmsl'
            elif 'tmp_z2' in small_tar_file:
                image_subdir = 'tmp_2m'
            elif 'tcdc_total' in small_tar_file:
                image_subdir = 'tot_cld_cover'
            elif 'ugrd_vgrd_z10' in small_tar_file:
                image_subdir = 'ugrd_vgrd_10m'
            elif 'ugrd_z10' in small_tar_file:
                image_subdir = 'ugrd_10m'
            elif 'vgrd_z10' in small_tar_file:
                image_subdir = 'vgrd_10m'
            elif 'gust_z0' in small_tar_file:
                image_subdir = 'gust'
            image_dir = os.path.join(
                gfs_envir_atmos_dir, big_tar_file_verif_case_type.split('_')[0],
                image_subdir, 'images'
            )
        else:
            image_dir = os.path.join(
                gfs_envir_atmos_dir, big_tar_file_verif_case_type.split('_')[0],
                'images'
            )
        if not os.path.exists(image_dir):
            print(f"Making {image_dir}")
            os.makedirs(image_dir)
        print(f"Untarring {small_tar_file} to {image_dir}")
        os.system('tar -xvf '+small_tar_file+' -C '+image_dir)
        os.remove(small_tar_file)
    if arg_envir != 'prod':
        os.remove(big_tar_file)
                            untar_images_headline.py                                                                            0000644 0006162 0005714 00000004762 14565657660 015056  0                                                                                                    ustar   mrow                            EnVeGrp                                                                                                                                                                                                                import os
import glob
import datetime
import sys

gfs_base_dir = '/home/people/emc/www/htdocs/users/verification/global/gfs'
prod_tar_files_dir = '/common/data/model/com/evs/v1.0/global_det'

def usage():
    """! How to call this script.
    """
    filename = os.path.basename(__file__)
    print ("Usage: "+filename+" arg1 arg2\n"
           +"-h|--help               Display this usage statement\n"
           +"Arguments:\n"
           +"   --date=PDY              optional, "
           +"date (format YYYYmmdd) to run for, "
           +"default: today\n"
           +"   --envir=ENVIR           required, "
           +"webpage environment")

# Print usage statement
help_args = ('-h', '--help')
for help_arg in help_args:
    if help_arg in sys.argv:
        usage()
        sys.exit(0)

# Check number of command line arguments
if len(sys.argv[1:]) > 2:
    print("ERROR: Too many agruments")
    usage()
    sys.exit(1)

# Read agruments
have_envir = False
have_date = False
for arg in sys.argv[1:]:
    if '--envir' in arg:
        have_envir = True
        arg_envir = arg.replace('--envir=', '')
    elif '--date' in arg:
        have_date = True
        arg_date = arg.replace('--date=', '')
if not have_envir:
    print("ERROR: No envir provided, exit")
    sys.exit(1)
if have_date:
    if len(arg_date) != 8:
        print("ERROR: argument date must be in YYYYmmdd, exit")
        sys.exit(1)
else:
    print("WARNING: No date provided, using today")
    arg_date =  f"{datetime.date.today():%Y%m%d}"

# Set directory
gfs_envir_atmos_dir = os.path.join(gfs_base_dir, arg_envir, 'atmos')
if os.path.exists(gfs_envir_atmos_dir):
    print(f"Putting images within {gfs_envir_atmos_dir}")
else:
    print(f"ERROR: {gfs_envir_atmos_dir} does not exists, exit")
    sys.exit(1)

# Untar tar file
if arg_envir == 'prod':
    tar_file = os.path.join(prod_tar_files_dir, f"headline.{arg_date}",
                            f"evs.plots.global_det.atmos.headline.v{arg_date}.tar")
else:
    tar_file = os.path.join(gfs_envir_atmos_dir, 'tar_files',
                            f"evs.plots.global_det.atmos.headline.v{arg_date}.tar")
image_dir = os.path.join(gfs_envir_atmos_dir, 'headline', 'images')
if not os.path.exists(tar_file):
    print(f"ERROR: {tar_file} does not exist, exit")
    sys.exit(1)
if not os.path.exists(image_dir):
    print("Making {image_dir}")
    os.makedirs(image_dir)
print(f"Untarring {tar_file} to {image_dir}")
os.system('tar -xvf '+tar_file+' -C '+image_dir)
if arg_envir != 'prod':
    os.remove(tar_file)
              untar_images_wave.py                                                                                0000644 0006162 0005714 00000005206 14565657125 014235  0                                                                                                    ustar   mrow                            EnVeGrp                                                                                                                                                                                                                import os
import glob
import datetime
import sys

gfs_base_dir = '/home/people/emc/www/htdocs/users/verification/global/gfs'
prod_tar_files_dir = '/common/data/model/com/evs/v1.0/global_det'

def usage():
    """! How to call this script.
    """
    filename = os.path.basename(__file__)
    print ("Usage: "+filename+" arg1 arg2\n"
           +"-h|--help               Display this usage statement\n"
           +"Arguments:\n"
           +"   --date=PDY              optional, "
           +"date (format YYYYmmdd) to run for, "
           +"default: today\n"
           +"   --envir=ENVIR           required, "
           +"webpage environment")

# Print usage statement
help_args = ('-h', '--help')
for help_arg in help_args:
    if help_arg in sys.argv:
        usage()
        sys.exit(0)

# Check number of command line arguments
if len(sys.argv[1:]) > 2:
    print("ERROR: Too many agruments")
    usage()
    sys.exit(1)

# Read agruments
have_envir = False
have_date = False
for arg in sys.argv[1:]:
    if '--envir' in arg:
        have_envir = True
        arg_envir = arg.replace('--envir=', '')
    elif '--date' in arg:
        have_date = True
        arg_date = arg.replace('--date=', '')
if not have_envir:
    print("ERROR: No envir provided, exit")
    sys.exit(1)
if have_date:
    if len(arg_date) != 8:
        print("ERROR: argument date must be in YYYYmmdd, exit")
        sys.exit(1)
else:
    print("WARNING: No date provided, using today")
    arg_date =  f"{datetime.date.today():%Y%m%d}"

# Set directory 
gfs_envir_wave_dir = os.path.join(gfs_base_dir, arg_envir, 'wave')
if os.path.exists(gfs_envir_wave_dir):
    print(f"Putting images within {gfs_envir_wave_dir}")
else:
    print(f"ERROR: {gfs_envir_wave_dir} does not exist, exit")
    sys.exit(1)

# Get tar files
if arg_envir == 'prod':
    tar_file_wildcard = os.path.join(
        prod_tar_files_dir, f"wave.{arg_date}",
        f"evs.plots.global_det.wave.*.v{arg_date}.tar"
    )
else:
    tar_file_wildcard = os.path.join(
        gfs_envir_wave_dir, 'tar_files',
        f"evs.plots.global_det.wave.*.v{arg_date}.tar"
    )
tar_file_list = glob.glob(tar_file_wildcard)
if len(tar_file_list) == 0:
    print(f"ERROR: No tar files matching {tar_file_wildcard}, exit")
    sys.exit(1)

# Untar files
for tar_file in tar_file_list:
    if 'grid2obs' in tar_file:
        image_dir = os.path.join(gfs_envir_wave_dir, 'grid2obs', 'images')
    print(f"Untarring {tar_file} to {image_dir}")
    if not os.path.exists(image_dir):
        print(f"Making {image_dir}")
        os.makedirs(image_dir)
    os.system('tar -xvf '+tar_file+' -C '+image_dir)
    if arg_envir != 'prod':
        os.remove(tar_file)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
