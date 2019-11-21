
import optparse
import sys
import os
import time
import subprocess
import traci
from bastralib import BastraLog
from bastralib import Sim as Sim
from bastralib import Command
from sumolib import checkBinary
from lxml import etree



def getConfig():
    parser = optparse.OptionParser("Configuration file is needed: bastra2.py -c name.conf.xml")
    parser.add_option("-c", dest="config_file", type="string")
    (options, args) = parser.parse_args()
    return options

def readOption(option, program):
    try:
        tree=etree.parse(config_file)
        root=tree.getroot()
        l_config=root.findall(program)
        label=l_config[ 0].find(option)
        value=label.get("value")
    except:
        sys.exit("Configuration error: value for " + option + " in " + program + " not found.")

    return value

def load_config():
    dict_conf={}
    dict_conf["tmp_dir"]=readOption("tmp_dir", "Bastra")
    dict_conf["results_dir"]=readOption("results_dir", "Bastra")
    dict_conf["log_dir"]=readOption("log_dir", "Bastra")
    dict_conf["log_file"]=readOption("log_file", "Bastra")
    dict_conf["log_level"]=readOption("log_level", "Bastra")
    try:
      dict_conf["log_every_n_steps"]=int(readOption("log_every_n_steps", "Bastra"))
    except:
      dict_conf["log_every_n_steps"]=1
      
    dict_conf["dump_dir"]=readOption("dump_dir", "Bastra")
    dict_conf["new_routes_file"]=readOption("new_routes_file", "Bastra")
    dict_conf["route_file"]=readOption("route_file", "Bastra")
    dict_conf["logit"]=readOption("logit", "Bastra")
    if (float(dict_conf["logit"])> 1.0):
        sys.exit("Configuration error: LOGIT parameter must be between 0.0 and 1.0")
    dict_conf["commands_file"]=readOption("commands_file", "Bastra")
    dict_conf["statistics_f"]=readOption("statistics_file", "Bastra")
    dict_conf["begin"]=readOption("begin", "Bastra")
    dict_conf["end"]=readOption("end", "Bastra")

    dict_conf["f_tries"]=0
    try:
      dict_conf["f_tries"]=int(readOption("foresight_tries", "Bastra"))
    except:
      dict_conf["f_tries"]=0

    dict_conf["f_steps"]=0
    try:
      dict_conf["f_steps"]=int(readOption("foresight_steps", "Bastra"))
    except:
      dict_conf["f_steps"]=0

    dict_conf["f_halting"]=readOption("foresight_halting", "Bastra")
    dict_conf["f_penalty"]=readOption("foresight_penalty", "Bastra")

    # Alvaro Added: 15/09/16
    try:
      dict_conf["csv_sep"]=readOption("csv_sep", "Bastra")
    except:
       dict_conf["csv_sep"]=','

    # Alvaro Added: 10/10/16
    dict_conf["edge_stats_dump"]=False
    try:
      # True / False
      if( readOption("edge_stats_dump", "Bastra").lower() == "true" ):
        dict_conf["edge_stats_dump"]=True
    except:
       dict_conf["edge_stats_dump"]=False
    try:
      dict_conf["edge_stats_file"]=readOption("edge_stats_file", "Bastra")
    except:
      dict_conf["edge_stats_file"]='edge_stats.csv'

    try:
      dict_conf["edge_stats_sampling"]=int(readOption("edge_stats_sampling", "Bastra"))
    except:
      # If not defined, use a value enough to take at least 100 samples
      v = int((int(dict_conf["end"])-int(dict_conf["begin"]))/100)
      if( v < 0 ):
        v = 1
      dict_conf["edge_stats_sampling"]=v

    try:
      dict_conf["routing_algorithm"]=readOption("routing_algorithm", "Bastra").lower()
    except:
      dict_conf["routing_algorithm"]=""
    if( not dict_conf["routing_algorithm"] in ['','dijstra','astar','ch','chwrapper'] ):
      dict_conf["routing_algorithm"]=""

    str_verbose=readOption("verbose", "Bastra")
    str_verbose.lower()
    if str_verbose=="true":
        dict_conf["verbose"]=True
    elif str_verbose=="false":
        dict_conf["verbose"]=False
    else:
        sys.exit("Configuration error: wrong value for 'verbose' in bastra's configuration file")
    str_balanced=readOption("use_balance", "Bastra")
    balanced=str_balanced.lower()
    if balanced=="true":
        dict_conf["balanced"]=True
    elif balanced=="false":
        dict_conf["balanced"]=False
    else:
        sys.exit("Configuration error: wrong value for 'use_balance' in bastra's configuration file")

    str_interactive=readOption("interactive", "Sumo")
    str_interactive.lower()
    if str_interactive=="true":
        dict_conf["interactive"]=True
    elif str_interactive=="false":
        dict_conf["interactive"]=False
    dict_conf["net_file"]=readOption("net_file", "Sumo")
    dict_conf["sumo_log_file"]=readOption("log_file", "Sumo")
    dict_conf["sumo_config"]=readOption("sumo_config", "Sumo")
    str_sumoPort=readOption("port", "Sumo")
    try:
        dict_conf["sumoPort"]=int(str_sumoPort)
    except:
        sys.exit("Configuration error: wrong value for SumoPort in " + config_file)

    if not os.path.isdir(dict_conf["tmp_dir"]):
        sys.exit("Configuration error: directory pointed by tmp_dir value not found")

    if not os.path.isdir(dict_conf["log_dir"]):
        sys.exit("Configuration error: directory pointed by log_dir value not found")

    if not os.path.isdir(dict_conf["dump_dir"]):
        sys.exit("Configuration error: directory pointed by dump_dir value not found")

    if not os.path.isdir(dict_conf["results_dir"]):
        sys.exit("Configuration error: directory pointed by results_dir value not found")


    return dict_conf


