# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 09:40:29 2019

@author: simon
"""

"""
https://www.keysight.com/en/pd-3456A%3Aepsg%3Apro-pn-3456A/6-1-2-digit-digital-multimeter
Manual: HP3456A - Sec 3-16x - p. 45/385 - Table 3-9A. HP-IB Program Codes




            Control                         Programm Code
FUNCTION    Shift Function Off (Unshifted)  S0
            DCV                             F1
            ACV                             F2
            ACV + DCV                       F3
            2 Wire K Ohms                   F4
            4 Wire K Ohms                   F5
            Shift Function On (Shifted)     Sl
            DCV / DCV Ratio                 F1
            ACV/DCV Ratio                   F2
            ACV+DCV/DCV Relic               F3
            O.C. 2 Wire K Ohms              F4
            0.C. 4 Wire K Ohms              F5

RANGE       Auto                            R1
            100 mV or .l KOhrns             R2
            1000 mV at 1 K Ohms             R3
            10 V or 10 KOhms                R4
            100 V or 100 KOhms              R5
            1000 V or 1 MOhms               R6
            10 M Ohms                       R7
            100 M Ohms                      R8
            1000 M Ohms                     R9

TRIGGER     Internal                        T1
            External                        T2
            Single                          T3
            Hold                            T4

AUTOZERO    On                              Z1
            Off                             Z0

FILTER      On                              FL1
            0ff                             FL0

TEST        On                              TE1
            Off                             TE0

REGISTERS   Storing into Registers          ST
            Recalling Registers             RE
            Number of Readings              N
            Number of Dig-ts Displlyad      G
            Number of Power Line Cyc. Int.  I
            Delay                           D
            Mean Register [Read only)       M
            Variance Register (Read OnIy)   V
            Count Register (Read only]      C
            Lower Register                  L
            R Register                      F
            Upper Register                  U
            Y Register                      Y
            Z Register                      Z

MATH        0ff                             M0
            Pass/Fail                       M1
            Statistic (Mean, Variance, Count) M2
            Null                            M3
            dBm                             M4
            Thermistor °Fl                  M5
            Thermistor °Cl                  M6
            Scale [(X - Z)/Y]               M7
            %Error [(X - Y)/Y x 100]        M8
            dB (20 Log X/V)                 M9

READING STORAGE On                          R51
            Off                             R50

SYSTEM OUTPUT MODE On                       RS1
            Off                             RS0

DISPLAY     On                              D1
            Off                             D0

OUTPUT FORMAT 
            Packed Format On                 Pl
            Packed Format Off (ASCII Format) P0

CLEAR-CONTINUE Active                       CL1

NUMERIC SEPARATDR 
            Separates Numbers (e.g. F1W1OSTN) W

HOME COMMAND Software Reset                 H

FRONTIREAH SWITCH SENSE 1 = Front, 0 = Rear SW1

EOI         Enable                          O1
            Disable                         O0

PROGRAM MEMORY 
            Load Program (Syntax) On        L1
            Load Program (Syntex) Off       Q
            Execute Program Memory          X1

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
        
    # measurement mode
    def measurement(self, mode='vdc'):
        mode = mode.lower()
        if(mode == 'vdc'):
            self.measurement_type = 1
            self.bus.write(self.address, 'F1')
        elif(mode == 'vac'):
            self.measurement_type = 2
            self.bus.write(self.address, 'F2')
        elif(mode == 'fast vac'):
            self.measurement_type = 3
            self.bus.write(self.address, 'F3')
        elif(mode == '2 wire kr'):
            self.measurement_type = 4
            self.bus.write(self.address, 'F4')
        elif(mode == '4 wire kr'):
            self.measurement_type = 5
            self.bus.write(self.address, 'F5')
        elif(mode == 'test'):
            self.measurement_type = 6
            self.bus.write(self.address, 'F6')
        else:
            raise ValueError('Unknown measurement type: {}'.format(mode))
            
    # range
    def range(self, range='auto'):
        range = range.lower()
        if(range == 'auto'):
            self.range = 7
            self.bus.write(self.address, 'R1')
        elif(range in ['0.1', '.1', '100m', '100mV', '0.1kOhms']):
            self.range = 2
            self.bus.write(self.address, 'R2')
        elif(range in ['1', '1000m', '1000mV', '1kOhms']):
            self.range = 3
            self.bus.write(self.address, 'R3')
        elif(range in ['10', '10V', '10k', '10kOhms']):
            self.range = 4
            self.bus.write(self.address, 'R4')
        elif(range in ['100', '100V', '0.1kV', '100k', '100kOhms']):
            self.range = 5
            self.bus.write(self.address, 'R5')
        elif(range in ['1000', '1000V', '1kV', '1M', '1Meg', '1MOhms']):
            self.range = 6
            self.bus.write(self.address, 'R6')
        elif(range in ['10M', '10Meg', '10MOhms']):
            self.range = 7
            self.bus.write(self.address, 'R7')
        elif(range in ['100M', '100Meg', '100MOhms']):
            self.range = 8
            self.bus.write(self.address, 'R8')
        elif(range in ['1000M', '1000Meg', '1000MOhms']):
            self.range = 9
            self.bus.write(self.address, 'R9')
        else:
            raise ValueError('{} is not a valid range setting [auto, .1, 1, 10, 100, 1k, 10k]'.format(range))
        
    # trigger type
    def trigger_mode(self, trigger='internal'):
        trigger = trigger.lower()
        if(trigger in ['int', 'internal']):
            self.trigger_type = 1
            self.bus.write(self.address, 'T1')
        elif(trigger in ['ext', 'external']):
            self.trigger_type = 2
            self.bus.write(self.address, 'T2')
        elif(trigger in ['single']):
            self.trigger_type = 3
            self.bus.write(self.address, 'T3')
        elif(trigger in ['hold']):
            self.trigger_type = 4
            self.bus.write(self.address, 'T4')
        else:
            raise ValueError('invalid trigger type: {}. must be [int, ext, manual]'.format(trigger))
        
    # autozero
    def enable_autozero(self, enable=True):
        if(enable):
            self.autozero = True
            self.bus.write(self.address, 'Z1')
        else:
            self.autozero = False
            self.bus.write(self.address, 'Z0')
    
    # filter
    def enable_filter(self, enable=True):
        if(enable):
            self.filter = True
            self.bus.write(self.address, 'FL1')
        else:
            self.filter = False
            self.bus.write(self.address, 'FL0')
    
    # test
    def enable_test(self, enable=True):
        if(enable):
            self.test = True
            self.bus.write(self.address, 'TE1')
        else:
            self.test = False
            self.bus.write(self.address, 'TE0')


        
        
        
        
