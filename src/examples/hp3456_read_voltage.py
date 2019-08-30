# -*- coding: utf-8 -*-
#%%
import time
import interface.prologix_gpib as prologix
import devices.hp_3456a as hp3456

import numpy as np
import matplotlib.pyplot as plt

iface = prologix.usb(com='ASRLCOM31::INSTR', baudrate=19200, timeout=5000, log_level=1)

dvm = hp3456.device(iface, 8)  # address 8 on prologix interface
dvm.measurement('vac')
dvm.trigger_mode('hold')

for k in range(0,3):
    dvm.measurement('vdc')
    print('DC: ' + str(dvm.read_voltage()))
    dvm.measurement('vac')
    print('AC: ' + str(dvm.read_voltage()))
    
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





