# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 12:10:40 2019

@author: simon
"""

import time
import interface.prologix_gpib as prologix

import devices.rohde_schwarz_upa as upaa

import numpy as np
import matplotlib.pyplot as plt
import utilities.Exporter as Exporter

# PARAMETERS
ADDR_UPA = 2

# sweep
PTS_PER_OCTAVE = 2
F_START = 20
F_STOP  = 20e+3

UPA_MEAS_TIME = 5

n_octaves = np.log2(F_STOP-F_START)
n_pts = int(n_octaves * PTS_PER_OCTAVE)
f = np.logspace(start=np.log2(F_START), stop=np.log2(F_STOP), num=n_pts, base=2)

print('estimated time for distortion sweep: ' + str(np.ceil((UPA_MEAS_TIME*n_pts/60))) + ' min')

time_ms = lambda: int(round(time.time() * 1000))
time_s  = lambda: int(round(time.time()))
tim = time_s()
def tic():
    global tim
    tim = time_s()
def toc():
    global tim
    elapsed = time_s() - tim
    print('Elapsed time: ' + str(elapsed) + ' s')
    tim = time_s()
tic()
toc()

val = {}
val['frequency'] = f
val['distortion'] = np.zeros(n_pts)
val['level'] = np.zeros(n_pts)

#%%
iface = prologix.usb(com='ASRLCOM31::INSTR', baudrate=19200, timeout=5000, log_level=1)
iface.loc()  # local mode
upa = upaa.device(iface, ADDR_UPA)
upa.rst()

def read_distortion():
    upa.write('TRIGGER(MODE(FNCT))')
    upa.write('TRIGGER(SINGLE)')
    time.sleep(UPA_MEAS_TIME)
    a = upa.read() # "DISPC     0.0169E+0"
    a = a.split(' ')[-1]
    return float(a)
    
def read_level():
    upa.write('TRIGGER(MODE(LEV))')
    upa.write('TRIGGER(SINGLE)')
    time.sleep(1)
    a = upa.read() # "DISPC     0.0169E+0"
    a = a.split(' ')[-1]
    return float(a)
    
#%%

#upa.write('SWEEP (FREQ START) 20')
#upa.write('SWEEP (FREQ STOP) 20000')
#upa.write('SWEEP (INCREMENT FREQUENCY AUTO)')
#upa.write('SWEEP (FREQ ENABLE)')

upa.write('SOURCE (LEVEL DBM) 18')
upa.write('OUTPUT (LEFT UNBAL)')
upa.write('SOURCE (RS600OHM)')
upa.write('DISTORTION(TOTAL)')
upa.write('MEASUREMENT(FUNCTION PC)')

#%% 
for i in range(0, len(f)):
    freq = int(f[i])
    print(freq)
    upa.write('SOURCE (FREQ) ' + str(freq))
    val['frequency'][i] = freq
    time.sleep(.1)
    a = read_distortion()
    print(a)
    val['distortion'][i] = a
    
print('DONE!')

#%%

plt.figure(figsize=(8,5))
plt.plot(val['frequency'], val['distortion'], marker='x', linestyle='solid', color='cornflowerblue')
plt.grid()
#plt.xscale('log')
plt.title('THD of STUDER LineAmp 1.914.501')
plt.xlabel('Frequency f [Hz]')
plt.ylabel('THD [%]')

plt.savefig('THD_Studer_LineAmp.png', dpi=200)  # 200dpi -> 1600x1000


#%%
upa.write('SOURCE (FREQ) 2000')
upa.write('DISTORTION(TOTAL)')
upa.write('MEASUREMENT(FUNCTION PC)')
upa.write('TRIGGER (SINGLE)')
time.sleep(3)
upa.read()

#%%
iface.close()

#%%
# Export the raw values for later use
exp = Exporter.Exporter()
exp.dump_to_json_file('values_UPA_Studer_distortion_1.json', val)













