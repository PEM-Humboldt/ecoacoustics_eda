#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 20:12:09 2019

@author: jsulloa
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
from maad import features
from librosa.core import resample

def rms(s):
    return np.sqrt(np.mean(s**2))

fpath = '../platanillo/'
fpath_save = '../data_features/PLG02.csv'
fname_open = 'PLG02.pkl'
fs = 48000

print('Processing file:', fname_open)
pickle_in = open(fpath+fname_open,'rb')
s_dict = pickle.load(pickle_in)
flist = s_dict['flist']

# iterate by day
flist = flist.iloc[0:100,:]
psd = pd.DataFrame()
rms_s = pd.Series()
for idx, row in flist.iterrows():
    print(idx, '/', len(flist), ':', row.fname_audio )
    s = s_dict[row.date]['s']
    # Compute rms
    rms_s = rms_s.append(pd.Series(rms(s)))
    # Compute psd
    aux, fidx = features.psd(s, fs, nperseg=256, method='welch', window='hanning')
    psd = psd.append(aux)

# format dataframes   
rms_s.reset_index(drop=True, inplace=True)
rms_s.name = 'rms'
psd.reset_index(drop=True, inplace=True)
df = pd.concat([flist, psd, rms_s], axis=1)

# save dataframe
df.to_csv(fpath_save)


# plot data

df = pd.read_csv('../data_features/PLG02.csv')
df['date_fmt'] = pd.to_datetime(df.date,  format='%Y-%m-%d %H:%M:%S')
df['period'] = 'night'
df['period'].loc[(df.date_fmt.dt.hour <= 18) & (df.date_fmt.dt.hour >= 8)] = 'transition'
df['period'].loc[(df.date_fmt.dt.hour <= 16) & (df.date_fmt.dt.hour >= 4)] = 'day'
df[['period', 'date_fmt']]
idx_psd = df.columns.str.startswith('psd_')
plt_data = df.iloc[600:800,idx_psd].sample(n=40)

plt.close('all')
for idx, plt_row in plt_data.iterrows():
    if df['period'].loc[idx] == 'night':
        plt.plot(fidx, plt_row, alpha=0.3, color='blue')
    else:
        plt.plot(fidx, plt_row, alpha=0.3, color='red')


plt.close('all')
plt.style.use('ggplot')
plt.figure()
fig, ax = plt.subplots(1,2)
plt_data = df.iloc[600:800,idx_psd].sample(n=200)
plt_data = plt_data.iloc[:,0:125]
fidx = np.arange(0, 125)
for idx, plt_row in plt_data.iterrows():
    if df['period'].loc[idx] == 'night':
        ax[0].plot(fidx, np.log(plt_row), alpha=0.1, color='#9ebcda')
    else:
        pass
plt_data_night = np.mean(np.log(df.loc[df.period=='night',idx_psd]),0)
plt_data_night = plt_data_night.iloc[0:125]
ax[0].plot(fidx, plt_data_night, alpha=1, color='#8856a7')

for idx, plt_row in plt_data.iterrows():
    if df['period'].loc[idx] == 'day':
        ax[1].plot(fidx, np.log(plt_row), alpha=0.1, color='#99d8c9')
    else:
        pass
plt_data_day = np.mean(np.log(df.loc[df.period=='day',idx_psd]),0)
plt_data_day = plt_data_day.iloc[0:125]
ax[1].plot(fidx, plt_data_day, alpha=1, color='#2ca25f')



plt.plot(df.date_fmt, df.rms)
plt.plot(df.rms)


plt.plot(df.date_fmt, df.rms)