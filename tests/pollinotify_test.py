'''
Created on 30 Jun 2014

@author: julianporter
'''


import random
import unittest
import multiprocessing
import collections
import tempfile
import time
import os
import sys

from .actions import EventGenerator, EventObserver

         
 
class TestInotify(unittest.TestCase):
    
    def __init__(self,methodName='runTest',nTests=10):
        super(TestInotify,self).__init__(methodName)
        
        self.nTests=nTests
    
    def setUp(self):
        self.duration=random.randint(2,10)
        self.path=os.path.join(tempfile.gettempdir(),'inotify')
        try:
            os.mkdir(self.path)
        except:
            pass
        
        srcE, self.dstE = multiprocessing.Pipe()
        srcO, self.dstO = multiprocessing.Pipe()

        observerBarrier=multiprocessing.Semaphore()
        sourceBarrier=multiprocessing.Semaphore()
        self.observer=EventObserver(observerBarrier,sourceBarrier,srcO,path=self.path)
        self.source=EventGenerator(observerBarrier,sourceBarrier,srcE,self.duration,path=self.path)
        
    
        self.source.init()
        self.observer.init()
        self.observerTask=multiprocessing.Process(target=self.observer)
        self.sourceTask=multiprocessing.Process(target=self.source)
        
        self.observerTask.start()
        self.sourceTask.start()
        
        self.wait()

        self.events=collections.defaultdict(lambda : 0)
        self.events.update(self.dstE.recv())
        
        self.observations=collections.defaultdict(lambda : 0)
        self.observations.update(self.dstO.recv())
        
        self.dstE.close()
        self.dstO.close()
        
        
    def tearDown(self):
        
        self.observer.shutdown()
        self.source.shutdown()
        
    def wait(self):    
        for _ in range(self.duration):
            print('.', end='')
            sys.stdout.flush()
            time.sleep(1) 
    
    def test_Create(self):
        self.assertEqual(self.observations['Create'],self.events['WRITE'])
        
    def test_Read(self):
        self.assertEqual(self.observations['CloseOther'],self.events['READ'])
         
    def test_Write(self):    
        self.assertEqual(self.observations['CloseWrite'],self.events['WRITE']+self.events['TOUCH']+self.events['MODIFY'])
        
    def test_Change(self):
        self.assertEqual(self.observations['Modify'],self.events['WRITE']+self.events['MODIFY'])
        
    def test_Delete(self):  
        self.assertEqual(self.observations['Delete'], self.events['DELETE'])
        
    def test_Move(self):
        self.assertEqual(self.observations['MoveFrom'],self.events['MOVE'])
        self.assertEqual(self.observations['MoveTo'],self.events['MOVE'])
        
    def test_Open(self):  
        self.assertEqual(self.observations['Open'],self.events['READ']+self.events['WRITE']+self.events['TOUCH']+self.events['MODIFY'])
       
def teardown_module():
    pass    
        

if  __name__=='__main__':
    unittest.main(exit=False)
