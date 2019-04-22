'''
Created on 27/09/2016

@author: Alvaro Paricio alvaro.paricio@uah.es
'''

import time
from mutraff import Controller

import argparse
import sys
import os
import re
import time
from lxml import etree

# ----------------------------------
def printBanner():
  # Take here the banner: http://patorjk.com/software/taag/#p=display&f=Doom&t=mutraff%20ctrl
  # Font: Doom
  print("                          _              __  __        _        _ ")
  print("                         | |            / _|/ _|      | |      | |")
  print("          _ __ ___  _   _| |_ _ __ __ _| |_| |_    ___| |_ _ __| |")
  print("         | '_ ` _ \| | | | __| '__/ _` |  _|  _|  / __| __| '__| |")
  print("         | | | | | | |_| | |_| | | (_| | | | |   | (__| |_| |  | |")
  print("         |_| |_| |_|\__,_|\__|_|  \__,_|_| |_|    \___|\__|_|  |_|\n")
  print("                 TRAFFIC OPERATIONS CENTER CONTROLLER")
  print("")

# ----------------------------------
flag_exit    = False
commands = {}

commands['help'] = { 'group':'GLOBAL', 'callb':'helpCb', 'label':'Print commands help', 'help':'Args: all|*|command', 'args':1 }
commands['?'] = commands['help']

commands['quit'] = { 'group':'GLOBAL', 'callb':'quitCb', 'label':'Quit', 'help':'No args', 'args':0 }
commands['exit'] = commands['quit']
commands['.'] = commands['quit']

commands['verbose'] = { 'group':'GLOBAL', 'callb':'verboseCb', 'label':'Verbose mode', 'help':'Args: entity level. Entity can be all|Controller|TOC|VEHICLES|concreteName. Level is a 0-10 integer.', 'args':2 }

commands['about'] = { 'group':'GLOBAL', 'callb':'aboutCb', 'label':'About Mutraff', 'help':'No args', 'args':0 }

commands['stopall'] = { 'group':'GLOBAL', 'callb':'stopAllCb', 'label':'Stop whole MuTRAFF distributed system: TOC, vehicles, signalling, etc', 'help':'No args', 'args':0 }

commands['map'] = { 'group':'TOC', 'callb':'mapPublishCb', 'label':'Publish changes in TWM (Traffic Weight Maps)', 'help':'Args: mapDistributionFile\n      Example: > map grid16_Bastra_rand05x4_timeALL_fulltraffic_logit50.maps.xml', 'args':1 }

commands['incident'] = { 'group':'TOC', 'callb':'incidentPublishCb', 'label':'Publish traffic incident at edge', 'help':'Args: add|del incidentName edge\n      Example: > incident add ACCIDENT-37 1/2to0/2', 'args':3 }

commands['edge'] = { 'group':'TOC', 'callb':'edgePublishCb', 'label':'Publish changes at edge', 'help':'Args: edgeName feature value\n      Example: > edge 1/2to0/2 weight 30.45', 'args':3 }

commands['globalwarn'] = { 'group':'TOC', 'callb':'globalwarnPublishCb', 'label':'Publish a global warning to disuade demand', 'help':'Args: intensity (0-100)\n      Example: > globalwarn 20', 'args':1 }

commands['edgewarn'] = { 'group':'TOC', 'callb':'edgewarnPublishCb', 'label':'Publish a warning on edge to disuade demand. Used at incoming edges', 'help':'Args: edgeName intensity (0-100)\n      Example: > edgewarn 1/2to0/2 20', 'args':2 }

# ----------------------------------
def getConfig():
  parser = argparse.ArgumentParser("mutraff_ctl")
  # REQUIRED OPTS
  # parser.add_argument( "-c","--config_file", help='Configuration_file', default="mutraff_toc.conf", required=True )
  parser.add_argument( "-x","--amqp_exchange_name", help='AMQP Exchange name', default="es.uah.gist.mutraff.toc1", required=True)
  # NON-REQUIRED OPTS
  parser.add_argument( "-H","--amqp_host", help='AMQP host DNS name or IP address. Defaul is localhost', default="localhost")
  options = vars(parser.parse_args())
  return options

# ----------------------------------
def quitCb():
  print("Exiting MuTRAFF Controller")
  global flag_exit
  flag_exit = True

# ----------------------------------
def verboseCb(entity,level):
  return Controller.verbosePublish(entity,level)

# ----------------------------------
def mapPublishCb(mapFile):
  return Controller.mapPublish(mapFile)

# ----------------------------------
def incidentPublishCb(action, incName, edgeName):
  return Controller.incidentPublish(action, incName, edgeName)

# ----------------------------------
def edgePublishCb(edgeName, feature, value):
  return Controller.edgePublish(edgeName, feature, value)

# ----------------------------------
def globalwarnPublishCb(intensity):
  msg = raw_input("Warn Message > ")
  return Controller.globalwarnPublish(intensity,msg)

# ----------------------------------
def edgewarnPublishCb(edgeName, intensity):
  msg = raw_input("Warn Message > ")
  return Controller.edgewarnPublish(edgeName, intensity,msg)

# ----------------------------------
def stopAllCb():
  print("Sending STOP signal to all the MuTRAFF entities")
  return Controller.stopSimulation()
    

# ----------------------------------
def aboutCb():
  printBanner()
  print("Created by:\n  Alvaro Paricio (alvaro.paricio@uah.es)\n  Miguel Angel Lopez Carmona (miguelangel.lopez@uah.es)\nAt UAH - GIST Research Group, www.uah.es\n")
  print("Thanks and acknoledges to:")
  print("  Valentin Alberti, for Bastra contributions")
  print("  http://patorjk.com/software/taag/#p=display&f=Doom&t=mutraff%20ctrl for the banner")
  return 0


# ----------------------------------
def helpCb(topic):
  if( topic == 'all' or topic == '*' ):
    print("Available commands:")
    for opt in commands:
      print("  * "+ opt + ": "+ commands[opt]['label'] )
      # print("      "+ commands[opt]['help'] )
    print("For more info type 'help topic'")
  else:
    if( topic in commands ):
      print("  * "+ topic + ": "+ commands[topic]['label'] )
      print("      "+ commands[topic]['help'] )
    else:
      print("  Unknown help topic '{:s}'".format(topic))
  return 0

# ----------------------------------
# MAIN
# ----------------------------------
if __name__ == '__main__':
  # --- Config reading parameters
  args=getConfig()
  printBanner();

  Controller = Controller.Controller( args['amqp_host'], args['amqp_exchange_name'] )
  Controller.connectionsStart()
  Controller.listenChannels()
  print("Check the About option and enter help or ? for commands info.\n")
  opt = ""
  while( not flag_exit ):
    opt = raw_input("Mutraff > ").lower()
    if( opt == "" ):
      continue
    opts = re.sub( '^ ','', re.sub(' +',' ',opt)).split(' ')
    cmd = opts[0]
    del opts[0]
    if( cmd in commands ):
      if( commands[cmd]['args'] != len(opts) ):
	print( cmd+": Invalid arguments syntax. "+commands[cmd]['help'] )
      else:
        # print("Calling:",commands[cmd]['callb']+"()")
        result = eval(commands[cmd]['callb']+str(tuple(opts)))
    else:
      print("* Unknown command. Use ? for help *")
  Controller.connectionsStop()
  sys.exit(0)
