# -------------------------------------------------------------
# Run LOT TRAFFIC SCENARIOS
# 
BUS=es.uah.gist.mutraff.toc1
SCENE_DIR=scenes
# -------------------------------------------------------------
SCENES="\
 S_grid16_Bastra_rand05x8_timeALL_fulltraffic_logit100\
 S_grid16_Bastra_rand05x8_timeALL_fulltraffic_logit50\
 S_grid16_noBastra_reference_fulltraffic\
 M_grid16_Bastra_rand05x8_timeALL_fulltraffic_logit100\
 M_grid16_Bastra_rand05x8_timeALL_fulltraffic_logit50\
 M_grid16_noBastra_reference_fulltraffic\
 L_grid16_Bastra_rand05x8_timeALL_fulltraffic_logit100\
 L_grid16_Bastra_rand05x8_timeALL_fulltraffic_logit50\
 L_grid16_noBastra_reference_fulltraffic\
"

for i in $SCENES
do
  echo "===================================="
  echo $i
  # ./run_toc.sh $BUS $SCENE_DIR/$i
  ./run_darwin.sh $i
done

run_grid16.sh
