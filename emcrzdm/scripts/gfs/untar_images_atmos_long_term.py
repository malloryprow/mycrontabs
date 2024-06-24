import os
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
