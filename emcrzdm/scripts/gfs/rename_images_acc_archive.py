import os
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
