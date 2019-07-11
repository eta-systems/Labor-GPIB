# -*- coding: utf-8 -*-
"""
@author: simon

Copyright (c) 2019 eta systems GmbH. All rights reserved.

This Software is distributed WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY 
or FITNESS FOR A PARTICULAR PURPOSE. 
"""

import visa
from time import sleep
from sys import stderr

class usb:
    def __init__(self, com='ASRL1::INSTR', baudrate=19200, timeout=2000, log_level=0):
        self.com = com
        self.baudrate = baudrate
        self.timeout = timeout
        self.address = 1
        self.log_level = int(log_level)  # 0=off, 1=log
        rm = visa.ResourceManager()
        rm.list_resources()
        self.instr = rm.open_resource(self.com)
        self.write(self.address, '++clr')
        self.write(self.address, '++loc')
        message = self.instr.query('++ver')
        if('Prologix' in message):
            print(message)
        else:
            raise RuntimeError('Prologix USB Adapter not connected')
    
    def set_address(self, address):
        if(address in range(0, 30)):
            if(address != self.address):
                self.address = address
                if(self.log_level>0):
                    print('[w|-] ++addr ' + str(self.address))
                self.instr.write('++addr ' + str(self.address))
        else:
            raise ValueError('GPIB address {} not in range 0-30 (integer)'.format(address))
        
    def write(self, address, message):
        self.set_address(address)
        if(self.log_level>0):
            print('[w|' + str(self.address) + '] ' + str(message))
        self.instr.write(message) 
    
    def read(self, address):
        self.set_address(address)
        if(self.log_level>0):
            print('[r|' + str(self.address) + '] ', end = '') # end -> no \n
        val = self.instr.read()
        print(val)
        return val
    
    # Untested
    def read_eoi(self, address):
        self.set_address(address)
        if(self.log_level>0):
            print('[w|-] ++read eoi')
        self.instr.write('++read eoi')
        if(self.log_level>0):
            print('[r|' + str(self.address) + '] ', end = '') # end -> no \n
        val = self.instr.read()
        print(val)
        return val
    
    def read_until_char(self, address, char):
        self.set_address(address)
        if(self.log_level>0):
            print('[w|-] ++read ' + str(char))
        self.instr.write('++read ' + str(char))
        if(self.log_level>0):
            print('[r|' + str(self.address) + '] ', end = '') # end -> no \n
        val = self.instr.read()
        print(val)
        return val
    
    def request(self, address, message):
        self.set_address(address)
        if(self.log_level>0):
            print('[q|' + str(self.address) + '] ' + str(message), end='')
        self.instr.write(message)
        self.instr.write('++read 10')
        try:
            ret = self.instr.read()
        except visa.VisaIOError as e:
            print('\n[-|-] Exception: ' + str(e.description))
            ret = ''
        else:
            print(ret) # when no exception occurrs
        # ret = self.instr.query(message)
        return ret
            
    def rst(self):
        if(self.log_level>0):
            print('[w|-] ++rst')
        self.write(self.address, 'rst')
        sleep(5.0)
        
    def clr(self):
        self.write(self.address, '++clr')
    
    def trg(self):
        self.write(self.address, '++trg')
    
    def reset(self):
        self.write(self.address, '++rst')
    
    # TODO
    # spoll = 65/68 is not received from hp345x devices
    def spoll(self):
        if(self.log_level>0):
            print('[w|-] ++spoll', end='')
        val = self.instr.query('++spoll')
        #val = self.instr.read()
        print(' [r|-] ' + str(val), end='')
        return val
    
    def loc(self):
        self.write(self.address, '++loc')
        
    def close(self):
        self.instr.close()
            
##############################################################################
# # Commands for the PROLOGIX GPIO-USB converter 
##############################################################################
#
#  The following commands are available: 
#  ++addr 0-30 [96-126]  -- specify GPIB address 
#  ++addr                -- query GPIB address 
#  ++auto 0|1            -- enable (1) or disable (0) read-after-write 
#  ++auto                -- query read-after-write setting 
#  ++clr                 -- issue device clear 
#  ++eoi 0|1             -- enable (1) or disable (0) EOI with last byte 
#  ++eoi                 -- query eoi setting 
#  ++eos 0|1|2|3         -- EOS terminator - 0:CR+LF, 1:CR, 2:LF, 3:None 
#  ++eos                 -- query eos setting 
#  ++eot_enable 0|1      -- enable (1) or disable (0) appending eot_char on EOI 
#  ++eot_enable          -- query eot_enable setting 
#  ++eot_char <char>     -- specify eot character in decimal 
#  ++eot_char            -- query eot_char character 
#  ++ifc                 -- issue interface clear 
#  ++loc                 -- set device to local 
#  ++lon                 -- enable (1) or disable (0) listen only mode 
#  ++mode 0|1            -- set mode - 0:DEVICE, 1:CONTROLLER 
#  ++mode                -- query current mode 
#  ++read [eoi|<char>]   -- read until EOI, <char>, or timeout 
#  ++read_tmo_ms 1-3000  -- set read timeout in millisec
#  ++read_tmo_ms         -- query timeout 
#  ++rst                 -- reset controller 
#  ++savecfg 0|1         -- enable (1) or disable (0) saving configuration to EPROM 
#  ++savecfg             -- query savecfg setting 
#  ++spoll               -- serial poll currently addressed device 
#  ++spoll 0-30 [96-126] -- serial poll device at specified address 
#  ++srq                 -- query SRQ status 
#  ++status 0-255        -- specify serial poll status byte 
#  ++status              -- query serial poll status byte 
#  ++trg                 -- issue device trigger 
#  ++ver                 -- query controller version 
#  ++help                -- display this help
##############################################################################
 

