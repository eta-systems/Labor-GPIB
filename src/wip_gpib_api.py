# -*- coding: utf-8 -*-
"""
Created on Sun May 12 20:55:54 2019

@author: simon
"""

import prologix_gpib
import rohde_schwarz_ngmo2 as ngmo

iface = prologix_gpib.usb(baudrate=250000, timeout=2000)
print(iface.get_baudrate())

battery = ngmo.device(iface=iface)
battery.set_voltage('A', 12.4)




