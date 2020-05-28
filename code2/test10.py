from pathos.multiprocessing import ProcessingPool as Pool
import tqdm
import BESTPLAN as bp
class A():
    def __init__(self, new_feed,treatfile):
        self.imap = Pool().imap
        self.new_feed = new_feed
        self.treatfile=treatfile
        self.test_data=self.treatfile.data_first.iloc[0:10].copy()
        self.gare_position=self.treatfile.gare_position
        self.result=self.start()
    def start(self):
        result=[]
#         for i in range(10):
#             res=self.RunProcess(i)
#             result.append(res)
        #result = list(tqdm.tqdm(self.imap(self.RunProcess, range(10)),total=10))
        result=self.imap(self.RunProcess, range(10))
        return result
    def RunProcess(self, i):
        test_data=self.test_data
        gare_position=self.gare_position
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
            return test_path,plan.transfer_name,plan.tripchoise  
        except:
            return '','',''
    