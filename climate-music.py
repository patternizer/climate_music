#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
# PROGRAM: climate-music.py
#------------------------------------------------------------------------------
# Version 0.1
# 2 November, 2020
# Michael Taylor
# https://patternizer.github.io
# patternizer AT gmail DOT com
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# IMPORT PYTHON LIBRARIES
#------------------------------------------------------------------------------
import numpy as np
import pandas as pd
from mod import Mod
import matplotlib.pyplot as plt; plt.close('all')

from miditime.miditime import MIDITime 
# Use the midi-making midiutil
# https://github.com/duggan/midiutil produced by Mark Conway Wirt 
# http://www.emergentmusics.org/site-information
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# SETTINGS: 
#------------------------------------------------------------------------------

fontsize = 20
load_crutem = True
noctaves = 2 # either side of anomaly=0

#------------------------------------------------------------------------------
# CHOOSE DATASET: 
#------------------------------------------------------------------------------

if load_crutem == True:
    
    datafile = 'crutem4.6.0.0-2019-12.global.txt'
    cru_music = 'crutem4.midi'

#------------------------------------------------------------------------------
# METHODS: 
#------------------------------------------------------------------------------

def nearest_indices(musicmap_array, data_array):

    def find_nearest(musicmap_array, value):
        idx = (np.abs(musicmap_array - value)).argmin()
        return idx
    indices = np.zeros_like(data_array, dtype=musicmap_array.dtype)
    for i in range(len(data_array)):
        indices[i] =  find_nearest(musicmap_array, data_array[i])
    return indices

#------------------------------------------------------------------------------
# LOAD DATASET: 
#------------------------------------------------------------------------------

print('loading_data...')

f = open(datafile)
lines = f.readlines()
dates = []
anom = []
for i in range(len(lines)):
    words = lines[i].split()
    if len(words) > 1:
        date = float(words[0])
        val = (len(words)-1)*[None]
        for j in range(len(val)):
            try: val[j] = float(words[j+1])
            except: pass
        if not None in val:
            if Mod(i,2) == 0:
                dates.append(date)
                anom.append(val) 
f.close()
dates = np.array(dates).astype('int')
anom = np.array(anom)
    
# DATAFRAME:

df = pd.DataFrame(columns=['year','1','2','3','4','5','6','7','8','9','10','11','12'])
df['year'] = dates
for j in range(1,13):
    df[df.columns[j]] = [ anom[i][j-1] for i in range(len(anom)) ]
df['yearly_mean'] = df[df.columns[range(1,13)]].mean(axis=1)
data_array = np.array(df['yearly_mean'])

# Set anomaly=0 as A440 and create 88 piano key map to +/- 2 octaves centered on 0 anomaly:
musicmap_array = np.array(np.linspace(-noctaves, noctaves, 88))

# Map data onto 88 array and align nearest bin values:
indices = nearest_indices(musicmap_array, data_array)
mapped_array = [ musicmap_array[indices[i].astype(int)] for i in range(len(indices)) ]

# Check status of data discretisation

fig,ax = plt.subplots(figsize=(15,10))
plt.step(df.year, data_array, color='red', label='raw data')
plt.step(df.year, mapped_array, color='blue', label='88 bin alignment')
#plt.step(df.year, mapped_array, color='blue', ls='dashed', label='88 bin alignment')
plt.ylim(-noctaves,noctaves)
plt.ylabel('Yearly anomaly', fontsize=fontsize)
plt.title(datafile, fontsize=fontsize)
ax.yaxis.grid(True, which='major')    
ax.tick_params(axis='both', which='major', labelsize=fontsize)     
plt.legend(loc='upper left', fontsize=12)
plt.savefig('data_discretisation.png')

# Histogram of discretised values

fig,ax = plt.subplots(figsize=(15,10))
plt.hist(data_array, color='red', bins=88, label='raw data')    
plt.hist(mapped_array, color='blue', bins=88, label='88 bin alignment') 
plt.xlim(-noctaves,noctaves)
plt.xlabel('Yearly anomaly', fontsize=fontsize)
plt.ylabel('Count', fontsize=fontsize)
plt.title(datafile, fontsize=fontsize)
ax.yaxis.grid(True, which='major')    
ax.tick_params(axis='both', which='major', labelsize=fontsize)     
plt.legend(loc='upper left', fontsize=12)
plt.savefig('data_discretisation_histogram.png')

# Note frequency array (A440 --> n=49)
musicfreq_array = [ 440 * (2**(1/12))**((n+1)-49) for n in range(88) ] 

# Map data values onto frequencies
notefreq_array = [ musicfreq_array[indices[i].astype(int)] for i in range(len(indices)) ]

fig,ax = plt.subplots(figsize=(15,10))
plt.step(df.year, notefreq_array, color='blue', label='values as notes')
plt.axhline(y=1760, color='orange', lw=2, label='A1760')
plt.axhline(y=880, color='red', lw=2, ls='dashed', label='A880')
plt.axhline(y=440, color='red', lw=3, label='A440')
plt.axhline(y=220, color='red', lw=2, ls='dashed', label='A220')
plt.axhline(y=110, color='orange', lw=2, label='A110')
plt.ylabel('Freuqnecy, Hz', fontsize=fontsize)
plt.title(datafile, fontsize=fontsize)
ax.yaxis.grid(True, which='major')   
ax.tick_params(axis='both', which='major', labelsize=fontsize)     
plt.legend(loc='upper left', fontsize=12)
plt.savefig('data_note_frequencies-ylinear.png')

fig,ax = plt.subplots(figsize=(15,10))
plt.step(df.year, notefreq_array, color='blue', label='values as notes')
plt.axhline(y=1760, color='orange', lw=2, label='A1760')
plt.axhline(y=880, color='red', lw=2, ls='dashed', label='A880')
plt.axhline(y=440, color='red', lw=3, label='A440')
plt.axhline(y=220, color='red', lw=2, ls='dashed', label='A220')
plt.axhline(y=110, color='orange', lw=2, label='A110')
plt.ylabel('Freuqnecy, Hz', fontsize=fontsize)
plt.title(datafile, fontsize=fontsize)
ax.yaxis.grid(True, which='major')   
ax.set_yscale('log') 
ax.tick_params(axis='both', which='major', labelsize=fontsize)     
plt.legend(loc='upper left', fontsize=12)
plt.savefig('data_note_frequencies-ylog.png')

# Start MIDI class with tempo 120 beats per minute [bpm]:
    
climate_midi = MIDITime(120, cru_music)

# Create note array [beats, note, velocity, duration]

duration = 1     # 1 beat per datum 
velocity = 127   # 
climate_song = []
for i in range(len(data_array)):
    climate_song.append([i, int(indices[i]), velocity, duration])

# Add track and save .midi file

climate_midi.add_track(climate_song)
climate_midi.save_midi()

#------------------------------------------------------------------------------
# IMPORT .MIDI INTO LINUX LMMS AND PLAY WITH PIANO ROLL & CAPTURE WITH KAZAM
#------------------------------------------------------------------------------
 
#------------------------------------------------------------------------------
print('** END')

