# -*- coding: utf-8 -*-

import time
import interface.prologix_gpib as prologix

import devices.rohde_schwarz_ngmo2 as ngmo2

import numpy as np
import matplotlib.pyplot as plt

#%%
iface = prologix.usb(com='ASRL31::INSTR', baudrate=19200, timeout=5000)
iface.loc()  # local mode
ngmo = ngmo2.device(iface, 7)

ngmo.clear()
time.sleep(.100)

print(ngmo.get_idn())
time.sleep(.100)

ngmo.display.enable(False)  # high speed mode
ngmo.format.data('ASCII')
chan = ngmo.output('A')

# INIT
iface.write(7, ':SOUR:A:VOLT 0.0')          # 0V
iface.write(7, ':SOUR:A:CURR:LIM 0.5')      # current limmit = 0.5A
iface.write(7, ':SENS:A:FUNC CURR')         # measurement mode = current
iface.write(7, ':SENS:A:MEAS:INT 2.00E-3')  # measurement interval = 2ms
iface.write(7, ':SENS:A:MEAS:AVER:COUN 1')  # averaging uses 1 sample

volts = np.zeros(100)
amps = np.zeros(100)

chan.on()
for i in range(0, 100):
    volt = i/100;
    iface.write(7, ':SOUR:A:VOLT ' + str(volt))
    time.sleep(0.02)     # let voltage settle
    iface.write(7, ':MEAS:A?')
    r = iface.read_until_char(7, '10')
    print(r)
    volts[i] = volt
    amps[i] = r

chan.off()

rfit = np.polyfit(amps, volts, 1)
R = rfit[0]
print('Resistance is: ' + str(round(R,4)) + ' Ohm')

plt.plot(volts[:10], amps[:10])
plt.xlabel('U [V]')
plt.ylabel('I [A]')
plt.title('voltage vs. current of a ' + str(round(R,2)) + ' Ohm resistor')
plt.savefig('voltage_vs_current_R_' + str(round(R,2)) + '.pdf') 




















