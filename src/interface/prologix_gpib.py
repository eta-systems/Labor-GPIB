# -*- coding: utf-8 -*-
"""
Created on Sun May 12 20:51:03 2019

@author: simon
"""

import visa

class usb:
    
    def __init__(self, com='ASRL1::INSTR', baudrate=19200, timeout=2000):
        self.com = com
        self.baudrate = baudrate
        self.timeout = timeout
        self.address = 1
        rm = visa.ResourceManager()
        rm.list_resources()
        self.instr = rm.open_resource(self.com)
        
    def write(self, address, message):
        if(address < 10):
            if(address != self.address):
                self.address = address
                self.instr.write('++addr ' + str(self.address))
            self.instr.write(message) 
    
    def request(self, address, message):
        if(address < 10):
            if(address != self.address):
                self.address = address
                self.instr.write('++addr ' + str(self.address))
            self.instr.write(message)
            # ret = self.instr.read()
            # return ret
            
        

