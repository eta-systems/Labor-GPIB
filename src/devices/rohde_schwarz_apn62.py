# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 11:19:12 2019

@author: simon

Copyright (c) 2019 eta systems GmbH. All rights reserved.

This Software is distributed WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY 
or FITNESS FOR A PARTICULAR PURPOSE. 
"""

"""
*RST
FREQ 15.625KHZ
FREQ?;LEV?
++read 10
FREQUENCY 15625;LEVEL 10.00E-3
FREQUENCY 15625
FR?
++read 10
FREQUENCY 15625
"""

class device:
    def __init__(self, iface=None, address=7):
        self.bus = iface
        self.address = address

    # Returns the APN to the *RST default conditions
    def rst(self):
        self.bus.write(self.address, '*RST')

    def write(self, text):
        self.bus.write(self.address, text)
        
    # read a measurement
    def read(self):
        val = self.bus.read_until_char(self.address, '10')  # ASCII 10 = LF
        return val   
    
    def set_frequency(self, freq):
        self.bus.write(self.address, 'FR ' + str(freq) + 'HZ')


