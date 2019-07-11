# -*- coding: utf-8 -*-
#%%
import time
import interface.prologix_gpib as prologix
import devices.hp_3456a as hp3456

import numpy as np
import matplotlib.pyplot as plt

iface = prologix.usb(com='ASRL31::INSTR', baudrate=19200, timeout=5000, log_level=1)
iface.loc()  # Lokaler Modus

dvm = hp3456.device(iface, 8)  # address 8 on prologix interface

iface.write(8, 'S0F1R1Z1M0T4SM024')

iface.write(8, '++trg')
iface.write(8, '++spoll')
val = iface.read(8)
print(' [r|-] ' + str(val), end='')

iface.write(8, '++read 10')
val = iface.read(8)
print(' [r|-] ' + str(val), end='')

"""
for k in range(0,20):
    iface.trg()
    print('spoll: ' + str(iface.spoll()))
    print('volt: ' + str(float(iface.read_until_char(8, '10'))))
"""

iface.close()


#%%
"""
[w|1] ++clr
[w|1] ++loc
Prologix GPIB-USB Controller version 6.101

[w|1] ++loc
[w|-] ++addr 8
[w|8] ++clr
[w|8] F1
[w|8] R1
[w|8] T4
[w|8] S0F1R1Z1M0T4SM024
[w|8] ++trg
[w|-] ++spoll [r|-] 0
spoll: 0

[w|-] ++read 10
[r|8] -000.0024E-3

volt: -2.4e-06
[w|8] ++trg
[w|-] ++spoll [r|-] 0
spoll: 0

[w|-] ++read 10
[r|8] -000.0022E-3

volt: -2.2e-06
[w|8] ++trg
[w|-] ++spoll [r|-] 0
spoll: 0

[w|-] ++read 10
[r|8] -000.0027E-3

volt: -2.7e-06
[w|8] ++trg
[w|-] ++spoll [r|-] 0
spoll: 0

[w|-] ++read 10
[r|8] -000.0024E-3

volt: -2.4e-06
[w|8] ++trg
[w|-] ++spoll [r|-] 0
spoll: 0

[w|-] ++read 10
[r|8] -000.0024E-3

volt: -2.4e-06
"""





