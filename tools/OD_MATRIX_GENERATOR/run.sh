#!/bin/bash

if [ $# -ne 3 ]; then
  cat <<EOF
ERROR: Must specify a MAPNAME (or CITYNAME), a NODES file and a corresponding DEMAND file (trip file) to use.

USAGE: $0 MAPNAME NODES_FILE DEMAND_FILE

Example:
  $0 alcalahenares.net.xml alcalahenares.nod.xml alcalahenares_L_Bastra_uni1x8_timeALL_fulltraffic_logit50.trip.xml
EOF
fi
MAPNAME=$1
NODESFILE=$2
DEMAND_FILE=$3

set -x
python mutraff_odgen.py -n ${MAPNAME} -x ${NODESFILE} -d ${DEMAND_FILE} -A
