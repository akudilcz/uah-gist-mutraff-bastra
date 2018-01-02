# -------------------------------------------------------------
# Run LOT TRAFFIC SCENARIOS
# 
BUS=es.uah.gist.mutraff.toc1
SCENE_DIR=scenes
# -------------------------------------------------------------
SCENES="\
 alcalahenares_nomutraff_nomaps_tele60_fulltraffic \
 alcalahenares_L_mutraff_tele60_uni1x8_timeALL_fulltraffic_logit50 \
 alcalahenares_L_mutraff_tele60_uni5x16_timeALL_fulltraffic_logit50 \
 alcalahenares_L_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50 \
"
SCENES="\
 alcalahenares_XXL_mutraff_tele60_uni1x8_timeALL_fulltraffic_logit10 \
 alcalahenares_XXL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit10 \
 alcalahenares_XXL_mutraff_tele60_uni5x16_timeALL_fulltraffic_logit10 \
 alcalahenares_XXL_mutraff_tele60_uni1x8_timeALL_fulltraffic_logit20 \
 alcalahenares_XXL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit20 \
 alcalahenares_XXL_mutraff_tele60_uni5x16_timeALL_fulltraffic_logit20 \
 alcalahenares_XXL_mutraff_tele60_uni1x8_timeALL_fulltraffic_logit50 \
 alcalahenares_XXL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50 \
 alcalahenares_XXL_mutraff_tele60_uni5x16_timeALL_fulltraffic_logit50 \
 alcalahenares_XXL_mutraff_tele60_uni1x8_timeALL_fulltraffic_logit100 \
 alcalahenares_XXL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit100 \
 alcalahenares_XXL_mutraff_tele60_uni5x16_timeALL_fulltraffic_logit100 \
"
SCENES="\
 alcalahenares_XXL_mutraff_tele60_uni1x8_timeALL_fulltraffic_logit50 \
 alcalahenares_XXL_mutraff_tele60_uni5x16_timeALL_fulltraffic_logit50 \
 alcalahenares_XXL_mutraff_tele60_uni5x16_timeALL_fulltraffic_logit100 \
"

SCENES="\
 alcalahenares_XL_nomutraff_tele60_nomaps_fulltraffic \
 alcalahenares_XL_mutraff_tele60_uni1x8_timeALL_fulltraffic_logit10 \
 alcalahenares_XL_mutraff_tele60_uni1x8_timeALL_fulltraffic_logit20 \
 alcalahenares_XL_mutraff_tele60_uni1x8_timeALL_fulltraffic_logit50 \
 alcalahenares_XL_mutraff_tele60_uni1x8_timeALL_fulltraffic_logit100 \
 alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit10 \
 alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit20 \
 alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50 \
 alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit100 \
 alcalahenares_XL_mutraff_tele60_uni5x16_timeALL_fulltraffic_logit10 \
 alcalahenares_XL_mutraff_tele60_uni5x16_timeALL_fulltraffic_logit20 \
 alcalahenares_XL_mutraff_tele60_uni5x16_timeALL_fulltraffic_logit50 \
 alcalahenares_XL_mutraff_tele60_uni5x16_timeALL_fulltraffic_logit100 \
"

for i in $SCENES
do
  echo "===================================="
  echo $i
  # ./run_toc.sh $BUS $SCENE_DIR/$i
  ./run_darwin.sh $i
done

