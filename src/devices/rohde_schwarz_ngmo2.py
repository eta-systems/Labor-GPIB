# -*- coding: utf-8 -*-
"""
Created on Sun May 12 21:05:35 2019

@author: simon
"""

class device:
    def __init__(self, iface=None, address=7):
        self.bus = iface
        self.address = address
    
    # todo:
    # ValueError with defined strings
    def set_voltage(self, channel='A', voltage=0):
        if(channel not in 'ABab' or len(channel) != 1):
            raise ValueError('Channel can only be "A" or "B". channel = {}'.format(channel))
        # 3.3 specifications (0-15V)
        if(not 0 <= voltage <= 15):
            raise ValueError('Voltage must be in range(0, 30). voltage = {}'.format(voltage))
        voltage = round(voltage, 3)  # 1mV resolution
        self.bus.write(self.address, ':SOURce:' + channel + ':VOLTage ' + str(voltage))

    def set_output(self, channel='A', on=False):
        channel = channel[0].upper()
        if(channel not in 'AB'):
            raise ValueError('Channel can only be "A" or "B". channel = {}'.format(channel))
        
        if(on):
            self.bus.write(self.address, ':OUT:' + channel + ' ON')
        else:
            self.bus.write(self.address, ':OUT:' + channel + ' OFF')
    
    def get_output(self, channel='A'):
        channel = channel[0].upper()
        if(channel not in 'AB'):
            raise ValueError('Channel can only be "A" or "B". channel = {}'.format(channel))
        value = self.bus.request(self.address, ':OUT:' + channel + ':STATe?')
        if('ON' in value.upper()):
            return True
        elif('OFF' in value.upper()):
            return False
        else:
            raise ConnectionError('Did not receive an appropriate state value: {}'.format(value))
            
        
    def get_idn(self):
        value = self.bus.request(self.address, '*IDN?')
        # ROHDE&SCHWARZ,NGMO2,100778,1.16 /A:3:1.14,B:3:1.14
        return value
    
    def send_command(self, command):
        self.bus.write(self.address, command)
        
    def reset(self):
        self.send_command('*RST')
    
    def save_preset(self, number):
        if(not 1 <= number <= 9):
            raise ValueError('Preset number must be in range 1 .. 9. number = {}'.format(number))
        self.send_command('*SAV ' + str(round(number, 0))[0])
        
    def get_status(self):
        value = self.bus.request(self.address, '*STB?')
        return value
    
    # Performs a checksum test on ROM and 
    # returns 0 for test OK and 1 for test failed
    def test_rom(self):
        value = self.bus.request(self.address, '*TST?')
        if('0' in value):
            return True
        else:
            return False
            
    def set_output_format(self, form):
        form = form.lower()
        if(form == 'ascii' or form == 'asci'):
            self.bus.write(self.address, ':FORMat:DATA ASCii')
        elif(form == 'long'):
            self.bus.write(self.address, ':FORMat:DATA LONG') # long int
        elif(form == 'short' or form == 'sreal'):
            self.bus.write(self.address, ':FORMat:DATA SREal') # short real
        elif(form == 'double' or fomr == 'dreal'):
            self.bus.write(self.address, ':FORMat:DATA DREal') # double real
        else:
            raise ValueError('Unknown format specified: {}'.format(form))
    
    def get_output_format(self):
        value = self.bus.request(self.address, ':FORMat:DATA?')
        return value
    
    def set_output_byte_order(self, order):
        order = order.lower()
        if(order == 'normal' or order == 'msbfirst'):
            self.bus.write(self.address, ':FORMat:BORDer NORMal')
        elif(order == 'swapped' or order == 'lsbfirst'):
            self.bus.write(self.address, ':FORMat:BORDer SWAPped')
            
        
        
        