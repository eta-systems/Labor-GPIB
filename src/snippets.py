# -*- coding: utf-8 -*-



#%%
schlumi = schlumberger.device(iface, 13)

values = np.zeros(100)              # leeres Array mit 100 Werten
for i in range(0, len(values)):
    schlumi.trigger()               # single shot
    values[i] = schlumi.read()      # Wert lesen
    time.sleep(0.1)                 # 100ms warten

plt.plot(values)                    # plotten
plt.ylabel('U [V]')
plt.xlabel('Messung Nr.')







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


#%%
iface = prologix.usb(com='ASRL31::INSTR', baudrate=19200, timeout=5000)
iface.loc()  # Lokaler Modus
schlumi = schlumberger.device(iface, 13)

#%%
schlumi.measurement('vdc')         # Vdc
schlumi.range('auto')             # autorange
schlumi.integral_period('0.006') # 6.66ms
schlumi.trigger_type('single')  # single shot
schlumi.units(False)                    # keine Einheiten

values = np.zeros(20)                   # leeres Array mit 20 Werten

#%%
for i in range(0, 20):
    schlumi.trigger()           # single shot
    values[i] = schlumi.read()  # Wert lesen, dauert min. 6.66ms

plt.plot(values)                # plotten
plt.ylabel('U [V]')
plt.xlabel('Messung Nr.')

#%%

hp34 = hp3455.device(iface, 9)  # address 9 on prologix interface

#%%
values = np.zeros(20)         # leeres Array mit 20 Werten

for i in range(0, 20):
    hp34.trigger()            # single shot
    values[i] = hp34.read_rqs()

plt.plot(values)                # plotten
plt.ylabel('U [V]')
plt.xlabel('Messung Nr.')




