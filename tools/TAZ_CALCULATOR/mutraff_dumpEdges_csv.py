'''
Created on 09/12/2016
@author: Alvaro Paricio
@description: Calculator of lat,long edge positions and dump them as CSV por map plotting
'''
import sys
sys.path.insert(1,'lib')

import argparse as arg
from TazGeometry import taz_test, MuTazCalculator


# --------------------------------------------------------------
opts= {}

# --------------------------------------------------------------
def getConfig():
  parser = arg.ArgumentParser(
  	prog="mutraff_tazcalc",
	formatter_class=arg.RawDescriptionHelpFormatter,
  	description='''\
MuTRAFF EDGE as csv dumper. Used for google-maps traffic plotting.
Examples:
    python mutraff_dumpEdges_csv.py -net alcalahenares.net.xml -nod alcalahenares.nod.xml -edg alcalahenares.edg.xml 
''')

  # REQUIRED OPTS
  parser.add_argument( "-net","--in-net", help='Input. SUMOs XML net description file', default="mutraff.net.xml", required=True)
  parser.add_argument( "-nod","--in-nodes", help='Input. SUMOs XML nodes description file', default="mutraff.nod.xml", required=True)
  parser.add_argument( "-edg","--in-edges", help='Input. SUMOs XML edges description file', default="mutraff.edg.xml", required=True)

  # OPTIONAL OPTS
  parser.add_argument( "-p","--net-path", help='Input. Path to locate files', default='.' )
  parser.add_argument( "-v","--verbose", help='Verbose output', default=False, action='store_true')
  parser.add_argument( "-t","--run-tests", help='Run tests', default=False, action='store_true')
  parser.add_argument( "-csv_edges","--out-csv_edges", help='Output. Generate output to CSV edges file', required=False)


  options = vars(parser.parse_args())

  options['in_net'] = options['net_path'] + '/' + options['in_net']
  options['in_nodes'] = options['net_path'] + '/' + options['in_nodes']
  options['in_edges'] = options['net_path'] + '/' + options['in_edges']

  if( options['verbose'] ):
    print(options)

  return options


# --------------------------------------------------------------
def printBanner():
  # Take here the banner: http://patorjk.com/software/taag/#p=display&f=Doom&t=mutraff%20odgen
  # Font: Doom
  print("                 _              __  __   _                     _      ")
  print("                | |            / _|/ _| | |                   | |     ")
  print(" _ __ ___  _   _| |_ _ __ __ _| |_| |_  | |_ __ _ _______ __ _| | ___ ")
  print("| '_ ` _ \| | | | __| '__/ _` |  _|  _| | __/ _` |_  / __/ _` | |/ __|")
  print("| | | | | | |_| | |_| | | (_| | | | |   | || (_| |/ / (_| (_| | | (__ ")
  print("|_| |_| |_|\__,_|\__|_|  \__,_|_| |_|    \__\__,_/___\___\__,_|_|\___|\n")
  print("                 MUTRAFF TAZ Calculator")
  print("                    alvaro.paricio@uah.es")
  print("")

 
if __name__ == '__main__':
  printBanner()
  opts=getConfig()
  if( opts['run_tests'] ):
    taz_test()
  else:
    tazcalc = MuTazCalculator(opts)
    tazcalc.loadDataCsv()
    tazcalc.dumpEdgesCsv()

