'''
Created on 27 de ene. de 2016

@author: Valentin
'''

import optparse
import sys
import os
import traci
import time
import thread
import subprocess
from multiprocessing import Queue
from sumolib import checkBinary
from lxml import etree
from bastralib import Trip
from bastralib import Command
from bastralib import Sim
from bastralib import BastraLog

#Constants declaration
LEVEL1=1
LEVEL2=2
LEVEL3=3
#End of constants declaration

#Begining of function declarations of SumoCom
def getConfig():
    parser = optparse.OptionParser("Configuration file is needed: SumoCom -c name.conf.xml")
    parser.add_option("-c", dest="config_file",
    type="string")
    (options, args) = parser.parse_args()
    return options

def readOption(option, program):
    try:
        tree=etree.parse(config_file)
        root=tree.getroot()
        l_config=root.findall(program)
        label=l_config[0].find(option)
        value=label.get("value")
    except:
        sys.exit("Configuration error: value for " + option + " in " + program + " not found.")

    return value

def load_config():
    dict_conf={}
    str_verbose=readOption("verbose", "SumoCom")
    str_verbose.lower()
    if str_verbose=="true":
        dict_conf["verbose"]=True
    elif str_verbose=="false":
        dict_conf["verbose"]=False
    else:
        sys.exit("Configuration error: wrong value for Verbose in SumoCom")

    interactive=readOption("interactive", "SumoCom")
    interactive=interactive.lower()
    if interactive=="true":
        dict_conf["sumocom_interactive"]=True
    elif interactive=="false":
        dict_conf["sumocom_interactive"]=False
    else:
        sys.exit("Configuration error: wrong value for Interactive in SumoCom config")

    str_balanced=readOption("use_balance", "SumoCom")
    balanced=str_balanced.lower()
    if balanced=="true":
        dict_conf["balanced"]=True
    elif balanced=="false":
        dict_conf["balanced"]=False
    else:
        sys.exit("Configuration error: wrong value for use_balance in SumoCom config")

    str_dua=readOption("DUA", "SumoCom")
    dua=str_dua.lower()
    if dua=="true":
        dict_conf["dua"]=True
    elif dua=="false":
        dict_conf["dua"]=False
    else:
        sys.exit("Configuration error: wrong value for DUA in SumoCom config")
    dict_conf["max_tries"]=readOption("max_tries_foresight", "SumoCom")

    dict_conf["route_file"]=readOption("route_file", "SumoCom")
    dict_conf["incident_file"]=readOption("incident", "SumoCom")
    dict_conf["commands_file"]=readOption("commands_file", "SumoCom")
    dict_conf["new_routes_file"]=readOption("new_routes_file", "SumoCom")
    dict_conf["new_trips_file"]=readOption("new_trips_file", "SumoCom")
    dict_conf["log_file"]=readOption("log_file", "SumoCom")
    dict_conf["log_level"]=readOption("log_level", "SumoCom")
    dict_conf["logit"]=readOption("logit", "SumoCom")
    dict_conf["max_tries"]=readOption("max_tries_foresight", "SumoCom")
    dict_conf["s_foresight"]=readOption("steps_foresight", "SumoCom")

    str_sumoPort=readOption("port", "Sumo")
    try:
        dict_conf["sumoPort"]=int(str_sumoPort)
    except:
        sys.exit("Configuration error: wrong value for SumoPort in " + config_file)

    dict_conf["sumo_netfile"]=readOption("net_file", "Sumo")
    sumo_interactive=readOption("interactive", "Sumo")
    if sumo_interactive=="true":
        dict_conf["sumo_interactive"]=True
    elif sumo_interactive=="false":
        dict_conf["sumo_interactive"]=False
    else:
        sys.exit("Configuration error: wrong value for Interactive in Sumo")

    dict_conf["sumo_config"]=readOption("sumo_config", "Sumo")
    dict_conf["net_file"]=readOption("net_file", "Sumo")
    dict_conf["sumo_log_file"]=readOption("log_file", "Sumo")

    return dict_conf

