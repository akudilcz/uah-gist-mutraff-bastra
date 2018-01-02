# -------------------------------------------------------------
# Run LOT TRAFFIC SCENARIOS
# 
BUS=es.uah.gist.mutraff.toc1
SCENE_DIR=scenes
# -------------------------------------------------------------
cp scenes/DEMANDS/radial16/L.typed-routes.xml scenes/radial16_noBastra_L_fulltraffic/radial16_noBastra_L_fulltraffic.typed-routes.xml
cp scenes/DEMANDS/radial16/M2.typed-routes.xml scenes/radial16_noBastra_M2_fulltraffic/radial16_noBastra_M2_fulltraffic.typed-routes.xml
cp scenes/DEMANDS/radial16/M.typed-routes.xml scenes/radial16_noBastra_M_fulltraffic/radial16_noBastra_M_fulltraffic.typed-routes.xml
cp scenes/DEMANDS/radial16/S.typed-routes.xml scenes/radial16_noBastra_S_fulltraffic/radial16_noBastra_S_fulltraffic.typed-routes.xml
cp scenes/DEMANDS/radial16/XL2.typed-routes.xml scenes/radial16_noBastra_XL2_fulltraffic/radial16_noBastra_XL2_fulltraffic.typed-routes.xml
cp scenes/DEMANDS/radial16/XS.typed-routes.xml scenes/radial16_noBastra_XS_fulltraffic/radial16_noBastra_XS_fulltraffic.typed-routes.xml
# scenes/radial16_L_Bastra_rand05x1_timeALL_fulltraffic_logit05/radial16_L_Bastra_rand05x1_timeALL_fulltraffic_logit05.typed-routes.xml
# ./run_toc.sh $BUS $SCENE_DIR/$i

./run_darwin.sh radial16_noBastra_XXS_fulltraffic
./run_darwin.sh radial16_noBastra_XS_fulltraffic
./run_darwin.sh radial16_noBastra_S_fulltraffic
./run_darwin.sh radial16_noBastra_M2_fulltraffic
./run_darwin.sh radial16_noBastra_M_fulltraffic
./run_darwin.sh radial16_noBastra_L_fulltraffic
./run_darwin.sh radial16_noBastra_XL2_fulltraffic

