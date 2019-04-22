#!/bin/bash

cat <<EOF
==================================================================
			MUTRAFF LAUNCH

			UAH - Universidad de Alcala
			alvaro.paricio@uah.es

Example: mutraff_vehicle.sh uah.gist.mutraff.comms.bus_alvaro SCENARIO_A
==================================================================
EOF

function usage(){
cat <<EOF
*** USAGE ERROR ***
Usage: $0 MESSAGE_BROKER_NAME SCENARIO.
- MESSAGE_BROKER_NAME is the selected busname for the communications.
- SCENARIO: is the running scenario (input data, configurations, etc) Must provide a simulation scenario name.Check scenes dir for available ones
EOF
exit 1
}

# ==================================================================
[ $# -lt 2 ] && { usage; }

SCENE_DIR="../scenes"
COMM_OPTS="-x $1"
BENV_SCENE=$2
[ -d "${SCENE_DIR}/${BENV_SCENE}" ] || { echo "Error. Scenario ${SCENE_DIR}/${BENV_SCENE} doesn't exist"; exit 1; }
echo "Selected simulation scene: $BENV_SCENE"

# ==================================================================
# Check environment
[ -z "$PYENV_ROOT" ] && {
  echo "Setting PYENV vars"
  export PYENV_ROOT="$HOME/.pyenv"
  export PATH="$PYENV_ROOT/bin:$PATH"
}

# ==================================================================
DATE=`date +'%y%m%d_%H%M%S'`

cd ..
DATA_ROOT=./data
DATA_DIR=${DATA_ROOT}_${BENV_SCENE}_${DATE}
echo "Data dirs setup: ${DATA_DIR}"
(
  unlink ${DATA_ROOT}
  unlink ${DATA_DIR}
  mkdir -p ${DATA_DIR}/logs
  ln -s ${DATA_DIR} ${DATA_ROOT}
) 2>/dev/null

cd ${DATA_ROOT}
# ==================================================================
BENV_SCENE_DIR=../scenes/$BENV_SCENE

PYTHON_VERSION=2.7.6
PYTHON_DEBUG="-m pdb"
PYTHON_DEBUG=""
# CURR_PYTHON="`python -V`"
# [ "$PYTHON_VERSION" != "$CURR_PYTHON" ] && { echo "ERROR: incorrect python version $CURR_PYTHON. Expected $PYTHON_VERSION."; exit 1; }

# /opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages:\
export PYTHONPATH=$PYTHONPATH:\
../libs

echo "PYTHONPATH=$PYTHONPATH"

# This is your application name
PYTHON_APP="mutraff_vehicle.py"

# Add here any arguments your applicaton needs.
PYTHON_ARGS_1=""
PYTHON_ARGS_2=""

if [ ! -z "${PYTHON_DEBUG}" ]; then
  cat <<EOF
==================================================================
		DEBUGGING MODE is ON

Type "run" to execute, ctrl-C to stop, "c" to continue, etc.
==================================================================
EOF
  set -x
  python ${PYTHON_DEBUG} ../bin/$PYTHON_APP $COMM_OPTS PYTHON_ARGS
else
  echo
#  (
    DATE_START=`date +%s`
    echo "Execution Starts on: `date -j -f '%s' ${DATE_START}`"
    echo "=================================================================="

    python ../bin/$PYTHON_APP $COMM_OPTS $PYTHON_ARGS

    DATE_END=`date +%s`
    echo "=================================================================="
    echo "Execution End    on: `date -j -f '%s' ${DATE_END}`"

    PROCESS_TIME=$(echo "${DATE_END} - ${DATE_START}" | bc)
    echo "Execution total time: ${PROCESS_TIME}"
#  ) 2>&1 | tee time.out
fi


