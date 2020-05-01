#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compute features on spectrograms for multiple sites. 
Features include: index of activity and spectral distribution for night and day periods

@author: jsulloa
"""

import numpy as np
import pandas as pd
from skimage import io
from personal_utilities import listdir_pattern

## Set variables
fpath = '../soundscape_selection/'
fpath_save = './data_metrics/metrics_psd_dic.pkl'
bloque_list = ['platanillo','rumiyaco','venado']
subsample_psd_by = 8


# Compute psd and acoustic activity
# -----------
# Batch compute features on all sites
metrics_psd = pd.DataFrame()
for bloque in bloque_list:
    fpath_dir = fpath+bloque+'/'
    flist_dir = listdir_pattern(fpath_dir, ends_with='png')
    for fname in flist_dir:
        print(bloque, '-',fname)
        im = io.imread(fpath_dir+fname)
        im = np.flipud(im)
        # roll image to separate night and day easily
        im = np.roll(im, shift=np.int(im.shape[1]/4),axis=1)
        # devide psd into day and night
        psd_day = np.median(im[0::subsample_psd_by,np.int(im.shape[1]/2):], axis=1)
        psd_night = np.median(im[0::subsample_psd_by,0:np.int(im.shape[1]/2)], axis=1)
        # subsample psd
        psd = np.concatenate([psd_day,psd_night])
        psd = pd.Series(psd)
        # compute index of activity
        #idx_activity = len(np.where(im.ravel()>th)[0])/len(im.ravel())*100
        # format dataframe
        cols=['psd_' + str(idx).zfill(3) for idx in range(1,len(psd)+1)]
        psd.index = cols
        #psd['idx_activity'] = idx_activity
        psd['fname'] = fname
        psd['bloque'] = bloque
        psd['sensor_name'] = fname[0:5]
        metrics_psd = metrics_psd.append(psd, ignore_index=True)


# normalize psd
idx_psd = metrics_psd.columns.str.startswith('psd')
metrics_psd.loc[:,idx_psd] = metrics_psd.loc[:,idx_psd].apply(lambda x: x/metrics_psd.loc[:,idx_psd].max().max(), axis=1)

# make psd_idx based on min max frequencies used to build the spectrograms. Here 0.1 to 10 kHz
cols = ['psd_day_' + str(idx).zfill(3) for idx in range(1,len(psd_day)+1)] + ['psd_ngt_' + str(idx).zfill(3) for idx in range(1,len(psd_night)+1)]
f_idx = pd.Series(np.tile(np.linspace(start=0.01, stop=24, num=len(psd_day)),2),
                  index=cols)

# save data
import pickle
metrics_psd_dic = { 'df': metrics_psd,
                    'frequency_index': f_idx,
                    'description': 'Data frame with normalized psd of sites'}

with open(fpath_save, 'wb') as output:
    pickle.dump(metrics_psd_dic, output, pickle.HIGHEST_PROTOCOL)

