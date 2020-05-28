# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 12:01:49 2019

Best-plan 
version 2.0

@author: Yazi ZHU
"""
import itertools

class Best_Plan():
    #in:
    #start_time and end_time have format like 00:00:00
    #data is new_feed.feed
    #path has the format like '8U4PV_StopPoint:8738221:800:L'
    def __init__(self, start_time, end_time, data, path, graph_walk):
        #change the format of time to seconds
        self.start = self.to_seconds(start_time)
        self.end =self.to_seconds(end_time)
        #conserve stoptime duting start and end in the data1
        self.data1 = data.stop_times[(data.stop_times['departure_time']>self.start)&(data.stop_times['departure_time']<self.end)]
        #conserve stops for search stop name
        self.data2=data.stops
        #deal with the format of the path ,test_path has the format like '8U4PV_StopPoint:8738221:800:L'
        self.test_path = path
        #change format of path to StopPoint:8738221:800:L
        self.stop_path = [x.split('_')[1] for x in path]
        self.tripchoise,self.transfer_points=self.GetTripID(graph_walk)
       
        #self.finalplan=self.Final_Sevice_Plan()   this stage cost two much time ,so we could use it as externel function
        self.transfer_name=self.find_transfer_name()
        
    def find_transfer_name(self):
        transfer_name=[]
        for stop in self.transfer_points:
            transfer_name.append(self.data2[self.data2['stop_id']==stop]['stop_name'].to_string(index=False))
        
        return transfer_name
       
    def GetTripID(self,graph_walk):
        stop_path=self.stop_path
        data1=self.data1
        test_path=self.test_path
        
        transfer_points=[]
        tripchoise=[]
        transfer_points.append(stop_path[0])
        listA=list(data1[data1['stop_id']== stop_path[0]]['trip_id'])
        for i in range(1,len(stop_path)):
            listB=list(data1[data1['stop_id']== stop_path[i]]['trip_id'])

            if len(self.same(listA,listB))==0:
                if graph_walk[test_path[i-1]][test_path[i]][0]['mode']=='walk':
                    if i!=1:
                        tripchoise.append(listA)
                    listA=listB
                    if stop_path[i-1] not in transfer_points:
                        transfer_points.append(stop_path[i-1])
                    if stop_path[i] not in transfer_points:
                        transfer_points.append(stop_path[i])
                    tripchoise.append({'walk':graph_walk[test_path[i-1]][test_path[i]][0]['length']})
                    continue
                else:  
                    tripchoise.append(listA)
                    if stop_path[i-1] not in transfer_points:
                        transfer_points.append(stop_path[i-1])
                    listA=list(data1[data1['stop_id']== stop_path[i-1]]['trip_id'])
                    
            listA=self.same(listA,listB)  
            for x in listA:
                dataA=data1[data1['stop_id']== stop_path[i-1]]
                dataB=data1[data1['stop_id']== stop_path[i]]
                if int(dataA[dataA['trip_id']==x]['stop_sequence'])>int(dataB[dataB['trip_id']==x]['stop_sequence']):
                    listA.remove(x)
        if graph_walk[test_path[-2]][test_path[-1]][0]['mode']!='walk':    
            tripchoise.append(listA) 
        if stop_path[-1] not in transfer_points:
            transfer_points.append(stop_path[-1])  
            
            
        return tripchoise,transfer_points
        
    def plan_combine(self):
        tripchoise=self.tripchoise
        transfer_points=self.transfer_points
        data1=self.data1
        x=[list_element for list_element in tripchoise if type(list_element)is list]
        stop_path=self.stop_path
        plan=[]
        #if no correspondant
        if len(x)==1:
            plan=x  
            
        else:
            index1=tripchoise.index(x[0])
            index2=tripchoise.index(x[-1])
            if index1!=0:
                for service in x[0]:
                    test=data1[data1['stop_id']== stop_path[1]]
                    if int(test[test['trip_id']==service]['departure_time'])<=self.start+tripchoise[0]['walk']:
                        x[0].remove(service)

            if index2!=len(tripchoise)-1:
                for service in x[-1]:
                    test=data1[data1['stop_id']== stop_path[-2]]
                    if int(test[test['trip_id']==service]['arrival_time'])+tripchoise[-1]['walk']>=self.end:
                        x[0].remove(service)

            for i in range(len(x)-1):
                listA=x[i]
                listB=x[i+1]
                index1=tripchoise.index(listA)
                index2=tripchoise.index(listB)
                point_plan=list(itertools.product(listA, listB))
                plan.append(point_plan)
                if index1+1==index2:
                    self.check_plan(data1,plan[i],transfer_points[index2],transfer_points[index2])
                else:
                    self.check_plan(data1,plan[i],transfer_points[index1+1],transfer_points[index2],tripchoise[index1+1]['walk'])
        
        return plan    
        #correspondant
    
    def check_plan(self,data1,plan,point1,point2,*args):
        list1=[]
        for i in range(len(plan)):
            trip1,trip2=plan[i]
            test1=data1[data1['stop_id']==point1]
            test2=data1[data1['stop_id']==point2]
            if len(args):
                if int(test1[test1['trip_id']==trip1]['arrival_time'])<int(test2[test2['trip_id']==trip2]['departure_time'])+args[0]:
                    list1.append(i)
            else:
                if int(test1[test1['trip_id']==trip1]['arrival_time'])<int(test2[test2['trip_id']==trip2]['departure_time']):
                    list1.append(i)       
        for index in sorted(list1, reverse=True):
            del plan[index]    
            
            
    def Final_Sevice_Plan(self):
        list_change=self.plan_combine()
        list1=list_change[0]
        if len(list_change)<2:
            list1=list_change
        else:
            for list2 in list_change[1:]:
                list3=[]
                for listA in list1:
                    for listB in list2:
                        if len(self.same(listA,listB)):
                            list3.append(self.union(listA,listB))
                list1=list3
    
        return list1       
    
    #some functtion tools:
    #calcul total seconds
    def to_seconds(self,string):
        return sum(x * int(t) for x, t in zip([3600, 60, 1], string.split(":")))
    
    #return union between two list
    def union(self,listA,listB):#
        return list(set(listA).union(set(listB)))

    #return intersection between two list
    def same(self,listA,listB):
        return list(set(listA).intersection(set(listB)))
    