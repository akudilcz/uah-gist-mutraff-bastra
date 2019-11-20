# -------------------------------------------------------------
# Run LOT TRAFFIC SCENARIOS
# 
BUS=es.uah.gist.mutraff.toc1
SCENE_DIR=scenes
# -------------------------------------------------------------
SCENES="\
  alcalahenares_3L3h_Emergency_TWM50_L_01
  alcalahenares_3L3h_Emergency_noTWM_L_01
"

SCENES="\
  alcalahenares_Emergency_TWM50_L_noTELE_01
  alcalahenares_Emergency_noTWM_L_noTELE_01
"

for i in $SCENES
do
  echo "===================================="
  echo $i
  # ./run_toc.sh $BUS $SCENE_DIR/$i
  ./run_darwin.sh $i
done

