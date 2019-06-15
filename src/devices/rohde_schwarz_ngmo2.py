# -*- coding: utf-8 -*-
"""
Created on Sun May 12 21:05:35 2019

@author: simon
"""

class device:
    def __init__(self, iface=None, address=7):
        self.bus = iface
        self.address = address
        self.display = Display(self.bus, self.address)
        self.format = Format(self.bus, self.address, 'ASC')
        self.output = Output(self.bus, self.address)
    
    # Clears all event registers and error queues
    def cls(self):
        self.bus.write(self.address, '*CLS')
    
    # Program the standard event enable register
    def ese(self, num_val=None):
        if (num_val == None):
            # Reads the standard event enable register
            return self.bus.request(self.address, '*ESE?')
        else:
            self.bus.write(self.address, '*ESE ' + str(num_val))

    # Reads the standard event enable register and clears it
    def esr(self):
        return self.bus.request(self.address, '*ESR?')
    
    
    # Returns the manufacturer, model number, serial number, 
    # and firmware revision levels of the unit
    def idn(self):
        return self.bus.request(self.address, '*IDN?')
    
    # Sets the operation complete bit in the standard event register
    def opc(self, val=None):
        if (val == None):
            # Places an ASCII "1" into the output queue 
            return self.bus.request(self.address, '*OPC?')
        else:
            self.bus.write(self.address, '*OPC')
    
    # Returns the power supply to the usersaved setup (0...9)
    # when selected device operations have been completed
    # 0 Factory settings
    # 1 First user setting
    # 9 Ninth user setting
    # MIN Factory settings
    # MAX Ninth user setting
    def rcl(self, val=0):
        if(val.lower() == 'min'):
            val = 0
        if(val.lower() == 'max'):
            val = 9
        if(val in range(0,9)):
            self.bus.write(self.address, '*ESE ' + str(val))
        else:
            raise ValueError('Parameter: {} out of range(0..9)'.format(val))
    
    # Queries the possible min and Max value
    def rcl_q(self, val=None):
        return self.bus.request(self.address, '*RCL?')
    
    # Returns the power supply to the *RST default conditions
    def rst(self):
        self.bus.write(self.address, '*RST')
    
    def reset(self):
        self.rst()
    
    def clear(self):
        self.rst()
        
    # Saves the present setup as the usersaved setup (1..9)
    # 0 Factory settings
    # 1 First user setting
    # 9 Ninth user setting
    # MIN Factory settings
    # MAX Ninth user setting
    def sav(self, val):
        if(val.lower() == 'min'):
            val = 0
        if(val.lower() == 'max'):
            val = 9
        if(val in range(0,9)):
            self.bus.write(self.address, '*SAV ' + str(val))
        else:
            raise ValueError('Parameter: {} out of range(0..9)'.format(val))
    
    def read_sav(self):
        return self.bus.request(self.address, '*SAV?')
    
    # Programs the service request enable register
    def sre(self, num_val):
        num_val = float(num_val)
        self.bus.write(self.address, '*SRE ' + str(num_val))
    
    # Queries the serviee request enable register
    def read_sre(self, num_val):
        num_val = float(num_val)
        return self.bus.request(self.address, '*SRE ' + str(num_val))
    
    # Reads the status byte register
    def stb(self):
        self.bus.request(self.address, '*STB?')
        
    # Sends a “SENSE:PULSE:START ON" command to both channels
    def arm(self):
        self.bus.write(self.address, '*ARM')
        
    # Sends a “SENSE:PULSE:START ON" command to channel A
    def aarm(self):
        self.bus.write(self.address, '*AARM')
    
    # Sends a “SENSE:PULSE:START ON" command to channel B
    def barm(self):
        self.bus.write(self.address, '*BARM')   
    
    # Sends a “SENSE:PULSE:START ON" and a soft trigger
    # command to both channels
    def trg(self):
        self.bus.write(self.address, '*TRG')
        
    # Sends a “SENSE:PULSE:START ON" and a soft trigger
    # command to channel A
    def atrg(self):
        self.bus.write(self.address, '*ATRg')
        
    # Sends a “SENSE:PULSE:START ON" and a soft trigger
    # command to channel B
    def btrg(self):
        self.bus.write(self.address, '*BTRg')
    
    # @TODO: test string compare
    # Performs a checksum test on ROM and returns
    # 0 for test OK and
    # 1 for test failed
    def tst(self):
        if(self.bus.request(self.address, '*TST?') == '1'):
            return True
        else:
            return False
    
    # Waits until all previous commands are executed
    def wait(self):
       self.bus.write(self.address, '*WAI')
       
    
    
    
    
        
        
        
            
    
    
    
    
    #####################################################        
    def get_idn(self):
        value = self.bus.request(self.address, '*IDN?')
        # ROHDE&SCHWARZ,NGMO2,100778,1.16 /A:3:1.14,B:3:1.14
        return value
    
    def send_command(self, command):
        self.bus.write(self.address, command)
    
    def save_preset(self, number):
        if(not 1 <= number <= 9):
            raise ValueError('Preset number must be in range 1 .. 9. number = {}'.format(number))
        self.send_command('*SAV ' + str(round(number, 0))[0])
        
    def get_status(self):
        value = self.bus.request(self.address, '*STB?')
        return value
    
    # Performs a checksum test on ROM and 
    # returns 0 for test OK and 1 for test failed
    def test_rom(self):
        value = self.bus.request(self.address, '*TST?')
        if('0' in value):
            return True
        else:
            return False
            
    def set_output_format(self, form):
        form = form.lower()
        if(form == 'ascii' or form == 'asci'):
            self.bus.write(self.address, ':FORMat:DATA ASCii')
        elif(form == 'long'):
            self.bus.write(self.address, ':FORMat:DATA LONG') # long int
        elif(form == 'short' or form == 'sreal'):
            self.bus.write(self.address, ':FORMat:DATA SREal') # short real
        elif(form == 'double' or form == 'dreal'):
            self.bus.write(self.address, ':FORMat:DATA DREal') # double real
        else:
            raise ValueError('Unknown format specified: {}'.format(form))
    
    def get_output_format(self):
        value = self.bus.request(self.address, ':FORMat:DATA?')
        return value
    
    def set_output_byte_order(self, order):
        order = order.lower()
        if(order == 'normal' or order == 'msbfirst'):
            self.bus.write(self.address, ':FORMat:BORDer NORMal')
        elif(order == 'swapped' or order == 'lsbfirst'):
            self.bus.write(self.address, ':FORMat:BORDer SWAPped')




