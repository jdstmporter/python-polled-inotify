'''
Created on 4 Sep 2014

@author: julianporter
'''

import random
import collections
import time
import os
import shutil


class EventGenerator(object):
    
    
    def __init__(self,oBarrier,sBarrier,pipe,duration,path='.',minInterval=10,maxInterval=1000):
        self.oBarrier=oBarrier
        self.sBarrier=sBarrier
        self.sBarrier.acquire()
        self.pipe=pipe
        self.counts=collections.defaultdict(lambda : 0)
        self.path=path
        self.duration=duration
        self.minInterval=minInterval
        self.maxInterval=maxInterval
        self.fileSet=[]
        self.fileCount=0
        
    def newFile(self):
        self.fileCount+=1
        name='file%s_%s' % (self.fileCount,random.randint(0,100))
        name=os.path.join(self.path,name)
        return name
    
    def randomFile(self):
        return self.fileSet[random.randrange(0,len(self.fileSet))]
    
    
    
    def randomText(self,f):
        for _ in range(random.randint(0,100)):
            f.write(str(random.random()))
        
        
        
    def write(self):
        name=self.newFile()
        with open(name,'w') as f:
            self.randomText(f)
        self.fileSet.append(name)
                
    def move(self):
        name=self.randomFile()
        newName=self.newFile()
        os.rename(name, newName)
        self.fileSet.append(newName)
        self.fileSet.remove(name)
        
        
    def read(self):
        name=self.randomFile()
        with open(name,'r') as f:
            f.read()
        
    
    def delete(self):
        name=self.randomFile()
        os.remove(name)
        self.fileSet.remove(name)
        
    def modify(self):
        name=self.randomFile()
        with open(name,'a') as f:
            self.randomText(f)    
        
        
    def touch(self):
        name=self.randomFile()
        open(name,'a').close()
        
        
    def init(self):
        for _ in range(10):
            self.write()
    
    def __call__(self):
        self.oBarrier.acquire()
        
        modes=['READ','WRITE','DELETE','MOVE','TOUCH','MODIFY']
  
        functions={
                   'READ':self.read,
                   'WRITE':self.write,
                   'MODIFY':self.modify,
                   'MOVE':self.move,
                   'DELETE':self.delete,
                   'TOUCH':self.touch
                   }
        n=len(modes)
        
        now=time.time()
        cls=self.__class__
        while time.time()-now<self.duration:
            delay=random.randint(self.minInterval,self.maxInterval)
            time.sleep(delay/1000.0)
            mode=modes[random.randrange(0,n)]
            functions[mode]()
            self.counts[mode]+=1
        
        self.pipe.send({k:v for k,v in self.counts.items()})
        self.pipe.close()
        self.sBarrier.release()
        
        
    def shutdown(self):
        shutil.rmtree(self.path)