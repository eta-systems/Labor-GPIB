# -*- coding: utf-8 -*-
"""
Created on Tue May 14 09:33:31 2019

@author: simon

for hp 3488a switch control unit
"""

"""

page 63, standard commands

CTYPE 1
++read 10
VHF SW     44472
CTYPE 2
++read 10
NO CARD    00000
CTYPE 3
++read 10
DIGITAL IO 44474
CTYPE 4
++read 10
GP RELAY   44471
CTYPE 5
++read 10
GP RELAY   44471

---

CRESET 4    # CARD RESET

---

CPAIR

---

CMON

---

SLIST101,401
STEP
STEP

---

ID?
++read 10
HP3488A

---

asdf
STATUS
++read 10
+00032        # --> Error

0 1 End of scan sequence
1 2 Output available
2 4 Powereon SRO asserted
3 8 Front panel SRO key pressed
4 16 Ready for instructions
5 32 Error
6 64 R08
7 i28 Not used

ERROR
++read 10
+00001          # --> Syntax Error

l Syntax Error
2 Execution Error
possibie meanings include:
a F’arameter out of range
b. Card type n’résmatch
or Attempt to access a nonexistent stored state or scan list.
4 Hardware Trigger too Fast
8 Logic Failure
16 Power Supply Failure

---

DON / DOFF  # display on/off

---

OPEN 101     # CARD,SLOT
CLOSE 101

---

LOCK 1  # lock the keyboard --> faster operation

"""


class device:
    def __init__(self, iface=None, address=9):
        self.bus = iface
        self.address = address
        self.cards = [None, None, None, None, None]
    
    def relay_open(self, card, channel):
        # card in range 1 - 5
        # channel in range 0 - 15 ?
        return None
    
    def _write(self, cmd):
        self.bus.write(self.address, cmd)
        
    def read_val(self):
        return self.bus.read_until_char(self.address, '10')
        
    def set_slot(self, slot, card):
        if(card in range(44470, 44476)):
            self.cards[slot] = Card(self, slot, card)
        else:
            raise ValueError('Card out of range')
        
    def channel(self, slot):
        return self.cards[slot]

        
class Card:
    def __init__(self, motherboard, slot, card):
        self.mother = motherboard
        self.ch_range = range(0, 11)
        self.slot = slot
        self.card = card
        
        self.mother._write('CTYPE ' + str(slot))
        val = self.mother.read_val()
        number = int(''.join(i for i in val if i.isdigit()))
#        if not(str(number) is str(self.card)):
#            raise RuntimeError('Cardtype: ' + str(card) + ' does not match card present: ' + str(number))
        return
    
    def open(self, channel):
        if(channel in self.ch_range):
            # must be in the format 101 where 1 is slot and 01 is channel
            # :02d is adding the leading zero
            self.mother._write('OPEN ' + str(self.slot) + str("{:02d}".format(channel)))
        else:
            raise ValueError('channel out of range')
        
    def close(self, channel):
        if(channel in self.ch_range):
            # must be in the format 101 where 1 is slot and 01 is channel
            # :02d is adding the leading zero
            self.mother._write('CLOSE ' + str(self.slot) + str("{:02d}".format(channel)))
        else:
            raise ValueError('channel out of range')

"""
VIEW 401
++read 10
OPEN   1
CLOSE 401
VIEW 401
++read 10
CLOSED 0
"""

"""
DWRITE 301,124
DWRITE 301,555
CTYPE 3
++read 10
DIGITAL IO 44474
"""

"""
DREAD 301
++read 10
+00255
"""













