#!/bin/bash

for NET in madrid_retiro madrid_las_tablas madrid_barrio_salamanca
do
  echo "GENERATING : $NET"
  PREFIX="${NET}"
  OUTFILE="${NET}.out"
  MAPNAME="${NET}/${NET}_L_nomaps_tele60_fulltrafic.net.xml"
  NODESFILE="${NET}/${NET}.nod.xml"
  DEMAND_FILE="${NET}/${NET}_L_nomaps_tele60_fulltrafic.trip.xml"

  #set -x
  python mutraff_odgen.py -O ${NET} -p ${PREFIX} -n ${MAPNAME} -x ${NODESFILE} -d ${DEMAND_FILE} -A 2>&1 | tee ${OUTFILE}
  #set +x
  echo "Generated output at ${OUTFILE}"
done
