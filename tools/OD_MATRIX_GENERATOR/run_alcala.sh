#!/bin/bash

if [ $# -ne 3 ]; then
  cat <<EOF
ERROR: Must specify a MAPNAME (or CITYNAME), a NODES file and a corresponding DEMAND file (trip file) to use.

USAGE: $0 MAPNAME NODES_FILE DEMAND_FILE

Example:
  $0 alcalahenares.net.xml alcalahenares.nod.xml alcalahenares_L_Bastra_uni1x8_timeALL_fulltraffic_logit50.trip.xml
EOF
fi
DIR="alcalahenares"
PREFIX="${DIR}"
OUTFILE="${DIR}.out"
MAPNAME="${DIR}/sumo/alcalahenares.net.xml"
NODESFILE="${DIR}/sumo/alcalahenares.nod.xml"
DEMAND_FILE="${DIR}/alcalahenares_XL_nomutraff_tele60_nomaps_fulltraffic.trip.xml"

set -x
python mutraff_odgen.py -p ${PREFIX} -n ${MAPNAME} -x ${NODESFILE} -d ${DEMAND_FILE} -A 2>&1 | tee ${OUTFILE}
set +x
echo "Generated output at ${OUTFILE}"
