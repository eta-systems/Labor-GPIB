# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 11:28:06 2019

@author: simon
"""


import time
import interface.prologix_gpib as prologix

import devices.rohde_schwarz_apn62 as apn62

import numpy as np
import matplotlib.pyplot as plt
import utilities.Exporter as Exporter

# PARAMETERS
ADDR_APN = 6

#%%
iface = prologix.usb(com='ASRLCOM31::INSTR', baudrate=19200, timeout=5000, log_level=0)
iface.loc()  # local mode
apn = apn62.device(iface, ADDR_APN)
apn.rst()

# presets for calibrating STUDER 1.914.501-11 boards

# calibrate level to +6dBV on balanced output
# by applying 0dBV unbalanced
def preset_level():
    print('1 kHz / 0 dBV / 600 R')
    apn.write('RSource 600OHM')
    apn.write('FRequency 1KHZ')
    apn.write('LEvel 0DBV')

# calibrate distortion by applying 30Hz 18dBm
def preset_distortion():
    print('30 Hz / 18 dBm / 600 R')
    apn.write('RSource 600OHM')
    apn.write('FRequency 30HZ')
    apn.write('LEvel 18DBM')

#%%
preset_level()

#%%
preset_distortion()

#%%
iface.close()







