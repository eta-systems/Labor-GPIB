# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 08:22:30 2019

@author: simon
"""

"""
Spectrum/Network Analyzer

The device must have the following settings:
    - Key [U] "Local/HP.IB"
    - "Addressbl only"
    - Peripheral Address set to address in python code

Simple SCPI cmd:
    *IDN?
    ++read 10
    "HEWLETT-PACKARD,3589A,3129A00504,A.00.02"
    
    SENS:FREQ:SPAN?
    ++read 10

WAI command might be useful / needed



page 291
SENS:BAND:RES DOWN
SENS:BAND:RES UP
SENS:BAND:RES 9200HZ
SENS:BAND:RES 4.6KHZ

page 314
SENS:FREQ:STAR 10KHZ
SENS:FREQ:STOP 100KHZ
only for Network Sweep measurement type
SENS:FUNC?
++read 10
"POWER:NETWORK"

page 399 - TRACE Subsystem
page 402
TRAC:TITL '0123456789ABCDE'

Command Summary
page 410
"""


from time import sleep
from warnings import warn

class device:
    def __init__(self, iface=None, address=13):
        self.bus = iface
        self.address = address
        # self.clear()
    
    
    def idn(self):
        return self.bus.request(self.address, '*IDN?')
    
    def write(self, cmd):
        self.bus.write(self.address, cmd)
    
    def query(self, cmd):
        return self.bus.request(self.address, cmd)
    
    
    
    
    
    