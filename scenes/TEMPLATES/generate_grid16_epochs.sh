# -------------------------------------------------------------------
# ALCALA DE HENARES : XL
# -------------------------------------------------------------------
EPOCHS=1

PARAMS=" \
S_grid16_noTWM_timeALL_left2right.param \
S_grid16_incident_timeALL_left2right.param \
S_grid16_incidentTWM_timeALL_left2right.param \
S_grid16_incidentTWM_logit50_timeALL_left2right.param \
"

PARAMS=" \
S_grid16_incidentTWM_logit50_timeALL_left2right.param \
"

for p in $PARAMS
do
echo "====== GENERATING $p ============"
generate_city_epochs.sh param/$p $EPOCHS
echo;echo "<Press intro>"
read $A
done
