# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 18:17:25 2019

@author: simon
"""

def lead_battery_12V(ngmo):
    ngmo.output.open_sense(True)
    ngmo.output.a.off()
    ngmo.output.a.voltage(12.4)
    ngmo.output.impedance(0.5)
    