def readCommandsSequence(file_name):
    command_list=[]

    try:
        tree=etree.parse(file_name)
        root=tree.getroot()
        l_commands=root.findall("command")
        for comm in l_commands:
            time=int(comm.get("time"))
            theCommand=comm.get("name")
            str_param =comm.get("param")
            theArgs=str_param.split(' ')
            new_command=Command.Command(theCommand, time, theArgs )
            command_list.append(new_command)
    except:
        log_file.printLog(LEVEL1_ERRORS, "Error reading commands for " + file_name + "\n" )
        sys.exit("Error reading commands for " + file_name)
    return command_list


# ==========================================================================
if __name__ == '__main__':

    #constants
    LEVEL1_ERRORS=1		# ERRORS
    LEVEL2_CPU_TIME=2		# 
    LEVEL3_FULL=3		# Time iterations

    # -------------------------------------------------
    # Config reading parameters
    # -------------------------------------------------
    param=getConfig()
    config_file=param.config_file
    config=load_config().copy()
    log_file=BastraLog.BastraLog(config)

    # -- Alvaro 09/12/2016
    # DECORATOR FOR TIME MANAGEMENT
    # Usage as:
    # @log_computing_time(log_file,'la_funcion')
    def log_computing_time(log_file,txt):
      def time_decorator(func):
        def wrapper(*args, **kwargs):
          beg_ts = time.time()
          func(*args, **kwargs)
          end_ts = time.time()
          #print(txt+":elapsed time: %f" % (end_ts - beg_ts))
          log_file.printLog(LEVEL2_CPU_TIME,txt+":elapsed time: %f" % (end_ts - beg_ts)+ "\n")
        return wrapper
      return time_decorator

    # -------------------------------------------------
    # Check sumo installed
    # -------------------------------------------------
    try:
        sys.path.append(os.path.join(os.path.dirname(
            __file__), '..', '..', '..', '..', "tools"))
        sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
            os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in doc
    except ImportError:
        sys.exit("please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")

    sim = Sim.simulated_traffic(config, log_file)
    if config["interactive"]:
        sumoBinary = checkBinary('sumo-gui')
    else:
        sumoBinary = checkBinary('sumo')

    # -------------------------------------------------
    # Start sumo and connect to it (traci)
    # -------------------------------------------------
    commands_sequence=readCommandsSequence(config["commands_file"])
    for c in commands_sequence:
      print( "------> PLANNED COMMAND: {:05d}:{}:{}".format(c.time,c.name,c.param))
    
    # sumoProcess = subprocess.Popen([sumoBinary, "-c", config["sumo_config"],"--remote-port", str(config["sumoPort"])], stdout=sys.stdout, stderr=sys.stderr)
    # *************************************
    # WARNING
    # TIMEOUT IN JUNCTIONS: 60
    JUNCTION_BLOCK_TIMEOUT="60"
    # *************************************
    # sumoProcess = subprocess.Popen([sumoBinary, "-c", config["sumo_config"],"--remote-port", str(config["sumoPort"])], "--ignore-junction-blocker", JUNCTION_BLOCK_TIMEOUT, stdout=sys.stdout, stderr=sys.stderr)
    sumoProcess = subprocess.Popen([sumoBinary, "-c", config["sumo_config"],"--remote-port", str(config["sumoPort"])], stdout=sys.stdout, stderr=sys.stderr)
    traci.init(config["sumoPort"])

    # -------------------------------------------------
    # Simulation main loop:
    #	- End condition 1: reach max num simulations
    #	- End condition 2: do not exceed max time
    # -------------------------------------------------
    while (traci.simulation.getMinExpectedNumber() > 0) and (int(sim.getCurTime())<int(sim.getEnd())):
    	# ---------------------------------------------
	# For each simulation step:
    	# ---------------------------------------------
	# Update simulation timestamp
        sim.actCurTime()
        if ( (sim.getCurTime() % config["log_every_n_steps"]) == 0 ):
           log_file.printLog(LEVEL1_ERRORS,"Minute:{} - Processing step:{}\n".format( int(sim.getCurTime() / config["log_every_n_steps"]), sim.getCurTime() ))
        # Process pending vehicle movements
        sim.processPendings()
        # ---------------------------------------------
        # Check if there are commands pending for the step
        # ---------------------------------------------
        timestep = sim.getCurTime()
        step_commands = filter( lambda x: x.getTime()==timestep, commands_sequence)
        for command in step_commands:
        #   print( "------> STEP COMMAND: {:05d}:{}:{}".format(c.time,c.name,c.param))
        # while len(commands_sequence)>0 and commands_sequence[0].getTime()==sim.getCurTime():
        #     command=commands_sequence.pop(0)
            # log_file.printLog (LEVEL3_FULL,str(command.getParams()) + "\n")
            com_name=command.getName().lower()
            com_params=command.getParams()

	    # if there is a MAP-APPLY command
            if com_name=="maps":
                errTxt = "+++++++++ NEW TWM TO BE APPLIED: {}\n".format( com_params[0] )
                log_file.printLog (LEVEL1_ERRORS, errTxt )
                sim.processMaps(com_params[0])

	    # If there is a road-incident
            elif com_name=="incident":
                errTxt = ">>>>>>>> INCIDENT DETECTION AT: {}\n".format( com_params[0] )
                log_file.printLog (LEVEL1_ERRORS, errTxt )
                sim.processIncident(com_params[0])

	    # If there is a road-incident restoration
            elif com_name=="restore":
                errTxt = "<<<<<<<< INCIDENT CLEARANCE AT: {}\n".format( com_params[0] )
                log_file.printLog (LEVEL1_ERRORS, errTxt )
                sim.processRestore(com_params[0])

	    # Unknown command
            else:
                log_file.printLog(LEVEL3_FULL, "COMMAND NOT RECOGNIZED {}:{}\n".format( com_name, com_params ))

	# Reroute vehicles if necessary
        veh_list=traci.vehicle.getIDList()
        sim.reroute(veh_list)

	# Check congestion foresights if necessary
        sim.foresight(veh_list, config)

	# Do simulation STEP
        sim.simulationStep()

        # Get stats from the simulation step
        sim.get_simulation_results()
        sim.edges_scan()

    # -------------------------------------------------
    # End of simulation
    # -------------------------------------------------
    sim.edge_stats_dump( )
    traci.close()
    print("Process terminated: step " + str(sim.getCurTime()) + "\n")
    sumoProcess.terminate()
    sim.saveStatistics(config)

exit(0)
