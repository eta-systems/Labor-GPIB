# -*- coding: utf-8 -*-

# This Superclass is dead
# Superclasses are ugly as fuck!

class gpib_device:
    def __init__(self, iface=None, address=None):
        self.bus = iface
        self.address = address
        
    def d_write(self, command):
        self.bus.write(self.address, command)
    
    def d_set_address(self, address):
        if(address in range(0, 30)):
            if(address != self.address):
                self.address = address
                self.bus.set_address(address)
        else:
            raise ValueError('GPIB address {} not in range 0-30 (integer)'.format(address))
        
    # (!) because read() is a standard function
    def d_read(self):
        return self.bus.read(self.address)
    
    def d_read_eoi(self):
        return self.d_request('++read eoi')
    
    def d_read_until_char(self, char):
        return self.d_request(str(char))
    
    def d_request(self, message):
        print('requesting: ' + str(message))
        self.d_write(message)
        ret = self.d_read()
        # ret = self.instr.query(message)
        return ret

    def d_spoll(self):
        return self.bus.spoll()
    