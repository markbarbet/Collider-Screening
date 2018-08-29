# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 00:29:44 2018

@author: HP USER
"""

import os
import efficiency_manipulate as em
import ig_delay as ig
import numpy as np
import cantera as ct
import soln2cti as ctiw
import ntpath
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import matplotlib.pyplot as plt

nominal_models=[os.getcwd()+'\\Mechanisms\\Aramco2.0\\chem.cti',
                os.getcwd()+'\\Mechanisms\\nheptane\\nheptane.cti',
                os.getcwd()+'\\Mechanisms\\cyclohexane\\chem.cti',
                os.getcwd()+'\\Mechanisms\\isopentanol\\chem.cti',
                os.getcwd()+'\\Mechanisms\\UdatedH2Model110725\\chem.cti']
nominal_models=[os.getcwd()+'\\Mechanisms\\cyclohexane\\chem.cti']
nominal_models=[os.getcwd()+'\\Mechanisms\\nheptane\\nheptane.cti']
nominal_models=[os.getcwd()+'\\Mechanisms\\isopentanol\\chem.cti']
#nominal_models=[os.getcwd()+'\\Mechanisms\\UdatedH2Model110725\\chem.cti']
nominal_models=[os.getcwd()+'\\Mechanisms\\Aramco2.0\\chem.cti']


#nominal_models=[os.getcwd()+'\\Mechanisms\\nheptane\\nheptane.cti',
#                os.getcwd()+'\\Mechanisms\\cyclohexane\\chem.cti']
modified_models=[]

fuels=[['CH4','C2H6','C2H4','C2H2','C3H8','C3H6','C3H4','C4H10','IC4H10','C4H8-1','C4H8-2','IC4H8','C4H6-1','C4H6-2','C4H6','C4H612'],
       ['NC7H16'],
       ['chx'],
       ['ic5h11oh'],
       ['H2']]
fuels=[['chx']]
fuels=[['NC7H16']]
fuels=[['ic5h11oh']]
fuels=[['H2']]
fuels=[['CH4','C2H6','C2H4','C2H2','C3H8','C3H6','C3H4','C4H10','IC4H10','C4H8-1','C4H8-2','IC4H8','C4H6-1','C4H6-2','C4H6','C4H612']]
#fuels=[['NC7H16'],
#       ['chx']]
#fuels=[['C2H2']]
P=[1.0,10.0,100.0]
#P=[1.0]
phi=[0.5,1.0,2.0,4.0]
#phi=[4.0]
T=np.arange(500.0,2000.0,300)
reactorType='cv'
val='all'
outputfile=os.getcwd()+'\\figures\\collider_screening\\col_screen.txt'
coeffs=[[2.0,3.5,3.0,2.5,5.0,4.5,4.0,6.5,6.5,6.0,6.0,6.0,5.5,5.5,5.5,5.5],
        [11.0],
        [9.0],
        [7.5],
        [1.0]]
coeffs=[[9.0]]
coeffs=[[11.0]]
coeffs=[[7.5]]
#coeffs=[[2.5]]
coeffs=[[1.0]]
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
#for n in np.arange(len(nominal_models)):
#    for p in np.arange(len(P)):
#        for i in np.arange(len(phi)):
#            for f in np.arange(len(fuels)):
#                for subf in np.arange(len(fuels[f])):
#                    X={}
#                    X={fuels[f][subf]:phi[i],'O2':coeffs[f][subf],'N2':3.76*coeffs[f][subf]}
#                    conditionsTup.append([nominal_models[n],modified_models[n],P[p],phi[i],fuels[f][subf],X,T])
for n in np.arange(len(nominal_models)):
    for p in np.arange(len(P)):
        for i in np.arange(len(phi)):
            #for f in np.arange(len(fuels)):
                for subf in np.arange(len(fuels[n])):
                    X={}
                    X={fuels[n][subf]:phi[i],'O2':coeffs[n][subf],'N2':3.76*coeffs[n][subf]}
                    conditionsTup.append([nominal_models[n],modified_models[n],P[p],phi[i],fuels[n][subf],X,T])
def solver(conditions,output):
            import matplotlib.pyplot as plt

            nominal_model=conditions[0]
            modified_model=conditions[1]
            P=conditions[2]
            phi=conditions[3]
            fuels=conditions[4]
            X=conditions[5]
            T=conditions[6]
            print('Working on '+fuels+' at phi='+str(phi)+', '+str(P)+' atm.')
            
            #X={Fuels[f]:phi[x],'O2':num[f],'N2':3.76*num[f]}
            #efficiency_manipulate=True
            reactorType='cv'
            nominalDelays=[]
            modifiedDelays=[]
            for j in np.arange(len(T)):
                try:
                    try:
                        nominalDelays.append(ig.ignition_delay(nominal_model,T[j],P,X,options=reactorType))
                    except:
                        new_dict={}
                        new_dict[fuels]=X.pop(fuels)
                        new_dict['o2']=X.pop('O2')
                        new_dict['n2']=X.pop('N2')
                        nominalDelays.append(ig.ignition_delay(nominal_model,T[j],P,new_dict,options=reactorType))
                except:
                    nominalDelays.append('Temperature '+str(T[j])+'K failed')
            for j in np.arange(len(T)):
                try:
                    try:
                        modifiedDelays.append(ig.ignition_delay(modified_model,T[j],P,X,options=reactorType))
                    except:
                        new_dict={}
                        new_dict[fuels]=X.pop(fuels)
                        new_dict['o2']=X.pop('O2')
                        new_dict['n2']=X.pop('N2')
                        modifiedDelays.append(ig.ignition_delay(modified_model,T[j],P,new_dict,options=reactorType))
                except:
                    modifiedDelays.append('Temperature '+str(T[j])+'K failed')
#            for i in np.arange(len(files)):
#                #gas=ct.Solution(mechanism[i])
#                delays.append([])
#                for j in np.arange(len(T)):
#                    try:
#                        delays[i].append(ig.ignition_delay(files[i],T[j],p,X,options=reactorType))
#                    except:
#                        delays[i].append('Temperature '+str(T[j])+'K failed')
            plt.figure()
            #colors=['b','r','k','g','c','m']
            #for i in np.arange(len(files)):
            tempdel=[]
            tempT=[]
            for j in np.arange(len(np.array(nominalDelays))):
                if str(type(nominalDelays[j]))!="<type 'str'>":
                        tempdel.append(nominalDelays[j])
                        tempT.append(T[j])
            plt.plot(1000.0/np.array(tempT),np.log10(tempdel),'b-')
            plt.title(fuels+' at phi= '+str(phi)+', '+str(P)+' atm')
            tempdel1=[]
            tempT1=[]
            for j in np.arange(len(np.array(modifiedDelays))):
                if str(type(modifiedDelays[j]))!="<type 'str'>":
                        tempdel1.append(modifiedDelays[j])
                        tempT1.append(T[j])
            plt.plot(1000.0/np.array(tempT1),np.log10(tempdel1),'r--')
            plt.savefig(os.getcwd()+'\\figures\\collider_screening\\'+ntpath.dirname(nominal_model).split('\\')[-1]+'_'+fuels+'_'+str(P)+'atm_phi'+str(phi)+'.pdf',dpi=1200,bbox_inches='tight')  
            try:
                differences=np.subtract(tempdel,tempdel1)
                percent_diff=100*np.divide(differences,tempdel)   
                max_dif=np.max(np.abs(percent_diff))
                conditions.append(max_dif)
                logdiffs=np.subtract(np.log10(tempdel),np.log10(tempdel1))
                percent_logdiff=100*np.divide(logdiffs,np.log10(tempdel))
                max_logdif=np.max(np.abs(percent_logdiff))
                l=[tempT,tempdel,tempT1,tempdel1]
                l=zip(*l)
                datafile=os.getcwd()+'\\figures\\collider_screening\\'+nominal_model.split('\\')[-2]+'_P'+str(P)+'_phi'+str(phi)+'_'+fuels+'.txt'
                with open(output,'a') as f:
                    f.write('Model: '+nominal_model.split('\\')[-2]+', Pressure: '+str(P)+', phi: '+str(phi)+', Fuel: '+fuels+'\n   Max Percent Difference: '+str(max_dif)+', Max Percent Difference log: '+str(max_logdif)+'\n')
                #print(l)
                with open(datafile,'w') as f:
                    f.write('T,t,T1,t1\n')
                    for i in l:
                        f.write(str(i[0])+', '+str(i[1])+', '+str(i[2])+', '+str(i[3])+'\n')
            except:
                conditions.append('Failed to find max for some reason-maybe modified mechanism failed')
                with open(output,'a') as f:
                    f.write('Model: '+nominal_model.split('\\')[-2]+', Pressure: '+str(P)+', phi: '+str(phi)+', Fuel: '+fuels+'\n   Max Percent Difference: '+'failed'+', Max Percent Difference log: '+'failed'+'\n')
                
            return conditions
results=[]
for conditions in conditionsTup:
        results.append(solver(conditions,outputfile))
#            nominal_model=conditions[0]
#            modified_model=conditions[1]
#            P=conditions[2]
#            phi=conditions[3]
#            fuels=conditions[4]
#            X=conditions[5]
#            T=conditions[6]
#            print('Working on '+fuels+' at phi='+str(phi)+', '+str(P)+' atm.')
#            
#            #X={Fuels[f]:phi[x],'O2':num[f],'N2':3.76*num[f]}
#            #efficiency_manipulate=True
#            reactorType='cv'
#            nominalDelays=[]
#            modifiedDelays=[]
#            for j in np.arange(len(T)):
#                try:
#                    try:
#                        nominalDelays.append(ig.ignition_delay(nominal_model,T[j],P,X,options=reactorType))
#                    except:
#                        new_dict={}
#                        new_dict[fuels]=X.pop(fuels)
#                        new_dict['o2']=X.pop('O2')
#                        new_dict['n2']=X.pop('N2')
#                        nominalDelays.append(ig.ignition_delay(nominal_model,T[j],P,new_dict,options=reactorType))
#                except:
#                    nominalDelays.append('Temperature '+str(T[j])+'K failed')
#            for j in np.arange(len(T)):
#                try:
#                    try:
#                        modifiedDelays.append(ig.ignition_delay(modified_model,T[j],P,X,options=reactorType))
#                    except:
#                        new_dict={}
#                        new_dict[fuels]=X.pop(fuels)
#                        new_dict['o2']=X.pop('O2')
#                        new_dict['n2']=X.pop('N2')
#                        modifiedDelays.append(ig.ignition_delay(modified_model,T[j],P,new_dict,options=reactorType))
#                except:
#                    modifiedDelays.append('Temperature '+str(T[j])+'K failed')
##            for i in np.arange(len(files)):
##                #gas=ct.Solution(mechanism[i])
##                delays.append([])
##                for j in np.arange(len(T)):
##                    try:
##                        delays[i].append(ig.ignition_delay(files[i],T[j],p,X,options=reactorType))
##                    except:
##                        delays[i].append('Temperature '+str(T[j])+'K failed')
#            plt.figure()
#            #colors=['b','r','k','g','c','m']
#            #for i in np.arange(len(files)):
#            tempdel=[]
#            tempT=[]
#            for j in np.arange(len(np.array(nominalDelays))):
#                if str(type(nominalDelays[j]))!="<type 'str'>":
#                        tempdel.append(nominalDelays[j])
#                        tempT.append(T[j])
#            plt.semilogy(1000.0/np.array(tempT),tempdel,'b-')
#            plt.title(fuels+' at phi= '+str(phi)+', '+str(P)+' atm')
#            tempdel=[]
#            tempT=[]
#            for j in np.arange(len(np.array(modifiedDelays))):
#                if str(type(modifiedDelays[j]))!="<type 'str'>":
#                        tempdel.append(modifiedDelays[j])
#                        tempT.append(T[j])
#            plt.semilogy(1000.0/np.array(tempT),tempdel,'r--')
#            plt.savefig(os.getcwd()+'\\figures\\collider_screening\\'+'test_'+ntpath.dirname(nominal_model).split('\\')[-1]+'_'+fuels+'_'+str(P)+'atm_phi'+str(phi)+'.pdf',dpi=1200,bbox_inches='tight')                
#                
                
#pool = ThreadPool(4) 
#results = results+pool.map(solver,conditionsTups)
#pool.map(solver,conditionsTup)