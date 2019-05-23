# -------------------------------------------------------------------
# ALCALA DE HENARES : XL
# -------------------------------------------------------------------
EPOCHS=20

# generate_city.sh param/alcalahenares_XL_nomaps_tele60_fulltraffic.param $EPOCHS

# ------------------
# UNI5 x 8
# ------------------
# generate_city.sh param/alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit10.param $EPOCHS
# generate_city.sh param/alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit20.param $EPOCHS
# generate_city.sh param/alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit100.param $EPOCHS

generate_city_epochs.sh param/alcalahenares_XL_mutraff_tele60_uni5x8_timeALL_fulltraffic_logit50.param $EPOCHS

# ------------------
# UNI5 x 16
# ------------------
# generate_city.sh param/alcalahenares_XL_mutraff_tele60_uni5x16_timeALL_fulltraffic_logit10.param $EPOCHS
# generate_city.sh param/alcalahenares_XL_mutraff_tele60_uni5x16_timeALL_fulltraffic_logit20.param $EPOCHS
# generate_city.sh param/alcalahenares_XL_mutraff_tele60_uni5x16_timeALL_fulltraffic_logit50.param $EPOCHS
# generate_city.sh param/alcalahenares_XL_mutraff_tele60_uni5x16_timeALL_fulltraffic_logit100.param $EPOCHS

