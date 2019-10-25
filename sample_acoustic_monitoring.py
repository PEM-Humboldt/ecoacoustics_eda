#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sample data from acoustic monitoring taking a sample from each file.
The data is organized into a dictionary.

@author: jsulloa
"""

import pandas as pd
import numpy as np
from librosa.core import load
from personal_utilities import search_files
import pickle

## -- Set variables -- ##
path_dir = '/Volumes/TOSHIBA EXT/monitoreo_acustico_putumayo/Archivos_sonido/Venado/'
fname_csv = '../../audio_metadata/data_tables/venado.csv'
date_range = ['2019-01-01 00:00:00','2019-12-01 23:50:00']
t_window = 5 # window of audio per file in seconds
fs = 48000 # homogeneous sampling frequency
# -------------------- #

flist_full = pd.read_csv(fname_csv)
sensor_name_list = flist_full.sensor_name.unique()
for sensor_name in sensor_name_list:

    fname_save = sensor_name + '.pkl'
    
    # load and format flist
    flist_full['date_fmt'] = pd.to_datetime(flist_full.date,  format='%Y-%m-%d %H:%M:%S')
    idx_dates = (flist_full['date_fmt'] > date_range[0]) & (flist_full['date_fmt'] <= date_range[1])
    idx_sensor = (flist_full.sensor_name==sensor_name)
    flist = flist_full.loc[idx_dates & idx_sensor,:]
    flist_days = flist.groupby(flist.date_fmt.dt.dayofyear)
    
    s_dict = dict()
    for idx_global, (day, flist_spectro) in enumerate(flist_days):
        date = flist_spectro.date_fmt.iloc[0].strftime('%y-%m-%d')
        print('Processing date: ', date)
        # list trough each file
        
        # iterate by day    
        for idx, (index, flist_row) in enumerate(flist_spectro.iterrows()):
            fname = flist_row['fname_audio']
            date_str = flist_row['date']
            flist_row['fs'] = fs
            flist_row['t_window'] = t_window
            print('day', idx_global+1,'/',len(flist_days), ': file', idx+1, '/', len(flist_spectro), fname)
            fname_path = search_files(path_dir, fname)
            s, fs = load(fname_path, sr=fs, duration=t_window)
            s_dict[date_str] = {'s' : s,
                               'audio_metadata': flist_row}
        
    # save
    s_dict['flist'] = flist
    pickle_out = open(fname_save, 'wb')
    pickle.dump(s_dict, pickle_out)
    pickle_out.close()  
    s_dict= dict()  