def print_menu():
    os.system("cls")
    print ("\n\n")
    print ("\t\t************SumoCom program**************\n")
    print ("\t\t*                                       *\n")
    print ("\t\t*                                       *\n")
    print ("\t\t*               Options                 *\n")
    print ("\t\t*                                       *\n")
    print ("\t\t*     S -> Start Simulation             *\n")
    print ("\t\t*     I -> Interrupt Simulation         *\n")
    print ("\t\t*          to introduce forbiden        *\n")
    print ("\t\t*          edge                         *\n")
    print ("\t\t*     C -> Continue with Simulation     *\n")
    print ("\t\t*     Q -> Quit                         *\n")
    print ("\t\t*                                       *\n")
    print ("\t\t*                                       *\n")
    print ("\t\t*****************************************\n")
    print ("\n\n")
    return


def msgToSumo(threadName, q):
    while(1):
        print_menu()
        option=raw_input("Introduce option: ")
        option=option.upper()

        if option[0]=="S":
            mesg.put(option)
        elif option[0]=="I":
            mesg.put(option)
            edge=raw_input("Introduce edge's ID: ")
            mesg.put(edge)
        elif option[0]=="R":
            mesg.put(option)
            edge=raw_input("Introduce edge's ID: ")
            mesg.put(edge)
        elif option[0]=="C":
            mesg.put(option)
        elif option[0]=="Q":
            confirm=raw_input("Are you sure? [Y/N]: ")
            confirm=confirm.upper()
            if confirm[0]=="Y":
                mesg.put(option)
                exit(0)
        else:
            print "Incorrect option. Retry after 5 seconds"
            time.sleep(5)
            mesg.put(option)
    return

def search_new_route(veh_id):
    tree=etree.parse(config["new_route_file"])
    root=tree.getroot()

    l_vehicles=root.findall("vehicle")
    for vehicle in l_vehicles:
        id=vehicle.get("id")
        if id==veh_id:
            route=vehicle.find("route")
            str_edges=route.get("edges")
            l_edges=str_edges.split(' ')
            return l_edges
    return []

def get_simulation_results():
    cur_time=traci.simulation.getCurrentTime()/1000
    l_vehicles_in=traci.vehicle.getIDList()
    for veh in l_vehicles_in:
        wait_time=traci.vehicle.getWaitingTime(veh)
        sim.act_vehicle_statistics(veh, wait_time, traci.vehicle.getRoadID(veh))
    l_vehicles_out=traci.simulation.getArrivedIDList()
    for veh in l_vehicles_out:
        sim.act_arrive_time(veh, cur_time)

    return

def genMaps(edge, cur_time):
    comm="mapGen.py -f " + edge + " -d 2 -n " + config["sumo_netfile"] + " -t " + str(cur_time) + " -p 5.5 "
    log_file.printLog(LEVEL1, "Executing: " + comm + "\n")
    try:
        #Esta linea funciona si no se ejecuta en eclipse. Descomentar
        os.system(comm)
        #time.sleep(5)
        log_file.printLog(LEVEL1, "EXECUTED\n")
    except:
        log_file.printLog(LEVEL1, "Error in the execution of mapGen. Please check if the program is available.\n" )
        sys.exit("Error in the execution of mapGen. Please check if the program is available.")

    return

def readCommandsSequence(file_name):
    command_list=[]

    try:
        tree=etree.parse(file_name)
        root=tree.getroot()
        l_commands=root.findall("command")
        for comm in l_commands:
            time=int(comm.get("time"))
            name=comm.get("name")
            str_param=comm.get("param")
            param=str_param.split(' ')
            new_command=Command.Command(name, time, param)
            command_list.append(new_command)
    except:
        log_file.printLog(LEVEL1, "Error reading commands for " + file_name + "\n" )
        sys.exit("Error reading commands for " + file_name)

    return command_list


def readMaps(file_name):

    maps_res=[]
    try:
        tree=etree.parse(file_name)
        root=tree.getroot()
        l_maps=root.findall("map")
        for map in l_maps:
            file=map.get("file")
            maps_res.append(file)
    except:
        log_file.printLog(LEVEL1, "Error reading maps from file " + file_name + "\n" )
        sys.exit("Error reading maps from filer " + file_name)

    return maps_res

