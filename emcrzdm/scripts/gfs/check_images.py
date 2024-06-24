import os
import glob
import datetime
import time
import sys

gfs_base_dir = '/home/people/emc/www/htdocs/users/verification/global/gfs'

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

# Set directory to check
gfs_envir_dir = os.path.join(gfs_base_dir, arg_envir)
if os.path.exists(gfs_envir_dir):
    print(f"Checking images in {gfs_envir_dir}")
else:
    print(f"ERROR: {gfs_envir_dir} does not exists, exit")
    sys.exit(1)

# Set date to check
check_date_dt = datetime.datetime.strptime(
    arg_date, '%Y%m%d'
)
print(f"Checking for date {arg_date}")

# Check images
#### atmos
atmos_tar_files_dir = os.path.join(
    gfs_envir_dir,
    'atmos', 'tar_files'
)
if len(os.listdir(atmos_tar_files_dir)) != 0:
    print(f"{atmos_tar_files_dir} not empty")
atmos_check_images_dir_list = []
atmos_grid2grid_images_dir = os.path.join(
    gfs_envir_dir,
    'atmos', 'grid2grid', 'images'
)
atmos_check_images_dir_list.append(atmos_grid2grid_images_dir)
atmos_grid2obs_images_dir = os.path.join(
    gfs_envir_dir,
    'atmos', 'grid2obs', 'images'
)
atmos_check_images_dir_list.append(atmos_grid2obs_images_dir)
if arg_envir != 'expr':
    for g2o_subdir in os.listdir(os.path.join(gfs_envir_dir, 'atmos', 'grid2obs')):
        if os.path.exists(os.path.join(gfs_envir_dir, 'atmos', 'grid2obs',
                                       g2o_subdir, 'images')):
            atmos_check_images_dir_list.append(
                os.path.join(gfs_envir_dir, 'atmos', 'grid2obs',
                             g2o_subdir, 'images')
            )
for atmos_check_images_dir in atmos_check_images_dir_list:
    for img in glob.glob(atmos_check_images_dir+'/*'):
        img_mtime_dt = datetime.datetime.strptime(
            time.ctime(os.path.getmtime(img)),
            '%a %b %d %H:%M:%S %Y'
        )
        if (img[-4:]) not in ['.png', '.gif']:
            print(f"{img} not a png or gif")
        if img_mtime_dt < check_date_dt:
            print(f"{img} has date of {img_mtime_dt:%b %d %Y}")
    atmos_check_images_dir_count = len(glob.glob(atmos_check_images_dir+'/*'))
    print(f"{atmos_check_images_dir} Count: {atmos_check_images_dir_count}")
