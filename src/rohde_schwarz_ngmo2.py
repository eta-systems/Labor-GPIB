# -*- coding: utf-8 -*-
"""
Created on Sun May 12 21:05:35 2019

@author: simon
"""

class device:
    def __init__(self, iface=None):
        self.bus = iface
    
    def set_voltage(self, channel='A', voltage=0):
        self.bus.write('Channel A is now ' + str(voltage) + 'V')

