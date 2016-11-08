'''
Created on 27/09/2016

@author: Alvaro Paricio alvaro.paricio@uah.es
'''

import time
from mutraffLib import Controller

import argparse
import sys
import os
import time
from lxml import etree
from mutraffLib import TrafficCenter

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

# ----------------------------------
commands = {}
commands['help'] = { 'group':'GLOBAL', 'callb':'helpCb', 'label':'Help', 'help':'Print Mutraff Controller help' }
commands['?'] = commands['help']
commands['quit'] = { 'group':'GLOBAL', 'callb':'quitCb', 'label':'Quit', 'help':'Quit Mutraff Controller' }
commands['exit'] = commands['quit']
commands['.'] = commands['quit']
commands['about'] = { 'group':'GLOBAL', 'callb':'aboutCb', 'label':'About Mutraff', 'help':'About Mutraff Controller' }
commands['stopall'] = { 'group':'GLOBAL', 'callb':'stopAllCb', 'label':'STOP ALL', 'help':'STOP all entities (TOC, vehicles, signalling, etc)' }
commands['map_publish'] = { 'group':'TOC', 'callb':'mapPublishCb', 'label':'Publish MAP', 'help':'Publish MAP' }

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
  sys.exit(0)

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
def helpCb():
  print("Available commands:")
  for opt in commands:
    print("  * "+ opt + ": "+ commands[opt]['help'] )
  return 0

# ----------------------------------
# MAIN
# ----------------------------------
if __name__ == '__main__':
  # --- Config reading parameters
  args=getConfig()
  Controller = Controller.Controller( args['amqp_host'], args['amqp_exchange_name'] )
  printBanner();
  print("Check the About option and enter help or ? for commands info.\n")
  opt = ""
  while( opt != "quit" ):
    # print("Mutraff >")
    # opt = sys.stdin.readline()
    opt = raw_input("Mutraff > ").lower()
    if( opt in commands ):
      # print("Calling:",commands[opt]['callb']+"()")
      result = eval(commands[opt]['callb']+"()")
