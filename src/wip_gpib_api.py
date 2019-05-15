# -*- coding: utf-8 -*-
"""
Created on Sun May 12 20:55:54 2019

@author: simon
"""

import time
import interface.prologix_gpib as prologix
import devices.rohde_schwarz_ngmo2 as ngmo
import devices.hp_3455a as hp3455
import devices.hp_3488a as hp3488

#%%
iface = prologix.usb(baudrate=19200, timeout=5000)
print(iface.baudrate)

#%% 
battery = ngmo.device(iface, 9)
battery.set_voltage('A', 12.4)
battery.set_output('A', True)

time.sleep(1.000)  # delay 1 second

#%%
switcher = hp3488.device(iface, 7)

#%%
voltmeter = hp3455.device(iface, 9)
iface.clr()
iface.write(9, 'F1R2A0H0M3D1T3')
iface.spoll()
val = iface.request(9, '++read 10')



