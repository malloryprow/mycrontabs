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
