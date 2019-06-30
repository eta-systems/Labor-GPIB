# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 16:42:55 2019

@author: simon
"""

#%%
class boum(plant):
    def  __init__(self, name):
        plant.__init__(self, name)
        self._blatt = blatt(self.name)
    
    def blatt(self, a=None):
        print(str(a))
        return self._blatt
        
class blatt:
    def __init__(self, name):
        self.name = name
        
    def enable(self, on):
        print(on)
        print(self.name)

tanne = boum('grüen')
tanne.blatt().enable(False)
tanne.blatt('asdf')


