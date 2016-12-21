# -------------------------------------------------------------
# Run LOT TRAFFIC SCENARIOS
# 
BUS=es.uah.gist.mutraff.toc1
SCENE_DIR=scenes
# -------------------------------------------------------------
SCENES="\
 alcalahenares_noBastra_nomaps_fulltraffic \
 alcalahenares_L_Bastra_uni1x8_timeALL_fulltraffic_logit50\
 alcalahenares_L_Bastra_uni5x8_timeALL_fulltraffic_logit50\
 alcalahenares_L_Bastra_uni5x16_timeALL_fulltraffic_logit50\
"

for i in $SCENES
do
  echo "===================================="
  echo $i
  # ./run_toc.sh $BUS $SCENE_DIR/$i
  ./run_darwin.sh $i
done

