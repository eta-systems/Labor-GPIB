# -*- coding: utf-8 -*-
#%%
import interface.prologix_gpib as prologix
import devices.hp_3455a as hp3455
import numpy as np
import time

try:
    iface = prologix.usb(com='ASRLCOM31::INSTR', baudrate=19200, timeout=5000, log_level=0)
    iface.loc()  # Lokaler Modus
    
    hp34 = hp3455.device(iface, 12)  # address 9 on prologix interface
    hp34.clear()
    hp34.measurement('vac')
    
    print('Voltage : ' + str(float(hp34.read_voltage())))
    
    for i in range(0, 10):
        # read load ripple
        ripple = np.zeros(3)
        for k in range(0, 3):
            print(k)
            ripple[k] = hp34.read_voltage()
            time.sleep(0.01)
        print('VAC ' + str(ripple))
    
    iface.close()

except Exception as e:
    print(e)
    print('Error')
    iface.close()





