#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Load data from pickle files and save images of spectrogram
The pipeline includes:
    - A low Butterworth pass filter
    - Spectrogram computation
    - A gaussian smoothing of the spectrogram
    - Nomalization of the spectrogram accoring to vmin, vmax values


@author: jsulloa
"""
import numpy as np
import pickle
from maad import sound
from personal_utilities import listdir_pattern, crossfade_list
from skimage import io
from librosa import output
from personal_utilities import butter_filter
from skimage.filters import gaussian

# settings
fs = 48000
opt_spec = {'wl': 1024, 'ovlp': 0.5, 'fcrop': [10,24000], 'db_range': 250}
fpath = '../data_pkl/platanillo/'
path_save = '../figures/platanillo/fullday_PLG10/'
fmt = '.png'
tlims = [00,24]  # tiempo en horas
write_wav = True

# --

im_dict= dict()
# load elements
flist_dir = listdir_pattern(fpath, ends_with='pkl')
for fname_open in flist_dir:
    print(fname_open)
    pickle_in = open(fpath+fname_open,'rb')
    s_dict = pickle.load(pickle_in)
    flist = s_dict['flist']
    sensor_type = flist.recorder_model.iloc[0]        
    # filter flist
    idx_time = (flist.date_fmt.dt.hour >= tlims[0]) & (flist.date_fmt.dt.hour <= tlims[1])
    flist = flist.loc[idx_time,:]
    flist_days = flist.groupby(flist.date_fmt.dt.dayofyear)
        
    # iterate by day    
    for day, flist_day in flist_days:
        date = flist_day.date_fmt.iloc[0].strftime('%y-%m-%d')
        print('Processing date: ', date)
        # concat audio into array
        s_sum = list()
        for index, row in flist_day.iterrows():
            s = s_dict[row.date]['s']
            s_sum.append(s)
        
        # crossfade and high pass filtering
        s_sum = crossfade_list(s_sum, fs)         
        s_sum = butter_filter(s_sum,cutoff=200, fs=fs, order=2, ftype='high')
        
        # compute spectrogram
        im, dt, df, ext = sound.spectrogram(s_sum, fs, nperseg=opt_spec['wl'],cmap='viridis', 
                                            overlap=opt_spec['ovlp'], fcrop=opt_spec['fcrop'],
                                            rescale=True, db_range=opt_spec['db_range'])
        # Apply gaussian smoothing
        im = gaussian(im, sigma=0.5, mode='reflect')
        
        # Normalize spectrogram according to sensor model         
        vmin, vmax = 0.4, 0.8  # Audiomoth
        im[im<vmin] = vmin
        im[im>vmax] = vmax
        im = (im - im.min())/(im.max() - im.min())
        # save to file
        im = np.flip(im, axis=0)
        key = fname_open[0:-4]+'_'+date
        io.imsave(path_save+key+fmt, im)
        if write_wav:
            output.write_wav(path_save+key+'.wav', s_sum, fs)
        else:
            pass
            

# create montage
fpath = '../figures/platanillo/fullday_PLG10/'
path_save_montage = '../figures/montage_PLG10.png'
flist_dir = listdir_pattern(fpath, ends_with='png')
flist_dir = flist_dir[5:25]  # to remove
im_site = list()
for idx, fname in enumerate(flist_dir):
    im_site.append(io.imread(fpath+fname))

montage_site = np.concatenate(im_site, axis=0)
io.imsave(path_save_montage, montage_site)


