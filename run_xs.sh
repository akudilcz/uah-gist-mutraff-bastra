# -------------------------------------------------------------
# Run LOT TRAFFIC SCENARIOS
# 
BUS=es.uah.gist.mutraff.toc1
SCENE_DIR=scenes
# -------------------------------------------------------------
DEMAND_REFERENCE="$SCENE_DIR/XS_grid16_noBastra_reference_fulltraffic/XS_grid16_noBastra_reference_fulltraffic.typed-routes.xml"
SCENES="\
 XS_grid16_noBastra_reference_fulltraffic\
 XS_grid16_Bastra_rand05x8_timeALL_fulltraffic_logit05\
 XS_grid16_Bastra_rand05x8_timeALL_fulltraffic_logit10\
 XS_grid16_Bastra_rand05x8_timeALL_fulltraffic_logit20\
 XS_grid16_Bastra_rand05x8_timeALL_fulltraffic_logit50\
 XS_grid16_Bastra_rand05x8_timeALL_fulltraffic_logit100\
"

for i in $SCENES
do
  echo "===================================="
  cp $DEMAND_REFERENCE $SCENE_DIR/$i/$i.typed-routes.xml
  echo $i
  # ./run_toc.sh $BUS $SCENE_DIR/$i
  ./run_darwin.sh $i
done

