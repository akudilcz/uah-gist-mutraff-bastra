'''
Created on 09/11/2016

@author: Alvaro Paricio alvaro.paricio@uah.es, Valentin Alberti
'''

import sys
import os
import subprocess
import traci
from mutraffSim import Sim as Sim
from mutraffSim import Command
from mutraffSim import BastraLog
from sumolib import checkBinary
from lxml import etree
from mutraff import Ruleset as Rules

#constants
LOG_LEVEL1=1
LOG_LEVEL2=2
LOG_LEVEL3=3

# ============================================================================
class MutraffSimulator:
# ============================================================================

  # -----------------------------------------
  def __init__(self, conf):
    self.conf			= conf
    self.commandSchedule	= []
    self.log_file		= BastraLog.BastraLog(conf)
    self.theSimulator		= None
    self.sumoProcess		= None

  # -----------------------------------------
  def setRuleset(self,*ruleset):
    self.the

  # -----------------------------------------
  def commandScheduleReadfile(self,file_name):
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
            self.commandSchedule.append(new_command)
    except:
        return False

    return True

  # -----------------------------------------
  def setTrafficAlertRules(self):
    rules = Rules.Ruleset()
    #	traf_travel_time
    #	traf_waiting_time
    #	traf_total_veh_num
    #	traf_halted_veh_num
    #	traf_av_occupancy
    #	traf_av_speed
    #	emission_co2
    #	emission_co
    #	emission_hc
    #	emission_noise
    #	emission_nox
    #	emission_PMx
    #	consum_epower
    #	consum_fuel
    # inclass, feature, rulename, cond, text
    rules.addRule( 'edge', 'traf_av_occupancy', 'edge_occupancy_high', 'if {:f} > 0.6', 'Edge Congested over 60%' )
    rules.addRule( 'edge', 'traf_halted_veh_num', 'edge_halted_veh_high', 'if {:f} > 4', 'Number of halted vehicles exceed 4' )
    rules.addRule( 'edge', 'traf_waiting_time', 'edge_waiting_time_high', 'if {:f} > 4', 'High waiting time for vehicles' )

    self.theSimulator.setRuleset(rules)

  # -----------------------------------------
  def start(self):
    errCode = 0
    errText = ""

    # -------------------------------------------------
    # Check if SUMO installed
    # -------------------------------------------------
    try:
      sys.path.append(os.path.join(os.path.dirname( __file__), '..', '..', '..', '..', "tools"))
      sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
      os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in doc
    except ImportError:
      errCode = 2
      errText = "Undeclared 'SUMO_HOME' environment variable as the root directory of your SUMO installation (it should contain folders 'bin', 'tools' and 'docs')"
      return { 'errCode': errCode, 'errText': errText }

    # -------------------------------------------------
    # Check commands file
    # -------------------------------------------------
    if( not self.commandScheduleReadfile( self.conf["commands_file"] )):
        # self.log_file.printLog(LOG_LEVEL1, "Error reading commands for " + file_name + "\n" )
	errCode = 1
        errText = "Cannot read commands file: "+ self.conf["commands_file"]
        return { 'errCode': errCode, 'errText': errText }

    # -------------------------------------------------
    # Launch SUMO with GUI or not
    # -------------------------------------------------
    self.theSimulator = Sim.simulated_traffic(self.conf, self.log_file)
    if self.conf["interactive"]:
        sumoBinary = checkBinary('sumo-gui')
    else:
        sumoBinary = checkBinary('sumo')

    # -------------------------------------------------
    # Start sumo and connect to it (traci)
    # -------------------------------------------------
    self.sumoProcess = subprocess.Popen([sumoBinary, "-c", self.conf["sumo_config"],"--remote-port", str(self.conf["sumoPort"])], stdout=sys.stdout, stderr=sys.stderr)
    traci.init(self.conf["sumoPort"])

    # -------------------------------------------------
    # Define Traffic Supervision Alerts
    # -------------------------------------------------
    self.setTrafficAlertRules()

    return { 'errCode': errCode, 'errText': errText }

  # -----------------------------------------
  def applyCommands(self):
    while len(self.commandSchedule)>0 and self.commandSchedule[0].getTime()==self.theSimulator.getCurTime():
      command=self.commandSchedule.pop(0)
      self.log_file.printLog(LOG_LEVEL3,str(command.getTime()) + ": " + command.getName() + "\n")
      self.log_file.printLog (LOG_LEVEL3,str(command.getParams()) + "\n")
      com_name=command.getName().lower()
      com_params=command.getParams()

      if com_name=="maps":
        self.theSimulator.processMaps(com_params[0])
      elif com_name=="incident":
        self.theSimulator.processIncident(com_params[0])
      elif com_name=="restore":
        self.theSimulator.processRestore(com_params[0])
      else:
        self.log_file.printLog(LOG_LEVEL1,"Command " + com_name + " not recognized \n")

  # -----------------------------------------
  def updateVehicles(self):
    l_vehicles_in=traci.vehicle.getIDList()
    for veh in l_vehicles_in:
        self.theSimulator.actVehicleStatistics(veh)
    l_vehicles_out=traci.simulation.getArrivedIDList()
    for veh in l_vehicles_out:
        self.theSimulator.actArriveTime(veh)
    return

  # -----------------------------------------
  # Check if the current simulation has finished.
  # Termination conditions:
  #	- End condition 1: reach max num simulations
  #	- End condition 2: do not exceed max time
  # -----------------------------------------
  def notFinished(self):
    if(     (traci.simulation.getMinExpectedNumber() > 0)
        and (int(self.theSimulator.getCurTime())<int(self.theSimulator.getEnd())) ):
      return True
    else:
      return False

  # -----------------------------------------
  def preStep(self):
    self.theSimulator.actCurTime()
    self.log_file.printLog(LOG_LEVEL3,"Processing step: " + str(self.theSimulator.getCurTime()) + "\n")
    self.theSimulator.processPendings()

  # -----------------------------------------
  def doSimulationStep(self):
    self.applyCommands()
    veh_list=traci.vehicle.getIDList()

    self.theSimulator.reroute(veh_list)
    self.theSimulator.foresight(veh_list, self.conf)
    traci.simulationStep()

    self.updateVehicles()
    alerts = self.theSimulator.edges_scan( )
    return alerts

  # -------------------------------------------------
  # End of simulation
  # -------------------------------------------------
  def stop(self):
    self.theSimulator.edge_stats_dump()
    traci.close()
    print("Process terminated: step " + str(self.theSimulator.getCurTime()) + "\n")
    self.sumoProcess.terminate()
    self.theSimulator.saveStatistics(self.conf)
