# -------------------------------------------------------------
# Run LOT TRAFFIC SCENARIOS
# 
BUS=es.uah.gist.mutraff.toc1
SCENE_DIR=scenes
# -------------------------------------------------------------
REFERENCE=M.typed-routes.xml
DEMAND_REFERENCE="$SCENE_DIR/DEMANDS/$REFERENCE"

# grid16_BastraAstar_rand05x8_timeALL_fulltraffic_logit05\
# grid16_BastraAstar_rand05x8_timeALL_fulltraffic_logit10\
SCENES="\
 grid16_noBastraAstar_reference_fulltraffic\
 grid16_BastraAstar_rand05x8_timeALL_fulltraffic_logit20\
 grid16_BastraAstar_rand05x8_timeALL_fulltraffic_logit50\
 grid16_BastraAstar_rand05x8_timeALL_fulltraffic_logit100\
"

for i in $SCENES
do
  echo "===================================="
  echo $i
  cp $DEMAND_REFERENCE $SCENE_DIR/$i/$i.typed-routes.xml
  # ./run_toc.sh $BUS $SCENE_DIR/$i
  ./run_darwin.sh $i
done

