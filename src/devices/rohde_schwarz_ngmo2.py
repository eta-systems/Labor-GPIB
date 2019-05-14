# -*- coding: utf-8 -*-
"""
Created on Sun May 12 21:05:35 2019

@author: simon
"""

class device:
    def __init__(self, iface=None, address=9):
        self.bus = iface
        self.address = address
    
    # todo:
    # ValueError with defined strings
    def set_voltage(self, channel='A', voltage=0):
        if(channel not in 'ABab' or len(channel) != 1):
            raise ValueError('Channel can only be "A" or "B". channel = {}'.format(channel))
        if(voltage >= 30 or voltage < 0):
            raise ValueError('Voltage must be in range(0, 30). voltage = {}'.format(voltage))
        self.bus.write(self.address, ':SOURce:' + channel + ':VOLTage ' + str(voltage))

    def set_output(self, channel='A', on=False):
        if(channel not in 'ABab' or len(channel) != 1):
            raise ValueError('Channel can only be "A" or "B". channel = {}'.format(channel))
            
        if(on):
            self.bus.write(self.address, ':OUT:A ON')
        else:
            self.bus.write(self.address, ':OUT:A OFF')
        
    def get_id(self):
        value = self.bus.request(self.address, '*IDN?')
        # ROHDE&SCHWARZ,NGMO2,100778,1.16 /A:3:1.14,B:3:1.14
        return value
        