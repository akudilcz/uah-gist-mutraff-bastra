# -------------------------------------------------------------
# Run LOT TRAFFIC SCENARIOS
# 
BUS=es.uah.gist.mutraff.toc1
SCENE_DIR=scenes
# -------------------------------------------------------------
SCENES="\
  S_grid16_noTWM_timeALL_left2right_01 \
  S_grid16_incident_timeALL_left2right_01 \
  S_grid16_incidentTWM_timeALL_left2right_01 \
"

SCENES="\
  S_grid16_incidentTWM_logit50_timeALL_left2right_01 \
"

for i in $SCENES
do
  echo "===================================="
  echo $i
  # ./run_toc.sh $BUS $SCENE_DIR/$i
  ./run_darwin.sh $i
done

