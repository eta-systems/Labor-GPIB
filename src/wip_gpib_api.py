# -*- coding: utf-8 -*-

import time
import interface.prologix_gpib as prologix
import interface.debug_gpib as dummybus

import devices.rohde_schwarz_ngmo2 as ngmo2
# import devices.hp_3455a as hp3455
# import devices.hp_3488a as hp3488
# import devices.schlumberger_7150plus as schlumberger

import presets.preset_ngmo2 as ngmo_preset

import numpy as np
import matplotlib.pyplot as plt

#%%
iface = prologix.usb(com='ASRL31::INSTR', baudrate=19200, timeout=5000)
# iface = dummybus.usb()
iface.loc()  # Lokaler Modus

ngmo = ngmo2.device(iface, 7)

#%%
ngmo.clear()
print(ngmo.get_idn())

ngmo.display.enable(True)
ngmo.format.data('ASCII')
ngmo.format.border('NORMAL')

ngmo.output('A').sense('CURRENT')
ngmo.output('A').on()

ngmo.output('A').interval('3.4e-3')
ngmo.output('A').set_averaging_samples(3)

print(ngmo.output('A').relay(1).is_open())

