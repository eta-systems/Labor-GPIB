# -*- coding: utf-8 -*-
"""
Created on Tue May 14 09:35:46 2019

@author: simon
"""

"""
Manual: HP3455A - Sec III - p. 32/220 - Table 3-4. HP-IB Program Codes

Function    DC Volts        F1
            AC Volts        F2
            Fast AC Volts   F3
            2 Wire kR       F4
            4 Wire kR       F5
            Test            F6

Range       .1              R1
            1               R2
            10              R3
            100             R4
            1k              R5
            10k             R6
            AUTO            R7
            
Trigger     Internal        T1
            External        T2
            Hold/Manual     T3
            
Math        Scale           M1
            Error           M2
            Off             M3
        
Enter       Y               EY
            Z               EZ
            
Store       Y               SY
            Z               SZ
            
Auto Cal    Off             A0
            On              A1
            
High Res    Off             H0
            On              H1

Data Ready  Off             D0
(RQS)       On              D1

Binary Program              B

"""

"""
Current Device '9'. Sending:   '++clr'
Current Device '9'. Sending:   'F1R2A0H0M3D1T3'
Current Device '9'. Sending:   '++trg'
Current Device '9'. Sending:   '++spoll'
Current Device '9'. Receiving: '65'
Current Device '9'. Sending:   '++read 10'
Current Device '9'. Receiving: '+0.043950E+00'
F1 = vdc
R2 = 1V range
A0 = no auto cal
H0 = no high res
M3 = math off
D1 = ready RQS
T3 = manual trigger
"""

from time import sleep
from warnings import warn

