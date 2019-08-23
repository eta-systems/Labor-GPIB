# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 16:38:10 2019

@author: simon
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 15:00:26 2019

@author: simon
"""

"""

ngmo 2:
    - maximum allowed Voltage: 25V
    - fixed load
    - variable current: 0 - 1A
    
hp 6624A:
    - fixed voltage: 5V



"""

import time
import interface.prologix_gpib as prologix

import devices.hp_6624a as hp6624a

import numpy as np
import matplotlib.pyplot as plt
import utilities.Exporter as Exporter

# PARAMETERS
PSU_ADDR = 6


#%%
iface = prologix.usb(com='ASRL31::INSTR', baudrate=19200, timeout=5000, log_level=0)
iface.loc()  # local mode

psu = hp6624a.device(iface, PSU_ADDR)
psu.clear()

psu.write('VSET 1,1.000')
psu.write('ISET 1,0.01')

psu.write('VSET 2,1.000')
psu.write('ISET 2,0.01')





