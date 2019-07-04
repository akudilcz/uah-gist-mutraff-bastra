# -------------------------------------------------------------------
# ALCALA DE HENARES : XL
# -------------------------------------------------------------------
EPOCHS=1

PARAMS=" \
alcalahenares_L3h_nomaps_timeALL_fulltraffic.param \
alcalahenares_L3h_mutraff_uni5x16_timeALL_fulltraffic_logit50.param \
alcalahenares_L3h_mutraff_uni5x8_timeALL_fulltraffic_logit50.param \
"

for p in $PARAMS
do
echo "====== GENERATING $p ============"
generate_city_epochs.sh param/$p $EPOCHS
echo;echo "<Press intro>"
read $A
done
