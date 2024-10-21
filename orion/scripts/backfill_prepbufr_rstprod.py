import os
import sys
import subprocess
import datetime
import shutil

start_date = '20220701'
end_date = '20240815'

##### Orion
orion_base_user_dir = '/work/noaa/rstprod/verif'
##### Hera
hera_base_user_dir = '/scratch1/NCEPDEV/global/Mallory.Row'
hera_client = 'dtn-hera.fairmont.rdhpcs.noaa.gov'
hera_user = 'Mallory.Row'


date_dt = datetime.datetime.strptime(start_date, '%Y%m%d')
end_date_dt = datetime.datetime.strptime(end_date, '%Y%m%d')
while date_dt <= end_date_dt:
    # GDAS
    pb = 'gdas'
    for cyc in ['00', '06', '12', '18']:
        file_name = f"prepbufr.gdas.{date_dt:%Y%m%d}{cyc}"
        hera_file = os.path.join(hera_base_user_dir, 'prepbufr', pb, file_name)
        orion_file = os.path.join(orion_base_user_dir, 'prepbufr', pb, file_name)
        if not os.path.exists(orion_file):
            # Get file
            print(' '.join(['rsync', '-ahr', '-P',hera_user+'@'+hera_client+':'+hera_file, orion_file]))
            RSYNC_cmd = subprocess.run(
                ['rsync', '-ahr', '-P',
                 hera_user+'@'+hera_client+':'
                 +hera_file, orion_file]
            )
            os.system('chmod 650 '+orion_file)
            os.system('chgrp rstprod '+orion_file)
        else:
            print(orion_file+" exists")
    # NAM
    pb = 'nam'
    for cyc in ['00', '06', '12', '18']:
        for tm in ['00', '03']:
            file_name = f"nam.{date_dt:%Y%m%d}/nam.t{cyc}z.prepbufr.tm{tm}"
            hera_file = os.path.join(hera_base_user_dir, 'prepbufr', pb, file_name)
            orion_file = os.path.join(orion_base_user_dir, 'prepbufr', pb, file_name)
            if not os.path.exists(orion_file):
                # Get file
                orion_date_dir = orion_file.rpartition('/')[0]
                if not os.path.exists(orion_date_dir):
                    os.makedirs(orion_date_dir)
                    os.system('chmod 750 '+orion_date_dir)
                    os.system('chgrp rstprod '+orion_date_dir)
                print(' '.join(['rsync', '-ahr', '-P',hera_user+'@'+hera_client+':'+hera_file, orion_file]))
                RSYNC_cmd = subprocess.run(
                    ['rsync', '-ahr', '-P',
                     hera_user+'@'+hera_client+':'
                     +hera_file, orion_file]
                )
                os.system('chmod 650 '+orion_file)
                os.system('chgrp rstprod '+orion_file)
            else:
                print(orion_file+" exists")
    date_dt = date_dt + datetime.timedelta(days=1)
