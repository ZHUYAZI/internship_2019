#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 13:54:16 2019

@author: yazi
"""
import partridge as ptg
import networkx as nx
import pandas as pd
import osmnx as ox
import peartree as pt
from datetime import date
import geopandas as gpd
import feed as fr
import BESTPLAN as bp
import time
from func_timeout import func_timeout, FunctionTimedOut
import multiprocessing as mp
from pathos.multiprocessing import ProcessingPool as Pool
import tqdm

class completefile():
    def __init__(self,new_feed,treatfile):
        self.imap = Pool().imap
        self.new_feed=new_feed
        self.treatfile=treatfile
        self.list1=self.treatement_trajet()
    
    def choix_way(self,i):
        test_data=self.treatfile.data_first.iloc[0:100].copy()
        gare_position=self.treatfile.gare_position
        new_feed=self.new_feed
        try:
            row=test_data.iloc[i]
            pos1=[gare_position[gare_position['nomlong']==row['O']].iloc[0].geometry.y,\
                  gare_position[gare_position['nomlong']==row['O']].iloc[0].geometry.x]
            pos2=[gare_position[gare_position['nomlong']==row['D']].iloc[0].geometry.y,\
                  gare_position[gare_position['nomlong']==row['D']].iloc[0].geometry.x]
            start_time=row['Ot']
            end_time=row['Dt']
            test_path=new_feed.get_shortest_path(pos1,pos2)
            plan=bp.Best_Plan(start_time, end_time, new_feed.feed,test_path, new_feed.G_add_walk)
            return plan.transfer_name,plan.tripchoise  
        except:
            return '','' 
    
    
#     def fun_time_decorate(self,arg1):
#         try:
#             #timeout=100 s
#             return func_timeout(100, self.choix_way, args=(arg1,))
#         except FunctionTimedOut:
#             return '',''
        
    def treatement_trajet(self):
        test_data=self.treatfile.data_first.iloc[0:100].copy()
        r = list(tqdm.tqdm(self.imap(self.choix_way, range(len(test_data))), total=len(test_data)))
        list_test=pd.DataFrame(r,columns=['transfer_name','tripchoise'])
        return list_test
