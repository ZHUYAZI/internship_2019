from func_timeout import func_timeout, FunctionTimedOut
import BESTPLAN as bp



# def fun_time_decorate(func,arg0,arg1,arg2,arg3):
#     try:
#         return func_timeout(100, func, args=(arg0,arg1,arg2,arg3))
#     except FunctionTimedOut:
#         return '',''
    
def choix_path(i,test_data,gare_position,new_feed):
    try:
        row=test_data.iloc[i]
        index=i
        pos1=[gare_position[gare_position['nomlong']==row['O']].iloc[0].geometry.y,\
              gare_position[gare_position['nomlong']==row['O']].iloc[0].geometry.x]
        pos2=[gare_position[gare_position['nomlong']==row['D']].iloc[0].geometry.y,\
              gare_position[gare_position['nomlong']==row['D']].iloc[0].geometry.x]
        start_time=row['Ot']
        end_time=row['Dt']
    #   test_path=new_feed.get_shortest_path(pos1,pos2)
    #    plan=bp.Best_Plan(start_time, end_time, new_feed.feed,test_path, new_feed.G_add_walk)

        return pos1 
    except:
        return ''