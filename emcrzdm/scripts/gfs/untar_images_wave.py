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
elif arg_envir == 'dev':
    tar_file_wildcard = os.path.join(
        dev_tar_files_dir, f"wave.{arg_date}",
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
    if arg_envir not in ['prod', 'dev']:
        os.remove(tar_file)
