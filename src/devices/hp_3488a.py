# -*- coding: utf-8 -*-
"""
Created on Tue May 14 09:33:31 2019

@author: simon

for hp 3488a switch control unit
"""

class device:
    def __init__(self, iface=None, address=9):
        self.bus = iface
        self.address = address
    
    # todo: delete and write actual methods
    def set_voltage(self, channel='A', voltage=0):
        if(channel not in 'ABab' or len(channel) != 1):
            raise ValueError('Channel can only be "A" or "B". channel = {}'.format(channel))
        if(voltage >= 30 or voltage < 0):
            raise ValueError('Voltage must be in range(0, 30). voltage = {}'.format(voltage))
        self.bus.write(self.address, ':SOURce:' + channel + ':VOLTage ' + str(voltage))

    def set_output(self, channel='A', action='off'):
        if(channel not in 'ABab' or len(channel) != 1):
            raise ValueError('Channel can only be "A" or "B". channel = {}'.format(channel))
            
        if(action == 'on'):
            self.bus.write(self.address, ':OUT:A ON')
        elif(action == 'off'):
            self.bus.write(self.address, ':OUT:A OFF')
        else:
            raise ValueError('Action must be "on" or "off". action = {}'.format(action))
        
        