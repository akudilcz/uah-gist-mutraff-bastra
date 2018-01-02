import pandas as pd
import numpy as np
import argparse as arg

opts={}

# ----------------------------------------
def getConfig():
  global opts
  parser = arg.ArgumentParser(
		prog="pygrep",
		formatter_class=arg.RawDescriptionHelpFormatter,
		description='''\
pygrep: a python grep utility
Copyright: alvaro.paricio@uah.es for Mutraff project
''')
  parser.add_argument( "-d","--data-file", help='Input. Data file to be grep,ed', default="data", required=True)
  parser.add_argument( "-f","--filter-file", help='Input. Filter file, one filter per line', default="none", required=True)
  parser.add_argument( "-v","--v", help='Doesnt contain', default="", required=False, action='store_true')
  opts = vars(parser.parse_args())

# ----------------------------------------
found = False
def is_found( row, line):
  global found
  if( row[0] in line ):
  	found = True

# ----------------------------------------
getConfig()
df = pd.read_csv(opts['filter_file'], header=None)

with open(opts['data_file']) as f:
  for line in f:
    found = False
    line = line.rstrip("\n")
    df['found']=df.apply( lambda x: is_found(x, line), axis=1)
    #print("LINE:'{}'->{}'".format(line,found))
    if( opts['v']== '' ):
      if( found ):
        print(line)
    else:
      if( not found ):
        print(line)
