# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 14:58:50 2019

@author: simon
"""


# Sorensen DCS 50-40M16
# does not have GPIB
# controll via external voltage
# todo: write wrapper that uses hp6624 PSU


from time import sleep
from warnings import warn

class device:
    def __init__(self, iface=None, address=6):
        self.bus = iface
        self.address = address
        self.bus.set_address(address)
        self.clear()
    
    # clear
    def clear(self):
        self.bus.clr()
            
    def write(self, text):
        self.bus.write(self.address, text)
        
    # read a measurement
    def read(self):
        val = self.bus.read_until_char(self.address, '10')  # ASCII 10 = LF
        return val   
    
    def read_voltage(self, ch=1):
        self.write('VOUT? ' + str(ch))
        return self.read()
    
    def read_current(self, ch=1):
        self.write('IOUT? ' + str(ch))
        return self.read()
        
        