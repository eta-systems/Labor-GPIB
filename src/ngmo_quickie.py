# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 10:51:30 2019

@author: simon
"""

import time
import interface.prologix_gpib as prologix

import devices.rohde_schwarz_ngmo2 as ngmo2

import numpy as np
import matplotlib.pyplot as plt

#%%
iface = prologix.usb(com='ASRL31::INSTR', baudrate=19200, timeout=5000)
iface.loc()  # local mode
ngmo = ngmo2.device(iface, 7)

ngmo.clear()
time.sleep(.100)

print(ngmo.get_idn())
time.sleep(.100)

ngmo.display.enable(True)  # high speed mode
ngmo.format.data('ASCII')

srce = ngmo.output('A')
load = ngmo.output('B')

# INIT

SOURCE_CONST_VOLT = 13.0
LOAD_CURRENT_MAX = 0.1
LOAD_CURRENT_MIN = 1.0
DELTA_LOAD_CURRENT = LOAD_CURRENT_MAX - LOAD_CURRENT_MIN
DPOINTS = 100

iface.write(7, ':SOUR:A:VOLT ' + str(SOURCE_CONST_VOLT))         # 13V input into DCDC
iface.write(7, ':SOUR:A:CURR:LIM 1.5')      # current limmit = 1.5A
iface.write(7, ':SENS:A:FUNC CURR')         # measurement mode = current
iface.write(7, ':SENS:A:MEAS:INT 1.00E-4')  # measurement interval = 2ms
iface.write(7, ':SENS:A:MEAS:AVER:COUN 10')  # averaging uses 1 sample

iface.write(7, ':SOUR:B:VOLT 0.0')          # 0V output of DCDC
iface.write(7, ':SOUR:B:CURR:LIM ' + str(LOAD_CURRENT_MIN))      # current limmit = 0.1A
iface.write(7, ':SENS:B:FUNC CURR')         # measurement mode = current
iface.write(7, ':SENS:B:MEAS:INT 1.00E-4')  # measurement interval = 2ms
iface.write(7, ':SENS:B:MEAS:AVER:COUN 10')  # averaging uses 1 sample

val = {}
val['source'] = {}
val['source']['voltage'] = np.ones(DPOINTS)*SOURCE_CONST_VOLT
val['source']['current'] = np.zeros(DPOINTS)
val['source']['power'] = np.zeros(DPOINTS)
val['load'] = {}
val['load']['voltage'] = np.zeros(DPOINTS)
val['load']['current'] = np.zeros(DPOINTS)
val['load']['power'] = np.zeros(DPOINTS)

srce.on()
load.on()

   
iface.write(7, ':SENS:A:FUNC CURR')
iface.write(7, ':MEAS:A?')
time.sleep(.1)
r = iface.read_until_char(7, '10')
print(r)


# read source voltage
iface.write(7, ':SENS:A:FUNC VOLT')
iface.write(7, ':MEAS:A?')
time.sleep(.01)
r = iface.read_until_char(7, '10')
print(r)

time.sleep(1)
# read source voltage
iface.write(7, ':SENS:B:FUNC VOLT')
iface.write(7, ':MEAS:B?')
time.sleep(.01)
r = iface.read_until_char(7, '10')
print(r)


time.sleep(1)
srce.off()
load.off()








