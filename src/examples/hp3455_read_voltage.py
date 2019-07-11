# -*- coding: utf-8 -*-
#%%
import interface.prologix_gpib as prologix
import devices.hp_3455a as hp3455

iface = prologix.usb(com='ASRL31::INSTR', baudrate=19200, timeout=5000, log_level=1)
iface.loc()  # Lokaler Modus

hp34 = hp3455.device(iface, 9)  # address 9 on prologix interface

print('Voltage : ' + str(float(hp34.read_voltage())))

iface.close()








