# -------------------------------------------------------------
# Run LOT TRAFFIC SCENARIOS
# 
BUS=es.uah.gist.mutraff.toc1
SCENE_DIR=scenes
# -------------------------------------------------------------
SCENES="\
 LT_grid16_Bastra_rand05x8_timeALL_fulltraffic_logit100\
 LT_grid16_Bastra_rand05x8_timeALL_fulltraffic_logit50\
 LT_grid16_noBastra_reference_fulltraffic\
"

for i in $SCENES
do
  echo "===================================="
  echo $i
  ./run_toc.sh $BUS $SCENE_DIR/$i
done

