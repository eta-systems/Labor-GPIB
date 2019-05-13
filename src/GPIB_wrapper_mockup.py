# -*- coding: utf-8 -*-
#!/usr/bin/env python3

"""
Created on Sun May 12 20:28:14 2019

@author: simon
"""

# pyvisa package
import visa

# wrapper for Prologix GPIB device (USB or Ethernet)
import prologix_gpib as prologix
# import individual devices
import devices.hp3456a as hp3465a
import devices.rhodeschwarz_ngmo2 as ngmo

'''
# this is how pyvisa works
rm = visa.ResourceManager()
rm.list_resources()
# ('ASRL10::INSTR', 'ASRL31::INSTR')
# COM10 and COM31

inst = rm.open_resource('ASRL31::INSTR')
inst.baudrate = 19200
inst.timeout = 2000
'''

'''
initialize gpib interface 
interface has methods:
    - write (data_to_send)
    - request (data_to_send)
'''

iface = prologix.usb(com='ASRL1::INSTR', baudrate=19200, timeout=2000)
iface.mode('listen')  # ++mode 0
print( iface.idn() )  # ++ irgendwas

# initialize device handlers with interface, 
# so that they can use read() and request()
voltmeter = hp3465a(iface, address=9)
battery = ngmo(iface, address=7)

# devices have their own methods
voltmeter.range('auto')
battery.voltage('A', 0)
battery.overcurrent('A', 1)

for k in range(10):
    battery.voltage('A', k)
    sleep(1000)
    value = voltmeter.read()
    

