#!/bin/bash
if [ $# -ne 1 ]; then
  cat <<EOF
ERROR: a MAP name (or city name) is required.

USAGE: $0 MAPNAME (or CITYNAME)

It will check for the following files presence:
- A netfile: MAPFILE.net.xml
- A nodes file: MAPFILE.nod.xml
- A edges file: MAPFILE.edg.xml
- A mutaz file: MAPFILE.mutaz.xml

And it will generate:
- An output taz file: MAPFILE.taz.xml
EOF

fi


MAPNAME="$1"
MUTAZ_FILE="${MAPNAME}.mutaz.xml"
MUTAZ_NUMBERING_SEED="1000"
set -x
python mutraff_tazcalc.py \
  -net ${MAPNAME}.net.xml \
  -nod ${MAPNAME}.nod.xml \
  -edg ${MAPNAME}.edg.xml \
  -mutaz $MUTAZ_FILE \
  -i ${MUTAZ_NUMBERING_SEED} \
  -sumo_taz ${MAPNAME}.taz.xml 


# python mutraff_tazcalc.py -net alcalahenares.net.xml -nod alcalahenares.nod.xml -edg alcalahenares.edg.xml -mutaz alcalahenares.mutaz.xml 
