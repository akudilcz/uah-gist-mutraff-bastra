# -------------------------------------------------------------
# Run LOT TRAFFIC SCENARIOS
# 
BUS=es.uah.gist.mutraff.toc1
SCENE_DIR=scenes
# -------------------------------------------------------------
SCENES="\
 alcalahenares_XL_nomutraff_tele60_nomaps_fulltraffic \
"

SCENES="\
  alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50_01 \
  alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50_02 \
  alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50_03 \
  alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50_04 \
  alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50_05 \
  alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50_06 \
  alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50_07 \
  alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50_08 \
  alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50_09 \
  alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50_10 \
  alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50_11 \
  alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50_12 \
  alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50_13 \
  alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50_14 \
  alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50_15 \
  alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50_16 \
  alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50_17 \
  alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50_18 \
  alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50_19 \
  alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50_20 \
"

for i in $SCENES
do
  echo "===================================="
  echo $i
  # ./run_toc.sh $BUS $SCENE_DIR/$i
  ./run_darwin.sh $i
done

