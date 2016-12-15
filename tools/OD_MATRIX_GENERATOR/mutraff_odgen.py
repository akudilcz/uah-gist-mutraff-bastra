'''
Created on: 14/12/2016

@author: Alvaro Paricio
@description: Extract the O/D weight matrix from a network diagram
'''

import argparse as arg
import sys
from lxml import etree
import numpy as np
import pandas as pd
from collections import defaultdict

# --------------------------------------------------------------
def printBanner():
  # Take here the banner: http://patorjk.com/software/taag/#p=display&f=Doom&t=mutraff%20odgen
  # Font: Doom
  print("                 _              __  __             _                  ")
  print("                | |            / _|/ _|           | |                 ")
  print(" _ __ ___  _   _| |_ _ __ __ _| |_| |_    ___   __| | __ _  ___ _ __  ")
  print("| '_ ` _ \| | | | __| '__/ _` |  _|  _|  / _ \ / _` |/ _` |/ _ \ '_ \ ")
  print("| | | | | | |_| | |_| | | (_| | | | |   | (_) | (_| | (_| |  __/ | | |")
  print("|_| |_| |_|\__,_|\__|_|  \__,_|_| |_|    \___/ \__,_|\__, |\___|_| |_|")
  print("                                                      __/ |           ")
  print("                                                     |___/            \n")
  print("                 MUTRAFF O/D Matrix generator")
  print("                    alvaro.paricio@uah.es")
  print("")

# --------------------------------------------------------------
opts		= {}
edge_weights	= defaultdict(dict)
od_trips	= defaultdict(dict)
od_edgeIds	= defaultdict(dict)
od_types	= defaultdict(dict)
od_weights	= defaultdict(dict)
od_names	= defaultdict(dict)
od_priorities	= defaultdict(dict)

# --------------------------------------------------------------
def error(code,msg):
  print('ERROR: '+msg)
  exit(code)

# --------------------------------------------------------------
def getConfig():
  parser = arg.ArgumentParser(
  	prog="mutraff_odgen",
	formatter_class=arg.RawDescriptionHelpFormatter,
  	description='''\
MuTRAFF Origin/Destination Demand Matrices generator.
Generates different kinds of O/D matrices from the SUMO simulation files: network and trip files.
Examples:
  * Generate all matrices:
    python mutraff_odgen.py -n alcalahenares.net.xml -d alcalahenares_L_Bastra_uni1x8_timeALL_fulltraffic_logit50.trip.xml -A
  * Generate time-filtered trip counters:
    python mutraff_odgen.py -fti 1 -fte 2 -n alcalahenares.net.xml -C -d alcalahenares_L_Bastra_uni1x8_timeALL_fulltraffic_logit50.trip.xml
''')
  # REQUIRED OPTS
  parser.add_argument( "-n","--in-net", help='Input. SUMOs XML net description file', default="mutraff.net.xml", required=True)
  # NON-REQUIRED OPTS
  parser.add_argument( "-d","--in-demand", help='Input. SUMOs trip file', required=False)
  parser.add_argument( "-v","--verbose", help='Verbose output', default=False, action='store_true')
  parser.add_argument( "-p","--out-prefix", help='Output. prefix for O/D generated files', default="mutraff", required=False)
  parser.add_argument( "-A","--out-all", help='Output. Generate all the O/D matrices', default=False, action='store_true')
  parser.add_argument( "-I","--out-edge-ids", help='Output. Generate O/D matrix with edge ids', default=False, action='store_true')
  parser.add_argument( "-T","--out-edge-types", help='Output. Generate O/D matrix with edge types', default=False, action='store_true')
  parser.add_argument( "-P","--out-edge-priorities", help='Output. Generate O/D matrix with edge priorities',default=False, action='store_true')
  parser.add_argument( "-W","--out-weights", help='Output. Generate O/D matrix with edge weights', default=False, action='store_true')
  parser.add_argument( "-C","--out-trip-counters", help='Output. Generate O/D matrix with timeless trip counters. Requires -d option enabled', default=False, action='store_true')
  parser.add_argument( "-N","--out-names", help='Output. Generate O/D matrix with street names', default=False, action='store_true')
  # filters
  parser.add_argument( "-fti","--filter-time-ini", help='Filter. Dump trips from specified time', default=False )
  parser.add_argument( "-fte","--filter-time-end", help='Filter. Dump trips up to specified time', default=False )

  options = vars(parser.parse_args())
  if( options['out_all'] ):
    options['out_edge_ids'] = True
    options['out_edge_types'] = True
    options['out_edge_priorities'] = True
    options['out_weights'] = True
    options['out_trip_counters'] = True
    options['out_names'] = True

  if( options['out_trip_counters'] and not options['in_demand'] ):
    parser.error('-C/--out-trip-counters requires -d/--in-demand setting enabled')
    error(1,'Bad config')

  if( options['filter_time_ini'] ):
    options['filter_time_ini'] = float(options['filter_time_ini'])

  if( options['filter_time_end'] ):
    options['filter_time_end'] = float(options['filter_time_end'])

  if( options['verbose'] ):
    print(options)
  return options


