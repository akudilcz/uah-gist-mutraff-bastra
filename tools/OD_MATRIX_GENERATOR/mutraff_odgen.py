'''
Created on: 14/12/2016

@author: Alvaro Paricio
@description: Extract the O/D weight matrix from a network diagram
'''

import argparse as arg
import os
import sys
import math
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
opts              = {}
edge_types_speeds = defaultdict(dict)
od_trips          = defaultdict(dict)
od_grouped_trips  = defaultdict(dict)
od_nodes          = defaultdict(dict)
od_edgeIds        = defaultdict(dict)
od_edges          = defaultdict(dict)
od_types          = defaultdict(dict)
od_speeds         = defaultdict(dict)
od_weights        = defaultdict(dict)
od_lengths        = defaultdict(dict)
od_names          = defaultdict(dict)
od_priorities     = defaultdict(dict)
od_tazs           = defaultdict(dict)
od_taz_nodes      = defaultdict(dict)

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
    python mutraff_odgen.py -n alcalahenares.net.xml -d alcalahenares_L_Bastra_uni1x8_timeALL_fulltraffic_logit50.trip.xml -A -x alcalahenares.nod.xml
  * Generate time-filtered trip counters:
    python mutraff_odgen.py -fti 1 -fte 2 -n alcalahenares.net.xml -C -d alcalahenares_L_Bastra_uni1x8_timeALL_fulltraffic_logit50.trip.xml -x alcalahenares.nod.xml
