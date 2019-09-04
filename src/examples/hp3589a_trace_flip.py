# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 08:27:35 2019

@author: simon
"""

"""

TRC_LOAD code ported from HP-BASIC example


"""

#%%

import interface.prologix_gpib as prologix
import devices.hp_3589a as hp3589a

import numpy as np

ADDR_HP = 6

iface = prologix.usb(com='ASRLCOM31::INSTR', baudrate=19200, timeout=5000, log_level=0)
speck = hp3589a.device(iface, ADDR_HP)
print(speck.idn())

#%%

def Upload_trace(hp, data, command):
    hp.write('FORM:DATA REAL')
    hp.write(command + ' ' + data)

speck.write('ARM:SOUR MAN')
speck.write('FORM:DATA ASCII')
csv = speck.query('TRAC:DATA?')
splt = csv.split(',')
Num_pts = len(splt)
values = np.zeros(Num_pts)

for k in range(Num_pts):
    values[k] = float(splt[k])

flip = np.flip(values)
data = str(flip).replace('\n', '').replace('[', '').replace(']', '').replace(' ',',')

Upload_trace(speck, data, 'TRAC:DATA')

iface.close()


