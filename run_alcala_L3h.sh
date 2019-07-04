# -------------------------------------------------------------
# Run LOT TRAFFIC SCENARIOS
# 
BUS=es.uah.gist.mutraff.toc1
SCENE_DIR=scenes
# -------------------------------------------------------------
SCENES="\
  alcalahenares_L3h_nomaps_timeALL_fulltraffic_01 \
  alcalahenares_L3h_mutraff_uni5x16_timeALL_fulltraffic_logit50_01 \
  alcalahenares_L3h_mutraff_uni5x8_timeALL_fulltraffic_logit50_01 \
"

for i in $SCENES
do
  echo "===================================="
  echo $i
  # ./run_toc.sh $BUS $SCENE_DIR/$i
  ./run_darwin.sh $i
done

