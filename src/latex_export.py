# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 16:03:54 2019

@author: simon
"""

#%%
from latex.lib.DocCreator import DocCreator
import json

datloc = '../results/values_86percent_efficiency.json'
with open(datloc) as fil:
    prev_data = json.load(fil)

#%%
replaceables = {}
replaceables['REPLACE-SERIAL-NUMBER'] = 'SN_00042'
replaceables['REPLACE-PCB-VERSION'] = "128_2.505.101.01_SG midi Main"
replaceables['REPLACE-OPERATOR'] = "BSI"
replaceables['REPLACE-SCRIPT-VERSION'] = "nightly"
replaceables['REPLACE-VOLTAGE-INPUT'] = 12.3
replaceables['REPLACE-CURRENT-OUT-MIN'] = 0.1
replaceables['REPLACE-CURRENT-OUT-MAX'] = 2.0
replaceables['REPLACE-DPOINTS'] = 100

#%%
cre = DocCreator()
cre.new_report(data=prev_data, strings=replaceables)
cre.replace_strings()
cre.make_pdf()