''')
  # REQUIRED OPTS
  parser.add_argument( "-n","--in-net", help='Input. SUMOs XML net description file', default="mutraff.net.xml", required=True)
  parser.add_argument( "-x","--in-nodes", help='Input. SUMOs XML nodes description file', default="mutraff.nod.xml", required=True)
  # NON-REQUIRED OPTS
  parser.add_argument( "-d","--in-demand", help='Input. SUMOs trip file', required=False)
  parser.add_argument( "-v","--verbose", help='Verbose output', default=False, action='store_true')
  parser.add_argument( "-p","--out-prefix", help='Output. prefix for O/D generated files', default="mutraff", required=False)
  parser.add_argument( "-O","--out-dir", help='Output. Directory for generated files', default=".", required=False)
  parser.add_argument( "-A","--out-all", help='Output. Generate all the O/D matrices', default=False, action='store_true')
  parser.add_argument( "-I","--out-edge-ids", help='Output. Generate O/D matrix with edge ids', default=False, action='store_true')
  parser.add_argument( "-T","--out-edge-types", help='Output. Generate O/D matrix with edge types', default=False, action='store_true')
  parser.add_argument( "-P","--out-edge-priorities", help='Output. Generate O/D matrix with edge priorities',default=False, action='store_true')
  parser.add_argument( "-W","--out-fftt", help='Output. Generate O/D matrix with edge weights as FREE-FLOW TRAVEL TIMES', default=False, action='store_true')
  parser.add_argument( "-L","--out-lengths", help='Output. Generate O/D matrix with edge lengths', default=False, action='store_true')
  parser.add_argument( "-S","--out-speeds", help='Output. Generate O/D matrix with edge speeds', default=False, action='store_true')
  parser.add_argument( "-C","--out-trip-counters", help='Output. Generate O/D matrix with timeless trip counters. Requires -d option enabled', default=False, action='store_true')
  parser.add_argument( "-G","--out-group-trip-counters", help='Output. Generate O/D matrix with timeless GROUPED trip counters. Requires -d option enabled', default=False, action='store_true')
  parser.add_argument( "-N","--out-names", help='Output. Generate O/D matrix with street names', default=False, action='store_true')
  parser.add_argument( "-W2","--out-edge-weights", help='Output. Dump default edge weights', default=False, action='store_true')
  parser.add_argument( "-X","--out-nodes", help='Output. Dump CSV nodes listing with GPS coordinates', default=False, action='store_true')
  # filters
  parser.add_argument( "-fti","--filter-time-ini", help='Filter. Dump trips from specified time', default=False )
  parser.add_argument( "-fte","--filter-time-end", help='Filter. Dump trips up to specified time', default=False )

  options = vars(parser.parse_args())
  if( options['out_all'] ):
    options['out_edge_ids'] = True
    options['out_edge_types'] = True
    options['out_edge_priorities'] = True
    options['out_speeds'] = True
    options['out_fftt'] = True
    options['out_lengths'] = True
    options['out_trip_counters'] = True
    options['out_group_trip_counters'] = True
    options['out_names'] = True
    options['out_nodes'] = True
    options['out_edge_weigths'] = True

  if( options['out_trip_counters'] and not options['in_demand'] ):
    parser.error('-C/--out-trip-counters requires -d/--in-demand setting enabled')
    error(1,'Bad config')

  if( options['out_group_trip_counters'] and not options['in_demand'] ):
    parser.error('-C/--out-group-trip-counters requires -d/--in-demand setting enabled')
    error(1,'Bad config')

  if( options['filter_time_ini'] ):
    options['filter_time_ini'] = float(options['filter_time_ini'])

  if( options['filter_time_end'] ):
    options['filter_time_end'] = float(options['filter_time_end'])

  if( options['verbose'] ):
    print(options)
    
  return options


# --------------------------------------------------------------
# http://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points
# --------------------------------------------------------------
def distance(lat1, lng1, lat2, lng2):
    #return distance as meter if you want km distance, remove "* 1000"
    radius = 6371.0 * 1000.0

    dLat = (lat2-lat1) * math.pi / 180
    dLng = (lng2-lng1) * math.pi / 180

    lat1 = lat1 * math.pi / 180
    lat2 = lat2 * math.pi / 180

    ang = 0
    try:
      val = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLng/2) * math.sin(dLng/2) * math.cos(lat1) * math.cos(lat2)    
      ang = 2 * math.atan2(math.sqrt(val), math.sqrt(1-val))
    except:
      error(2,"Calculating distance. Exception: "+str(sys.exc_info()) )
    return radius * ang

# --------------------------------------------------------------
def parseNodes(opts):
  global edge_types_speeds

  global od_edgeIds
  global od_edges
  global od_types
  global od_speeds
  global od_weights
  global od_lengths
  global od_names
  global od_priorities
  global od_nodes
  global od_trips

  print( "Start parsing nodes file" )

  root = {}
  nodesfile=opts['in_nodes']
  try:
    tree=etree.parse(nodesfile)
    root=tree.getroot()
  except:
    error(2,"Parsing "+nodesfile+" file. Exception: "+str(sys.exc_info()) )

  x_min = x_max = y_min = y_max = 0
  for elem in root:
   # print(elem)
   try:
    if( elem.tag ):
      if( elem.tag == 'node' ):
        id=elem.attrib['id']
        x= float(elem.attrib['x'])
        y= float(elem.attrib['y'])
        od_nodes[id]['x'] = x
        od_nodes[id]['y'] = y
        od_nodes[id]['taz'] = ''
        x_min = x if x < x_min else x_min
        x_max = x if x > x_max else x_max
        y_min = y if y < y_min else y_min
        y_min = y if y > y_max else y_max
        #print( "Pushed node:{}".format(id) )
   except:
     error(3,"Error parsing XML tree. Exception: "+sys.exc_info())
  print( "End parsing nodes file" )

  print( "Initializing O/D matrices")
  for x in od_nodes:
    #print "--> {}".format(x)
    for y in od_nodes:
      od_edgeIds[x][y] = ''
      od_types[x][y] = ''
      od_speeds[x][y] = 0
      od_weights[x][y] = 0
      od_lengths[x][y] = 0
      od_names[x][y] = 0
      od_priorities[x][y] = 0
      od_trips[x][y] = 0
      od_grouped_trips[x][y] = 0

# --------------------------------------------------------------
def parseNet(opts):
  global edge_types_speeds

  global od_edgeIds
  global od_edges
  global od_types
  global od_speeds
  global od_weights
  global od_lengths
  global od_names
  global od_priorities
  global od_nodes
  global od_tazs
  global od_taz_nodes

  flag_debug=False

  print( "Start parsing netfile" );
  od_taz_nodes['from']={}
  od_taz_nodes['to']={}

  root = {}
  netfile=opts['in_net']
  try:
    tree=etree.parse(netfile)
    root=tree.getroot()
  except:
    error(2,"Parsing "+netfile+" file. Exception: "+str(sys.exc_info()) )

  # -- Weight format --
  # {'priority': '1', 'width': '2.00', 'allow': 'pedestrian', 'oneway': '1', 'numLanes': '1', 'speed': '2.78', 'id': 'highway.bridleway'}

  for elem in root:
   if flag_debug:
     print(elem)
   try:
    if( elem.tag ):
      # ----------------------------------------------
      if( elem.tag == 'type' ):
        edge_types_speeds[elem.attrib['id']] = elem.attrib['speed']

      # ----------------------------------------------
      if( elem.tag == 'edge' ):
        if( not ('function' in elem.attrib and elem.attrib['function'] == 'internal' )):
          edge_id = elem.attrib['id']
          #print('edge['+vfrom+','+vto+']='+edge_id)
          #print(elem.attrib)

          vfrom = elem.attrib['from']
          vto = elem.attrib['to']

          # -----------------
          od_edgeIds[vfrom][vto] = edge_id

          # -----------------
          od_edges[edge_id]['from'] = vfrom
          od_edges[edge_id]['to'] = vto

          # -----------------
          vtype = elem.attrib['type']
          od_types[vfrom][vto] = vtype

          # -----------------
          speed = 0
          if vtype in edge_types_speeds:
            speed = float(edge_types_speeds[vtype])
          od_speeds[vfrom][vto] = speed

          # -----------------
          od_edges[edge_id]['speed'] = speed
          lat1 = od_nodes[vfrom]['y']
          lon1 = od_nodes[vfrom]['x']
          lat2 = od_nodes[vto]['y']
          lon2 = od_nodes[vto]['x']
          linear_distance = distance(lat1, lon1, lat2, lon2)
	  # Length = true path length
	  # Distance = linear distance between origen and destiantion coordinates
          od_edges[edge_id]['length'] = linear_distance
          od_edges[edge_id]['distance'] = linear_distance
          weight = 999
          if speed > 0:
             weight = linear_distance/speed
          od_edges[edge_id]['weight'] = weight
          od_weights[vfrom][vto] = weight
          od_lengths[vfrom][vto] = linear_distance
          if flag_debug:
             print("EDGE({}: {}->{}): lindist={}, speed={}, FFTT={}".format( edge_id, vfrom, vto, linear_distance, speed, weight ))

          # -----------------
          od_names[vfrom][vto] = elem.attrib['name'] if 'name' in elem.attrib else ''
          # -----------------
          od_priorities[vfrom][vto] = elem.attrib['priority'] if 'priority' in elem.attrib else 0

          # ----------------------------------------------
          # edge_id, vfromm, vto --> coming from previous edge xml-tag
          for elem2 in elem.iter("lane"):
             if( elem2.tag == 'lane' ):
                #print("lane:{}".format( elem2.attrib))
                lane_id     = elem2.attrib['id']
                lane_speed  = float(elem2.attrib['speed'])
                lane_length = float(elem2.attrib['length'])
                lane_weight = 999
                if lane_speed > 0:
                   lane_weight = lane_length/lane_speed
                od_weights[vfrom][vto] = lane_weight
                od_lengths[vfrom][vto] = lane_length
                od_speeds[vfrom][vto]  = lane_speed
                od_edges[edge_id]['weight'] = lane_weight
                od_edges[edge_id]['speed']  = lane_speed
                od_edges[edge_id]['length'] = lane_length
                if flag_debug:
                   print("   LANE({}: {}->{}): length={}, speed={}, FFTT={}".format( edge_id, vfrom, vto, lane_length, lane_speed, lane_weight ))

      # ----------------------------------------------
      if( elem.tag == 'tazs' ):
        for e2 in elem:
          try:
            # --- ADD A NEW TAZ ------------------------
            if( e2.tag and e2.tag == 'taz' ):
              # print("TAZ: {}".format(e2.attrib['edges']))
              taz_id = e2.attrib['id']
              #print("Adding taz {}".format(taz_id))

              od_tazs[taz_id]['edges'] = e2.attrib['edges'].split(' ')
              od_tazs[taz_id]['nodes']  = {}
              od_tazs[taz_id]['nodes']['from'] = []
              od_tazs[taz_id]['nodes']['to'] = []
              od_tazs[taz_id]['nodes']['leader_from']=None
              od_tazs[taz_id]['nodes']['leader_to']=None

              # -- Create nodes list  ---------------
              for e in od_tazs[taz_id]['edges']:

                try:
                  vfrom = od_edges[e]['from']
                except:
                  print("Warning: TAZ parsing: found edge from-node {} out of the map".format(e))
                  continue
                try:
                  vto   = od_edges[e]['to']
                except:
                  print("Warning: TAZ parsing: found edge to-node {} out of the map".format(e))
                  continue
                od_tazs[taz_id]['nodes']['from'].append(vfrom)
                od_tazs[taz_id]['nodes']['to'].append(vto)

                if not vfrom in od_taz_nodes['from']:
                  od_taz_nodes['from'][vfrom]=[]
                od_taz_nodes['from'][vfrom].append(taz_id)

                if not vto in od_taz_nodes['from']:
                  od_taz_nodes['from'][vto]=[]
                od_taz_nodes['from'][vto].append(taz_id)

                od_nodes[vfrom]['taz'] = taz_id
                od_nodes[vto]['taz'] = taz_id

              # -- Calculate TAZ centroids  ---------------
              x =  y = 0
              for node in od_tazs[taz_id]['nodes']['from']:
                #print("--> {},{}".format(  od_nodes[node]['x'],  od_nodes[node]['y'] ))
                #print("<-- {},{}".format(  float(od_nodes[node]['x']),  float(od_nodes[node]['y']) ))
                x += od_nodes[node]['x']
                y += od_nodes[node]['y']
              x = x/len(od_tazs[taz_id]['nodes']['from'])
              y = y/len(od_tazs[taz_id]['nodes']['from'])
              od_tazs[taz_id]['nodes']['centroid']={ 'x': x, 'y':y }
          except:
            error(4,"Error parsing XML tree in TAZ. Exception: "+str(sys.exc_info()))

#      if( elem.tag == 'tlLogic' or elem.tag == 'junction' ):
#        print("End parsing")
#        return
   except:
     error(3,"Error parsing XML tree. Exception: "+str(sys.exc_info()))
  print( "End parsing netfile" );

# --------------------------------------------------------------
def calc_distance( x1, y1, x2, y2 ):
  return math.sqrt( math.pow(x1-x2,2)+math.pow(y1-y2,2) )

# --------------------------------------------------------------
def calculate_taz_leaders(opts):
  global od_tazs
  global od_taz_nodes
  print("Selecting distance leader nodes")
  num_tazs = len(od_tazs)
  for taz in od_tazs:
    # Calculate centroid from centroids of rest of tazs
    cen_x = cen_y = 0
    for t in od_tazs:
      if not taz == t:
        cen_x += od_tazs[taz]['nodes']['centroid']['x']
        cen_y += od_tazs[taz]['nodes']['centroid']['y']
    cen_x = cen_x/(num_tazs-1)
    cen_y = cen_y/(num_tazs-1)
    #print("TAZ[{}] --> Distance Centroid:{} , {}".format(taz,cen_x,cen_y) )

    # Obtain the most far node from taz to the taz centroids
    d = 0
    leader = ''
    for n in od_tazs[taz]['nodes']['from']:
      d1 = calc_distance( cen_x, cen_y, od_nodes[n]['x'], od_nodes[n]['y'] )
      #print("n:{} --> Taz[{}] --> far node:{}".format(n,taz,leader))
      if d1 > d:
        d=d1
        leader=n

    print("   Taz[{}] --> distance leader node:{}".format(taz,leader))
    od_tazs[taz]['nodes']['leader']=leader

# --------------------------------------------------------------
def dump_taz_nodes(opts):
  global od_tazs
  global od_taz_nodes
  print("=== DUMPING TAZ NODES ==================")
  for taz in od_tazs:
    print("NODES.FROM.TAZ[{}]: {}".format(taz,od_tazs[taz]['nodes']['from']))
    print("CENTROID.FROM.TAZ[{}]: {}".format(taz,od_tazs[taz]['nodes']['centroid']))
  print("========================================")

# --------------------------------------------------------------
def count_individual_trips(vfrom,vto):
  global od_trips
  if( vfrom in od_trips and vto in od_trips[vfrom] ):
    od_trips[vfrom][vto] += 1
  else:
    od_trips[vfrom][vto] = 1

# --------------------------------------------------------------
def count_group_trips(vfrom,vto):
  global od_grouped_trips
  global od_taz_nodes
  global od_tazs

  # get vfrom and vto equivalences
  if vfrom in  od_taz_nodes['from'] and len(od_taz_nodes['from'][vfrom]) > 0:
    taz = od_taz_nodes['from'][vfrom][0]
    eqfrom = od_tazs[taz]['nodes']['leader']
    #print("  --> FOUND TAZ leader equivalence for FROM:{}".format( vfrom) )
  else:
    print("  --> Not found TAZ leader equivalence for FROM:{}".format( vfrom) )
    eqfrom = vfrom

  if vto in  od_taz_nodes['from'] and len(od_taz_nodes['from'][vto]) > 0:
    taz = od_taz_nodes['from'][vto][0]
    eqto = od_tazs[taz]['nodes']['leader']
    #print("  --> FOUND TAZ leader equivalence for TO:{}".format( vfrom) )
  else:
    print("  --> Not found TAZ leader equivalence for TO:{}".format( vto) )
    eqto = vto

  if( eqfrom in od_grouped_trips and eqto in od_grouped_trips[eqfrom] ):
    od_grouped_trips[eqfrom][eqto] += 1
  else:
    od_grouped_trips[eqfrom][eqto] = 1

# --------------------------------------------------------------
def parseDemand(opts):
  global od_grouped_trips
  global od_edgeIds
  global od_edges
  global od_nodes

  tot_trips = 0
  count_trips = 0

  print( "Start parsing demand file" );
  # Read Demand file
  root = {}
  demandfile=opts['in_demand']
  try:
    tree=etree.parse(demandfile)
    root=tree.getroot()
  except:
    error(2,"Parsing "+demandfile+" file. Exception: "+ str(sys.exc_info()) )

  # -- Trip format --
  # from and to fields are ***edges*** not nodes. It is necessary to change them.
  # <trip id="9100" depart="0.14" from="4616750#0" to="23858590#3" fromTaz="4" toTaz="99" departLane="best" departSpeed="0"/>

  for elem in root:
   try:
    if( elem.tag ):
      if( elem.tag == 'trip' ):
        tot_trips += 1
        # print(elem.attrib)
        edgeFrom = elem.attrib['from']
        edgeTo = elem.attrib['to']
        depart = float(elem.attrib['depart'])
        consider = True

        if( opts['filter_time_ini'] and depart < opts['filter_time_ini'] ):
          consider = False
        if( opts['filter_time_end'] and depart > opts['filter_time_end'] ):
          consider = False

        if( consider ):
          vfrom = od_edges[edgeFrom]['from']
          vto   = od_edges[edgeTo]['to']
          count_trips += 1

          # Count individual trips
          count_individual_trips(vfrom,vto)

          # Count leader trips
          count_group_trips( vfrom, vto );
   except:
     error(3,"Error setting value. Exception: "+str(sys.exc_info()))
  print( "End parsing demand file" );

  print("Counted trips: "+str(count_trips)+"/"+str(tot_trips) )

# --------------------------------------------------------------
def dumpODmatrices():
  global od_edgeIds
  global od_types
  global od_speeds
  global od_weights
  global od_lengths
  global od_names
  global od_priorities
  global od_trips
  global od_grouped_trips
  global od_nodes

  if not os.path.exists(opts['out_dir']):
    print( "Creating directory "+opts['out_dir'])
    os.makedirs(opts['out_dir'])

  if( 'out_fftt' in opts) & (opts['out_fftt']) :
    print("Generating od matrix for edge weights")
    df = pd.DataFrame(od_weights).T.fillna(0)
    df.to_csv( opts['out_dir']+'/'+opts['out_prefix']+"_od_weights.csv" )

  if( 'out_speeds' in opts) & (opts['out_speeds']) :
    print("Generating od matrix for edge speeds")
    df = pd.DataFrame(od_speeds).T.fillna(0)
    df.to_csv( opts['out_dir']+'/'+opts['out_prefix']+"_od_speeds.csv" )

  if( 'out_lengths' in opts) & (opts['out_lengths']) :
    print("Generating od matrix for edge lengths")
    df = pd.DataFrame(od_lengths).T.fillna(0)
    df.to_csv( opts['out_dir']+'/'+opts['out_prefix']+"_od_lengths.csv" )

  if( 'out_edge_types' in opts) & (opts['out_edge_types']) :
    print("Generating od matrix for edge types")
    df = pd.DataFrame(od_types).T.fillna(0)
    df.to_csv( opts['out_dir']+'/'+opts['out_prefix']+"_od_types.csv" )

  if( 'out_edge_ids' in opts) & (opts['out_edge_ids']) :
    print("Generating od matrix for edge ids")
    df = pd.DataFrame(od_edgeIds).T.fillna(0)
    df.to_csv( opts['out_dir']+'/'+opts['out_prefix']+"_od_edgeids.csv" )

  if( 'out_names' in opts) & (opts['out_names']) :
    print("Generating od matrix for edge names")
    df = pd.DataFrame(od_names).T.fillna(0)
    df.to_csv( opts['out_dir']+'/'+opts['out_prefix']+"_od_names.csv", encoding='utf-8' )

  if( 'out_edge_priorities' in opts) & (opts['out_edge_priorities']) :
    print("Generating od matrix for edge priorities")
    df = pd.DataFrame(od_priorities).T.fillna(0)
    df.to_csv( opts['out_dir']+'/'+opts['out_prefix']+"_od_priorities.csv" )

  if( 'out_trip_counters' in opts) & (opts['out_trip_counters']) :
    print("Generating od matrix for trip counters")
    df = pd.DataFrame(od_trips).T.fillna(0)
    df.to_csv( opts['out_dir']+'/'+opts['out_prefix']+"_od_trips.csv" )

  if( 'out_group_trip_counters' in opts) & (opts['out_group_trip_counters']) :
    print("Generating od matrix for grouped trip counters")
    df = pd.DataFrame(od_grouped_trips).T.fillna(0)
    df.to_csv( opts['out_dir']+'/'+opts['out_prefix']+"_od_group_trips.csv" )

  if( 'out_nodes' in opts) & (opts['out_nodes']) :
    print("Generating od matrix for nodes")
    df = pd.DataFrame(od_nodes).T
    df.to_csv( opts['out_dir']+'/'+opts['out_prefix']+"_od_nodes.csv" )

# --------------------------------------------------------------
if __name__ == '__main__':
  printBanner();
  opts=getConfig()
  parseNodes(opts)
  parseNet(opts)
  calculate_taz_leaders(opts)
  # dump_taz_nodes(opts)
  if( opts['out_trip_counters'] ):
    parseDemand(opts)
  dumpODmatrices()

print("Generated files")
