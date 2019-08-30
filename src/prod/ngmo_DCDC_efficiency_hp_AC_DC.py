# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 11:37:08 2019

@author: simon

Copyright (c) 2019 eta systems GmbH. All rights reserved.

This Software is distributed WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY 
or FITNESS FOR A PARTICULAR PURPOSE. 
"""

"""
NOT FUNCTIONAL !

Measure the efficiency of a DC/DC converter

Constant input voltage with variable load

Channel A: DC-Source: Constant Voltage: 13.0V
Channel B: DC-Load:   Variable Current: 0.1 - 2.5A

              +---------+
    +---------+DC       +---------------+
    |         |         |---------+     |
(A) |         |         |-------+ |     | (B)      ---> HP3456A (AC ripple)
13V |     +---+       DC+---+   | |     | 0.1-2.5A
    |     |   +---------+   |   | |     |
    _     _                 _  (sense)  _

"""

import time
import interface.prologix_gpib as prologix

import devices.rohde_schwarz_ngmo2 as ngmo2
import devices.hp_3456a as hp3456

import numpy as np
import matplotlib.pyplot as plt
import utilities.Exporter as Exporter

# PARAMETERS
SOURCE_CONST_VOLT = 14.0  # prototype requires 14.0V
LOAD_CURRENT_MAX = 1.0
LOAD_CURRENT_MIN = 0.05
DELTA_LOAD_CURRENT = LOAD_CURRENT_MAX - LOAD_CURRENT_MIN
DPOINTS = 100
DELAY_LOAD_SET = 0.5
DELAY_MEAS_TRIG = 0.005
AVER_REPEATS = 5
NGMO_ADDR = 7
HP34_ADDR = 8

#%%
tic = time.time()
iface = prologix.usb(com='ASRLCOM31::INSTR', baudrate=19200, timeout=5000, log_level=0)
iface.loc()  # local mode
ngmo = ngmo2.device(iface, NGMO_ADDR)
hp34 = hp3456.device(iface, HP34_ADDR)

hp34.clear()
ngmo.clear()
time.sleep(.100)

print(ngmo.get_idn())
time.sleep(.100)

#ngmo.display.enable(False)  # high speed mode
ngmo.format.data('ASCII')

srce = ngmo.output('A')
load = ngmo.output('B')

# INIT
iface.write(NGMO_ADDR, ':SOUR:A:VOLT ' + str(SOURCE_CONST_VOLT))         # 13V input into DCDC
iface.write(NGMO_ADDR, ':SOUR:A:CURR:LIM 1.0')      # current limmit = 1.5A
iface.write(NGMO_ADDR, ':SENS:A:FUNC CURR')         # measurement mode = current
iface.write(NGMO_ADDR, ':SENS:A:MEAS:INT 1.00E-4')  # measurement interval = 2ms
# iface.write(NGMO_ADDR, ':SENS:A:MEAS:AVER:COUN 10')  # averaging uses 1 sample

iface.write(NGMO_ADDR, ':SOUR:B:VOLT 0.0')          # 0V output of DCDC
iface.write(NGMO_ADDR, ':SOUR:B:CURR:LIM ' + str(LOAD_CURRENT_MIN))      # current limmit = 0.1A
iface.write(NGMO_ADDR, ':SENS:B:FUNC CURR')         # measurement mode = current
iface.write(NGMO_ADDR, ':SENS:B:MEAS:INT 1.00E-4')  # measurement interval = 2ms
# iface.write(NGMO_ADDR, ':SENS:B:MEAS:AVER:COUN 10')  # averaging uses 1 sample

val = {}
val['source'] = {}
val['source']['voltage'] = np.ones(DPOINTS)*SOURCE_CONST_VOLT
val['source']['current'] = np.zeros(DPOINTS)
val['source']['power'] = np.zeros(DPOINTS)
val['load'] = {}
val['load']['voltage'] = np.zeros(DPOINTS) # measure with ngmo
val['load']['vdc'] = np.zeros(DPOINTS)     # measure with hp3456
val['load']['vac'] = np.zeros(DPOINTS)     # measure with hp3456
val['load']['current'] = np.zeros(DPOINTS)
val['load']['power'] = np.zeros(DPOINTS)

srce.on()
load.on()

for i in range(0, DPOINTS):
    iface.set_address(NGMO_ADDR)
    current = round(DELTA_LOAD_CURRENT/DPOINTS * i, 5)
    iface.write(NGMO_ADDR, ':SOUR:B:CURR:LIM ' + str(abs(current)))
    time.sleep(DELAY_LOAD_SET)
    print('new voltage set')
    
    # read source voltage
    iface.write(NGMO_ADDR, ':SENS:A:FUNC VOLT')
    iface.write(NGMO_ADDR, ':MEAS:A?')
    time.sleep(DELAY_MEAS_TRIG)
    r = iface.read_until_char(NGMO_ADDR, '10')
    print('Vsrc: ' + str(r))
    val['source']['voltage'][i] = float(r)
    
    # read source current
    iface.write(NGMO_ADDR, ':SENS:A:FUNC CURR')
    iface.write(NGMO_ADDR, ':MEAS:A?')
    time.sleep(DELAY_MEAS_TRIG)
    r = iface.read_until_char(NGMO_ADDR, '10')
    print('Isrc' + str(r))
    val['source']['current'][i] = float(r)
    
    # read load voltage
    iface.write(NGMO_ADDR, ':SENS:B:FUNC VOLT')
    iface.write(NGMO_ADDR, ':MEAS:B?')
    time.sleep(DELAY_MEAS_TRIG)
    r = iface.read_until_char(NGMO_ADDR, '10')
    print('Vload ' + str(r))
    val['load']['voltage'][i] = r
    
    # read load current
    iface.write(NGMO_ADDR, ':SENS:B:FUNC CURR')
    iface.write(NGMO_ADDR, ':MEAS:B?')
    time.sleep(DELAY_MEAS_TRIG)
    r = iface.read_until_char(NGMO_ADDR, '10')
    print('Iload ' + str(r))
    val['load']['current'][i] = r
    
    # read load VDC
    iface.set_address(HP34_ADDR)
    vdc = np.zeros(AVER_REPEATS)
    hp34.measurement('vdc')
    time.sleep(0.05)
    for k in range(0, AVER_REPEATS):
        vdc[k] = hp34.read_voltage()
        time.sleep(DELAY_MEAS_TRIG)
    print('VDC ' + str(vdc))
    val['load']['vdc'][i] = np.average(vdc)
    
    # read load VAC
    vac = np.zeros(AVER_REPEATS)
    hp34.measurement('vac')
    time.sleep(0.05)
    for k in range(0, AVER_REPEATS):
        vac[k] = hp34.read_voltage()
        time.sleep(DELAY_MEAS_TRIG)
    print('VAC ' + str(vac))
    val['load']['vac'][i] = np.average(vac)

    print('PROGRESS: ' + str(i) + '/' + str(DPOINTS))
    
srce.off()
load.off()
iface.close()

toc = time.time()
elapsed = tic - toc
print('Elapsed Time: ' + str(elapsed))
#%%
val['load']['current'] = val['load']['current'] * (-1)
val['source']['power'] = val['source']['voltage'] * val['source']['current']
val['load']['power']   = val['load']['voltage']   * val['load']['current']
val['efficiency']      = val['load']['power']   / val['source']['power']
val['resistance']      = val['load']['voltage']   / val['load']['current']

val['load']['power2']   = val['load']['vdc']   * val['load']['current']
val['efficiency2']      = val['load']['power2']   / val['source']['power']
val['resistance2']      = val['load']['vdc']   / val['load']['current']

#%%
# Export the raw values for later use
exp = Exporter.Exporter()
exp.dump_to_json_file('values_DCDC_ngmo_hp3456_100dp.json', val)

#%%
plt.figure(figsize=(8,5))
plt.plot(val['load']['current'])
plt.grid()


#%%
plt.figure(figsize=(8,5))
plt.plot(val['load']['voltage'])
plt.grid()

#%%
plt.figure(figsize=(8,5))
plt.plot(val['load']['power'])
plt.grid()

#%%
plt.figure(figsize=(8,5))
plt.plot(val['source']['current'])
plt.grid()

#%%
plt.figure(figsize=(8,5))
plt.plot(val['resistance'][1:], val['efficiency'][1:])
plt.xlabel(r'resistance R $[\Omega]$')
plt.ylabel(r'efficiency coefficient $\eta$')
plt.title('Efficiency Coefficient vs. Load')
plt.grid()
#plt.savefig('Efficiency_vs_LoadResistance.pdf')
#plt.savefig('Efficiency_vs_LoadResistance.png', dpi=200)

#%%
plt.figure(figsize=(8,5))
plt.plot(val['load']['current'][2:], val['efficiency'][2:])
plt.plot(val['load']['current'][2:], val['efficiency2'][2:])
plt.ylim(0.55, 0.90)
plt.xlabel(r'load current $I_L$ [A]')
plt.ylabel(r'efficiency coefficient $\eta$')
plt.title('Efficiency vs. Load Current')
plt.legend(['load voltage was measured with R&S NGMO2', 'load voltage was measured with HP 3456A'])
plt.grid()
#plt.savefig('Efficiency_vs_LoadCurrent.pdf')
plt.savefig('Efficiency_vs_LoadCurrent_NGMO2vsHP3456.png', dpi=200)  # 200dpi -> 1600x1000

#%%
plt.figure(figsize=(16,9))
plt.plot(val['load']['current'], val['load']['vdc'])
plt.plot(val['load']['current'], val['load']['voltage'])

#%%
plt.figure(figsize=(16,9))
plt.plot(val['load']['current'][1:], val['load']['vac'][1:])
plt.ylim(0.0, 0.002)



