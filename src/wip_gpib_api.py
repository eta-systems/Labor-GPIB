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

#%%
iface = prologix.usb(com='ASRL31::INSTR', baudrate=19200, timeout=5000)
print(iface.baudrate)

#%%
voltmeter = hp3455.device(iface, 9)
#%%
iface.set_address(9)
time.sleep(.100)
iface.clr()
time.sleep(.100)
iface.loc()
time.sleep(.100)
iface.set_address(9)
time.sleep(.100)
iface.clr()
time.sleep(.100)
iface.write(9, 'F1R2A0H0M3D1T3')
time.sleep(.100)
iface.trg()
time.sleep(.100)
print( iface.spoll() )

#%%
val = iface.request(9, '++read 10')
print( val )

#%%
for k in range(10):
    iface.clr()
    time.sleep(.100)
    iface.write(9, 'F1R2A0H0M3D1T3')
    time.sleep(.100)
    iface.trg()
    time.sleep(.100)
    print( iface.spoll() )
    time.sleep(.100)
    val = iface.request(9, '++read 10')
    print( val )
    



#%% 
battery = ngmo.device(iface, 9)
battery.set_voltage('A', 12.4)
battery.set_output('A', True)

time.sleep(1.000)  # delay 1 second

#%%
switcher = hp3488.device(iface, 7)


