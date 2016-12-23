'''
Created on 09/12/2016
@author: Alvaro Paricio
@description: Calculator of TRAFFIC ASSIGNMENT ZONES (TAZ). Given a networkfile and a polygon description, get all the nodes of the network included inside the polygon.
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
MuTRAFF TAZ Calculator
Given an XML taz definition file based on polygon coordinates in GPS format(lat,lon), generate the associated SUMO TAZ definiton file with the edges contained inside each taz polygon.
Examples:
  * Generate the TAZs associated to a given polygon:
    python mutraff_tazcalc.py -net alcalahenares.net.xml -nod alcalahenares.nod.xml -edg alcalahenares.edg.xml -mutaz alcalahenares.mutaz.xml -sumo_taz alcalahenares.taz.xml
''')

  # REQUIRED OPTS
  parser.add_argument( "-net","--in-net", help='Input. SUMOs XML net description file', default="mutraff.net.xml", required=True)
  parser.add_argument( "-nod","--in-nodes", help='Input. SUMOs XML nodes description file', default="mutraff.nod.xml", required=True)
  parser.add_argument( "-edg","--in-edges", help='Input. SUMOs XML edges description file', default="mutraff.edg.xml", required=True)
  parser.add_argument( "-mutaz","--in-mutaz", help='Input. MUTRAFF XML description file', default="mutraff.mutaz.xml", required=True)

  # OPTIONAL OPTS
  parser.add_argument( "-sumo_taz","--out-sumo-taz", help='Output. Generate output to SUMO TAZ XML description file', required=False)
  parser.add_argument( "-p","--net-path", help='Input. Path to locate files', default='.' )
  parser.add_argument( "-v","--verbose", help='Verbose output', default=False, action='store_true')
  parser.add_argument( "-t","--run-tests", help='Run tests', default=False, action='store_true')
  parser.add_argument( "-i","--taz-id-seed", help='USe this number as TAZ id numbering seed', default="1000", required=False)

  options = vars(parser.parse_args())

  options['in_net'] = options['net_path'] + '/' + options['in_net']
  options['in_nodes'] = options['net_path'] + '/' + options['in_nodes']
  options['in_edges'] = options['net_path'] + '/' + options['in_edges']
  options['in_mutaz'] = options['net_path'] + '/' + options['in_mutaz']
  if 'out_sumo_taz' in options and options['out_sumo_taz']:
	options['out_sumo_taz'] = options['net_path'] + '/' + options['out_sumo_taz']

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
    tazcalc.loadData()
    tazcalc.calculateTazs()
    tazcalc.dumpTazFile()

