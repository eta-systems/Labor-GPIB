# -*- coding: utf-8 -*-
"""
Created on Tue May 14 09:35:46 2019

@author: simon
"""

class device:
    def __init__(self, iface=None, address=9):
        self.bus = iface
        self.address = address
        self.bus.set_address(address)
        