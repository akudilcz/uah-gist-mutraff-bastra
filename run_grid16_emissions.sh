# -------------------------------------------------------------
# Run LOT TRAFFIC SCENARIOS
# 
BUS=es.uah.gist.mutraff.toc1
SCENE_DIR=scenes
# -------------------------------------------------------------

SCENES="\
  grid16EMISSIONS_noBastra_reference_fulltraffic_01 \
"

for i in $SCENES
do
  echo "===================================="
  echo $i
  # ./run_toc.sh $BUS $SCENE_DIR/$i
  ./run_darwin.sh $i
done

