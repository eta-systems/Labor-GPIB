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
Measure the efficiency of a DC/DC converter

Constant input voltage with variable load

Channel A: DC-Source: Constant Voltage: 13.0V
Channel B: DC-Load:   Variable Current: 0.1 - 2.5A

              +---------+
    +---------+DC       +---------------+
    |         |         |---------+     |
(A) |         |         |-------+ |     | (B)      ---> HP3456A (DC)
13V |     +---+       DC+---+   | |     | 0.1-2.5A ---> HP3455A (AC ripple)
    |     |   +---------+   |   | |     |
    _     _                 _  (sense)  _

"""

import time
import interface.prologix_gpib as prologix

import devices.rohde_schwarz_ngmo2 as ngmo2
import devices.hp_3456a as hp3456
import devices.hp_3455a as hp3455

import numpy as np
import matplotlib.pyplot as plt
import utilities.Exporter as Exporter

# PARAMETERS
SOURCE_CONST_VOLT = 14.0  # prototype requires 14.0V
LOAD_CURRENT_MAX = 1.2
LOAD_CURRENT_MIN = 0.05
DELTA_LOAD_CURRENT = LOAD_CURRENT_MAX - LOAD_CURRENT_MIN
DPOINTS = 25
DELAY_LOAD_SET = 0.6
DELAY_MEAS_TRIG = 0.005
NGMO_ADDR = 7
HP3456_ADDR = 8
HP3455_ADDR = 12

time_ms = lambda: int(round(time.time() * 1000))
tim = time_ms()
def tic():
    global tim
    tim = time_ms()
def toc():
    global tim
    elapsed = time_ms() - tim
    print('Elapsed time: ' + str(elapsed) + ' ms')
    tim = time_ms()
tic()
toc()

#%%
#tic = time.time()
iface = prologix.usb(com='ASRLCOM31::INSTR', baudrate=19200, timeout=5000, log_level=0)
iface.loc()  # local mode
ngmo = ngmo2.device(iface, NGMO_ADDR)
meter_dc = hp3456.device(iface, HP3456_ADDR)
meter_ac = hp3455.device(iface, HP3455_ADDR)

meter_dc.clear()
meter_dc.measurement('vdc')
meter_dc.trigger_mode('internal')

meter_ac.clear()
meter_ac.measurement('fast ac')

ngmo.clear()
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

t_start = time_ms()
for i in range(0, DPOINTS):
    iface.set_address(NGMO_ADDR)
    current = round(DELTA_LOAD_CURRENT/DPOINTS * i, 5)
    iface.write(NGMO_ADDR, ':SOUR:B:CURR:LIM ' + str(abs(current)))
    time.sleep(DELAY_LOAD_SET)
    
    # read source voltage
    iface.write(NGMO_ADDR, ':SENS:A:FUNC VOLT')
    iface.write(NGMO_ADDR, ':MEAS:A?')
    time.sleep(DELAY_MEAS_TRIG)
    r = iface.read_until_char(NGMO_ADDR, '10')
    # print('Vsrc: ' + str(r))
    val['source']['voltage'][i] = float(r)
    
    # read source current
    iface.write(NGMO_ADDR, ':SENS:A:FUNC CURR')
    iface.write(NGMO_ADDR, ':MEAS:A?')
    time.sleep(DELAY_MEAS_TRIG)
    r = iface.read_until_char(NGMO_ADDR, '10')
    # print('Isrc' + str(r))
    val['source']['current'][i] = float(r)
    
    # read load voltage
    iface.write(NGMO_ADDR, ':SENS:B:FUNC VOLT')
    iface.write(NGMO_ADDR, ':MEAS:B?')
    time.sleep(DELAY_MEAS_TRIG)
    r = iface.read_until_char(NGMO_ADDR, '10')
    # print('Vload ' + str(r))
    val['load']['voltage'][i] = r
    
    # read load current
    iface.write(NGMO_ADDR, ':SENS:B:FUNC CURR')
    iface.write(NGMO_ADDR, ':MEAS:B?')
    time.sleep(DELAY_MEAS_TRIG)
    r = iface.read_until_char(NGMO_ADDR, '10')
    # print('Iload ' + str(r))
    val['load']['current'][i] = r
    
    tic()
    # read load VDC
    iface.set_address(HP3456_ADDR)
    vdc = meter_dc.read_voltage()
    # print('VDC ' + str(vdc))
    val['load']['vdc'][i] = vdc
    
    # read load VAC
    iface.set_address(HP3456_ADDR)
    vac = meter_ac.read_voltage()
    # print('VAC ' + str(vac))
    val['load']['vac'][i] = vac
    print('PROGRESS: ' + str(i+1) + '/' + str(DPOINTS))
    toc()
    
srce.off()
load.off()
iface.close()
print('Total time: ' + str(time_ms() - t_start) + ' ms')

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
# apply polyfit
degree = 8
coef = np.polyfit(val['load']['current'][1:], val['efficiency2'][1:], degree)
n = len(val['load']['current'])
x = np.linspace(val['load']['current'][1], val['load']['current'][-1], n)
y = np.zeros(n)
for i in range(degree):
    y = y + pow(x, degree-i) * coef[i]
y = y + coef[degree]

plt.figure(figsize=(8,5))
plt.plot(val['load']['current'][1:], val['efficiency'][1:], marker='x', linestyle='None', color='cornflowerblue')
plt.plot(val['load']['current'][1:], val['efficiency2'][1:], marker='x', linestyle='None', color='sandybrown')
plt.plot(x, y, marker='None', linestyle='solid', color='deeppink')
plt.ylim(0.55, 0.90)
plt.xlabel(r'load current $I_L$ [A]')
plt.ylabel(r'efficiency coefficient $\eta$')
plt.title('Efficiency vs. Load Current')
plt.legend(['load voltage was measured with R&S NGMO2', 
            'load voltage was measured with HP 3456A', 
            'polinominal fit (degree: ' + str(degree) + ')'])
plt.grid()
#plt.savefig('Efficiency_vs_LoadCurrent.pdf')
plt.savefig('Efficiency_vs_LoadCurrent_NGMO2_HP3455_HP3456.png', dpi=200)  # 200dpi -> 1600x1000

#%%
plt.figure(figsize=(8,5))
plt.plot(val['load']['current'], val['load']['vdc'])
plt.plot(val['load']['current'], val['load']['voltage'])

#%%
plt.figure(figsize=(8,5))
plt.plot(val['load']['current'][1:], val['load']['vac'][1:])
plt.grid()
plt.ylim(0.0, 0.005)



