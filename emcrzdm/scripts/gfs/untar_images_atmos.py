import os
import glob
import datetime
import sys

gfs_base_dir = '/home/people/emc/www/htdocs/users/verification/global/gfs'
prod_tar_files_dir = '/common/data/model/com/evs/v1.0/global_det'
dev_tar_files_dir = '/home/people/emc/www/htdocs/users/verification/emc.vpppg/dev_tar_files/global_det'

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
elif arg_envir == 'dev':
    big_tar_file_wildcard = os.path.join(
        dev_tar_files_dir, f"atmos.{arg_date}",
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
                and arg_envir in ['prod', 'para', 'dev', 'test']:
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
    if arg_envir not in ['prod', 'dev']:
        os.remove(big_tar_file)
