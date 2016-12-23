'''
Created on 27 de ene. de 2016

@author: Valentin
'''

import sys
import traci
import os
import re
import time
from lxml import etree
import Vehicle
import NewTripClass
import random

# -- Alvaro 09/12/2016
# DECORATOR FOR TIME MANAGEMENT
# Usage as:
# @log_computing_time('la_funcion')
def log_computing_time(txt):
  def time_decorator(func):
    def wrapper(*args, **kwargs):
      beg_ts = time.time()
      func(*args, **kwargs)
      end_ts = time.time()
      #print(txt+":elapsed time: %f" % (end_ts - beg_ts))
      myself = args[0]
      myself.log_file.printLog(myself.LEVEL2,txt+":elapsed time: %f" % (end_ts - beg_ts)+ "\n")
    return wrapper
  return time_decorator

class simulated_traffic:
#Las pongo de momento, ya veremos si uso otra cosa
    LEVEL1=1
    LEVEL2=2
    LEVEL3=3
#Son como quien dice auxiliares
    vehicle_list=[]
    dict_index={}
    edge_weigths={}
    edge_lengths={}
    pending_vehicles=[]
    incident_list=[]
    trip_file_list=[]
    begin=""
    end=""
    log_file=""
    dump_dir=""
    net_file=""
    new_routes_file=""
    route_file=""
    sumo_log_file=""
    logit=""
    cur_time=0
    max_tries=0
    # Para el seguimiento de Duarouter
    duarouter_sec=0

    # Alvaro Added: 10/10/16
    edge_stats_onoff = False
    edge_stats_file = ""
    edge_stats_sampling = 10
    edge_stats = []
    edge_desc = {}
    edge_ruleset = {}
    
    def __init__(self, config, bastra_log_file):
        self.log_file=bastra_log_file
        self.dump_dir=config["dump_dir"]
        self.net_file=config["net_file"]
        self.new_routes_file=config["new_routes_file"]
        self.route_file=config["route_file"]
        self.sumo_log_file=config["sumo_log_file"]
        self.logit=config["logit"]
        self.balanced=config["balanced"]
        self.max_tries=config["f_tries"]
        self.begin=config["begin"]
        self.end=config["end"]

        # Alvaro Added: 15/11/16
        self.routing_algorithm=config["routing_algorithm"]
	if( self.routing_algorithm != "" ):
	  self.routing_algorithm = "--routing-algorithm "+self.routing_algorithm

	# Alvaro Added: 10/10/16
        self.edge_stats_onoff = config["edge_stats_dump"]
        self.edge_stats_file = config["edge_stats_file"]
        self.edge_stats_sampling = config["edge_stats_sampling"]
	if( self.edge_stats_sampling <= 0 ):
          self.edge_stats_onoff = False

        tree=etree.parse(self.route_file)
        root=tree.getroot()
        l_vehicles=root.findall("vehicle")
        
        for veh in l_vehicles:
            id=veh.get("id")
            route=veh.find("route")
            str_edges=route.get("edges")
            l_edges=str_edges.split(' ')
            count=len(l_edges)
            if count!=0:
                init=l_edges[0]
                end=l_edges[count-1]
            start=float(veh.get("depart"))
            type=veh.get("type")
            if type is None:
                type=""
            self.add_vehicle(id, start, init, end, l_edges, self.logit, type)

        self.loadEdges()
            
        return

    def now(self):
        return (traci.simulation.getCurrentTime()/1000)

    def actCurTime(self):
        self.cur_time=self.now()
        return

    def getCurTime(self):
        return self.cur_time

    def getEnd(self):
        return self.end

    def validEdge(self,e):
      return self.edge_weigths.has_key(e)

    def loadEdges(self):
        tree=etree.parse(self.net_file)
        root=tree.getroot()
        l_edges=root.findall("edge")

	num = 0
        for edg in l_edges:
            fun_name=edg.get("function")
            if fun_name != "internal" :
                edge_id=edg.get("id")
                edge_from=edg.get("from")
                edge_to=edg.get("to")
                edge_prio=edg.get("priority")

                l_lane=edg.find("lane")

                self.edge_weigths[edge_id]=l_lane.get("speed")
                self.edge_lengths[edge_id]=l_lane.get("length")
		# ALVARO: 6/11/2016: BUG CORRECTION: sometimes SHAPE brings 3D coordinates
                # [x1, y1, x2, y2 ] = re.split( '[, ]', l_lane.get("shape") )
                [x1, y1, x2, y2 ] = re.split( '[, ]', l_lane.get("shape") )[0:4]
		av_x = (float(x1)+float(x2))/2
		av_y = (float(y1)+float(y2))/2
		
		# Alvaro Added: 10/10/16
		# Inventory the edges
                self.edge_desc[edge_id]={'id':num, 'name':edge_id, 'priority': edge_prio, 'from':edge_from, 'to': edge_to, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'av_x': av_x, 'av_y': av_y }
		num += 1
	self.saveEdges()
        return

    def saveEdges(self):
      # TO BE IMPLEMENTED LATER
      # file=open(self.edge_stats_file, "a")
      file=open("./edges.csv", "w")
      file.write( '{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s}\n'.format("id","name","priority","from", "to","x1", "y1", "x2", "y2", "av_x", "av_y"))
      for e in self.edge_desc:
        file.write( '{:s},{:d},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:f},{:f}\n'.format(
          e, self.edge_desc[e]['id'],self.edge_desc[e]['priority'], self.edge_desc[e]['from'], self.edge_desc[e]['to'],
          self.edge_desc[e]['x1'], self.edge_desc[e]['y1'], self.edge_desc[e]['x2'], self.edge_desc[e]['y2'], 
          self.edge_desc[e]['av_x'], self.edge_desc[e]['av_y'] ))

      file.close()
      return

    def add_vehicle(self, id, start, init, end, route, logit, type):
        pos=len(self.dict_index)
        self.dict_index[id]=pos
        obj_vehicle=Vehicle.vehicle(id, start, init, end, route, logit, type)
        self.vehicle_list.append(obj_vehicle)
        return
    
    def actVehicleStatistics(self, id):

        index=self.dict_index[id]
        cur_edge=traci.vehicle.getRoadID(id)
        if self.validEdge(cur_edge):
            cur_path=[]
            cur_path.extend(self.vehicle_list[index].getPath())
            last=len(cur_path)-1
            if last < 0:
                self.vehicle_list[index].add2Path(cur_edge)
            else:
                if cur_path[last] != cur_edge:
                    self.vehicle_list[index].add2Path(cur_edge)
        return
    
    def actArriveTime(self, id):
        index=self.dict_index[id]
        self.vehicle_list[index].setEndTime(self.cur_time)
        self.vehicle_list[index].hasFinished()
        return
    
    def act_route(self, id, route):
        index=self.dict_index[id]
        self.vehicle_list[index].setRoute(route)
        return
    
    def getRoute(self, id):
        index=self.dict_index[id]
        route=self.vehicle_list[index].getRoute()
        return route
    
    def getIdList(self):
        id_list=[]
        for elem in self.vehicle_list:
            id_list.append(elem.getId())
        return id_list
    
    def getTrips(self, time):
        trips=[]
        for veh in self.vehicle_list:
            if veh.getDepartTime()>=time:
                trips.append((veh.getId(), veh.getDepartTime(), veh.getOrigin(), veh.getDestiny()))
        return trips
    
    def addPending(self, id):
        self.pending_vehicles.append(id)
        return
    
    def getPendings(self):
        return self.pending_vehicles
    
    def deletePendings(self):
        while len(self.pending_vehicles)>0:
            self.pending_vehicles.pop()
        return        
        
    def saveNewRoutes(self, file_name):

        if not os.path.isfile(file_name):
            self.log_file.printLog(self.LEVEL2, "Error en la lectura de " + file_name + "\n")
            print ("Error en la lectura de " + file_name + "\n")
            return -1

        tree=etree.parse(file_name)
        root=tree.getroot()
        l_vehicles=root.findall("vehicle")

        for veh in l_vehicles:
            id=veh.get("id")
            route=veh.find("route")
            str_edges=route.get("edges")
            l_edges=str_edges.split(' ')
            
            self.act_route(id, l_edges)
            
        return
    
    def addMap(self, cad, id):
        index=self.dict_index[id]
        self.vehicle_list[index].car_maps=cad
        return
    
    def getMaps(self, id):
        index=self.dict_index[id]
        return self.vehicle_list[index].car_maps
    
    def addIncident(self, edge, time):
        id=len(self.incident_list)
        inc=Incident.Incident(id, time, edge)
        self.incident_list.append(inc)
        return

    def readMaps(self, map_file):
        if not os.path.isfile(map_file):
            self.log_file.printLog(self.LEVEL1, "Error reading " + map_file + "\n")
            return

        tree=etree.parse(map_file)
        root=tree.getroot()
        l_maps=root.findall("map")

        result=[]
        for map in l_maps:
            file=map.get("file")
            prob=map.get("prob")
            tag=map.get("tag")
            if (file is None) or (prob is None):
                self.log_file.printLog(self.LEVEL1, "Data error: wrong data in maps file " + map_file + "\n")
                return None
            if tag is None:
                tag=""
            result.append((file, float(prob), tag))

        return result


    def chooseMap(self, id, map_rule):
        index=self.dict_index[id]
        tag=self.vehicle_list[index].getType()

        rand=random.random()
        prob=0
        for map in map_rule:
            if tag==map[2]:
                prob= prob + float(map[1])
                if rand <= prob:
                    return map[0]
        return ""

    def checkMapRule(self, data):

        weight_list={}
        for rule in data:
            tag=rule[2]
            if weight_list.has_key(tag):
                weight_list[tag]=weight_list[tag]+ rule[1]
            else:
                weight_list[tag]=rule[1]

        for key in weight_list.keys():
            if weight_list[key] != 1:
                self.log_file.printLog(self.LEVEL1,"Error in map definitions. Probability sum of map's probabilities is not 1.\n")
                return False

        return True


    def distMaps(self, map_file):

        map_rules=self.readMaps(map_file)
        if map_rules is None:
            self.log_file.printLog(self.LEVEL1, "Error in map assignment. Fail processing " + map_file + "\n")
            return None
        if not self.checkMapRule(map_rules):
            self.log_file.printLog(self.LEVEL1, "Error in map assignment. Fail processing " + map_file + "\n")
            return None
        for veh in self.vehicle_list:
            #if self.cur_time<= int(veh.getDepartTime()):
                if veh.isAttended():
                    id=veh.getId()
                    map=self.chooseMap(id, map_rules)
                    veh.setMap(map)
                    veh.setRerouted(True)
        return
    
    def recoverPendings(self,log_file):
        log = open(log_file, "r")
        str_line=log.readline()
        while str_line!="":
            if (str_line.find("has no valid route"))>-1:
                first_tag=str_line.find("\'")
                last_tag=str_line.rfind("\'")
                id=str_line[(first_tag+1):(last_tag)]
                self.addPending(id)
            str_line=log.readline()
        self.log_file.printLog(self.LEVEL2, "Pendientes: " +  str(self.getPendings()) + "\n")
        log.close()
        return
    
    def assingTrips(self, id_list):
        
        for id in id_list:
            index=self.dict_index[id]
            if self.vehicle_list[index].isRerouted():
                veh_maps=self.vehicle_list[index].getCarMaps()
                done=False
                for trip_f in self.trip_file_list:
                    veh_maps.sort()
                    weight_maps=trip_f.getWeightMaps()
                    if veh_maps==weight_maps:
                        self.log_file.printLogVeh(self.LEVEL3, id, "Maps: " + str(veh_maps) + " - Corresponding trip found: " + trip_f.getFileName() + "\n")
                        self.vehicle_list[index].setTripFile(trip_f.getFileName())
                        done=True
                        break
                        #else:
                        #    print ("Las cadenas no coinciden")
                        #time.sleep(0.1)
                if not done:
                    new_trip= NewTripClass.NewTripFile(self.dump_dir + "trip_file_I" + str(self.cur_time) + "_" + str(len(self.trip_file_list)))
                    self.log_file.printLogVeh(self.LEVEL3, id, "Maps: " + str(veh_maps) + "\n")
                    self.log_file.printLogVeh(self.LEVEL3, id, "Creating a new trip:" + new_trip.getFileName() + "\n")
                    new_trip.weight_maps=veh_maps
                    self.trip_file_list.append(new_trip)
                    self.vehicle_list[index].setTripFile(new_trip.getFileName())

        self.dump_vehicles("vehicles_trips")
                    
        return
    
    def prepareTrips(self, id_list):
        
        for id in id_list:
            index=self.dict_index[id]
            if self.vehicle_list[index].isRerouted():
                t_f_name=self.vehicle_list[index].getTripFile()
                for trip_f in self.trip_file_list:
                    if t_f_name==trip_f.getFileName():
                        veh_running=traci.vehicle.getIDList()

                        if self.vehicle_list[index].getId() in veh_running:
                            cur_edge=traci.vehicle.getRoadID(self.vehicle_list[index].getId())
                            if self.validEdge(cur_edge):
                                trip_f.addTrip(self.vehicle_list[index].getId(), self.vehicle_list[index].getDepartTime(), cur_edge, self.vehicle_list[index].getDestiny())
                            else:
                                self.addPending(self.vehicle_list[index].getId())
                            break
                        else:
                            trip_f.addTrip(self.vehicle_list[index].getId(), self.vehicle_list[index].getDepartTime(), self.vehicle_list[index].getOrigin(), self.vehicle_list[index].getDestiny())
                            break

                #if pulse:
                #    mitrip = self.trip_file_list[0]
                #    mitrip.addTrip("0", 0.5, "2", "3")
                #    pulse=False
                #else:
                #    otrotrip=self.trip_file_list[1]
                #    otrotrip.addTrip(veh.id, veh.getDepartTime(), veh.getOrigin(), veh.getDestiny())
                #    pulse=True
        
        cont=0
        for trip_f in self.trip_file_list:
            trip_f.dumpTripFile("dump_trip_"+str(cont))
            cont=cont+1
        
        return
    
    
    def calcNewRoutes(self):

        cont=0
 	now = self.now()
        for trip_f in self.trip_file_list:
            trip_f.generateFile()
            if self.balanced:
                map_file_name=self.prepareMap(trip_f.getWeightMaps())
                self.getRouteForVehicle(now,trip_f.getFileName(), map_file_name, self.dump_dir, self.new_routes_file, "router_")
            else:
                self.getRouteForVehicle(now,trip_f.getFileName(), "", self.dump_dir, self.new_routes_file, "router_")

            self.saveNewRoutes(self.dump_dir + self.new_routes_file)
            self.recoverPendings(self.sumo_log_file)

        for trip_f in self.trip_file_list:
            self.trip_file_list.remove(trip_f)

        return
    
    def emptyTrips(self):
        for trip_f in self.trip_file_list:
            trip_f.deleteTrips()
        return
    
    def preparePendings(self):
        self.emptyTrips()
        
        for veh_id in self.pending_vehicles:
            index=self.dict_index[veh_id]
            veh=self.vehicle_list[index]

            vehicles_running=traci.vehicle.getIDList()
            if veh.getId() in vehicles_running:
                cur_edge=traci.vehicle.getRoadID(veh.getId())
                if self.validEdge(cur_edge):
                    veh.setCurrent(cur_edge)

            if veh.isRerouted():
                    t_f_name=veh.getTripFile()
                    for trip_f in self.trip_file_list:
                        if t_f_name==trip_f.getFileName():
                            trip_f.addTrip(veh.getId(), veh.getDepartTime(), veh.getCurrent(), veh.getDestiny())
                            break
            
        return
  
    def restore(self, edge, cur_time):
        
        done=False
        for inc in self.incident_list:
            if not inc.isRestored():
                if inc.getEdge()==edge:
                    self.log_file.printLogEdge(self.LEVEL3, edge, "incident=" + str(inc.getId()) + "Restoring service"+ "\n")
                    r_maps=inc.getIncMaps()
                    self.log_file.printLog(self.LEVEL3, "Deleting maps: " + str(r_maps) + "\n")
                    for veh in self.vehicle_list:
                        for map in r_maps:
                            if map in veh.getCarMaps():
                                veh.deleteMaps(r_maps)
                                veh.setRerouted(True)
                                self.log_file.printLogVeh(self.LEVEL3, veh.getId(), "Has been rerouted and now has the maps: " + str(veh.getCarMaps()) + "\n")
                    traci.edge.setMaxSpeed(edge, float(self.edge_weigths[edge]))
                    self.log_file.printLogEdge(self.LEVEL3, edge, "Service restored" + "\n")
                    #time.sleep(2)
                    done=True
                    break
            
        if not done:
            print ("There's no active incident on that edge. Simulation continues after 5 seconds.")
            self.log_file.printLogEdge(self.LEVEL1, edge, "There's no active incident on that edge. Simulation continues after 5 seconds.\n")
            time.sleep(5)
        return
    
    def restoreIncident(self, edge):
        done=False
        for inc in self.incident_list:
            if not inc.isRestored():
                if inc.getEdge()==edge:
                    inc.setRestored(True)
        return
    
    def prepareMap(self, list_maps):

        line={}

        for map_str in list_maps:
            if len(map_str)<=0:
                return ""
            tree=etree.parse(map_str)
            root=tree.getroot()
            interval=root.find("interval")
            l_edges=interval.findall("edge")

            for edg in l_edges:
                id=edg.get("id")
                travel_time=float(edg.get("traveltime"))

                if line.has_key(id):
                    t_time=line[id]
                    travel_time=travel_time+t_time
                else:
                    line[id]=travel_time

        file_name="weights_total.xml"

        if os.path.isfile(file_name):
            os.remove(file_name)
        xml_file=open(file_name, "w+")

        xml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        xml_file.write("\n")
        xml_file.write("<meandata>\n")
        xml_file.write("\t<interval begin=\"" + self.begin + "\" end=\""
                        + self.end + "\" id=\"whatever\">\n")

        for (id, value) in line.items():
            xml_file.write("\t\t<edge id=\"" + id
                                   + "\" traveltime=\"" + str(value) + "\"/>\n")

        xml_file.write("\t</interval>\n")
        xml_file.write("</meandata>\n")
        xml_file.close()

        return file_name


    def dump_vehicles(self, name_f):
        if os.path.isfile(name_f):
            os.remove(name_f)
        file_veh=open(name_f, "w")

        for veh in self.vehicle_list:
            file_veh.writelines("\nVehicle ID: " + veh.getId() + "\n")
            file_veh.writelines("\tCurrent: " + veh.getCurrent() + " -- Origin: " + veh.getOrigin() + "  -- Destiny: " + veh.getDestiny() + "\n")
            file_veh.write("\tRoutes: ")
            file_veh.writelines(veh.getRoute())
            file_veh.write("\n")
            if veh.isAttended():
                file_veh.writelines("\tSystem attended: True")
            else:
                file_veh.writelines("\tSystem attended: False")
            if veh.isRerouted():
                file_veh.writelines("\tRerouted: True\n")
            else:
                file_veh.writelines("\tRerouted: False\n")
            file_veh.writelines("\tTrip_file: " + veh.getTripFile() + "\n")
            file_veh.write("\tMaps: ")
            file_veh.writelines(veh.getCarMaps())
            file_veh.write("\tPath: ")
            file_veh.writelines (veh.getPath())
        file_veh.writelines("\n----------------------------------------------------------\n")
        file_veh.close()


    def jamCheck(self, id, route, steps, max_halting):

        index=self.dict_index[id]
        path=self.vehicle_list[index].getPath()
        jammed_edges=[]
        if steps==0:
            return jammed_edges

        if len(path)>0:
            edge=path[len(path)-1]
            if edge in route:
                pos=route.index(edge)
            else:
                result=[]
                self.log_file.printLogEdge(self.LEVEL3, edge, "veh=" + id + ":Vehicle no sigue la nueva ruta: " + str(route) + "\n" )
                return result
        else:
            pos=0

        check_list=route[pos:pos + steps]
        for an_edge in check_list:
            if self.validEdge(an_edge):
                if traci.edge.getLastStepHaltingNumber(an_edge) > max_halting: #Es el numero de vehiculos de velocidad 0 en el tramo
                    jammed_edges.append(an_edge)
            else:
                print ("El edge: " + an_edge + " no esta en la red\n")

        return jammed_edges


    def foresight(self, id_list, config):

        steps=config["f_steps"]
	if( steps == 0):
	  return

        max_halting=int(config["f_halting"])
        penalty=float(config["f_penalty"])

        for id in id_list:
            tries=0
            index=self.dict_index[id]
            route=self.vehicle_list[index].getRoute()
            new_route=[]

            if self.isAtEndOfEdge(id):
                jammed_list=self.jamCheck(id, route, steps, max_halting)
                jam_accum=[]
                while (len(jammed_list)>0) and (tries<self.max_tries):
                    jam_accum.extend(jammed_list)
                    new_route=self.jamReroute(jam_accum, id, penalty)
                    jammed_list=self.jamCheck(id, new_route, steps, max_halting)
                    tries=tries+1

                if len(new_route)>0:
                    self.vehicle_list[index].setRoute(new_route)
                    self.log_file.printLogVeh(self.LEVEL2, id, "Rerouting by trafic jam. New route: " + str(new_route) + "\n")
                    traci.vehicle.setRoute(id, new_route)
        return


    def jamReroute(self, pen_edges, veh_id, penalty):
	# BUG solved by Alvaro: 20/10/2016
        # jam_routes="jam_routes.xml"
        jam_routes="jam_routes.xml"
        cur_time=self.now()
        index=self.dict_index[veh_id]
        dest=self.vehicle_list[index].getDestiny()
        route=self.vehicle_list[index].getPath()
        if len(route)>0:
            cur_edge=route[len(route)-1]
        else:
            cur_edge=traci.vehicle.getRoadID(veh_id)

        trip_name=self.dump_dir + "jam_trip_" + str(cur_time) + "_" + veh_id + ".xml"
        trip_f=NewTripClass.NewTripFile(trip_name)
        trip_f.addTrip(veh_id, cur_time, cur_edge, dest)
        trip_f.generateFile()
        map_name=self.dump_dir + "jam_map_" + str(cur_time) + "_" + veh_id + ".xml"
        self.genJamMap(pen_edges, map_name, veh_id, penalty)

        self.getRouteForVehicle(cur_time,trip_f.getFileName(), map_name, self.dump_dir, jam_routes, "jam_")
        result=self.readJamFile(self.dump_dir+"/"+jam_routes)

        return result


    def readJamFile(self, file_name):

        result=[]
        if  not os.path.isfile(file_name):
            return result

        tree=etree.parse(file_name)
        root=tree.getroot()
        l_vehicles=root.findall("vehicle")
        for veh in l_vehicles:
            l_route=veh.findall("route")
            for route in l_route:
                str_result=route.get("edges")
                result.extend(str_result.split(' '))
        return result



    def joinMaps(self, list_maps, res_map):

        dict_edges={}
        for map in list_maps:
            if len(map)<=0:
                continue
            tree=etree.parse(map)
            root=tree.getroot()
            interval=root.find("interval")
            l_edges=interval.findall("edge")

            for edge in l_edges:
                edge_id=edge.get("id")
                ttime=edge.get("traveltime")

                if dict_edges.has_key(edge_id):
                    old_ttime=dict_edges[edge_id]
                    if ttime > old_ttime:
                        dict_edges[edge_id]=ttime
                else:
                    dict_edges[edge_id]=ttime

        if os.path.isfile(res_map):
            os.remove(res_map)
        xml_file=open(res_map, "w+")

        xml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        xml_file.write("\n")
        xml_file.write("<meandata>\n")
        xml_file.write("\t<interval begin=\"" + self.begin + "\" end=\""
                        + self.end + "\" id=\"whatever\">\n")

        for edge in dict_edges.keys():
             xml_file.write("\t\t<edge id=\"" + edge + "\" traveltime=\"" + dict_edges[edge] + "\"/>\n")

        xml_file.write("\t</interval>\n")
        xml_file.write("</meandata>\n")
        xml_file.close()

        return

    def genJamMap(self, pen_edges, name, veh_id, penalty):

        index=self.dict_index[veh_id]
        cur_maps=self.vehicle_list[index].getCarMaps()
        aux_map="aux_map.xml"

        if os.path.isfile(aux_map):
            os.remove(aux_map)
        xml_file=open(aux_map, "w+")

        xml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        xml_file.write("\n")
        xml_file.write("<meandata>\n")
        xml_file.write("\t<interval begin=\"" + self.begin + "\" end=\""
                        + self.end + "\" id=\"whatever\">\n")

        for edge in pen_edges:
            xml_file.write("\t\t<edge id=\"" + edge + "\" traveltime=\"" + str(float(self.edge_weigths[edge]) * penalty) + "\"/>\n")

        xml_file.write("\t</interval>\n")
        xml_file.write("</meandata>\n")
        xml_file.close()

        cur_maps.append(aux_map)
        self.joinMaps(cur_maps, name)

        return

    @log_computing_time('getRouteForVehicle')
    def getRouteForVehicle(self,cur_time,trip_file, map_file, dump_dir, output_file, dump_prefix ):
	xmlfile = dump_dir + "/" + output_file
	outfile = dump_dir + "/" + dump_prefix + str(cur_time) + "_" + str(self.duarouter_sec) + ".out"
	duarouter_opts = " --ignore-errors --no-warnings --remove-loops true --max-alternatives 10 --repair true --repair.to true --repair.from true "

        if len(map_file)>0:
          command="duarouter -n " + self.net_file + " -t " + trip_file + " -w " + map_file + " -o " + xmlfile + " --error-log " + self.sumo_log_file + duarouter_opts + self.routing_algorithm
        else:
          command="duarouter -n " + self.net_file + " -t " + trip_file + " -o " + xmlfile + " --error-log " + self.sumo_log_file + duarouter_opts + self.routing_algorithm
        self.log_file.printLog(self.LEVEL1,"Calculating new trips - duarouter sec " + str(self.duarouter_sec) + ": " + command + "\n")
        os.system(command)

        # ------------------------
        # 2016-09-19: Alvaro : Check command for operating system WIN/LIN
        # ------------------------
        if hasattr(sys, 'getwindowsversion'):
          # --- WINDOWS ---
          if os.path.isfile(xmlfile):
            #command="copy " + xmlfile + " " + self.dump_dir + dump_prefix + str(cur_time) + "_" + str(self.duarouter_sec) + ".out"
            #command="cd " + self.dump_dir + " & copy " + self.new_routes_file + " " + dump_prefix + str(cur_time) + "_" + str(self.duarouter_sec) + ".out"
            command="copy " + xmlfile + " " + outfile
            self.log_file.printLog(self.LEVEL3,"Copying duarouter results: " + command + "\n")
            os.system(command)
          else:
            self.log_file.printLog(self.LEVEL1, "No output for duarouter " + str(self.duarouter_sec) + ".\n")
        else:
          # --- LINUX ---
          if os.path.isfile(xmlfile):
            #command="cd " + self.dump_dir + " ; cp " + self.new_routes_file + " " + dump_prefix + str(cur_time) + "_" + str(self.duarouter_sec) + ".out"
            command="cp " + xmlfile + " " + outfile
            self.log_file.printLog(self.LEVEL3,"Copying duarouter results: " + command + "\n")
            os.system(command)
          else:
              self.log_file.printLog(self.LEVEL1, "No output for duarouter " + str(self.duarouter_sec) + ".\n")
        self.duarouter_sec=self.duarouter_sec + 1


    def isAtEndOfEdge(self, id):
        road=traci.vehicle.getRoadID(id)
        if not self.validEdge(road):
	  return False

        result=False
        lane=traci.vehicle.getLaneID(id)
        length=traci.lane.getLength(lane)
        edge_pos=traci.vehicle.getLanePosition(id)
        vel=traci.vehicle.getSpeed(id)

        if (edge_pos+vel)>length:
            index=self.dict_index[id]
            result=True

        return result

    def processMaps(self, maps_file):

        id_list=self.getIdList()
        self.distMaps(maps_file)
        self.assingTrips(id_list)
        self.prepareTrips(id_list)
        self.calcNewRoutes()

        return

    def reroute(self, veh_id_list):

        cont=0
        for veh_id in veh_id_list:
            index=self.dict_index[veh_id]
            veh=self.vehicle_list[index]
            if veh.isRerouted():
                cont=cont+1
                new_route=self.getRoute(veh_id)
                self.log_file.printLogVeh(self.LEVEL2, veh_id, "Rerouting - New route: "  + str(new_route) + "\n")
                self.log_file.printLogVeh(self.LEVEL3, veh_id, "Sumo's route by traci - Route : " + str(traci.vehicle.getRoute(veh_id)) + "\n")
                edge=traci.vehicle.getRoadID(veh_id)
                self.log_file.printLogEdge(self.LEVEL3, edge, "\n")
		try:
                  traci.vehicle.setRoute(veh_id,new_route)
                  veh.setRerouted(False)
                  color=traci.vehicle.getColor(veh_id)
                  traci.vehicle.setColor(veh_id, (255,0,0,0))
                  self.log_file.printLogVeh(self.LEVEL3, veh_id, "Final route: " + str(traci.vehicle.getRoute(veh_id)) + "\n")
		except:
                  self.log_file.printLogVeh(self.LEVEL3, veh_id, "ERROR ROUTING VEHICLE" + str(sys.exc_info()) + "\n")
                  self.log_file.printLogVeh(self.LEVEL3, veh_id, "Removed from routing queue\n")
                  veh.setRerouted(False)

        return

    def saveStatistics(self, config):
        file_name=config["statistics_f"]
        sep=config["csv_sep"]
        route_sep=":"

        if os.path.isfile(file_name):
            os.remove(file_name)
        file=open(file_name, "w")
        file.write(	"id"+sep+
                        "veh_type"+sep+
                        "t_depart_secs"+sep+
                        "t_arrival_secs"+sep+
                        "t_traveltime_secs"+sep+
                        "origin"+sep+
                        "destiny"+sep+
                        "route_calc_num"+sep+
                        "route_detail"+sep+
                        "route_path_num"+sep+
                        "route_distance"+sep+
                        "is_attended"+sep+
                        "has_finished"+sep+
                        "maps"+sep+
                        "tripfile"+
                        "\n")
        for veh in self.vehicle_list:
            file.write(	veh.getId() + sep+
			veh.getType()+sep+
                        str(veh.getDepartTime())+sep+
                        str(veh.getEndTime()) +sep+
                        str(veh.getEndTime()-veh.getDepartTime()) +sep+
                        veh.getOrigin() +sep+
                        veh.getDestiny() +sep+
                        str(veh.getRouteCalc()) +sep
                        )
            path_num=0
            path_distance=0
            for edge in veh.getPath():
                file.write(edge + route_sep )
                path_num += 1
                path_distance += float(self.edge_lengths[edge])
            file.write(sep + str(path_num) + sep + str(path_distance) + sep )
            if veh.isAttended():
                file.write("True")
            else:
                file.write("False")
            file.write(sep)
            if veh.isFinished():
                file.write("True")
            else:
                file.write("False")
            file.write(sep + str(veh.getCarMaps()) + sep + str(veh.getTripFile()) )
            file.write("\n")
        file.close()

        return

    def processPendings(self):
        if len(self.pending_vehicles)>0:
            id_list=[]
            id_list.extend(self.pending_vehicles)
            self.deletePendings()
            for id in id_list:
                index=self.dict_index[id]
                self.vehicle_list[index].setRerouted(True)
            self.assingTrips(id_list)
            self.prepareTrips(id_list)
            self.calcNewRoutes()
            self.reroute(id_list)
        return


    def processIncident(self, edge):
        if not self.validEdge(edge):
            self.log_file.printLogEdge(self.LEVEL1, edge, "Not defined in " + self.net_file + ".\n")
        else:
            traci.edge.setMaxSpeed(edge,0)
            self.log_file.printLogEdge(self.LEVEL1, edge, "Speed limited to 0 for this edge.\n")
        return

    def processRestore(self, edge):
        if not self.validEdge(edge):
            self.log_file.printLogEdge(self.LEVEL1, edge, "Not defined in " + self.net_file +".\n")
        else:
            traci.edge.setMaxSpeed(edge,float(self.edge_weigths[edge]))
            self.log_file.printLogEdge(self.LEVEL1, edge, "Speed limited for this edge, restored to " + self.edge_weigths[edge] + ".\n")
        return

    # -----------------------------------------------
    # Alvaro added: dump edge statistics
    # -----------------------------------------------
    def edge_stats_dump( self ):
      if( not self.edge_stats_onoff ):
        return
      file=open(self.edge_stats_file, "a")
      flag_print_edge_name = False
      if( flag_print_edge_name ):
        file.write( '{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s}\n'.format(
          "time","edge","edge_id",
          "traf_travel_time","traf_waiting_time","traf_total_veh_num","traf_halted_veh_num","traf_av_occupancy","traf_av_speed",
          "emission_co2", "emission_co", "emission_hc", "emission_noise", "emission_nox", "emission_PMx",
          "consum_epower", "consum_fuel"
          ))
        for i in range(0,len(self.edge_stats)-1):
          vals = self.edge_stats[i]['vals']
          for j in range(0,len(vals)-1):
  	    v = vals[j]
  	    # time
 	    # traf_travel_time, traf_waiting_time, traf_total_veh_num, traf_halted_veh_num, traf_av_occupancy, traf_av_speed,
 	    # emission_co2, emission_co, emission_hc, emission_noise, emission_nox, emission_PMx,
 	    # consum_epower, consum_fuel
            file.write( '{:d},{:s},{:d},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f}\n'.format(
             self.edge_stats[i]['time'],'xxxx',v[0],
	     v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8],v[9],v[10],v[11],v[12],v[13],v[14] )
 	     )
      else:
        file.write( '{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s}\n'.format(
          "time","edge_id",
          "traf_travel_time","traf_waiting_time","traf_total_veh_num","traf_halted_veh_num","traf_av_occupancy","traf_av_speed",
          "emission_co2", "emission_co", "emission_hc", "emission_noise", "emission_nox", "emission_PMx",
          "consum_epower", "consum_fuel"
          ))
        for i in range(0,len(self.edge_stats)-1):
          vals = self.edge_stats[i]['vals']
          for j in range(0,len(vals)-1):
  	    v = vals[j]
  	    # time
 	    # traf_travel_time, traf_waiting_time, traf_total_veh_num, traf_halted_veh_num, traf_av_occupancy, traf_av_speed,
 	    # emission_co2, emission_co, emission_hc, emission_noise, emission_nox, emission_PMx,
 	    # consum_epower, consum_fuel
            file.write( '{:d},{:d},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f}\n'.format(
             self.edge_stats[i]['time'],v[0],
	     v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8],v[9],v[10],v[11],v[12],v[13],v[14] )
 	     )
      file.close()
      return

    # -----------------------------------------------
    # Alvaro added: add edge statistics for current timestamp
    # -----------------------------------------------
    def edges_scan( self ):
      if( not self.edge_stats_onoff ):
        return
      if( self.cur_time % self.edge_stats_sampling != 0 ):
        return

      self.edge_stats.append( { 'time': self.cur_time, 'vals': [] } )
      i = len(self.edge_stats)-1

      for e in self.edge_desc:
	# --------------------------------
        # Ask traci for edge values
	# --------------------------------

	# --------------------------------
        # Discarded values:
        # traf_adaptedTravelTime=traci.edge.getAdaptedTravelTime(time)
	# traf_effort = traci.edge.getEffort(e,time)
	# traf_veh_mean_len = traci.edge.getEffort(e,time)

	# --------------------------------
        # Considered values:
        traf_travel_time = traci.edge.getTraveltime(e)
        traf_waiting_time = traci.edge.getWaitingTime(e)
        traf_total_veh_num = traci.edge.getLastStepVehicleNumber(e)
        traf_halted_veh_num = traci.edge.getLastStepHaltingNumber(e)
        traf_av_occupancy = traci.edge.getLastStepOccupancy(e)
        traf_av_speed = traci.edge.getLastStepMeanSpeed(e)
        emission_co2 = traci.edge.getCO2Emission(e)
        emission_co  = traci.edge.getCOEmission(e)
        emission_hc = traci.edge.getHCEmission(e)
        emission_noise = traci.edge.getNoiseEmission(e)
        emission_nox = traci.edge.getNOxEmission(e)
        emission_PMx = traci.edge.getPMxEmission(e)
        consum_epower = traci.edge.getElectricityConsumption(e)
        consum_fuel = traci.edge.getFuelConsumption(e)

	# --------------------------------
	# Save values
        self.edge_stats[i]['vals'].append(
	  [
            self.edge_desc[e]['id'],
	    traf_travel_time, traf_waiting_time, traf_total_veh_num, traf_halted_veh_num, traf_av_occupancy, traf_av_speed,
	    emission_co2, emission_co, emission_hc, emission_noise, emission_nox, emission_PMx,
	    consum_epower, consum_fuel
	  ] )
      return

# End of class Simulated_traffic    
    