# --------------------------------------------------------------
def parseNet(opts):
  global edge_weights

  global od_edgeIds
  global od_types
  global od_weights
  global od_names
  global od_priorities

  print( "Start parsing netfile" );

  root = {}
  netfile=opts['in_net']
  try:
    tree=etree.parse(netfile)
    root=tree.getroot()
  except:
    error(2,"Parsing "+netfile+" file. Exception: "+sys.exc_info()[0] )

  # -- Weight format --
  # {'priority': '1', 'width': '2.00', 'allow': 'pedestrian', 'oneway': '1', 'numLanes': '1', 'speed': '2.78', 'id': 'highway.bridleway'}

  for elem in root:
   #print(elem)
   try:
    if( elem.tag ):
      if( elem.tag == 'type' ):
        edge_weights[elem.attrib['id']] = elem.attrib['speed']

      if( elem.tag == 'edge' ):
        if( not ('function' in elem.attrib and elem.attrib['function'] == 'internal' )):
	  #print('edge['+vfrom+','+vto+']='+elem.attrib['id'])
	  #print(elem.attrib)

	  vfrom = elem.attrib['from']
	  vto = elem.attrib['to']

	  od_edgeIds[vfrom][vto] = elem.attrib['id']
	  vtype = elem.attrib['type']
	  od_types[vfrom][vto] = vtype
	  if vtype in edge_weights:
	    od_weights[vfrom][vto] = edge_weights[vtype]
	  else:
	    od_weights[vfrom][vto] = 0
	  od_names[vfrom][vto] = elem.attrib['name'] if 'name' in elem.attrib else ''
	  od_priorities[vfrom][vto] = elem.attrib['priority'] if 'priority' in elem.attrib else 0

      if( elem.tag == 'tlLogic' or elem.tag == 'junction' ):
        print("End parsing")
        return
   except:
     error(3,"Error parsing XML tree. Exception: "+sys.exc_info()[0])
  print( "End parsing netfile" );

# --------------------------------------------------------------
def parseDemand(opts):
  global od_trips
  global od_edgeIds

  tot_trips = 0
  count_trips = 0

  print( "Reset counters" );
  # Reset counters with default values
  for vfrom in od_edgeIds:
    for vto in od_edgeIds[vfrom]:
	  od_trips[vfrom][vto] = 0

  print( "Start parsing demand file" );
  # Read Demand file
  root = {}
  demandfile=opts['in_demand']
  try:
    tree=etree.parse(demandfile)
    root=tree.getroot()
  except:
    error(2,"Parsing "+demandfile+" file. Exception: "+sys.exc_info()[0] )

  # -- Trip format --
  # <trip id="9100" depart="0.14" from="4616750#0" to="23858590#3" fromTaz="4" toTaz="99" departLane="best" departSpeed="0"/>

  for elem in root:
   try:
    if( elem.tag ):
      if( elem.tag == 'trip' ):
	tot_trips += 1
	# print(elem.attrib)
	vfrom = elem.attrib['from']
	vto = elem.attrib['to']
	depart = float(elem.attrib['depart'])
	count = True

	if( opts['filter_time_ini'] and depart < opts['filter_time_ini'] ):
	  count = False
	if( opts['filter_time_end'] and depart > opts['filter_time_end'] ):
	  count = False

	if( count ):
	  count_trips += 1
	  if( vfrom in od_trips and vto in od_trips[vfrom] ):
            od_trips[vfrom][vto] += 1
	  else:
	    od_trips[vfrom][vto] = 1
   except:
     error(3,"Error setting value. Exception: "+sys.exc_info()[0])
  print( "End parsing demand file" );

  print("Counted trips: "+str(count_trips)+"/"+str(tot_trips) )

# --------------------------------------------------------------
def dumpODmatrices():
  global od_edgeIds
  global od_types
  global od_weights
  global od_names
  global od_priorities
  global od_trips

  if( opts['out_weights'] ):
    print("Generating od matrix for edge weights")
    df = pd.DataFrame(od_weights).T.fillna(0)
    df.to_csv( opts['out_prefix']+"_od_weights.csv" )

  if( opts['out_edge_types'] ):
    print("Generating od matrix for edge types")
    df = pd.DataFrame(od_types).T.fillna(0)
    df.to_csv( opts['out_prefix']+"_od_types.csv" )

  if( opts['out_edge_ids'] ):
    print("Generating od matrix for edge ids")
    df = pd.DataFrame(od_edgeIds).T.fillna(0)
    df.to_csv( opts['out_prefix']+"_od_edgeids.csv" )

  if( opts['out_names'] ):
    print("Generating od matrix for edge names")
    df = pd.DataFrame(od_names).T.fillna(0)
    df.to_csv( opts['out_prefix']+"_od_names.csv", encoding='utf-8' )

  if( opts['out_edge_priorities'] ):
    print("Generating od matrix for edge priorities")
    df = pd.DataFrame(od_priorities).T.fillna(0)
    df.to_csv( opts['out_prefix']+"_od_priorities.csv" )

  if( opts['out_trip_counters'] ):
    print("Generating od matrix for trip counters")
    df = pd.DataFrame(od_trips).T.fillna(0)
    df.to_csv( opts['out_prefix']+"_od_trips.csv" )

# --------------------------------------------------------------
if __name__ == '__main__':
  printBanner();
  opts=getConfig()
  parseNet(opts)
  if( opts['out_trip_counters'] ):
    parseDemand(opts)
  dumpODmatrices()

print("Generated files")
