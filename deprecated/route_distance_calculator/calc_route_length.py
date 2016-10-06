import sys # sys.path.append('.')
import optparse

import xmltodict as xt
import pandas as pd

# -----------------------------
def getConfig():
  parser = optparse.OptionParser("Usage: "+sys.argv[0]+" -n netfile.xml -o outfile.csv")
  parser.add_option("-n", dest="in_net_file", type="string")
  parser.add_option("-s", dest="in_stats_file", type="string")
  (options, args) = parser.parse_args()
  return options


# -----------------------------
def inspect(label,obj):
  print "Inspect",label,":", obj.__class__.__name__, "of length", len(obj), "\n", "Methods:", dir(obj)

# -----------------------------
def getLane( edge_id, lane ):
  sep = ','
  for k5, v5 in lane.items():
    # print "   -5->", k5, ":", v5
    if( k5 == "@id" ):
      lane_id = v5
    if( k5 == "@index" ):
      lane_index = v5
    if( k5 == "@speed" ):
      lane_speed = v5
    if( k5 == "@length" ):
      lane_length = v5
    if( k5 == "@shape" ):
      lane_shape = v5
  #print edge_id, sep, lane_id, sep, lane_index, sep, lane_speed, sep, lane_length
  # return [ edge_id, lane_id, lane_index, lane_speed, lane_length, lane_shape ]
  return { 'edge_id':edge_id, 'lane_id':lane_id, 'lane_index':lane_index, 'lane_speed':lane_speed, 'lane_length':lane_length, 'lane_shape':lane_shape }

# ==========================================================================
if __name__ == '__main__':
# ==========================================================================
  param=getConfig()

  in_net_file=param.in_net_file
  if( len(in_net_file) == 0):
    in_net_file = "./grid.net.xml"

  in_stats_file=param.in_stats_file
  if( len(in_stats_file) == 0):
    in_stats_file = "./statistics.csv"

  out_lanes_csv_file = in_net_file+".lanes.csv"
  out_edges_csv_file = in_net_file+".edges.csv"

  # -------------------------------------------------------
  print "Reading the NET file", in_net_file
  xmlfile = open( in_net_file, "r") # Open a file in read-only mode
  xmltxt  = xmlfile.read() # read the file object
  print "  Parsing XML data"
  theNet = xt.parse(xmltxt) # Parse the read document string
  # print "  Read structure: ", theNet.__class__.__name__, "of length", len(theNet)

  # lanes = pd.DataFrame( columns=('edge_id','lane_id','lane_index', 'lane_speed','lane_length','lane_shape' ))
  lanes = []
  edges = {}

  for k1, v1 in theNet.items():
    for k2, v2 in v1.items():
      if( k2 == "edge"):
        print "  Detected edge structures"
        size2 = len(v2)
        for num_edge in range(0, size2):
          for k4, v4 in v2[num_edge].items():
            if( k4 == "@id" ):
	      the_edge_id = v4
            if( k4 == "lane" ):
	      edge_id = k4
	      # Check if has one or multiple lanes
	      # inspect("v4",v4)
	      # --- multiple lanes ---
	      if( v4.__class__.__name__ == "list"):
                size4 = len(v4)
                for num_lane in range(0, size4):
                  lane = getLane( the_edge_id, v4[num_lane] )
                  lanes.append( lane )
		  edges[the_edge_id] = lane
	      # --- single lane ---
	      else:
	        lane = getLane( the_edge_id, v4 )
	        lanes.append( lane )
		edges[the_edge_id] = lane
	      sys.stdout.flush()

  # -------------------------------------------------------
  print "  Obtained ", len(lanes), " lanes"
  print "  Exporting lanes to file", out_lanes_csv_file
  pd.DataFrame(lanes).to_csv( out_lanes_csv_file)

  edges2 = []
  for edge in edges:
    edges2.append(edges[edge])
  print "  Obtained ", len(edges2), " edges"
  print "  Exporting edges to file", out_edges_csv_file
  pd.DataFrame(edges2).to_csv( out_edges_csv_file )

  # -------------------------------------------------------
  print "Reading the statistics file", in_stats_file
  theStats = pd.read_csv( in_stats_file )

  route_lengths = []
  num_routes = 0

  # -------------------------------------------------------
  def process_route(route):
	global num_routes 
	global edges2 
	if( not route ):
	  route_lengths.append( 0 )
	  print "   (skipped non routed)"
	else:
	  # print "   Route:", route
	  route_len = 0
	  for e in route.split(':'):
	    if( e ):
	      route_len += float(edges[e]['lane_length'])
	      # print "    ",e,":",edges[e]['lane_length'],"total:",route_len
	  route_lengths.append( route_len )
	num_routes += 1

  print "  Calculating route lengths"
  theStats['route_detail'].apply( process_route )
  theStats['route_lenght'] = pd.Series( route_lengths )
  print "  Saving new stats to", "stats2.csv"
  pd.DataFrame(theStats).to_csv( "stats2.csv" )

  print "Done."
