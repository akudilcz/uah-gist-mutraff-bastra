'''
Created on 27 de ene. de 2016

@author: Valentin
'''

import os

class Trip_file:
    name=""
    trip_list=[]
    weight_maps=[]
    
    def __init__(self, name):
        self.name=name
        return
    
    def getName(self):
        return self.name
    
    def getWeightsMaps(self):
        return self.weight_maps
    
    def addTrip(self, vehicle, depart, start, end):
        self.trip_list.append((vehicle, depart, start, end))
        return
    
    def print_trips(self):
        print self.trip_list
        return
    
    def generateFile(self):
        if os.path.isfile(self.name):
            os.remove(self.name)
        xml_file=open(self.name, "w+")
        
        xml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        xml_file.write("\n")
        xml_file.write("<trips>\n")

        for trip in self.trip_list:
            xml_file.write("<trip id=\"" + trip[0] + "\" depart=\"" + str(trip[1]) + "\" from=\"" + trip[2] +
                           "\" to=\"" + trip[3] + "\" />\n" )
            print trip
        
        xml_file.write("</trips>\n")  
        xml_file.close()  
        
        return
#End of class Trip_file