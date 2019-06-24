# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 18:17:25 2019

@author: simon
"""

def lead_battery_12V(ngmo):
    ngmo.output.a.open_sense(True)
    ngmo.output.a.off()
    ngmo.output.a.voltage(12.4)
    ngmo.output.impedance(0.5)
    
# http://www.bb-battery.com/global/show.php?f=HR6-12.pdf.24fe96b07f7ea88e0c4bf07e441749a6&m=HR6-12.pdf
def HR6_12(ngmo):
    ngmo.output.a.open_sense(True)
    ngmo.output.a.off()
    ngmo.output.a.voltage(12.0) # 12V nominal
    ngmo.output.a.impedance(0.22) # 22mR
