'''
Created on 27 de ene. de 2016

@author: Valentin
'''
from sumolib.net.edge import Edge

class Incident:
    id=0
    edge=""
    map1=""
    map2=""
    time=0
    restored=False
    
    def __init__(self, id, time,edge):
        self.id=id
        self.edge=edge
        ALFA="I"+str(time)+"-alfa-weight.xml"
        BETA="I"+str(time)+"-beta-weight.xml"
        self.map1=ALFA
        self.map2=BETA
        self.time=time
        return
    
    def getId(self):
        return self.id
    
    def getEdge(self):
        return self.edge
    
    def setRestored(self, val):
        self.restored=True
        return
    
    def isRestored(self):
        return self.restored
    
    def getIncMaps(self):
        map_list=[]
        map_list.append(self.map1)
        map_list.append(self.map2)
        return map_list
    
#End of class Incident