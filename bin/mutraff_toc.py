'''
Created on 27/09/2016

@author: Alvaro Paricio alvaro.paricio@uah.es
'''

import argparse
import sys
import os
import time
from lxml import etree
from mutraff import TrafficCenter

# ----------------------------------
def printBanner(args):
  # Take here the banner: http://patorjk.com/software/taag/#p=display&f=Doom&t=mutraff%20ctrl
  # Font: Doom
  print("                 _              __  __   _____ _____ _____ ")
  print("                | |            / _|/ _| |_   _|  _  /  __ \\")
  print(" _ __ ___  _   _| |_ _ __ __ _| |_| |_    | | | | | | /  \/")
  print("| '_ ` _ \| | | | __| '__/ _` |  _|  _|   | | | | | | |    ")
  print("| | | | | | |_| | |_| | | (_| | | | |     | | \ \_/ / \__/\\")
  print("|_| |_| |_|\__,_|\__|_|  \__,_|_| |_|     \_/  \___/ \____/\n")
  print("                 TRAFFIC OPERATIONS CENTER \n")
  print("* Execution Mode: "+ args['exec_mode'])
  print("* Scenario      : "+ args['scene'])
  print("")


# ----------------------------------
# Read options under the desired branch (named as "program")
# ----------------------------------
def config_file_read_option(l_config, option, section ):
    try:
        label=l_config[ 0].find(option)
        value=label.get("value")
    except:
        sys.exit("Configuration error: value for " + option + " not found in section " + section )

    return value

# ----------------------------------
def config_file_load(conf_file):
    # ----------------------------
    conf_section="Bastra"
    # ----------------------------
    try:
        tree=etree.parse(conf_file)
        root=tree.getroot()
        l_config=root.findall(conf_section)
    except:
        sys.exit("Configuration file error for " + conf_file + " for XML section " + conf_section )

    f_conf={}
    f_conf["tmp_dir"]=config_file_read_option(l_config, "tmp_dir", conf_section )
    f_conf["results_dir"]=config_file_read_option(l_config, "results_dir", conf_section )
    f_conf["log_dir"]=config_file_read_option(l_config, "log_dir", conf_section )
    f_conf["log_file"]=config_file_read_option(l_config, "log_file", conf_section )
    f_conf["log_level"]=config_file_read_option(l_config, "log_level", conf_section )
    f_conf["dump_dir"]=config_file_read_option(l_config, "dump_dir", conf_section )
    f_conf["new_routes_file"]=config_file_read_option(l_config, "new_routes_file", conf_section )
    f_conf["route_file"]=config_file_read_option(l_config, "route_file", conf_section )
    f_conf["logit"]=config_file_read_option(l_config, "logit", conf_section )
    f_conf["commands_file"]=config_file_read_option(l_config, "commands_file", conf_section )
    f_conf["statistics_f"]=config_file_read_option(l_config, "statistics_file", conf_section )
    f_conf["begin"]=config_file_read_option(l_config, "begin", conf_section )
    f_conf["end"]=config_file_read_option(l_config, "end", conf_section )

    f_conf["f_tries"]=0
    try:
      f_conf["f_tries"]=int(config_file_read_option(l_config, "foresight_tries", conf_section ))
    except:
      f_conf["f_tries"]=0

    f_conf["f_steps"]=0
    try:
      f_conf["f_steps"]=int(config_file_read_option(l_config, "foresight_steps", conf_section ))
    except:
      f_conf["f_steps"]=0

    f_conf["f_halting"]=config_file_read_option(l_config, "foresight_halting", conf_section )
    f_conf["f_penalty"]=config_file_read_option(l_config, "foresight_penalty", conf_section )

    # Alvaro Added: 15/09/16
    try:
      f_conf["csv_sep"]=config_file_read_option(l_config, "csv_sep", conf_section )
    except:
       f_conf["csv_sep"]=','

    # Alvaro Added: 10/10/16
    f_conf["edge_stats_dump"]=False
    try:
      # True / False
      if( config_file_read_option(l_config, "edge_stats_dump", conf_section ).lower() == "true" ):
        f_conf["edge_stats_dump"]=True
    except:
       f_conf["edge_stats_dump"]=False
    try:
      f_conf["edge_stats_file"]=config_file_read_option(l_config, "edge_stats_file", conf_section )
    except:
      f_conf["edge_stats_file"]='edge_stats.csv'

    try:
      f_conf["edge_stats_sampling"]=int(config_file_read_option(l_config, "edge_stats_sampling", conf_section ))
    except:
      # If not defined, use a value enough to take at least 100 samples
      v = int((int(f_conf["end"])-int(f_conf["begin"]))/100)
      if( v < 0 ):
        v = 1
      f_conf["edge_stats_sampling"]=v

    # Alvaro Added: 11/11/16
    try:
      f_conf["publish_alerts"]=config_file_read_option(l_config, "publish_alerts", conf_section )
    except:
      f_conf["publish_alerts"]='true'

    # Alvaro Added: 15/11/16
    try:
      f_conf["publish_edgeStats"]=config_file_read_option(l_config, "publish_edgeStats", conf_section )
    except:
      f_conf["publish_edgeStats"]='false'

    # Alvaro Added: 15/11/16
    try:
      f_conf["routing_algorithm"]=config_file_read_option(l_config, "routing_algorithm", conf_section).lower()
    except:
      f_conf["routing_algorithm"]=""
    if( not f_conf["routing_algorithm"] in ['','dijstra','astar','ch','chwrapper'] ):
      f_conf["routing_algorithm"]=""
    log_file.printLog(LEVEL1, "Selected routing algorithm:"+f_conf["routing_algorithm"])


    str_verbose=config_file_read_option(l_config, "verbose", conf_section )
    str_verbose.lower()
    if str_verbose=="true":
        f_conf["verbose"]=True
    elif str_verbose=="false":
        f_conf["verbose"]=False
    else:
        sys.exit("Configuration error: wrong value for 'verbose' in bastra's configuration file")
    str_balanced=config_file_read_option(l_config, "use_balance", conf_section )
    balanced=str_balanced.lower()
    if balanced=="true":
        f_conf["balanced"]=True
    elif balanced=="false":
        f_conf["balanced"]=False
    else:
        sys.exit("Configuration error: wrong value for 'use_balance' in bastra's configuration file")

    # ----------------------------
    conf_section="Sumo"
    # ----------------------------
    try:
        l_config=root.findall(conf_section)
    except:
        sys.exit("Configuration error: value for " + option + " not found in section " + section )

    str_interactive=config_file_read_option(l_config, "interactive", conf_section )
    str_interactive.lower()
    if str_interactive=="true":
        f_conf["interactive"]=True
    elif str_interactive=="false":
        f_conf["interactive"]=False
    f_conf["net_file"]=config_file_read_option(l_config, "net_file", conf_section )
    f_conf["sumo_log_file"]=config_file_read_option(l_config, "log_file", conf_section )
    f_conf["sumo_config"]=config_file_read_option(l_config, "sumo_config", conf_section )
    str_sumoPort=config_file_read_option(l_config, "port", conf_section )
    try:
        f_conf["sumoPort"]=int(str_sumoPort)
    except:
        sys.exit("Configuration error: wrong value for SumoPort in " + config_file)

    # ----------------------------
    # Additional validations
    # ----------------------------
    if not os.path.isdir(f_conf["tmp_dir"]):
        sys.exit("Configuration error: directory pointed by tmp_dir value not found")

    if not os.path.isdir(f_conf["log_dir"]):
        sys.exit("Configuration error: directory pointed by log_dir value not found")

    if not os.path.isdir(f_conf["dump_dir"]):
        sys.exit("Configuration error: directory pointed by dump_dir value not found")

    if not os.path.isdir(f_conf["results_dir"]):
        sys.exit("Configuration error: directory pointed by results_dir value not found")

    return f_conf


