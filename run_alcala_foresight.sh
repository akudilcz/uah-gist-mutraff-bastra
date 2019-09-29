# -------------------------------------------------------------
# Run LOT TRAFFIC SCENARIOS
# 
BUS=es.uah.gist.mutraff.toc1
SCENE_DIR=scenes
# -------------------------------------------------------------

SCENES="\
  alcalahenares_3L3h_nomaps_timeALL_taz5-taz50_01 \
  alcalahenares_3L3h_nomaps_timeALL_taz5-taz50_incident_01 \
  alcalahenares_3L3h_nomaps_timeALL_taz5-taz50_fore2-3-4-10_01
  alcalahenares_3L3h_nomaps_timeALL_taz5-taz50_fore1-1-4-10_01
  alcalahenares_3L3h_nomaps_timeALL_taz5-taz50_fore1-1-4-10_incident_01
  alcalahenares_3L3h_nomaps_timeALL_taz5-taz50_fore2-3-4-10_incident_01
"

SCENES="\
  alcalahenares_3L3h_nomaps_timeALL_taz5-taz50S_01 \
  alcalahenares_3L3h_nomaps_timeALL_taz5-taz50S_incident_01 \
  alcalahenares_3L3h_nomaps_timeALL_taz5-taz50S_fore1-1-4-10_01 \
  alcalahenares_3L3h_nomaps_timeALL_taz5-taz50S_fore1-1-4-10_incident_01 \
  alcalahenares_3L3h_nomaps_timeALL_taz5-taz50S_fore2-3-4-10_01 \
  alcalahenares_3L3h_nomaps_timeALL_taz5-taz50S_fore2-3-4-10_incident_01 \
  alcalahenares_3L3h_nomaps_timeALL_taz5-taz50S_fore1-1-4-10_incident_alfa5-step5_01 \
"

SCENES="\
  alcalahenares_3L3h_nomaps_timeALL_taz5-taz50S_incident2_01 \
  alcalahenares_3L3h_nomaps_timeALL_taz5-taz50S_incident2_alfa5-step5-join_01 \
"

SCENES="\
  alcalahenares_3L3h_TWM_timeALL_taz5-taz50S_incident2x1-join_01 \
  alcalahenares_3L3h_nomaps_timeALL_taz5-taz50S_incident3_01 \
  alcalahenares_3L3h_TWM_timeALL_taz5-taz50S_incident3x1-join_01 \
"

SCENES="\
  alcalahenares_nomaps_timeALL_taz5-taz50XS_01 \
  alcalahenares_nomaps_timeALL_taz5-taz50XS_incident3_01 \
  alcalahenares_TWM_timeALL_taz5-taz50XS_incident3x1-join_01 \
"

SCENES="\
  alcalahenares_TWM_timeALL_taz5-taz50XS_incident3x1_logit10-join_01 \
  alcalahenares_TWM_timeALL_taz5-taz50XS_incident3x1_logit20-join_01 \
  alcalahenares_TWM_timeALL_taz5-taz50XS_incident3x1_logit50-join_01 \
"

for i in $SCENES
do
  echo "===================================="
  echo $i
  # ./run_toc.sh $BUS $SCENE_DIR/$i
  ./run_darwin.sh $i
done

