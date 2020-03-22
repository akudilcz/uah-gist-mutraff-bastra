#!/bin/bash

NET_DIR="../transportation_networks"
NET="OW.net"
NET="Madrid_Tablas.net"
NET="Madrid_Salamanca.net"
NET="GRID64_6F.net"
NET="Madrid_Retiro.net"

OUT="${NET}.out"
DEBUG="1"
KSP="3"

#------------------------------------------
# arguments:
#  -h, --help	show this help message and exit.
#  -f FILE	the graph file.
#  -k K		number of shortest paths to find.
#  -l OD_LIST	list of OD-pairs, in the format 'O|D;O|D;[and so on]', 
# 		where O are valid origin nodes, D are valid destination nodes.
#  -n FLOW	vehicles (flow) to consider when computing the links' costs.
#------------------------------------------
set -x
time python KSP.py -f ${NET_DIR}/${NET} -k ${KSP} 2>&1 | tee ${OUT}

