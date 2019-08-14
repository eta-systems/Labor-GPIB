# -*- coding: utf-8 -*-
"""

Not yet ready for prod
Example for how to write scripts for prod

@author: simon

Copyright (c) 2019 eta systems GmbH. All rights reserved.

This Software is distributed WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY 
or FITNESS FOR A PARTICULAR PURPOSE. 
"""

#%%

import interface.prologix_gpib as prologix
import interface.debug_gpib as dummybus
import devices.rohde_schwarz_ngmo2 as ngmo2

import numpy as np
import matplotlib.pyplot as plt
import time
from random import random

#%%
# Interface auswählen (COM31 --> ASLR31)
iface = prologix.usb(com='ASRL31::INSTR', baudrate=19200, timeout=5000)
iface.loc()  # Lokaler Modus

# Parameter für Prüfablauf
ch = 'A'                    # Channel A oder B
LED_serial_number = 112     # für Dokumentation
V_start = 0.0               # V
V_stop = 12.0               # V
t_delay = .100              # ms
impedance = 0.22            # Ohm

# NGMO init
ngmo = ngmo2.device(iface, 7)
ngmo.clear()
print(ngmo.get_idn())
ngmo.display.enable()
ngmo.display.set_channel(ch)
ngmo.format.data('ASCII')
ngmo.format.border('NORMAL')
ngmo.channel(ch).sense('current')

ngmo.output(ch).off()
ngmo.output(ch).voltage(0.0)
ngmo.output(ch).impedance(impedance)

V_range = V_stop - V_start
n = int(V_range*10)+1 # 12V x 10 steps/V
If = np.zeros(n)              # leeres Array
Uf = np.zeros(n)
v = V_start
for k in range(0, n):
    ngmo.output(ch).voltage(v)
    time.sleep(t_delay)         # warten bis neuer Wert erreicht
    # I = float( ngmo.output(ch).read() )    # NOT IMPLEMENTED !
    I = v + (random()-0.5)   # dummy trace
    Uf[k] = v
    If[k] = I
    v += 0.1

plt.plot(Uf, If)                    # plotten
plt.xlabel('Vf [V]')
plt.ylabel('If [mA]')
plt.title('(Ser.Nr: ' + str(LED_serial_number) + ')\n Voltage vs. Current draw')

plt.savefig('Silent_LED_Kennlinie_SN' + str(LED_serial_number) + '.pdf', )  # export


