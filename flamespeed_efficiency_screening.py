# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 15:14:12 2018

@author: HP USER
"""

import os
import efficiency_manipulate as em
import numpy as np
import cantera as ct
import soln2cti as ctiw
import ntpath
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import matplotlib.pyplot as plt
import free_flame as ff
import pandas as pd
outputfile=os.getcwd()+'\\figures\\collider_screening\\col_screen_flamespeed.txt'

nominal_models=[os.getcwd()+'\\Mechanisms\\FFCM-1\\FFCM1.cti',
                os.getcwd()+'\\Mechanisms\\Aramco2.0\\chem.cti',
                os.getcwd()+'\\Mechanisms\\nheptane\\nheptane.cti',
                os.getcwd()+'\\Mechanisms\\cyclohexane\\chem.cti',
                os.getcwd()+'\\Mechanisms\\isopentanol\\chem.cti',
                os.getcwd()+'\\Mechanisms\\UdatedH2Model110725\\chem.cti']

nominal_models=[os.getcwd()+'\\Mechanisms\\cyclohexane\\chem.cti']
nominal_models=[os.getcwd()+'\\Mechanisms\\nheptane\\nheptane.cti']
#nominal_models=[os.getcwd()+'\\Mechanisms\\isopentanol\\chem.cti']
#nominal_models=[os.getcwd()+'\\Mechanisms\\UdatedH2Model110725\\chem.cti']
nominal_models=[os.getcwd()+'\\Mechanisms\\Aramco2.0\\chem.cti']
#nominal_models=[os.getcwd()+'\\Mechanisms\\FFCM-1\\FFCM1.cti']

#nominal_models=[os.getcwd()+'\\Mechanisms\\nheptane\\nheptane.cti',
#                os.getcwd()+'\\Mechanisms\\cyclohexane\\chem.cti']
modified_models=[]

fuels=[['CH4','CH3OH','C2H2'],
       ['CH4','C2H6','C2H4','C2H2','C3H8','C3H6','C3H4','C4H10','IC4H10','C4H8-1','C4H8-2','IC4H8','C4H6-1','C4H6-2','C4H6','C4H612'],
       ['NC7H16'],
       ['chx'],
       ['ic5h11oh'],
       ['H2']]
fuels=[['chx']]
fuels=[['CH4','CH3OH','C2H2']]
#fuels=[['NC7H16']]
#fuels=[['ic5h11oh']]
#fuels=[['H2']]
fuels=[['CH4','C2H6','C2H4','C2H2','C3H8','C3H6','C3H4','C4H10','IC4H10','C4H8-1','C4H8-2','IC4H8','C4H6-1','C4H6-2','C4H6','C4H612']]
#fuels=[['NC7H16'],
#       ['chx']]
P=[1.0]
phi=[0.5,1.0,2.0,4.0]
phi=np.arange(0.5,5.0,1.0)
T=[400]
#reactorType='cv'
val='all'

coeffs=[[2.0,1.5,2.5],
        [2.0,3.5,3.0,2.5,5.0,4.5,4.0,6.5,6.5,6.0,6.0,6.0,5.5,5.5,5.5,5.5],
        [11.0],
        [9.0],
        [7.5],
        [1.0]]
coeffs=[[9.0]]
coeffs=[[2.0,1.5,2.5]]
#coeffs=[[11.0]]
#coeffs=[[7.5]]
#coeffs=[[1.0]]
coeffs=[[2.0,3.5,3.0,2.5,5.0,4.5,4.0,6.5,6.5,6.0,6.0,6.0,5.5,5.5,5.5,5.5]]
#coeffs=[[11.0],
#        [9.0]]
for i in nominal_models:
    gas=ct.Solution(i)
    gas.name='igDelayRateSwap_'+i.split('\\')[-1].rstrip('.cti')
    gas2=em.efficiency_rate_swap(gas,[val])
    newfilename=ntpath.dirname(i)+'\\modified2_'+ntpath.basename(i)
    new_file=ctiw.write(gas2,newfilename)
    modified_models.append(new_file)
    
    
conditionsTup=[]
for n in np.arange(len(nominal_models)):
    for p in np.arange(len(P)):
        for i in np.arange(len(T)):
            for subf in np.arange(len(fuels[n])):
                    oxidizer={}
                    oxidizer={'O2':coeffs[n][subf],'N2':3.76*coeffs[n][subf]}
                    conditionsTup.append([nominal_models[n],modified_models[n],P[p],phi,fuels[n][subf],oxidizer,T[i]])
                    
width=0.3
def solver(width,conditions,results,output):
    phi=conditions[3]
    nominals=[]
    modifieds=[]
    for i in np.arange(len(phi)):
        try:
            oxidizer=conditions[5]
            nominal_model=conditions[0]
            modified_model=conditions[1]
            pressure=conditions[2]
            fuel=conditions[4]
            T=conditions[6]
            #print(phi[i],fuel,oxidizer)
            gas=ct.Solution(nominal_model)
            gas.TP=T,pressure*ct.one_atm
            results.append(ff.free_flame(phi[i],fuel,oxidizer,gas,width,kinetic_sens=0,energycon=True,flamespeed_sens=1,soret=False))
            results[-1].add_mechanism(nominal_model)
            results[-1].add_fuel(fuel)
            nominals.append(results[-1].solution['u'][0])
        except:
            nominals.append('failed')
        
    for i in np.arange(len(phi)):
        try:
            oxidizer=conditions[5]
            nominal_model=conditions[0]
            modified_model=conditions[1]
            pressure=conditions[2]
            fuel=conditions[4]
            T=conditions[6]
            gas2=ct.Solution(modified_model)
            gas2.TP=T,pressure*ct.one_atm
            #print(phi[i],fuel,oxidizer)
            results.append(ff.free_flame(phi[i],fuel,oxidizer,gas2,width,kinetic_sens=0,energycon=True,flamespeed_sens=1,soret=False))
            results[-1].add_mechanism(modified_model)
            results[-1].add_fuel(fuel)
            #differences=results[-1].solution['u'][0]-results[-2].solution['u'][0]
            #percent_diff=100.0*np.divide(differences,results[-2].solution['u'][0])
            modifieds.append(results[-1].solution['u'][0])
        except:
            modifieds.append('failed')
        #results[-1].percent_diff(percent_diff)
    #print(phi)
    #print(nominals)
#    if 'failed' not in modifieds and 'failed' not in nominals:
#        plt.figure()
#        plt.plot(phi,nominals,'b-')
#        plt.plot(phi,modifieds,'r--')
#        plt.savefig(os.getcwd()+'\\figures\\collider_screening\\'+ntpath.dirname(nominal_model).split('\\')[-1]+'_'+fuel+'_'+str(pressure)+'atm'+str(T)+'K_flamespeed'+'.pdf',dpi=1200,bbox_inches='tight')
    if 'failed' in modifieds or 'failed' in nominals:
        tempn=[]
        tempm=[]
        tempp=[]
        for i in np.arange(len(modifieds)):
            if modifieds[i]!='failed' and nominals[i]!='failed':
               tempp.append(phi[i])
               tempm.append(modifieds[i])
               tempn.append(nominals[i])
        phi=tempp
        nominals=tempn
        modifieds=tempm
    if len(nominals)>0 and len(phi)>0 and len(modifieds)>0:
        plt.figure()
        plt.plot(phi,nominals,'b-')
        plt.plot(phi,modifieds,'r--')
        plt.savefig(os.getcwd()+'\\figures\\collider_screening\\'+ntpath.dirname(nominal_model).split('\\')[-1]+'_'+fuel+'_'+str(pressure)+'atm'+str(T)+'K_flamespeed'+'.pdf',dpi=1200,bbox_inches='tight')
        a=pd.DataFrame(columns=['phi','nominal','modified'])
        a['phi']=phi
        a['nominal']=nominals
        a['modified']=modifieds
        a.to_csv(os.getcwd()+'\\figures\\collider_screening\\'+ntpath.dirname(nominal_model).split('\\')[-1]+'_'+fuel+'_'+str(pressure)+'atm'+str(T)+'K_flamespeed.csv',index=False)
        diffs=np.subtract(nominals,modifieds)
        percent_diffs=100.0*np.divide(diffs,nominals)
        max_dif=np.max(np.abs(percent_diffs))
    
        with open(output,'a') as f:
            f.write('Model: '+nominal_model.split('\\')[-2]+', Pressure: '+str(pressure)+', Fuel: '+fuel+'\n   Max Percent Difference: '+str(max_dif)+'\n')
    elif not modifieds:
        with open(output,'a') as f:
            f.write('Model: '+nominal_model.split('\\')[-2]+', Pressure: '+str(pressure)+', Fuel: '+fuel+'\n   Max Percent Difference: failed'+'\n')
 
        
        #return results

results=[]
for i in conditionsTup:
    solver(width,i,results,outputfile)
    
    