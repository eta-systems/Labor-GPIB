# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 10:51:30 2019

@author: simon
"""

import time
import interface.prologix_gpib as prologix
import interface.debug_gpib as dummybus

import devices.rohde_schwarz_ngmo2 as ngmo2

import numpy as np
import matplotlib.pyplot as plt

#%%
# iface = prologix.usb(com='ASRL31::INSTR', baudrate=19200, timeout=5000)
#iface.loc()  # local mode
iface = dummybus.usb()
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

srce.voltage(SOURCE_CONST_VOLT)
srce.current(1.5)
srce.sense('current')
#srce.interval(1.00E-4)
#srce.set_averaging_samples(10)

load.voltage(0.0)
load.current(LOAD_CURRENT_MIN)
load.sense('current')
#srce.interval(1.00E-4)
#srce.set_averaging_samples(10)

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

#%%
# read source voltage
iface.write(7, ':SENS:A:FUNC VOLT')
iface.write(7, ':MEAS:A?')
time.sleep(.01)
r = iface.read_until_char(7, '10')
print(r)

r = srce.read_voltage()
print(r)


#%%
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