class device:
    def __init__(self, iface=None, address=9):
        self.bus = iface
        self.address = address
        self.bus.set_address(address)
        self.clear()
        self.measurement('vdc')
        self.range('auto')
        self.trigger_mode('manual')
        self.math_mode('Off')
        self.enable_high_resolution(False)
        self.enable_auto_cal(False)
        self.enable_rqs(True)
    
    # clear
    def clear(self):
        self.bus.clr()
        sleep(1)
            
    # measurement mode
    def measurement(self, mode='vdc'):
        mode = mode.lower()
        if(mode in ['vdc', 'dcv']):
            self.measurement_type = 1
            self.bus.write(self.address, 'F1')
        elif(mode in ['adc', 'acv', 'vac']):
            self.measurement_type = 2
            self.bus.write(self.address, 'F2')
        elif(mode in ['vdcvac', 'dcvacv', 'acdc']):
            self.measurement_type = 3
            self.bus.write(self.address, 'F3')
        elif(mode in ['2 wire kohms', '2 wire kr']):
            self.measurement_type = 4
            self.bus.write(self.address, 'F4')
        elif(mode in ['4 wire kohms', '4 wire kr']):
            self.measurement_type = 5
            self.bus.write(self.address, 'F5')
        elif(mode in ['shift', 'shift on', 'shifted']):
            self.measurement_type = 6
            self.bus.write(self.address, 'S1')
        elif(mode in ['unshift', 'shift off', 'unshifted']):
            self.measurement_type = 7
            self.bus.write(self.address, 'S0')
        else:
            raise ValueError('Unknown measurement type: {}'.format(mode))
        
    # range
    def range(self, range='auto'):
        range = range.lower()
        if(range == 'auto'):
            self.range = 7
            self.bus.write(self.address, 'R7')
        elif(range == '0.1' or range == '.1'):
            self.range = 1
            self.bus.write(self.address, 'R1')
        elif(range == '1'):
            self.range = 2
            self.bus.write(self.address, 'R2')
        elif(range == '10'):
            self.range = 3
            self.bus.write(self.address, 'R3')
        elif(range == '100'):
            self.range = 4
            self.bus.write(self.address, 'R4')
        elif(range == '1k' or range == '1000'):
            self.range = 5
            self.bus.write(self.address, 'R5')
        elif(range == '10k' or range == '10000'):
            self.range = 6
            self.bus.write(self.address, 'R6')
        else:
            raise ValueError('{} is not a valid range setting [auto, .1, 1, 10, 100, 1k, 10k]'.format(range))
    
    # trigger type
    def trigger_mode(self, trigger='manual'):
        trigger = trigger.lower()
        if(trigger in ['int', 'internal']):
            self.trigger_type = 1
            self.bus.write(self.address, 'T1')
        elif(trigger in ['ext', 'external']):
            self.trigger_type = 2
            self.bus.write(self.address, 'T2')
        elif(trigger in ['man', 'manual']):
            self.trigger_type = 3
            self.bus.write(self.address, 'T3')
        else:
            raise ValueError('invalid trigger type: {}. must be [int, ext, manual]'.format(trigger))
            
    # auto calibration
    def enable_auto_cal(self, on):
        if(on == True):
            self.bus.write(self.address, 'A1')
        else:
            self.bus.write(self.address, 'A0')
    
    # high resolution
    def enable_high_resolution(self, on):
        if(on == True):
            self.high_res = True
            self.bus.write(self.address, 'H1')
        else:
            self.high_res = False
            self.bus.write(self.address, 'H0')
            
    # math mode
    def math_mode(self, mode):
        mode = mode.lower()
        if(mode == 'scale'):
            self.math_mode_enabled = 1
            self.bus.write(self.address, 'M1')
        elif(mode == 'error'):
            self.math_mode_enabled = 2
            self.bus.write(self.address, 'M2')
        else:
            # Off
            self.math_mode_enabled = 3
            self.bus.write(self.address, 'M3')    
    
    # trigger a measurement
    def trigger(self):
        self.bus.trg()
        
    # read a measurement
    def read(self):
        val = self.bus.read_until_char(self.address, '10')  # ASCII 10 = LF
        return val
    
    def read_wait(self):
        val = self.bus.read_until_char(self.address, '10')  # ASCII 10 = LF
        sleep(.01)  # block program execution
        return val
    
    # 3-35. Data Ready Request. The DATA READY Request
    # feature permits the 3455A to signal the controller upon
    # the completion of a measurement. This feature would
    # normally be used where the 3455A is triggered from an
    # external source. In this mode of operation, the 3455A is
    # programmed to the appropriate measurement
    # parameters (FUNCTION, RANGE, etc.). The con-
    # troller is then free to control other instruments on the
    # Bus. Upon being triggered, the 3455A makes a measure-
    # ment and outputs a “Require Service” message to
    # notify the controller that the measurement information
    # information is ready. Upon receiving the service re-
    # quest, the controller with serial poll the 3455A to deter-
    # mine the nature of the service request. Upon being poll-
    # ed, the 3455A outputs a status byte, in this case the
    # ASCII character “A" (decimal 65), indicating the
    # measurement data is ready. The controller then disables
    # the serial poll and reads the measurement data. The pro—
    # gram codes for the DATA READY RQS feature are: .
    # D0 Data Ready Request off
    # D1 Data Ready Request on

    def enable_rqs(self, on):
        if(on == True):
            self.rqs_poll = True
            self.bus.write(self.address, 'D1')
        else:
            self.rqs_poll = False
            self.bus.write(self.address, 'D0')
    
    def poll(self):    
        val = self.bus.spoll()
        if(val == '65'):
            return True
        else:
            return False
    
    def read_srq(self):
        self.trigger()
        for k in range(0,2):
            if(self.poll() == True):
                return self.read()
        warn('Serial poll did not return an SRQ message')
        return '0.0'
    
    # TODO, check if mode is voltage
    # ++spoll
    # 65
    # ++read 10
    # +1.385460E-01
    def read_voltage(self):
        #if(self.poll() == '65'):
        #    val = self.read()
        #    return val
        self.trigger()
        self.poll()
        val = self.bus.read_until_char(self.address, '10')  # ASCII 10 = LF
        return val
        
        
    
    
    
    
    
    
    
    
    
    