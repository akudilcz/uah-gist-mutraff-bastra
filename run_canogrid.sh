# -------------------------------------------------------------
# EXPERIMENTS WITH
#	BASTRA: OFF
#	MAPS: none
#	TRAFFIC: ground / random
#	LOGIT: 10 / 20 / 50 / 100
# -------------------------------------------------------------
./run_darwin.sh canogrid_noBastra_nomaps_randomtraffic
./run_darwin.sh canogrid_noBastra_nomaps_fulltraffic
./run_darwin.sh canogrid_noBastra_nomaps_dirtraffic
./run_darwin.sh canogrid_noBastra_adhocmaps_randomtraffic
./run_darwin.sh canogrid_noBastra_adhocmaps_fulltraffic
./run_darwin.sh canogrid_noBastra_adhocmaps_dirtraffic

# -------------------------------------------------------------
# EXPERIMENTS WITH
#	BASTRA: ON
#	MAPS: none
#	TRAFFIC: ground / random
#	LOGIT: 10 / 20 / 50 / 100
# -------------------------------------------------------------
./run_darwin.sh canogrid_Bastra_logit10_nomaps_randomtraffic
./run_darwin.sh canogrid_Bastra_logit10_nomaps_fulltraffic
./run_darwin.sh canogrid_Bastra_logit20_nomaps_randomtraffic
./run_darwin.sh canogrid_Bastra_logit20_nomaps_fulltraffic
./run_darwin.sh canogrid_Bastra_logit50_nomaps_randomtraffic
./run_darwin.sh canogrid_Bastra_logit50_nomaps_fulltraffic
./run_darwin.sh canogrid_Bastra_logit100_nomaps_randomtraffic
./run_darwin.sh canogrid_Bastra_logit100_nomaps_fulltraffic

# -------------------------------------------------------------
# EXPERIMENTS WITH
#	BASTRA: ON
#	MAPS: adhoc
#	TRAFFIC: ground / random
#	LOGIT: 10 / 20 / 50 / 100
# -------------------------------------------------------------
./run_darwin.sh canogrid_Bastra_logit10_adhocmaps_randomtraffic
./run_darwin.sh canogrid_Bastra_logit10_adhocmaps_fulltraffic
./run_darwin.sh canogrid_Bastra_logit20_adhocmaps_randomtraffic
./run_darwin.sh canogrid_Bastra_logit20_adhocmaps_fulltraffic
./run_darwin.sh canogrid_Bastra_logit50_adhocmaps_randomtraffic
./run_darwin.sh canogrid_Bastra_logit50_adhocmaps_fulltraffic
./run_darwin.sh canogrid_Bastra_logit100_adhocmaps_randomtraffic
./run_darwin.sh canogrid_Bastra_logit100_adhocmaps_fulltraffic

