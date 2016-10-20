#!/bin/bash

# ----------------------------------------------------------------
function default_params() {

  # Group: global
  # Descr: name of simulation
  # Default: 
  export __PREFIX="canogrid_noBastra_adhocmaps_randomtraffic"

  # Group: global
  # Descr: commands file to use
  # Default: nomaps, adhocmaps
  export __CMDS_TYPE="adhocmaps"

  # Group: network
  # Descr: length of edges in meters
  # Default: 50
  export __ROADLENGTH="50"

  # Group: network
  # Descr: type of network to generate
  # Default: grid
  export __TYPE="grid"

  # Group: network
  # Descr: number of lanes per edge
  # Default: 1
  export __LANES="1"

  # Group: network
  # Descr: max speed in the edges
  # Default: 13.9
  export __MAX_SPEED="13.9"

  # Group: time
  # Descr: simulation starting time
  # Default: 0
  export __SIMUL_TIME_INI="0"

  # Group: time
  # Descr: simulation end time
  # Default: 4000
  export __SIMUL_TIME_END="4000"

  # Group: traffic
  # Descr: baseline traffic: random trips to be generated
  # Default: 3000
  export __TRAFFIC_BASELINE="3000"

  # Group: traffic
  # Descr: directional traffic, peaks, traffic to be generated at certain edges
  # Default: 200
  export __TRAFFIC_BRANCH="0"

  # Group: network-grid
  # Descr: square size of the grid
  # Default: 16
  export __GRID_SIZE="16"

  # Group: network-spider
  # Descr: number of radial arms starting from the central point
  # Default: 16
  export __SPIDER_ARMS="16"

  # Group: network-spider
  # Descr: number of rings for the network
  # Default: 16
  export __SPIDER_CIRCLES="16"

  # Group: bastra
  # Descr: bastra algorithms is active?
  # Default: true
  export __BASTRA_USE_BALANCE="false"

  # Group: bastra
  # Descr: percent of users using Bastra application to route their vehicles
  # Default:  0.5
  export __BASTRA_LOGIT="0"

  # Group: bastra-Foresight
  # Descr: oresight, following edges to consider in the planned route
  # Default: 1
  export __BASTRA_FORESIGHT_STEPS="0"

  # Group: bastra-Foresight
  # Descr: foresight, number of alternative edges to consider (in a 4 sides crossing, use the 3 resting edges)
  # Default: 3
  export __BASTRA_FORESIGHT_TRIES="0"

  # Group: bastra-Foresight
  # Descr: foresight, number of halted vehicles to decide jam occurence
  # Default: 3
  export __BASTRA_FORESIGHT_HALTING="0"

  # Group: bastra-Foresight
  # Descr: weight multiplier for function cost: if congestion is detected increment traveltime x this factor
  # Default: 50
  export __BASTRA_FORESIGHT_PENALTY="1"
}