def runInteractively():

    if config["sumo_interactive"]:
        sumoBinary = checkBinary('sumo-gui')
    else:
        sumoBinary = checkBinary('sumo')

    sumoProcess = subprocess.Popen([sumoBinary, "-c", config["sumo_config"],"--remote-port", str(config["sumoPort"]), "-l", "sumo_log"], stdout=sys.stdout, stderr=sys.stderr)

    traci.init(config["sumoPort"])
    thread.start_new_thread(msgToSumo, ("EdgeDisfunction",mesg))

    while traci.simulation.getMinExpectedNumber() > 0:
        option=mesg.get()
        option=option.upper()
        cur_time=traci.simulation.getCurrentTime()/1000

        if option[0]=="S":
            mesg.put(option)
            traci.simulationStep()
            get_simulation_results()
        elif option[0]=="I":
            while not mesg.empty():
                mesg.get()
            disEdge=mesg.get()

            edge_list= traci.edge.getIDList()
            if disEdge not in edge_list:
                print ("Attention: Supplied edge not in net. Simulation continues after 5 seconds")
                time.sleep(5)
            else:
                traci.edge.setMaxSpeed(disEdge, 0)
                sim.addIncident(disEdge, cur_time)
                if config["dua"]:
                    ALFA="I"+str(cur_time)+"-alfa-weight.xml"
                    BETA="I"+str(cur_time)+"-beta-weight.xml"
                    incident_maps=[]
                    incident_maps.append(ALFA)
                    incident_maps.append(BETA)
                    sim.distMaps(incident_maps, cur_time)
                    log_file.printLog(LEVEL3, "LLEga a los mapas\n")
                    genMaps(disEdge, cur_time)
                    log_file.printLog(LEVEL3, "LLega hasta reroute\n")
                    #time.sleep(2)
                    sim.assingTrips(cur_time)
                    sim.dump_vehicles("dump_con_trips")

                    sim.prepareTrips()
                    sim.calcNewTrips(cur_time)
                    sim.dump_vehicles("Dump_antes_traci")
            print_menu()
            print ("End of incident processing")

        elif option[0]=="R":
            while not mesg.empty():
                mesg.get()
            disEdge=mesg.get()

            edge_list= traci.edge.getIDList()
            if disEdge not in edge_list:
                print ("Attention: Supplied edge not in net. Simulation continues after 5 seconds")
                time.sleep(5)
            else:
                #time.sleep(5)
                sim.restore(disEdge, cur_time)
                sim.assingTrips(cur_time)
                sim.dump_vehicles("dump_veh_trips_restore")
                sim.prepareTrips()
                sim.calcNewTrips(cur_time)
                sim.dump_vehicles("dump_veh_routes_restore")
                sim.restoreIncident(disEdge)
                log_file.printLog (LEVEL1, "End of restore processing\n")
                print ( "End of restore processing")

        elif option[0]=="C":
            traci.simulationStep()
            cur_time=traci.simulation.getCurrentTime()/1000
            log_file.printLog (LEVEL3, "Simulation step completed\n")
            #time.sleep(2)
            if config["dua"]:

                if len(sim.getPendings())>0:
                    log_file.printLog(LEVEL3, "Se procesan los pendientes: \n")
                    log_file.printLog(LEVEL3, str(sim.getPendings()) + "\n")
                    sim.preparePendings()
                    sim.calcNewTrips(cur_time)
                    sim.reroute(sim.getPendings())

                l_new_vehicles=traci.simulation.getDepartedIDList()
                log_file.printLog (LEVEL3, "nuevos coches: " + str(l_new_vehicles) + "\n" )
                sim.reroute(l_new_vehicles)

            sim.foresight(traci.vehicle.getIDList(), config)
            get_simulation_results()
            print_menu()
            mesg.put(option)

        elif option[0]=="Q":
            traci.close()
            sumoProcess.terminate()
            exit(0)

    log_file.printLog(LEVEL1, "End of simulation\n")
    traci.close()
    print("End of simulation")
    sim.dump_vehicles("vehicles_fin")
    sumoProcess.terminate()

    return

