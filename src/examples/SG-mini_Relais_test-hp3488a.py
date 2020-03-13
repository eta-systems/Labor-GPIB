# -*- coding: utf-8 -*-
#%%

import interface.prologix_gpib as prologix
import devices.hp_3488a as hp3488a
import numpy as np

#import visa
#rm = visa.ResourceManager()
#rm.list_resources()

ADDR_HP = 9

iface = prologix.usb(com='ASRL4::INSTR', baudrate=115200, timeout=5000, log_level=1)
box = hp3488a.device(iface, ADDR_HP)

#box.print_available_cards()
box.set_slot(1, 44471)
box.set_slot(2, 44471)
box.set_slot(3, 44472)
box.set_slot(4, 44474)
box.set_slot(5, 44474)

# using 44474 in slot 4
card = box.channel(4)

#%%
for a in range(0,16):
    card.close(a)
#%%
for a in range(0,16):
    card.open(a)

#%%
card.close(9)
#%%
card.open(9)

#%%
box.channel(4).reset()






#%%
# Test clicking sound on 44471
box.channel(1).close(1)
#%%
box.channel(1).open(1)
#%%
box.channel(1).reset()


#%%
iface.close()
        
        
