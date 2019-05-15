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
        
    def set_address(self, address):
        if(address in range(0, 30)):
            if(address != self.address):
                self.address = address
                self.instr.write('++addr ' + str(self.address))
        else:
            raise ValueError('GPIB address {} not in range 0-30 (integer)'.format(address))
        
    def write(self, address, message):
        self.set_address(address)
        self.instr.write(message) 
    
    def request(self, address, message):
        self.set_address(address)
        self.instr.write(message) 
        ret = self.instr.read()
        return ret
            
    def clr(self):
        self.instr.write('++clr')
    
    def trg(self):
        self.instr.write('++trg')
    
    def reset(self):
        self.instr.write('++rst')
    
    def spoll(self):
        self.instr.write('++spoll')
            
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
 