# Inner Class for some easier Syntax
class Display:
    def __init__(self, bus, addr):
        self.bus= bus
        self.address = addr
        
    # @TODO Test if lower case letters can be left away
    # Enables or disables the LC Display
    def enable(self, on=True):
        if(on == True):
            self.display = True
            self.bus.write(self.address, ':DISP:ENAB:ON')
        else:
            self.display = False
            self.bus.write(self.address, ':DISP:ENAB:OFF')
        
    # Queries status of display
    def enabled(self):
        val = self.bus.request(self.address, ':DISP:ENAB?')
        if('on' in val.lower()):
            self.display = True
            return True
        elif('off' in val.lower()):
            self.display = False
            return False
        else:
            raise RuntimeError('Unhandled value from NGMO2: {}'.format(val))
            
    # Changes the active display channel
    def set_channel(self, channel):
        channel = channel.lower()
        if(channel == 'a' or channel == 'min'):
            cmd = 'A'
        elif(channel == 'b' or channel == 'max'):
            cmd = 'B'
        elif(channel == 'dvm a'):
            cmd = 'DVMA'
        elif(channel == 'dvm b'):
            cmd = 'DVMB'
        elif(channel == 'def'):
            cmd = 'DEF'
        else:
            raise ValueError('Unknown channel setting: {}'.format(channel))
        
    
    def selected_channel(self):
        val = self.bus.request(self.address, ':DISP:CHAN?')
        return val
    
