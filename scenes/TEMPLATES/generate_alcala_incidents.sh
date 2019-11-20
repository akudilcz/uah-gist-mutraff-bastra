# -------------------------------------------------------------------
# ALCALA DE HENARES : XL
# -------------------------------------------------------------------
EPOCHS=1

# Con TELEPORTING
# generate_city_epochs.sh param/alcalahenares_3L3h_Emergency_noTWM_L.param $EPOCHS
# generate_city_epochs.sh param/alcalahenares_3L3h_Emergency_TWM50_L.param   $EPOCHS

# Sin TELEPORTING
generate_city_epochs.sh param/alcalahenares_Emergency_noTWM_L_noTELE.param $EPOCHS
generate_city_epochs.sh param/alcalahenares_Emergency_TWM50_L_noTELE.param   $EPOCHS
