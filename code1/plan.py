import itertools

class Design_Plan():
    #data->new_feed.feed
    #path should remove '_' -> stop
    def __init__(self, start_time, end_time, data, path):
        self.start = self.to_seconds(start_time)
        self.end =self.to_seconds(end_time)
        self.data = data.stop_times[(data.stop_times['departure_time']>self.start)&(data.stop_times['departure_time']<self.end)]
        self.data2=data.stops
        self.path = path
        self.tripchoise,self.transfer_point=self.GetTripID()
        self.finalplan=self.combine_point()
        self.stopnames=self.find_stop_name()
    
    def find_stop_name(self):
        stop_name=[]
        for stop in self.transfer_point:
            name=list(self.data2[self.data2['stop_id']==stop]['stop_name'])
            stop_name.append(name)
            
        return stop_name  
    #get points where to transfer and the possible trips on each road
    def GetTripID(self):
        data=self.data
        stop_path=self.path
        
        tripchoise=[]
        transfer_points=[]
        listA=list(data[data['stop_id']== stop_path[0]]['trip_id'])
        for i in range(1,len(stop_path)):
            listB=list(data[data['stop_id']== stop_path[i]]['trip_id'])
            
            #correspondant
            if len(self.same(listA,listB))==0:
                tripchoise.append(listA)
                transfer_points.append(stop_path[i-1])
                listA=list(data[data['stop_id']== stop_path[i-1]]['trip_id'])
                
            listA=self.same(listA,listB)
            #compare the sequence to remove some incorrect trip id
            for x in listA:
                data1=data[data['stop_id']== stop_path[i-1]]
                data2=data[data['stop_id']== stop_path[i]]
                if int(data1[data1['trip_id']==x]['stop_sequence'])>int(data2[data2['trip_id']==x]['stop_sequence']):
                    listA.remove(x)
                    
        tripchoise.append(listA)
        
        return tripchoise,transfer_points
        
    def plan_combine(self):
        tripchoise=self.tripchoise
        transfer_points=self.transfer_point
        data=self.data
        
        plan=[]
        for i in range(len(transfer_points)):
            listA=tripchoise[i]
            listB=tripchoise[i+1]
            point_plan=list(itertools.product(listA, listB))
            plan.append(point_plan)
            self.check_plan(data,plan[i],transfer_points[i])
        return plan
    
    def check_plan(self,data,plan,point):
        list1=[]
        for i in range(len(plan)):
            trip1,trip2=plan[i]
            test=data[data['stop_id']==point]
            if int(test[test['trip_id']==trip1]['arrival_time'])<int(test[test['trip_id']==trip2]['departure_time']):
                list1.append(i)
                
        for index in sorted(list1, reverse=True):
            del plan[index]
    
    #change tiem with form ../../.. to secondes
    def to_seconds(self,string):
        return sum(x * int(t) for x, t in zip([3600, 60, 1], string.split(":")))
    
    #return union between two list
    def union(self,listA,listB):#
        return list(set(listA).union(set(listB)))

    #return intersection between two list
    def same(self,listA,listB):
        return list(set(listA).intersection(set(listB)))
  
    #if we have more than 2 point for transfer
    #we could combien the point if it has the same choice in the same trajectory
    #list_change have the same form with [[(),(),...],[(),(),...],[(),(),...],...]

    def combine_point(self):
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