#!/bin/bash
TWM_GEN="/Users/alvaro/Desktop/workspace/mutraff/uah-gist-mutraff-bastra/tools/MAP_GENERATOR/genmaps.bastra.py"

# ------------------------------------------
# ------------------------------------------
NET="alcalahenares_3L3h_nomaps_timeALL_taz5-taz50S_incident_alfa5-step5-join_01.net.xml"
TWM_GEN_CONF="twm_gen.1.conf"
TRIPS="tripfile-t30-0.xml"
WEIGHTS="new_map_weights_t30.xml"
WEIGHTS_ALT="new_map_weights_t30.alt.xml"
OUTNAME="new_routes"

# ------------------------------------------
# ------------------------------------------
WEIGHTS="new_map_weights_t30_manual.xml"
OUTNAME="new_routes_manual"

# ------------------------------------------
# ------------------------------------------
OUTPUT="$OUTNAME.xml"
OUTPUT_PY="$OUTNAME.py"
ERRORS="sumo.log"

FLAG_TWM_GEN=0
FLAG_DUA=1

if [ $FLAG_TWM_GEN -ne 0 ]; then
  echo "--> EXECUTING TWM_GEN"
  python $TWM_GEN -c $TWM_GEN_CONF
  mv .XXX.join_map_1.xml $WEIGHTS
  mv .XXX.join_map_1.alt.xml $WEIGHTS_ALT
else
  echo "--> SKIPPED TWM_GEN"
fi
#exit

if [ $FLAG_DUA -ne 0 ]; then
  echo "--> EXECUTING DUAROUTER"
  DUA_OPTIONS="--max-alternatives 10 --write-trips true"
  DUA_OPTIONS="--max-alternatives 100"
  set -x
  duarouter -n $NET -t $TRIPS -w $WEIGHTS -o $OUTPUT $DUA_OPTIONS --error-log $ERRORS
  # duarouter -n $NET -t $TRIPS -w $WEIGHTS -o $OUTPUT --error-log $ERRORS
  # duarouter -n $NET -t $TRIPS -o $OUTPUT --error-log $ERRORS
  set +x
  echo "    ERRORS:"
  cat $ERRORS
else
  echo "--> SKIPPED DUAROUTER"
fi

echo "--> EXTRACTING ROUTES"
VEH[0]=63
VEH[1]=519
n=0
echo "new_routes={}" > $OUTPUT_PY
grep " edges=" $OUTPUT | cut -f2 -d'=' | cut -f1 -d'/' | while read i
do
  echo "new_routes[${VEH[$n]}]=$i.split(' ')"
  n=$n+1
done >> $OUTPUT_PY
echo "PRODUCED FILES:"
ls -l $OUTNAME*.xml $OUTPUT_PY
echo "CALCULATED COSTS (from .alt.xml file)"
grep '<route cost="' $OUTNAME.alt.xml | cut -d' ' -f14

echo "--> CALCULATING IMPACTS"
python analize.py
