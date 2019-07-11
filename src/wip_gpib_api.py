# -*- coding: utf-8 -*-
#%%
import time
import interface.prologix_gpib as prologix
import devices.hp_3488a as hp3488

import numpy as np
import matplotlib.pyplot as plt

iface = prologix.usb(com='ASRL31::INSTR', baudrate=19200, timeout=5000, log_level=1)
iface.loc()  # Lokaler Modus

box = hp3488.device(iface, 8)  # address 8 on prologix interface


try:
    box.set_slot(1,44472)
    hfsw = box.channel(1)
    
    hfsw.close(0)
    time.sleep(0.5)
    hfsw.open(0)
    
    iface.close()

except KeyboardInterrupt:
    iface.close()

