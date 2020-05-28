from func_timeout import func_timeout, FunctionTimedOut


def fun_time_decorate(func,arg0,arg1,arg2):
    try:
        return func_timeout(100, func, args=(arg0,arg1,arg2))
    except FunctionTimedOut:
        return '',''

    
def add(i,df,class_yazi):
    x=df.iloc[i]['col1']
    y=df.iloc[i]['col2']
    z=df.iloc[i]['col3']
    r1=x
    r2=yazi(y,z)
    return r1+r2.result+class_yazi.result
    
class yazi():
    def __init__(self,a,b):
        self.a=a
        self.b=b
        self.result=self.add()
    def add(self):
        return self.a + self.b

