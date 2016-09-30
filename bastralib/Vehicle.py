'''
Created on 27 de ene. de 2016

@author: Valentin
'''

import sys
import random

class vehicle:
    id=""
    depart_time=0
    end_time=0
    current_edge=""
    origin_edge=""
    destiny_edge=""
    route=[]
    rerouted=False
    last_reroute=0
    car_maps=[]
    trip_file_name=""
    path=[]
    sys_attend=False
    jam_check=False
    type=""
    finished=False

    def __init__(self, id, depart, origin, destiny, route, logit, type):
        self.id=id
        self.depart_time=int(depart)
        self.origin_edge=origin
        self.destiny_edge=destiny
        self.route=route
        self.type=type

        num_logit=float(logit)
        rand=random.random()
        if rand < num_logit:
            self.setAttended(True)
        return

    def setId(self, cad):
        self.id=cad
        return

    def getId(self):
        return self.id

    def getDepartTime(self):
        return self.depart_time

    def setEndTime(self, time):
        self.end_time=time
        return

    def getEndTime(self):
        return self.end_time

    def setOrigin(self, edge):
        self.origin_edge= edge
        return

    def getOrigin(self):
        return self.origin_edge

    def setDestiny(self, edge):
        self.destiny_edge=edge
        return

    def getDestiny(self):
        return self.destiny_edge

    def setRoute(self, route):
        self.route=route
        return

    def getRoute(self):
        return self.route

    def isRerouted(self):
        return self.rerouted

    def setRerouted(self, value):
        if value==True:
            if self.isAttended():
                self.rerouted=True
        else:
            self.rerouted=False
        return

    def getLastReroute(self):
        return self.last_reroute

    def setLastReroute(self, time):
        self.last_reroute=time
        return

    def getCurrent(self):
        return self.current_edge

    def setCurrent(self, edge):
        self.current_edge=edge

    def addCarMap(self, map):

        if map not in self.car_maps:
            list=[]
            for old_map in self.car_maps:
                new_map=old_map
                list.append(new_map)

            list.append(map)
            self.car_maps=[]
            self.car_maps.extend(list)

    def setMap(self, map):
        self.car_maps=[]
        self.car_maps.append(map)
        return

    def getCarMaps(self):
        return self.car_maps

    def getTripFile(self):
        return self.trip_file_name

    def setTripFile(self, cad):
        self.trip_file_name=cad
        return

    def deleteMaps(self, l_maps):
        for map in l_maps:
            if map in self.car_maps:
                self.car_maps.remove(map)

    def print_vehicle(self):
        print ("ID: " + self.id)
        print ("Depart: " + str(self.depart_time))
        sys.stdout.write("Origin: " + self.origin_edge)
        sys.stdout.write("   Current: " + self.current_edge)
        sys.stdout.write("Destiny: " + self.destiny_edge+ "\n")
        sys.stdout.write("Route: ")
        print (self.route)
        sys.stdout.write("Maps: ")
        print (self.car_maps)
        if self.rerouted:
            print ("Is rerouted")
        else:
            print ("Is nor rerouted")
        return
        sys.stdout.write ("Path: ")
        print (self.path)
        return

    def add2Path(self, edge):
        aux_path=[]
        aux_path.extend(self.path)
        aux_path.append(edge)
        self.path=[]
        self.path.extend(aux_path)
        return

    def getPath(self):
        aux_path=[]
        aux_path.extend(self.path)
        return aux_path

    def setAttended(self, value):
        self.sys_attend=value
        return

    def isAttended(self):
        return self.sys_attend


    def setJamCheck(self, value):
        self.jam_check=value
        return

    def isJamCheck(self):
        return self.jam_check

    def setType(self, type):
        self.type=type
        return

    def getType(self):
        return self.type

    def hasFinished(self):
        self.finished=True

    def isFinished(self):
        return self.finished
