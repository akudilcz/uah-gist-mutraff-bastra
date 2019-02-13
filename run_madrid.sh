# -------------------------------------------------------------
# Run LOT TRAFFIC SCENARIOS
# 
BUS=es.uah.gist.mutraff.toc1
SCENE_DIR=scenes
# -------------------------------------------------------------
run_darwin.sh madrid_barrio_salamanca_L_nomaps_tele60_fulltrafic
run_darwin.sh madrid_las_tablas_L_nomaps_tele60_fulltrafic
run_darwin.sh madrid_retiro_L_nomaps_tele60_fulltrafic

run_darwin.sh madrid_barrio_salamanca_L_Bastra_rand05x8_timeALL_tele60_fulltrafic_logit20
run_darwin.sh madrid_barrio_salamanca_L_Bastra_rand05x8_timeALL_tele60_fulltrafic_logit50
run_darwin.sh madrid_barrio_salamanca_L_Bastra_rand05x8_timeALL_tele60_fulltrafic_logit100
run_darwin.sh madrid_barrio_salamanca_L_Bastra_uni5x8_timeALL_tele60_fulltrafic_logit50

run_darwin.sh madrid_las_tablas_L_Bastra_rand05x8_timeALL_tele60_fulltrafic_logit20
run_darwin.sh madrid_las_tablas_L_Bastra_rand05x8_timeALL_tele60_fulltrafic_logit50
run_darwin.sh madrid_las_tablas_L_Bastra_rand05x8_timeALL_tele60_fulltrafic_logit100
run_darwin.sh madrid_las_tablas_L_Bastra_uni5x8_timeALL_tele60_fulltrafic_logit50

run_darwin.sh madrid_retiro_L_Bastra_rand05x8_timeALL_tele60_fulltrafic_logit20
run_darwin.sh madrid_retiro_L_Bastra_rand05x8_timeALL_tele60_fulltrafic_logit50
run_darwin.sh madrid_retiro_L_Bastra_rand05x8_timeALL_tele60_fulltrafic_logit100
run_darwin.sh madrid_retiro_L_Bastra_uni5x8_timeALL_tele60_fulltrafic_logit50