def runAutomatically():

    if config["sumo_interactive"]:
        sumoBinary = checkBinary('sumo-gui')
    else:
        sumoBinary = checkBinary('sumo')

    print ("Starting in automatically mode")

    commands_sequence=readCommandsSequence(config["commands_file"])
    sumoProcess = subprocess.Popen([sumoBinary, "-c", config["sumo_config"],"--remote-port", str(config["sumoPort"])], stdout=sys.stdout, stderr=sys.stderr)
    traci.init(config["sumoPort"])

    while traci.simulation.getMinExpectedNumber() > 0:
        cur_time=traci.simulation.getCurrentTime()/1000
        if len(commands_sequence)>0 and commands_sequence[0].getTime()==cur_time:
            command=commands_sequence.pop(0)
            log_file.printLog(LEVEL3,str(command.getTime()) + ": " + command.getName() + "\n")
            log_file.printLog (LEVEL3,str(command.getParams()) + "\n")
            com_name=command.getName().lower()
            com_params=command.getParams()

            if com_name=="incident":
                edge_list= traci.edge.getIDList()
                if com_params[0] not in edge_list:
                    log_file.printLog(LEVEL2,"Attention: Supplied edge not in net. Simulation continues after 5 seconds\n")
                    print ("Attention: Supplied edge not in net. Simulation continues after 5 seconds")
                    time.sleep(5)
                else:
                    traci.edge.setMaxSpeed(com_params[0], 0)
                    sim.addIncident(com_params[0], cur_time)
                    if config["dua"]:
                        ALFA="I"+str(cur_time)+"-alfa-weight.xml"
                        BETA="I"+str(cur_time)+"-beta-weight.xml"
                        incident_maps=[]
                        incident_maps.append(ALFA)
                        incident_maps.append(BETA)
                        sim.distMaps(incident_maps, cur_time)
                        log_file.printLog(LEVEL3,"LLEga a los mapas\n")
                        genMaps(com_params[0], cur_time)
                        log_file.printLog(LEVEL3,"LLega hasta reroute\n")
                        #time.sleep(2)
                        sim.assingTrips(cur_time)
                        sim.dump_vehicles("dump_con_trips")

                        sim.prepareTrips()
                        sim.calcNewTrips(cur_time)
                        sim.dump_vehicles("Dump_antes_traci")
                        #sim.reroute()
            elif com_name=="restore":
                edge_list= traci.edge.getIDList()
                if com_params[0] not in edge_list:
                    print ("Attention: Supplied edge not in net. Simulation continues after 5 seconds")
                    log_file.printLog(LEVEL2,"Attention: Supplied edge not in net. Simulation continues after 5 seconds\n")
                    time.sleep(5)
                else:
                    sim.restore(com_params[0], cur_time)
                    sim.assingTrips(cur_time)
                    sim.dump_vehicles("dump_veh_trips_restore")
                    sim.prepareTrips()
                    sim.calcNewTrips(cur_time)
                    sim.dump_vehicles("dump_veh_routes_restore")
                    sim.restoreIncident(com_params[0])
                log_file.printLog(LEVEL1,"End of restore processing\n")
                print ("End of restore processing")
            elif com_name=="maps":
                map_list=readMaps(com_params[0])
                sim.distMaps(map_list, cur_time)
                sim.assingTrips(cur_time)
                sim.dump_vehicles("dump_con_trips")
                sim.prepareTrips()
                sim.calcNewTrips(cur_time)
                sim.dump_vehicles("Dump_antes_traci")
                sim.reroute(traci.vehicle.getIDList())

            else:
                log_file.printLog(LEVEL1, "Command " + com_name + " not recognized. Simulation continues.\n")
                print ("Command " + com_name + " not recognized. Simulation continues.")

        sim.foresight(traci.vehicle.getIDList(), config)
        traci.simulationStep()
        if config["dua"]:
            if len(sim.getPendings())>0:
                sim.preparePendings()
                sim.calcNewTrips(cur_time)
                sim.reroute(sim.getPendings())

            l_new_vehicles=traci.simulation.getDepartedIDList()
            log_file.printLog (LEVEL3,"nuevos coches:  " + str(l_new_vehicles) + "\n" )
            sim.reroute(l_new_vehicles)


        get_simulation_results()


    log_file.printLog(LEVEL1,"End of simulation\n")
    traci.close()
    print("End of simulation")
    sim.print_vehicles()
    sumoProcess.terminate()

    return


if __name__ == '__main__':

    incident_list=[]
    param=getConfig()
    config_file=param.config_file
    config=load_config().copy()
    log_file=BastraLog.BastraLog(config)

    try:
        sys.path.append(os.path.join(os.path.dirname(
            __file__), '..', '..', '..', '..', "tools"))
        sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
            os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in doc

    except ImportError:
        sys.exit("please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")


    mesg=Queue(1024)
    sim = Sim.simulated_traffic(config, log_file)

    if config["sumocom_interactive"]:
        runInteractively()
    else:
        runAutomatically()

    exit(0)