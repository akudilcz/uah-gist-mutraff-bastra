'''
Created on 27/09/2016

@author: Alvaro Paricio alvaro.paricio@uah.es
'''

import time
from mutraffLib import Controller

import optparse
import sys
import os
import time
from lxml import etree
from mutraffLib import TrafficCenter

# ----------------------------------
def getConfig():
  parser = optparse.OptionParser( sys.argv[0]+": required communications exchange reference with -x option. Example: -x my_comms")
  parser.add_option("-x", dest="message_exchange", type="string")
  (options, args) = parser.parse_args()
  return options

# ----------------------------------
# MAIN
# ----------------------------------
if __name__ == '__main__':
    # --- define constants

    # --- Config reading parameters
    param=getConfig()
    message_exchange = param.message_exchange

    # ----------------------------------
    Controller = Controller.Controller( "localhost", message_exchange )
    Controller.stopSimulation()