# ----------------------------------------------------------------
function load_config() {
  default_params
  [ $# -eq 1 ] || return
  CONF_FILE=$1
  if [ -f $CONF_FILE ]
  then
  	echo "Configuration file $CONF_FILE loaded"
	. $CONF_FILE
  else
	echo "Configuration file $CONF_FILE not found"
	return
  fi
}

echo ${PARAM_A}

# ----------------------------------------------------------------
load_config $*

# ----------------------------------------------------------------
cat <<EOF > /tmp/filter.sed
s/__PREFIX__/${__PREFIX}/g
s/__ROADLENGTH__/${__ROADLENGTH}/g
s/__TYPE__/${__TYPE}/g
s/__LANES__/${__LANES}/g
s/__MAX_SPEED__/${__MAX_SPEED}/g
s/__GRID_SIZE__/${__GRID_SIZE}/g
s/__SPIDER_ARMS__/${__SPIDER_ARMS}/g
s/__SPIDER_CIRCLES__/${__SPIDER_CIRCLES}/g
s/__BASTRA_USE_BALANCE__/${__BASTRA_USE_BALANCE}/g
s/__BASTRA_LOGIT__/${__BASTRA_LOGIT}/g
s/__BASTRA_FORESIGHT_STEPS__/${__BASTRA_FORESIGHT_STEPS}/g
s/__BASTRA_FORESIGHT_TRIES__/${__BASTRA_FORESIGHT_TRIES}/g
s/__BASTRA_FORESIGHT_HALTING__/${__BASTRA_FORESIGHT_HALTING}/g
s/__BASTRA_FORESIGHT_PENALTY__/${__BASTRA_FORESIGHT_PENALTY}/g
s/__SIMUL_TIME_INI__/${__SIMUL_TIME_INI}/g
s/__SIMUL_TIME_END__/${__SIMUL_TIME_END}/g
s/__TRAFFIC_BASELINE__/${__TRAFFIC_BASELINE}/g
s/__TRAFFIC_BRANCH__/${__TRAFFIC_BRANCH}/g
s/length=".*" /length="${__ROADLENGTH}" /g
EOF

# ----------------------------------------------------------------
__BASTRA_FILE="bastra.conf.xml"
__DUA_FILE="${__PREFIX}.duarouter.conf"
__CMDS_FILE="${__PREFIX}.commands.xml"
__MAPSFILE="${__PREFIX}.maps.xml"
__NET_FILE="${__PREFIX}.net.${__TYPE}.conf"
__OD_FILE="${__PREFIX}.od.conf"
__ODMAT_FILE="${__PREFIX}.odmat.xml"
__SUMO_FILE="${__PREFIX}.sumo.conf"
__NETGEN_FILE="${__PREFIX}.net.xml"
__TAZ_FILE="${__PREFIX}.${__TYPE}.taz.xml"
__VEH_FILE="${__PREFIX}.vehicle_distrib.conf"

TMPFILE="/tmp/tmp.net.xml"

# ----------------------------------------------------------------
function die() {
  echo "ERROR: $*"
  exit 1
}

# ----------------------------------------------------------------
echo "--- GENERATING SCENARIO: ${__PREFIX} --"

# ----------------------------------------------------------------
echo "--- Checking necessary TEMPLATES ---"
[ -r "TEMPLATE.bastra.conf" ]  || die "Cannot find TEMPLATE.bastra.conf"
[ -r "TEMPLATE.duarouter.conf" ] || die "Cannot find TEMPLATE.duarouter.conf"
[ -r "TEMPLATE.commands.${__CMDS_TYPE}.xml" ] || die "Cannot find TEMPLATE.commands.${__CMDS_TYPE}.xml"
[ -r "TEMPLATE.maps.xml" ]     || die "Cannot find TEMPLATE.maps.xml"
[ -r "TEMPLATE.net.${__TYPE}.conf" ] || die "Cannot find TEMPLATE.net.${__TYPE}.conf"
[ -r "TEMPLATE.od.conf" ]      || die "Cannot find TEMPLATE.od.conf"
[ -r "TEMPLATE.odmat.xml" ]    || die "Cannot find TEMPLATE.odmat.xml"
[ -r "TEMPLATE.sumo.conf" ]    || die "Cannot find TEMPLATE.sumo.conf"
[ -r "TEMPLATE.${__TYPE}.taz.xml" ] || die "Cannot find TEMPLATE.${__TYPE}.taz.xml"
[ -d "maps" ]                  || die "Cannot find maps dir"
echo "ok"

# ----------------------------------------------------------------
DIR="../${__PREFIX}"
mkdir $DIR 2>&1

# ----------------------------------------------------------------
(
cat <<EOF
.............................................
    BASTRA SIMULATION TOOL
    ESCENARIO: ${__PREFIX}

    alvaro.paricio@uah.es
(This file has been generated automatically by generate_scenes.sh)
.............................................
EOF
env | sort | grep __
) > $DIR/SCENARIO_DESCRIPTION.md

# ----------------------------------------------------------------
echo "--- Adapting conf files ---"

echo "Generating ${__BASTRA_FILE}"
sed -f /tmp/filter.sed TEMPLATE.bastra.conf > ${DIR}/${__BASTRA_FILE}

echo "Generating ${__DUA_FILE}"
sed -f /tmp/filter.sed TEMPLATE.duarouter.conf > ${DIR}/${__DUA_FILE}

echo "Generating ${__CMDS_FILE}"
sed -f /tmp/filter.sed TEMPLATE.commands.${__CMDS_TYPE}.xml > ${DIR}/${__CMDS_FILE}

echo "Generating ${__MAPSFILE}"
sed -f /tmp/filter.sed TEMPLATE.maps.xml > ${DIR}/${__MAPSFILE}

echo "Generating ${__NET_FILE}"
sed -f /tmp/filter.sed TEMPLATE.net.${__TYPE}.conf > ${DIR}/${__NET_FILE}

echo "Generating ${__OD_FILE}"
sed -f /tmp/filter.sed TEMPLATE.od.conf > ${DIR}/${__OD_FILE}

echo "Generating ${__ODMAT_FILE}"
sed -f /tmp/filter.sed TEMPLATE.odmat.xml > ${DIR}/${__ODMAT_FILE}

echo "Generating ${__SUMO_FILE}"
sed -f /tmp/filter.sed TEMPLATE.sumo.conf > ${DIR}/${__SUMO_FILE}

echo "Generating ${__TAZ_FILE}"
sed -f /tmp/filter.sed TEMPLATE.${__TYPE}.taz.xml > ${DIR}/${__TAZ_FILE}

echo "Generating ${__VEH_FILE}"
sed -f /tmp/filter.sed TEMPLATE.vehicle_distrib.conf > ${DIR}/${__VEH_FILE}
cp vehicle_types.xml ${DIR}/vehicle_types.xml

mkdir ${DIR}/maps
sed -f /tmp/filter.sed maps/TEMPLATE.gmp1.conf > ${DIR}/maps/gmp1.conf
sed -f /tmp/filter.sed maps/TEMPLATE.gmp2.conf > ${DIR}/maps/gmp2.conf
sed -f /tmp/filter.sed maps/TEMPLATE.gmp3.conf > ${DIR}/maps/gmp3.conf

cd $DIR

# ----------------------------------------------------------------
echo "--- Generating the NETWORK ---"
netgenerate -c ${__NET_FILE}
echo "Adjusting length and speed"
sed -f /tmp/filter.sed ${__NETGEN_FILE} | grep -v '</net>' > ${TMPFILE}
cat ${__TAZ_FILE} >> ${TMPFILE}
cp ${TMPFILE} ${__NETGEN_FILE}

# ----------------------------------------------------------------
# echo "--- Generating the DEMAND od2trips ---"
od2trips -c ${__OD_FILE} 

# ----------------------------------------------------------------
# echo "--- Generating the DEMAND duarouter ---"
duarouter -c ${__DUA_FILE} 

# ----------------------------------------------------------------
# echo "--- Typing the vehicles generated in the DEMAND file ---"
python ../../tools/randomVehType.py -c ${__VEH_FILE} 

# ----------------------------------------------------------------
cd -
