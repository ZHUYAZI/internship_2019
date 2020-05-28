#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 12:57:35 2019

@author: yazi
"""

import pandas as pd
import geopandas as gpd
from datetime import timedelta
from datetime import datetime

class treat():
    def __init__(self,OD_file,Parc_file,gare_file):
        self.data0=pd.read_csv(OD_file,delimiter=';',encoding='iso 8859-1',dtype=str)
        self.data_parc=gpd.read_file(Parc_file)
        self.gare_position = gpd.read_file(gare_file,encoding='latin-1')
        self.parc_list_name=list(self.data_parc['nom_gare'].apply(lambda x: x.split(" (")[0]))
        self.data_first=self.rebuild_data_first()
        self.data_last=self.rebuild_data_last()
        
    def rebuild_data_first(self):
        data_list0=pd.DataFrame()
        for i in range(len(self.parc_list_name)):
            data_temp=self.data0[(self.data0['O']==self.parc_list_name[i])&(self.data0['trip_id']=='1.0')]
            data_list0=data_list0.append(data_temp)  
            
        data_list0=data_list0.dropna()
        data_list0=data_list0.reset_index(drop=True)
        data_list0['Ot']=data_list0['Ot'].apply(lambda x:x.split(' ')[-1])
        data_list0['Dt']=data_list0['Dt'].apply(lambda x:x.split(' ')[-1])
        return data_list0
    
    def rebuild_data_last(self):
        data1=self.data0.copy()
        data1=data1.groupby('client_id').last()
        data1=data1.reset_index(drop=True)
        data1['Ot']=data1['Ot'].apply(lambda x:datetime.strptime(str(x),'%Y-%m-%d %H:%M:%S'))
        data1['Dt']=data1['Ot']+timedelta(minutes=30)
        
        data_list1=pd.DataFrame()
        for i in range(len(self.parc_list_name)):
            data_temp=data1[(data1['D']==self.parc_list_name[i])]
            data_list1=data_list1.append(data_temp)   
        
        data_list1=data_list1.dropna()
        data_list1=data_list1.reset_index(drop=True)
        data_list1['Ot']=data_list1['Ot'].apply(lambda x:datetime.strftime(x, '%Y-%m-%d %H:%M:%S'))
        data_list1['Dt']=data_list1['Dt'].apply(lambda x:datetime.strftime(x, '%Y-%m-%d %H:%M:%S')) 
        data_list1['Ot']=data_list1['Ot'].apply(lambda x:x.split(' ')[-1])
        data_list1['Dt']=data_list1['Dt'].apply(lambda x:x.split(' ')[-1])
        return data_list1