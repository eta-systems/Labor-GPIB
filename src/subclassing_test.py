# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 16:42:55 2019

@author: simon
"""

#%%
class plant:
    def __init__(self, name):
        self.name = name

class boum(plant):
    def  __init__(self, name):
        plant.__init__(self, name)
        self.blatt = blatt(self.name)
        
class blatt:
    def __init__(self, name):
        self.name = name
        
    def enable(self, on):
        print(on)
        print(self.name)

ferdi = boum('grüen')
ferdi.blatt.enable(False)


