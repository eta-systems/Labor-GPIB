# -*- coding: utf-8 -*-
#%%
import time
import interface.prologix_gpib as prologix
import devices.hp_3456a as hp3456

import numpy as np
import matplotlib.pyplot as plt

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

iface = prologix.usb(com='ASRLCOM31::INSTR', baudrate=115200, timeout=5000, log_level=1)
dvm = hp3456.device(iface, 8)  # address 8 on prologix interface
dvm.measurement('vac')
dvm.trigger_mode('internal')

for i in range(0,10):
    tic()
    val = iface.read_until_char(8, '10')
    val = iface.read_until_char(8, '10')
    val = iface.read_until_char(8, '10')
    toc()
    
iface.close()

# F2T1


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





