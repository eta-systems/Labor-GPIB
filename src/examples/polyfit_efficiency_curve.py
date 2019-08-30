# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 08:42:25 2019

@author: simon
"""

#%%
import json
import numpy as np

datloc = '../results/values_SGmini_5V_USB.json'
with open(datloc) as fil:
    prev_data = json.load(fil)

val = prev_data

# apply polyfit
degree = 20
coef = np.polyfit(val['load']['current'][1:], val['efficiency'][1:], degree)
n = len(val['load']['current'])
x = np.linspace(val['load']['current'][1], val['load']['current'][-1], n)
y = np.zeros(n)
for i in range(degree):
    y = y + pow(x, degree-i) * coef[i]
y = y + coef[degree]

plt.figure(figsize=(8,5))
plt.plot(val['load']['current'][1:], val['efficiency'][1:], marker='x', linestyle='None', color='skyblue')
plt.plot(x,y, marker='None', linestyle='solid', color='royalblue')
plt.ylim(0.55, 0.90)
plt.xlabel(r'load current $I_L$ [A]')
plt.ylabel(r'efficiency coefficient $\eta$')
plt.title('Efficiency vs. Load Current')
plt.grid()
#plt.savefig('Efficiency_vs_LoadCurrent.pdf')
plt.savefig('Efficiency_vs_LoadCurrent.png', dpi=200)  # 200dpi -> 1600x1000



