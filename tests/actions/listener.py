'''
Created on 4 Sep 2014

@author: julianporter
'''

import pollinotify
import collections


class EventObserver(object):
    
    def __init__(self,oBarrier,sBarrier,pipe,path='.',timeout=1000,mask=pollinotify.AllEvents):
        self.oBarrier=oBarrier
        self.sBarrier=sBarrier
        self.oBarrier.acquire()
        self.pipe=pipe
        self.counts=collections.defaultdict(lambda : 0)
        self.paths=collections.defaultdict(list)
        self.path=path
        self.timeout=timeout
        self.mask=mask
        
    def init(self):
        self.watcher=pollinotify.Watcher()
        self.watcher.addPath(self.path)
        
    def shutdown(self):
        pass
    
    def __call__(self):
        
        self.oBarrier.release()
        while not self.sBarrier.acquire(False):
            got=self.watcher.poll(timeout=self.timeout)
            if got:
                events=self.watcher.events(match=self.mask)
                for event in events:
                    for m in event.decode():
                        if m!='Access':
                            self.counts[m]+=1
                            self.paths[m].append(event.path)
        self.pipe.send({k:v for k,v in self.counts.items()})
        self.pipe.close()