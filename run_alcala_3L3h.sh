# -------------------------------------------------------------
# Run LOT TRAFFIC SCENARIOS
# 
BUS=es.uah.gist.mutraff.toc1
SCENE_DIR=scenes
# -------------------------------------------------------------
SCENES="\
 alcalahenares_L3h_nomaps_tele60_timeALL_fulltraffic \
 alcalahenares_L3h_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50_01 \
 alcalahenares_L3h_mutraff_tele60_uni5x16_timeALL_fulltraffic_logit50_01 \
 alcalahenares_3L3h_nomaps_tele60_timeALL_fulltraffic \
 alcalahenares_3L3h_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50_01 \
 alcalahenares_3L3h_mutraff_tele60_uni5x16_timeALL_fulltraffic_logit50_01 \
"

SCENES="\
 alcalahenares_3L3h_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit10_01 \
 alcalahenares_3L3h_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit20_01 \
 alcalahenares_3L3h_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit100_01 \
 alcalahenares_3L3h_mutraff_tele60_uni5x16_timeALL_fulltraffic_logit10_01 \
 alcalahenares_3L3h_mutraff_tele60_uni5x16_timeALL_fulltraffic_logit20_01 \
 alcalahenares_3L3h_mutraff_tele60_uni5x16_timeALL_fulltraffic_logit100_01 \
"

SCENES="\
 alcalahenares_3L3h_nomaps_tele60_timeALL_fulltraffic \
 alcalahenares_3L3h_nomaps_tele60_timeALL_fulltraffic_incident \
 alcalahenares_3L3h_mutraff_tele60_uni5x16_timeALL_fulltraffic_logit10_01 \
 alcalahenares_3L3h_mutraff_tele60_uni5x16_timeALL_fulltraffic_logit20_01 \
 alcalahenares_3L3h_mutraff_tele60_uni5x16_timeALL_fulltraffic_logit50_01 \
 alcalahenares_3L3h_mutraff_tele60_uni5x16_timeALL_fulltraffic_logit100_01 \
 alcalahenares_3L3h_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit10_01 \
 alcalahenares_3L3h_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit20_01 \
 alcalahenares_3L3h_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50_01 \
 alcalahenares_3L3h_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit100_01 \
"

SCENES="\
 alcalahenares_3L3h_nomaps_tele60_timeALL_crosstraffic_01 \
 alcalahenares_3L3h_nomaps_tele600_timeALL_fulltraffic_01 \
 alcalahenares_3L3h_nomaps_tele600_timeALL_crosstraffic_01 \
 alcalahenares_3L3h_nomaps_tele600_timeALL_crosstraffic_incident_01 \
"

SCENES="\
  alcalahenares_3L3h_nomaps_timeALL_taz5-taz50_01 \
  alcalahenares_3L3h_nomaps_timeALL_taz5-taz50_incident_01 \
  alcalahenares_3L3h_nomaps_timeALL_taz5-taz50_foresight_01 \
  alcalahenares_3L3h_nomaps_timeALL_taz5-taz50_foresight_incident_01 \
  alcalahenares_3L3h_nomaps_timeALL_taz5-taz50_fore2-3-4-10_01
  alcalahenares_3L3h_nomaps_timeALL_taz5-taz50_fore1-1-4-10_01
  alcalahenares_3L3h_nomaps_timeALL_taz5-taz50_fore1-1-4-10_incident_01
  alcalahenares_3L3h_nomaps_timeALL_taz5-taz50_fore2-3-4-10_incident_01
"

SCENES="\
  alcalahenares_3L3h_nomaps_timeALL_fulltraffic_01
  alcalahenares_3L3h_mutraff_uni5x16_timeALL_fulltraffic_logit10_01
  alcalahenares_3L3h_mutraff_uni5x16_timeALL_fulltraffic_logit20_01
  alcalahenares_3L3h_mutraff_uni5x16_timeALL_fulltraffic_logit50_01
  alcalahenares_3L3h_mutraff_uni5x16_timeALL_fulltraffic_logit100_01
  alcalahenares_3L3h_mutraff_uni5x8_timeALL_fulltraffic_logit10_01
  alcalahenares_3L3h_mutraff_uni5x8_timeALL_fulltraffic_logit20_01
  alcalahenares_3L3h_mutraff_uni5x8_timeALL_fulltraffic_logit100_01
  alcalahenares_3L3h_mutraff_uni5x8_timeALL_fulltraffic_logit50_01
"

SCENES="\
  alcalahenares_3L3h_nomaps_timeALL_ecotraffic_01
"

SCENES="\
  alcalahenares_3L3h_TopEdges_timeALL_fulltraffic_01
"

for i in $SCENES
do
  echo "===================================="
  echo $i
  # ./run_toc.sh $BUS $SCENE_DIR/$i
  ./run_darwin.sh $i
done

