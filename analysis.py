# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 18:09:02 2018

@author: Mark Barbet
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

output='C:\\Users\\HP USER\\Google Drive\\Burke Group\\Codes\\figures\\collider_screening\\col_screen.txt'
n=10

with open(output,'r') as f:
    lines=f.readlines()
    
final_max=[]
all_max=[]
final_max_log=[]
all_max_log=[]
final_conds=[]
all_conds=[]

for i in np.arange(len(lines)):
    #temp=[]
    if i%2==0 and 'failed' not in lines[i+1]:
        all_conds.append(lines[i])
        all_max.append(float(lines[i+1].split(',')[0].split(':')[-1]))
        all_max_log.append(float(lines[i+1].split(',')[1].split(':')[-1].strip('\n')))
        
dataframe=pd.DataFrame(columns=['Conditions','Max Abs','Max Log'])
dataframe['Conditions']=all_conds
dataframe['Max Abs']=all_max
dataframe['Max Log']=all_max_log

max_abs=dataframe.sort_values(by=['Max Abs'],ascending=False)
max_abs=max_abs[0:n-1]

max_log=dataframe.sort_values(by=['Max Log'],ascending=False)
max_log=max_log[0:n-1]

