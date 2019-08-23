# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 15:00:26 2019

@author: simon
"""

"""

ngmo 2:
    - maximum allowed Voltage: 25V
    - fixed load
    - variable current: 0 - 1A
    
hp 6624A:
    - fixed voltage: 5V



"""



import time
import interface.prologix_gpib as prologix

import devices.hp_6624a as hp6624a
import devices.rohde_schwarz_ngmo2 as ngmo2

import numpy as np
import matplotlib.pyplot as plt
import utilities.Exporter as Exporter

# PARAMETERS
SOURCE_CONST_VOLT = 5.0
CH_SRC = '3'
LOAD_CURRENT_MAX = 1.0
LOAD_CURRENT_MIN = 0.1
DELTA_LOAD_CURRENT = LOAD_CURRENT_MAX - LOAD_CURRENT_MIN
DPOINTS = 100
NGMO_ADDR = 7
PSU_ADDR = 6
DELAY_LOAD_SET = 0.100
DELAY_MEAS_TRIG = 0.005


#%%
iface = prologix.usb(com='ASRL31::INSTR', baudrate=19200, timeout=5000, log_level=0)
iface.loc()  # local mode

psu = hp6624a.device(iface, PSU_ADDR)
psu.clear()

ngmo = ngmo2.device(iface, NGMO_ADDR)
ngmo.clear()
time.sleep(.100)

# ngmo.display.enable(False)  # high speed mode
ngmo.format.data('ASCII')
load = ngmo.output('A')
load.off()
iface.write(NGMO_ADDR, ':SOUR:A:VOLT 0.0')          # 0V output of DCDC
iface.write(NGMO_ADDR, ':SOUR:A:CURR:LIM ' + str(LOAD_CURRENT_MIN))      # current limmit = 0.1A
iface.write(NGMO_ADDR, ':SENS:A:FUNC CURR')         # measurement mode = current
iface.write(NGMO_ADDR, ':SENS:A:MEAS:INT 1.00E-4')  # measurement interval = 2ms
# iface.write(NGMO_ADDR, ':SENS:B:MEAS:AVER:COUN 10')  # averaging uses 1 sample

val = {}
val['source'] = {}
val['source']['v_set'] = np.ones(DPOINTS)*SOURCE_CONST_VOLT
val['source']['voltage'] = np.zeros(DPOINTS)
val['source']['current'] = np.zeros(DPOINTS)
val['load'] = {}
val['load']['voltage'] = np.zeros(DPOINTS)
val['load']['current'] = np.zeros(DPOINTS)

psu.write('VSET ' + CH_SRC + ',5')    # 5V
psu.write('ISET ' + CH_SRC + ',1.1')  # 1.1A
load.on()


#%%
for i in range(0, DPOINTS):
    current = round(DELTA_LOAD_CURRENT/DPOINTS * i, 5)
    iface.write(NGMO_ADDR, ':SOUR:A:CURR:LIM ' + str(abs(current)))
    time.sleep(DELAY_LOAD_SET)
    
    # read source voltage
    r = psu.read_voltage(CH_SRC)
    print(r)
    val['source']['voltage'][i] = float(r)
    
    # read source current
    r = psu.read_current(CH_SRC)
    print(r)
    val['source']['current'][i] = float(r)
    
    # read load voltage
    iface.write(NGMO_ADDR, ':SENS:A:FUNC VOLT')
    iface.write(NGMO_ADDR, ':MEAS:A?')
    time.sleep(DELAY_MEAS_TRIG)
    r = iface.read_until_char(NGMO_ADDR, '10')
    print(r)
    val['load']['voltage'][i] = r
    
    # read load current
    iface.write(NGMO_ADDR, ':SENS:A:FUNC CURR')
    iface.write(NGMO_ADDR, ':MEAS:A?')
    time.sleep(DELAY_MEAS_TRIG)
    r = iface.read_until_char(NGMO_ADDR, '10')
    val['load']['current'][i] = r
    
psu.write('VSET ' + CH_SRC + ',0')
load.off()

val['load']['current'] = val['load']['current'] * (-1) # because sinking yields negative currents


#%%
# Export the raw values for later use
exp = Exporter.Exporter()
exp.dump_to_json_file('values_hp6624a_5V_1A.json', val)

#%% both measured currents
plt.figure(figsize=(8,5))
plt.plot(val['load']['current'])
plt.plot(val['source']['current'])
plt.grid()

#%% difference between measured currents
plt.figure(figsize=(8,5))
deviation = abs(val['load']['current'] - val['source']['current'])
plt.plot(deviation)
imean = np.mean(deviation)*1000
istd = np.std(deviation)*1000
print('I_diff = ' + str(round(imean,1)) + ' +/- ' + str(round(istd,1)) + ' mA')
plt.xlabel(r'datapoint')
plt.ylabel(r'absolute measurement deviation $I_{diff}$ [A]')
plt.title(r'current readback deviation between R&S NGMO2 and HP 6624A')
plt.legend([r'$I_{diff}$ = ' + str(round(imean,1)) + ' $\pm$ ' + str(round(istd,1)) + ' mA'])
plt.grid()
plt.savefig('current_readback_deviation.png', dpi=200)  # 200dpi -> 1600x1000


#%%
plt.figure(figsize=(8,5))
plt.plot(val['load']['voltage'])
plt.grid()

#%%
plt.figure(figsize=(8,5))
plt.plot(val['source']['current'])
plt.grid()

#%%
plt.figure(figsize=(8,5))
plt.plot(val['load']['current'], val['load']['voltage'])
plt.grid()
plt.ylabel(r'Load Voltage $V_{L}$ [V]')
plt.xlabel(r'Load Current $I_{L}$ [A]')

#%%
plt.figure(figsize=(8,5))
plt.plot(val['load']['current'], val['load']['voltage'])
plt.plot(val['source']['current'], val['load']['voltage'])
plt.grid()
plt.ylabel(r'Load Voltage $V_{L}$ [V]')
plt.xlabel(r'Current $I_{L}$ [A]')












