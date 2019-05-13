# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 10:22:25 2019

@author: simon
"""

import visa
rm = visa.ResourceManager()
rm.list_resources()
# ('ASRL10::INSTR', 'ASRL31::INSTR')

inst = rm.open_resource('ASRL1::INSTR')
inst.baudrate = 19200
inst.timeout = 2000

inst.write("++mode 1")      # PROLOGIX in write mode
inst.write("++addr 7")      # ROHDE&SCHWARZ NGMO 2
inst.write("++addr 9")

print(inst.query("*IDN?"))
# 

inst.write(":OUT:A OFF")
inst.write(":SOURce:A:VOLTage 3.3")
inst.write(":OUT:A ON")