class Format:
    def __init__(self, bus, addr, char_val):
        self.bus= bus
        self.address = addr
        # @TODO filter char_val
        self.a_format = char_val
        self.data(char_val)
        
    # Specifies the output data format for Fetch, Read and Message command.
    def data(self, char_val):
        char_val = char_val.lower()
        if('asc' in char_val or 'min' in char_val or 'def' in char_val):
            cmd = 'ASC'
        elif('long' in char_val):
            cmd = 'LONG'
        elif('short' in char_val or 'sre' in char_val):
            cmd = 'SRE'
        elif('double' in char_val or 'dre' in char_val or 'max' in char_val):
            cmd = 'DRE'
        else:
            raise ValueError('Unknown data format: {}'.format(char_val))
        self.a_data = char_val
        self.bus.write(self.address, ':FORM:DATA:' + str(cmd))
    
    def get_data(self):
        val = self.bus.request(self.address, ':FORM:DATA?')
        return val
    
    # Specifies byte order for non ASCII output formats.
    def border(self, char_val):
        char_val = char_val.lower()
        if('norm' in char_val or 'min' in char_val or 'def' in char_val):
            cmd = 'NORM'
        elif('swap' in char_val or 'max' in char_val):
            cmd = 'SWAP'
        else:
            raise ValueError('Unknown border format: {}'.format(char_val))
        self.a_border = char_val
        self.bus.write(self.address, ':FORM:BORD:' + str(cmd))
        
class Output:
    def __init__(self, bus, addr, char_val=None):
        self.bus= bus
        self.address = addr
        
        self.a = Channel(self.bus, self.address, 'A')
        self.b = Channel(self.bus, self.address, 'B')
        
        self.relay1 = Relay(self.bus, self.address, 1)
        self.relay2 = Relay(self.bus, self.address, 2)
        self.relay3 = Relay(self.bus, self.address, 3)
        self.relay4 = Relay(self.bus, self.address, 4)
        
    
    def open_sense(self, on=True):
        self.a_open_sense = on
        if(on == True):
            self.bus.write(self.address, ':OUT:OPEN:ON')
        else:
            self.bus.write(self.address, ':OUT:OPEN:OFF')
    
    def band_width(self, char_val):
        self.a_bandwidt = char_val
        # @TODO
    
    # Specifies the output impedance to apply. 0 Ohms to 
    # 1Ohms in 10 mOhm steps
    def impedance(self, val=0.00):
        self.a_impedance = val
    
class Relay:
    def __init__(self, bus, addr, num=1):
        self.bus= bus
        self.address = addr
        if(num not in range(1,5)):
            raise ValueError('Relay not in range 1-4: {}'.format(num))
        self.num = num
    
    def open(self):
        self.bus.write(self.address, ':OUT:RELay:' + str(self.num) + 'OFF')
    
    def close(self):
        self.bus.write(self.address, ':OUT:RELay:' + str(self.num) + 'ONE')
    
class Channel:
    def __init__(self, bus, addr, char_val=None):
        self.bus= bus
        self.address = addr
        # @TODO filter char_val
        if(char_val not in 'ABab' or len(char_val) != 1):
            raise ValueError('Channel can only be "A" or "B". channel = {}'.format(char_val))
        self.letter = char_val.upper()
    
    def on(self):
        self.bus.write(self.address, ':OUT:' + self.letter + ':ON')
    
    def off(self):
        self.bus.write(self.address, ':OUT:' + self.letter + ':OFF')
        
    # get state
    def is_on(self):
        val = self.bus.request(self.address, ':OUT:' + self.letter + 'STAT?')
        
    def voltage(self, voltage=0.0):
        # 3.3 specifications (0-15V)
        if(not 0 <= voltage <= 15):
            raise ValueError('Voltage must be in range(0, 30). voltage = {}'.format(voltage))
        voltage = round(voltage, 3)  # 1mV resolution
        self.bus.write(self.address, ':SOUR:' + self.letter + ':VOLT ' + str(voltage))

    # Selects Fetch, Read, Measure function type
    def sense(self, meas_type='VOLT'):
        self.a_meas_typ = meas_type
    
        
                    
            
            
            
            