# ----------------------------------
def getConfig():
  parser = argparse.ArgumentParser("Traffic Operations Center")
  # REQUIRED OPTS
  parser.add_argument( "-c","--config_file", help='Configuration_file', default="mutraff_toc.conf", required=True )
  parser.add_argument( "-x","--amqp_exchange_name", help='AMQP Exchange name', default="edu.uah.gist.mutraff.toc1", required=True)
  # NON-REQUIRED OPTS
  parser.add_argument( "-H","--amqp_host", help='AMQP host DNS name or IP address. Defaul is localhost', default="localhost")
  parser.add_argument( "-I","--amqp_toc_id", help='Traffic Operation Center unique ID. Default is: MAD-1', default="MAD-1")
  parser.add_argument( "-N","--amqp_toc_name", help='Traffic Operation Center name. Default is: MADRID TRAFFIC OPERATIONS CENTER 1', default="MADRID TRAFFIC OPERATIONS CENTER 1")
  parser.add_argument( "-m","--exec_mode", help='Execution mode. STANDARD, SIMULATION', default="SIMULATION")
  parser.add_argument( "-s","--scene", help='Scene name.', default="None")
  parser.add_argument( "-v","--verbose", help='Verbosity', default=1)
  options = vars(parser.parse_args())
  options['amqp_control'] = 'toc.control'

  options.update( config_file_load(options['config_file']) )

  return options

# ----------------------------------
# MAIN
# ----------------------------------
if __name__ == '__main__':
  # --- Read config parameters
  args=getConfig()

  printBanner(args)

  # --- define constants

  # --- Define and launch the Traffic Ops Center
  TOC = TrafficCenter.TrafficCenter( args )

  # TOC.setMapPublishEpochs( 10 )
  # TOC.setMapPublishFrecuency( 10 )

  TOC.connectionsStart()
  TOC.mainLoop()
  print( "END" )
  TOC.connectionsStop()

