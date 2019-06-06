# -*- coding: utf-8 -*-
"""
Created on Sun May 12 20:55:54 2019

@author: simon
"""

"""
So:
>>> my_instrument.query("*IDN?")
is the same as:
>>> my_instrument.write('*IDN?')
>>> print(my_instrument.read())
"""

# TODO: Look at Timing diagramms of HP 3455 A

import time
import interface.prologix_gpib as prologix

import devices.rohde_schwarz_ngmo2 as ngmo
import devices.hp_3455a as hp3455
import devices.hp_3488a as hp3488

import devices.schlumberger_7150plus as schlumberger

import numpy as np
import matplotlib.pyplot as plt

#%%
iface = prologix.usb(com='ASRL31::INSTR', baudrate=19200, timeout=5000)
iface.loc()  # Lokaler Modus
schlumi = schlumberger.device(iface, 13)

#%%
schlumi.measurement(mode='vdc')         # Vdc
schlumi.range(range='auto')             # autorange
schlumi.integral_period(period='0.006') # 6.66ms
schlumi.trigger_type(trigger='single')  # single shot
schlumi.units(False)                    # keine Einheiten

values = np.zeros(20)                   # leeres Array mit 20 Werten

#%%
for i in range(0, 20):
    schlumi.trigger()           # single shot
    values[i] = schlumi.read()  # Wert lesen, dauert min. 6.66ms

plt.plot(values)                # plotten
plt.ylabel('U [V]')
plt.xlabel('Messung Nr.')


#%%


