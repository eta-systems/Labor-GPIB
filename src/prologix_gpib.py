# -*- coding: utf-8 -*-
"""
Created on Sun May 12 20:51:03 2019

@author: simon
"""

# import visa

class usb:
    def __init__(self, baudrate=19200, timeout=2000):
        self.baudrate = baudrate
        self.timeout = timeout
        
    def get_baudrate(self):
        return self.baudrate
        
    def write(self, message):
        print('writing')
        print(message)
    
    def request(self, message):
        print(message)
        

