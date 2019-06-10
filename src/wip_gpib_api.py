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

# import devices.rohde_schwarz_ngmo2 as ngmo
import devices.hp_3455a as hp3455
# import devices.hp_3488a as hp3488
# import devices.schlumberger_7150plus as schlumberger

import numpy as np
import matplotlib.pyplot as plt

#%%
iface = prologix.usb(com='ASRL31::INSTR', baudrate=19200, timeout=5000)
iface.loc()  # Lokaler Modus

hp34 = hp3455.device(iface, 9)  # address 9 on prologix interface

#%%
values = np.zeros(20)         # leeres Array mit 20 Werten

for i in range(0, 20):
    hp34.trigger()            # single shot
    values[i] = hp34.read_rqs()

plt.plot(values)                # plotten
plt.ylabel('U [V]')
plt.xlabel('Messung Nr.')



