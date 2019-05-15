# PythonDeviceWrapper

---

Wrapper for several GPIB controllable devices.

(still work in progress)

The goal of this project is, to enable easy scripting of measurement procedures using a higher abstracction layer for GPIB devices.

---

### Example
```python
import interface.prologix_gpib as prologix
import devices.rohde_schwarz_ngmo2 as ngmo

iface = prologix.usb(com='ASRL1::INSTR', baudrate=19200, timeout=2000)

battery = ngmo.device(iface, 7)  # ngmo at address 7
battery.set_voltage('A', 12.4)   # set to 12.4 V
battery.set_output('A', True)    # turn on
```


