import os
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
