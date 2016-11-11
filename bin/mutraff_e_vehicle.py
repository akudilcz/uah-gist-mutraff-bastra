'''
Created on 27/09/2016

@author: Alvaro Paricio alvaro.paricio@uah.es
'''

import optparse
import sys
import os
import time
from lxml import etree
from mutraff import Vehicle

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

    # --- Read config parameters
    param=getConfig()
    message_exchange = param.message_exchange

    # --- Define and launch the Vehicle
    VEH = Vehicle.Vehicle( "veh-1", "(PLATE) M-6428-WP", "localhost", message_exchange )

    # To use internal amq exchange server, use this line. IT is not recommended though!
    # VEH = Vehicle.Vehicle( "veh-1", "(PLATE) M-6428-WP", "localhost", "amq.topic" )

    
    # VEH.setVRoutePublishEpochs( 10 )
    VEH.setVRoutePublishFrecuency( 10 )

    VEH.connectionsStart()
    VEH.mainLoop()
    VEH.connectionsStop()

