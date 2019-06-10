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
                        5   PRT (Diode)
                        
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
from warnings import warn

class device:
    def __init__(self, iface=None, address=13):
        self.bus = iface
        self.address = address
        #self.integration_time = 0.006
        #self.measurement_type = 0
        self.clear()
        self.measurement('vdc')
        self.range('auto')
        self.integral_period(0.006)
        self.trigger_mode('auto')
        self.enable_units(False)
        self.enable_srq(False)
    
    # measurement mode
    def measurement(self, mode='vdc'):
        mode = mode.lower()
        if(mode == 'vdc'):
            self.measurement_type = 0
            self.bus.write(self.address, 'M0')
        elif(mode == 'vac'):
            self.measurement_type = 1
            self.bus.write(self.address, 'M1')
        elif(mode == 'r' or mode == 'kr'):
            self.measurement_type = 2
            self.bus.write(self.address, 'M2')
        elif(mode == 'idc'):
            self.measurement_type = 3
            self.bus.write(self.address, 'M3')
        elif(mode == 'iac'):
            self.measurement_type = 4
            self.bus.write(self.address, 'M4')
        elif(mode == 'prt'):
            self.measurement_type = 5
            self.bus.write(self.address, 'M5')
        else:
            raise ValueError('Unknown measurement type: {}'.format(mode))
    
    # range
    def range(self, range='auto'):
        range = range.lower()
        if(range == 'auto'):
            self.range = 0
            self.bus.write(self.address, 'R0')
        elif(range == '0.2' or range == '0.2v'):
            self.range = 1
            self.bus.write(self.address, 'R1')
        elif(range == '2.0' or range == '2' or range == '2.0v' or range == '2v'):
            self.range = 2
            self.bus.write(self.address, 'R2')
        elif(range == '20' or range == '20v' or range == '20kr'):
            self.range = 3
            self.bus.write(self.address, 'R3')
        elif(range == '200' or range == '200v' or range == '200kr'):
            self.range = 4
            self.bus.write(self.address, 'R4')
        elif(range == '2000' or range == '2000v' or range == '2mr' or range == '2a'):
            self.range = 5
            self.bus.write(self.address, 'R5')
        elif(range == '20mr'):
            self.range = 6
            self.bus.write(self.address, 'R6')
        else:
            raise ValueError('{} is not a valid range setting [auto, 0.2, 2.0]'.format(range))
    
    # integration period
    def integral_period(self, period=0.006):
        if(period < 0.0067):
            self.integration_time = 0.00666
            self.bus.write(self.address, 'I0')
        elif(period <= 0.04):
            self.integration_time = 0.04
            self.bus.write(self.address, 'I1')
        elif(period <= 0.05):
            self.integration_time = 0.05
            self.bus.write(self.address, 'I2')
        elif(period <= 0.1):
            self.integration_time = 0.1
            self.bus.write(self.address, 'I6')
        elif(period <= 0.4):
            self.integration_time = 0.4
            self.bus.write(self.address, 'I3')
        elif(period <= (10*0.4)):
            if(self.measurement_type in [1, 4, 5]):
                warn('10x400ms cannot be used for Vac (M1) or Iac (M4) or diode (M5)')
            else:
                self.integration_time = 10*0.4
                self.bus.write(self.address, 'I4')
        else:
            raise ValueError('period must be < 4s - entered: {}'.format(period))
    
    # trigger type
    def trigger_mode(self, trigger='single'):
        trigger = trigger.lower()
        if(trigger == 'single' or trigger == 'sample' or trigger == '0'):
            self.trigger_type = 0
            self.bus.write(self.address, 'T0')
        elif(trigger == 'track' or trigger == 'auto' or trigger == '1'):
            self.trigger_type = 1
            self.bus.write(self.address, 'T1')
        else:
            raise ValueError('invalid trigger type: {}. must be [single, auto]'.format(trigger))
        
    # display units
    def enable_units(self, on):
        if(on == True):
            self.show_units = True
            self.bus.write(self.address, 'N0')
        else:
            self.show_units = False
            self.bus.write(self.address, 'N1')
    
    # trigger a measurement
    def trigger(self):
        self.bus.write(self.address, 'G')
    
    def sample(self):
        self.bus.write(self.address, 'G')
    
    # read a measurement
    def read(self):
        val = self.bus.read_until_char(self.address, '10')  # ASCII 10 = LF
        return val
    
    def read_wait(self):
        val = self.bus.read_until_char(self.address, '10')  # ASCII 10 = LF
        sleep(self.integration_time) # block program execution
        return val
    
    # return srq messages
    def enable_srq(self, on):
        if(on == True):
            self.show_srq = True
            self.bus.write(self.address, 'Q1')
        else:
            self.show_srq = False
            self.bus.write(self.address, 'Q0')
            
    # turn LCD on or off
    def enable_display(self, on):
        if(on == True):
            self.bus.write(self.address, 'D0')
        else:
            self.bus.write(self.address, 'D1')
    
    # device clear
    def clear(self):
        self.bus.write(self.address, 'A')
    
    ####################################################################
    # for testing purposes
    def dummy(self):
        self.bus.write(self.address, 'U0N1J0M0R0I3Q1T0')
        self.bus.write(self.address, 'G')
        if(self.bus.spoll() == 0):
            raise RuntimeError('Spoll returned 0')
        voltage = self.bus.read(self.address, 10)
        return voltage
        
        