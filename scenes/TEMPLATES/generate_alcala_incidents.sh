# -------------------------------------------------------------------
# ALCALA DE HENARES : XL
# -------------------------------------------------------------------
EPOCHS=1

# Con TELEPORTING
generate_city_epochs.sh param/alcalahenares_Emergency_pru.param $EPOCHS
#generate_city_epochs.sh param/alcalahenares_Emergency_noTWM_L_T60.param $EPOCHS
#generate_city_epochs.sh param/alcalahenares_Emergency_TWM50_L_T60.param   $EPOCHS

# Sin TELEPORTING
#generate_city_epochs.sh param/alcalahenares_Emergency_noTWM_L_noTELE.param $EPOCHS
#generate_city_epochs.sh param/alcalahenares_Emergency_TWM50_L_noTELE.param   $EPOCHS
