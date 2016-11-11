'''
Created on 3 de feb. de 2016

@author: Valentin
'''

import os

class NewTripFile:
    
    trip_list=""
    file_name=""
    weight_maps=[]
    sep="@"
    


    def __init__(self, f_name):
        '''
        Constructor
        '''
        self.file_name=f_name
        
    def getFileName(self):
        return self.file_name

    def getWeightMaps(self):
        return self.weight_maps
    
    def addMap(self, weight_map):
        self.weight_maps.append(weight_map)
        return
    
    def addTrip(self, id, depart_time, edge, destiny):
        self.trip_list=self.trip_list + id +" " + str(depart_time) + " " + edge + " " + destiny + self.sep
        return
    
    def deleteTrips(self):
        self.trip_list=""
        return
    
    def dumpTripFile(self, f_name):
        if os.path.isfile(f_name):
            os.remove(f_name)
        dump_file=open(f_name, "w+")
        
        dump_file.write("Nombre: " + self.file_name + "\n")
        for trip_map in self.weight_maps:
            dump_file.write(trip_map)
        dump_file.write(self.trip_list)       
        dump_file.close()
        return
    
    def generateFile(self):
        if os.path.isfile(self.file_name):
            os.remove(self.file_name)
        xml_file=open(self.file_name, "w+")
        
        xml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        xml_file.write("\n")
        xml_file.write("<trips>\n")
        
        #for trip in self.trip_list:
        #    xml_file.write("<trip id=\"" + trip[0] + "\" depart=\"" + str(trip[1]) + "\" from=\"" + trip[2] +
        #                   "\" to=\"" + trip[3] + "\" />\n" )
        #    print trip
        
        line_list=self.trip_list.split(self.sep)
        
        for line in line_list:
            trip_data=line.split(" ")
            if len(trip_data)==4:
                xml_file.write("<trip id=\"" + trip_data[0] + "\" depart=\"" + trip_data[1] + "\" from=\"" + trip_data[2] + "\" to=\"" + trip_data[3] + "\" />\n" )
            
        xml_file.write("</trips>\n")  
        xml_file.close()
        
        return
            
