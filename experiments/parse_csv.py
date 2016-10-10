import sys

if( len(sys.argv) <= 1 ):
  print "Usage 1: Print dataset columns", sys.argv[0], "file.csv" 
  print "Usage 2: get column by name", sys.argv[0], "file.csv column_name" 
  exit(1)

  exit(1)

import pandas as pd
ds = pd.read_csv( sys.argv[1] )
size=len(ds)
if( len(sys.argv) == 2 ):
  print ds.columns.values.tolist()
  print "rows: ", size
  exit(0)

sum = 0
for i in ds[sys.argv[2]]:
  print i
  sum += i
print "num:", size
print "max:", max( ds[sys.argv[2]] )
print "min:", min( ds[sys.argv[2]] )
print "mean:", sum/size
