#!/bin/bash

# ----------------------------------------------------------------
# PARAMETERS
#
export __ROADLENGTH="50"
export __PREFIX="devFastTest"
export __TYPE="grid"
export __GRID_SIZE="16"
export __SIMUL_TIME_INI="0"
export __SIMUL_TIME_END="100"

# Default:
# export __BASTRA_USE_BALANCE="true"
export __BASTRA_USE_BALANCE="true"

# Default:
# export __BASTRA_LOGIT="1"
export __BASTRA_LOGIT="0.5"
echo "__BASTRA_LOGIT=${__BASTRA_LOGIT} percent of user using Bastra system"

# Default:
export __BASTRA_FORESIGHT_STEPS="1"
# export __BASTRA_FORESIGHT_STEPS="0"
echo "__BASTRA_FORESIGHT_STEPS=${__BASTRA_FORESIGHT_STEPS} foresight, following edges to consider in the planned route"

# Default:
export __BASTRA_FORESIGHT_TRIES="3"
# export __BASTRA_FORESIGHT_TRIES="0"
echo "__BASTRA_FORESIGHT_TRIES=${__BASTRA_FORESIGHT_TRIES} foresight, number of alternative edges to consider"

# Default:
export __BASTRA_FORESIGHT_HALTING="3"
# export __BASTRA_FORESIGHT_HALTING="0"
echo "__BASTRA_FORESIGHT_HALTING=${__BASTRA_FORESIGHT_HALTING} foresight, number of halted vehicles to decide jam occurence"

# Default:
export __BASTRA_FORESIGHT_PENALTY="50.0"
# export __BASTRA_FORESIGHT_PENALTY="1"
echo "__BASTRA_FORESIGHT_PENALTY=${__BASTRA_FORESIGHT_PENALTY} foresight, x weight multiplier for function cost"

# ----------------------------------------------------------------
cat <<EOF > /tmp/filter.sed
s/__PREFIX__/${__PREFIX}/g
s/__ROADLENGTH__/${__ROADLENGTH}/g
s/__TYPE__/${__TYPE}/g
s/__GRID_SIZE__/${__GRID_SIZE}/g
s/__BASTRA_USE_BALANCE__/${__BASTRA_USE_BALANCE}/g
s/__BASTRA_LOGIT__/${__BASTRA_LOGIT}/g
s/__BASTRA_FORESIGHT_STEPS__/${__BASTRA_FORESIGHT_STEPS}/g
s/__BASTRA_FORESIGHT_TRIES__/${__BASTRA_FORESIGHT_TRIES}/g
s/__BASTRA_FORESIGHT_HALTING__/${__BASTRA_FORESIGHT_HALTING}/g
s/__BASTRA_FORESIGHT_PENALTY__/${__BASTRA_FORESIGHT_PENALTY}/g
s/__SIMUL_TIME_INI__/${__SIMUL_TIME_INI}/g
s/__SIMUL_TIME_END__/${__SIMUL_TIME_END}/g
s/length=".*" /length="${__ROADLENGTH}" /g
EOF

# ----------------------------------------------------------------
__BASTRA_FILE="bastra.conf.xml"
__DUA_FILE="${__PREFIX}.duarouter.conf"
__CMDS_FILE="${__PREFIX}.commands.xml"
__MAPSFILE="${__PREFIX}.maps.xml"
__NET_FILE="${__PREFIX}.net.${TYPE}.conf"
__OD_FILE="${__PREFIX}.od.conf"
__ODMAT_FILE="${__PREFIX}.odmat.xml"
__SUMO_FILE="${__PREFIX}.sumo.conf"
__NETGEN_FILE="${__PREFIX}.net.xml"
__TAZ_FILE="${__PREFIX}.taz.xml"

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
[ -r "TEMPLATE.commands.xml" ] || die "Cannot find TEMPLATE.commands.xml"
[ -r "TEMPLATE.maps.xml" ]     || die "Cannot find TEMPLATE.maps.xml"
[ -r "TEMPLATE.net.${__TYPE}.conf" ] || die "Cannot find TEMPLATE.net.${__TYPE}.conf"
[ -r "TEMPLATE.od.conf" ]      || die "Cannot find TEMPLATE.od.conf"
[ -r "TEMPLATE.odmat.xml" ]    || die "Cannot find TEMPLATE.odmat.xml"
[ -r "TEMPLATE.sumo.conf" ]    || die "Cannot find TEMPLATE.sumo.conf"
[ -r "TEMPLATE.taz.xml" ]      || die "Cannot find TEMPLATE.taz.xml"
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
sed -f /tmp/filter.sed TEMPLATE.commands.xml > ${DIR}/${__CMDS_FILE}

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
sed -f /tmp/filter.sed TEMPLATE.taz.xml > ${DIR}/${__TAZ_FILE}

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
cd -
