import os
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
def filterFile(data_file,filter_file):
  df = pd.read_csv(filter_file, header=None)

  with open(data_file) as f:
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
  f.close()

# ----------------------------------------
def filterNoFile(data_file):
  if( opts['v']== '' ):
    with open(data_file) as f:
      for line in f:
          print(line)
    f.close()
  else:
    # Nada
    return

# ----------------------------------------
getConfig()

if os.stat(opts['data_file']).st_size == 0:
  exit(0)

if os.stat(opts['filter_file']).st_size == 0:
  filterNoFile(opts['data_file'])
else:
  filterFile(opts['data_file'],opts['filter_file'])
