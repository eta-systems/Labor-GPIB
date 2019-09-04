# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 09:46:34 2019

@author: simon
"""

"""
extract different data values from Network Analyzer

apply math and plot the curve in a double logarithmic scale

"""

#%%

import interface.prologix_gpib as prologix
import devices.hp_3589a as hp3589a

import time
import numpy as np
import matplotlib.pyplot as plt
import utilities.Exporter as Exporter

ADDR_HP = 6

iface = prologix.usb(com='ASRLCOM31::INSTR', baudrate=19200, timeout=5000, log_level=1)
speck = hp3589a.device(iface, ADDR_HP)
print(speck.idn())

#speck.write('*RST')
#time.sleep(10)
tobj = time.localtime()
speck.write('SYST:DATE ' + str(tobj.tm_year) + ',' + str(tobj.tm_mon) + ',' + str(tobj.tm_mday) )
speck.write('SYST:TIME ' + str(tobj.tm_hour) + ',' + str(tobj.tm_min) + ',' + str(tobj.tm_sec) )


speck.write('SENS:FUNC:POWER:NETWORK')
speck.write('SENS:FREQ:STAR 10HZ')
speck.write('SENS:FREQ:STOP 10KHZ')
speck.write('SENS:BAND:RES 36HZ')

# here should be a measurement calibration
# speck.write()

speck.write('REST') # restart sweep

#speck.write('ARM:SOUR MAN')
speck.write('FORM:DATA ASCII')
csv = speck.query('CALC:DATA?')
splt = csv.split(',')
Num_pts = len(splt)
disp_val = np.zeros(Num_pts)
for k in range(Num_pts):
    disp_val[k] = float(splt[k])

csv = speck.query('TRAC:DATA?')
splt = csv.split(',')
Num_pts = len(splt)
raw_val = np.zeros(Num_pts)
for k in range(Num_pts):
    raw_val[k] = float(splt[k])

iface.close()

#%%
# this plots the values as they are stored in the display
# CALC:DATA
# no conversation is needed in order to print them

freq = np.logspace(1, 4, len(disp_val))

plt.figure(figsize=(8,5))
plt.plot(freq, disp_val)
plt.grid()
plt.xlabel('frequency [Hz]')
plt.ylabel('magnitude [dB]')
plt.xscale('log')


#%%
# this plots the raw values as they are stored in the trace
# TRACe:DATA
# the data are tuples of real and imag parts
# combine into complex array
# take abs value of complex and generate dB value with log10

freq = np.logspace(1, 4, len(disp_val))

real = raw_val[::2]
imag = raw_val[1::2]
comp = np.ndarray(len(real), dtype=complex)
for v in range(len(real)):
    comp[v] = complex(real[v], imag[v])
    
magn = np.log10(np.abs(comp))

plt.figure(figsize=(8,5))
plt.plot(freq, magn)
plt.grid()
plt.xlabel('frequency [Hz]')
plt.ylabel('magnitude [dB]')
plt.xscale('log')
#plt.savefig('Network_Analyzer_Capacitor.png', dpi=200)  # 200dpi -> 1600x1000

