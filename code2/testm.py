from pathos.multiprocessing import ProcessingPool as Pool
import tqdm
class A():
    def __init__(self, njobs=1000):
        self.map = Pool().imap
        self.njobs = njobs
        self.result=self.start()
    def start(self):
        result = list(tqdm.tqdm(self.map(self.RunProcess, range(self.njobs),range(self.njobs)),total=self.njobs))
        return result
    def RunProcess(self, i,j):
        return i+j+self.njobs