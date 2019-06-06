# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 19:00:33 2019

@author: simon
"""

"""

Measurement Type    M   0   Vdc
                        1   Vac
                        2   kR
                        3   Idc
                        4   Iac
                        5   PRT
                        
Range               R   0   auto
                        1   0.2V
                        2   2V    -     -
                        3   20V   20kR  -
                        4   200V  200kR -
                        5   2000V 2MR   2A
                        6   -     20MR  -
                        
Integration Period  I   0   6.66ms
                        1   40.0ms
                        2   50.0ms
                        3   400ms
                        4   10x400ms
                        5   reserved
                        6   100ms
                        
Send SRQ            Q   0   no (error only)
                        1   yes
                        
Sample/Trigger      T   0   single
                        1   repetitive

Device Clear        A
Display             D   0   on
                        1   off
                        
Sample              G       single shot
Output with Unit    N   0   on (Vdc, kR ...)
                        1   off


"""

from time import sleep

class device:
    def __init__(self, iface=None, address=13):
        self.bus = iface
        self.address = address
        self.integration_time = 0.006
    
    # todo: delete and write actual methods
    
    def measurement(self, mode='vdc'):
        mode = mode.lower()
        if(mode == 'vdc'):
            self.bus.write(self.address, 'M0')
        elif(mode == 'vac'):
            self.bus.write(self.address, 'M1')
        elif(mode == 'r'):
            self.bus.write(self.address, 'M2')
        else:
            raise ValueError('Unknown measurement type: {}'.format(mode))
        
    def range(self, range='auto'):
        range = range.lower()
        if(range == 'auto'):
            self.bus.write(self.address, 'R0')
        elif(range == '0.2'):
            self.bus.write(self.address, 'R1')
        elif(range == '2.0' or range == '2'):
            self.bus.write(self.address, 'R2')
        else:
            raise ValueError('{} is not a valid range setting [auto, 0.2, 2.0]'.format(range))
        
    def integral_period(self, period='0.006'):
        period = period.lower()
        if(period == '0.006'):
            self.bus.write(self.address, 'I0')
        elif(period == '0.04'):
            self.bus.write(self.address, 'I1')
        elif(period == '0.05'):
            self.bus.write(self.address, 'I2')
        else:
            raise ValueError('{} is not a valid period setting [0.006, 0.04, 0.05]'.format(period))
    
    def trigger_type(self, trigger='single'):
        # TODO
        self.bus.write(self.address, 'T0')
        
    def units(self, on):
        self.bus.write(self.address, 'N1')
    
    def trigger(self):
        self.bus.write(self.address, 'G')
        
    def read(self):
        val = self.bus.request(self.address, '++read 10')
        sleep(self.integration_time)
        return val
        
        
    def dummy(self):
        self.bus.write(self.address, 'U0N1J0M0R0I3Q1T0')
        self.bus.write(self.address, 'G')
        if(self.bus.spoll() == 0):
            raise RuntimeError('Spoll returned 0')
        voltage = self.bus.read(self.address, 10)
        return voltage
        
        