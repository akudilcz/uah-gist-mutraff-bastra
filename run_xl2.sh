# -------------------------------------------------------------
# Run LOT TRAFFIC SCENARIOS
# 
BUS=es.uah.gist.mutraff.toc1
SCENE_DIR=scenes
# -------------------------------------------------------------
REFERENCE=XL2_grid16_noBastra_reference_fulltraffic
DEMAND_REFERENCE="$SCENE_DIR/DEMANDS/L.typed-routes.xml"

SCENES="\
 XL2_grid16_noBastra_reference_fulltraffic\
 XL2_grid16_Bastra_rand05x8_timeALL_fulltraffic_logit50\
 XL2_grid16_Bastra_rand05x8_timeALL_fulltraffic_logit100\
"

for i in $SCENES
do
  echo "===================================="
  echo $i
  cp $DEMAND_REFERENCE $SCENE_DIR/$i/$i.typed-routes.xml
  # ./run_toc.sh $BUS $SCENE_DIR/$i
  ./run_darwin.sh $i
done

