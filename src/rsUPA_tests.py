# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 11:52:46 2019

@author: simon
"""

import time
import interface.prologix_gpib as prologix
import devices.rohde_schwarz_upa as upaa


# PARAMETERS
ADDR_UPA = 2

#%%
iface = prologix.usb(com='ASRLCOM31::INSTR', baudrate=19200, timeout=5000, log_level=1)
iface.loc()  # local mode
upa = upaa.device(iface, ADDR_UPA)
upa.rst()
time.sleep(.1)

# some test commands to try out the syntax
upa.write('INPUT(RIGHT BAL20KOHM)')
upa.write('INPUT(LEFT BAL20KOHM)')
upa.write('INPUT(RIGHT A/B20KOHM)')

iface.close()








