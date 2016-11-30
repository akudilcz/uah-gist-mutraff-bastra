#!/bin/bash

NET=alcalahenares
SRC_OSM_FILE=../osm/$NET.osm
DST_NET_FILE=$NET.net.xml
ERR_CONVERT=$NET.convert.err

CONF_TYPES_FILE=netconvert.osm.types.xml
OPTIONS="\
--output.original-names true \
--plain-output-prefix $NET \
--proj.plain-geo true \
--output.street-names true \
--remove-edges.by-type 
highway.bridleway,\
highway.cycleway,\
highway.footway,\
highway.ford,\
highway.path,\
highway.pedestrian,\
highway.stairs,\
highway.step,\
highway.steps,\
highway.track,\
railway.light_rail,\
railway.preserved,\
railway.rail,\
railway.subway,\
railway.tram\
 \
"

set -x
netconvert $OPTIONS --type-files $CONF_TYPES_FILE --osm-files $SRC_OSM_FILE --output-file $DST_NET_FILE 2>&1 | tee $ERR_CONVERT
