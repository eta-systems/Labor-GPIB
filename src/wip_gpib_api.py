# -*- coding: utf-8 -*-

import time
import interface.prologix_gpib as prologix

import devices.rohde_schwarz_ngmo2 as ngmo2
# import devices.hp_3455a as hp3455
# import devices.hp_3488a as hp3488
# import devices.schlumberger_7150plus as schlumberger

import presets.preset_ngmo2 as ngmo_preset

import numpy as np
import matplotlib.pyplot as plt

#%%
iface = prologix.usb(com='ASRL31::INSTR', baudrate=19200, timeout=5000)
# iface = dummybus.usb()
iface.loc()  # Lokaler Modus

ngmo = ngmo2.device(iface, 7)

#%%
ngmo.clear()
time.sleep(.100)

"""
print(ngmo.get_idn())
time.sleep(.100)
"""

ngmo.display.enable(False)  # high speed mode
ngmo.format.data('ASCII')

chan = ngmo.output('A')

iface.write(7, ':SOUR:A:VOLT 0.0')
iface.write(7, ':SOUR:A:CURR:LIM 0.5')

iface.write(7, ':SENS:A:FUNC CURR')
iface.write(7, ':SENS:A:MEAS:INT 2.00E-3') # 2ms
iface.write(7, ':SENS:A:MEAS:AVER:COUN 1') # 1 sample

volts = np.zeros(101)
amps = np.zeros(101)

chan.on()
for i in range(0, 100):
    volt = i/100;
    iface.write(7, ':SOUR:A:VOLT ' + str(volt))
    time.sleep(.100)
    iface.write(7, ':MEAS:A?')
    #time.sleep(.1)
    #iface.write(7, '++read 10')
    #r = iface.read(7)
    r = iface.read_until_char(7, '10')
    print(r)
    volts[i] = volt
    amps[i] = r

chan.off()

plt.plot(volts[:10], amps[:10])
plt.xlabel('U [V]')
plt.ylabel('I [A]')
plt.savefig('measurement_ngmo_resistor_weir_amp_readings.pdf') 





















