# -*- coding: utf-8 -*-

# TODO: add a Serial Interface instead of using pyvisa to prevent
# using a Visa Binary

import visa
from time import sleep

class usb:
    def __init__(self, com='ASRL1::INSTR', baudrate=19200, timeout=2000):
        self.com = com
        self.baudrate = baudrate
        self.timeout = timeout
        self.address = 1
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
                self.instr.write('++addr ' + str(self.address))
        else:
            raise ValueError('GPIB address {} not in range 0-30 (integer)'.format(address))
        
    def write(self, address, message):
        self.set_address(address)
        self.instr.write(message) 
        print('writing: ' + str(message))
    
    def read(self, address):
        self.set_address(address)
        return self.instr.read()
    
    def read_eoi(self, address):
        return self.request(address, '++read eoi')
    
    def read_until_char(self, address, char):
        return self.request(address, '++read ' + str(char))
    
    def request(self, address, message):
        self.set_address(address)
        print('requesting: ' + str(message))
        self.instr.write(message)
        self.instr.write('++read 10')
        ret = self.instr.read()
        # ret = self.instr.query(message)
        return ret
            
    def rst(self):
        self.write(self.address, 'rst')
        sleep(5.0)
        
    def clr(self):
        self.write(self.address, '++clr')
    
    def trg(self):
        self.write(self.address, '++trg')
    
    def reset(self):
        self.write(self.address, '++rst')
    
    def spoll(self):
       return  self.request(self.address, '++spoll')
    
    def loc(self):
        self.write(self.address, '++loc')
            
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
 

