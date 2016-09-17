'''
Created on 27 de ene. de 2016

@author: Valentin
'''

class Command:
    name=""
    time=0
    param=[]
    
    def __init__(self, name, time, param):
        self.name=name
        self.time=time
        self.param=param
        return
    
    def getName(self):
        return self.name
    
    def getTime(self):
        return self.time
        
    def getParams(self):
        return self.param
# End of class Command