# -------------------------------------------------------------
# Run LOT TRAFFIC SCENARIOS
# 
BUS=es.uah.gist.mutraff.toc1
SCENE_DIR=scenes

set -x
nohup ./run_darwin.sh alcalahenares_Emergency_noTWM_L_T60_01 2>&1 >nohup1.out &
sleep 5
nohup ./run_darwin.sh alcalahenares_Emergency_TWM50_L_T60_01 2>&1 >nohup2.out &
sleep 5
nohup ./run_darwin.sh alcalahenares_Emergency_noTWM_L_noTELE_01 2>&1 >nohup3.out &
sleep 5
nohup ./run_darwin.sh alcalahenares_Emergency_TWM50_L_noTELE_01 2>&1 >nohup4.out &
exit
# -------------------------------------------------------------
SCENES="\
  alcalahenares_Emergency_TWM50_L_T60_01
  alcalahenares_Emergency_noTWM_L_T60_01
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

