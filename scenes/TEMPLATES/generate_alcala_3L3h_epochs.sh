# -------------------------------------------------------------------
# ALCALA DE HENARES : XL
# -------------------------------------------------------------------
EPOCHS=1

PARAMS=" \
alcalahenares_3L3h_nomaps_timeALL_fulltraffic.param \
alcalahenares_3L3h_mutraff_uni5x16_timeALL_fulltraffic_logit10.param \
alcalahenares_3L3h_mutraff_uni5x16_timeALL_fulltraffic_logit100.param \
alcalahenares_3L3h_mutraff_uni5x16_timeALL_fulltraffic_logit20.param \
alcalahenares_3L3h_mutraff_uni5x16_timeALL_fulltraffic_logit50.param \
alcalahenares_3L3h_mutraff_uni5x8_timeALL_fulltraffic_logit10.param \
alcalahenares_3L3h_mutraff_uni5x8_timeALL_fulltraffic_logit100.param \
alcalahenares_3L3h_mutraff_uni5x8_timeALL_fulltraffic_logit20.param \
alcalahenares_3L3h_mutraff_uni5x8_timeALL_fulltraffic_logit50.param \
"

for p in $PARAMS
do
echo "====== GENERATING $p ============"
generate_city_epochs.sh param/$p $EPOCHS
print;print "<Press intro>"
read $A
done
