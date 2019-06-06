# -*- coding: utf-8 -*-

#%%
iface.set_address(9)
time.sleep(.100)
iface.clr()
time.sleep(.100)
iface.loc()
time.sleep(.100)
iface.set_address(9)
time.sleep(.100)
iface.clr()
time.sleep(.100)
iface.write(9, 'F1R2A0H0M3D1T3')
time.sleep(.100)
iface.trg()
time.sleep(.100)
print( iface.spoll() )

#%%
val = iface.request(9, '++read 10')
print( val )

#%%
for k in range(10):
    iface.clr()
    time.sleep(.100)
    iface.write(9, 'F1R2A0H0M3D1T3')
    time.sleep(.100)
    iface.trg()
    time.sleep(.100)
    print( iface.spoll() )
    time.sleep(.100)
    val = iface.request(9, '++read 10')
    print( val )
    



#%% 
battery = ngmo.device(iface, 9)
battery.set_voltage('A', 12.4)
battery.set_output('A', True)

time.sleep(1.000)  # delay 1 second

#%%
switcher = hp3488.device(iface, 7)


