# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 11:44:36 2019

@author: simon

Copyright (c) 2019 eta systems GmbH. All rights reserved.

This Software is distributed WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY 
or FITNESS FOR A PARTICULAR PURPOSE. 
"""

"""
UPA Audio Analyzer

// personal comment:
    - this device has an unusual (ugly) syntax
    - use braces ()
    - lower case is not supported



"""

class device:
    def __init__(self, iface=None, address=7):
        self.bus = iface
        self.address = address

    # Returns the UPA to the *RST default conditions
    def rst(self):
        self.bus.write(self.address, 'CLR')

    def write(self, text):
        self.bus.write(self.address, text)
        
    # read a measurement
    def read(self):
        val = self.bus.read_until_char(self.address, '10')  # ASCII 10 = LF
        return val   
    


