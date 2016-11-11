#!/bin/bash

cat <<EOF
==================================================================
			MUTRAFF LAUNCH

			UAH - Universidad de Alcala
			alvaro.paricio@uah.es

Example: run_toc.sh es.uah.gist.mutraff.toc_alvaro SCENARIO_A
==================================================================
EOF

# ==================================================================
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

MUTRAFF_ROOT="../../.."
COMM_OPTS="-x $1"
BENV_SCENE=`basename $2`
BENV_SCENE_FILE=$MUTRAFF_ROOT/scenes/$BENV_SCENE/bastra.conf.xml
[ -d "$2" ] || { echo "Error. Scenario $2 doesn't exist"; exit 1; }
# echo "Selected simulation scene: $BENV_SCENE"

# ==================================================================
# Check environment
[ -z "$PYENV_ROOT" ] && {
  # echo "Setting PYENV vars"
  export PYENV_ROOT="$HOME/.pyenv"
  export PATH="$PYENV_ROOT/bin:$PATH"
}

# ==================================================================
# Check if AMPQ is running
if rabbitmqctl status 2>&1>/dev/null
then
  echo "Message server (rabbitmq) is active and responding"
else
  cat <<EOF
******************************
MESSAGE SERVER (rabbitmq) IS NOT RUNNIG OR INCONSISTENT STATUS
******************************
TIP. use the following command to start it:
     rabbitmq-server -detached
EOF
  exit 1
fi

# ==================================================================
DATE=`date +'%y%m%d_%H%M%S'`
DATA_BASENAME=${BENV_SCENE}_${DATE}
DATA_ROOT=./experiments/tmp
DATA_DIR=${DATA_ROOT}/${DATA_BASENAME}
STATS_FILE=${BENV_SCENE}_${DATE}.csv
# cd ..
# echo "Data dirs setup: ${DATA_DIR}"
(
  unlink ${DATA_DIR}
  mkdir -p ${DATA_DIR}/logs
  mkdir -p ${DATA_DIR}/dumps
  mkdir -p ${DATA_DIR}/tmp
  mkdir -p ${DATA_DIR}/results
  cd ${DATA_ROOT}
  unlink data
  ln -s ${DATA_BASENAME} data
) 2>/dev/null

cd ${DATA_ROOT}/data
# ==================================================================
PYTHON_VERSION=2.7.6
PYTHON_DEBUG="-m pdb"
PYTHON_DEBUG=""
# CURR_PYTHON="`python -V`"
# [ "$PYTHON_VERSION" != "$CURR_PYTHON" ] && { echo "ERROR: incorrect python version $CURR_PYTHON. Expected $PYTHON_VERSION."; exit 1; }

export PYTHONPATH=$PYTHONPATH:\
/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages:\
$MUTRAFF_ROOT/libs

# echo "PYTHONPATH=$PYTHONPATH"

# This is your application name
PYTHON_APP_TOC="mutraff_toc.py"
PYTHON_APP_VEH="mutraff_e_vehicle.py"

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
  python ${PYTHON_DEBUG} $MUTRAFF_ROOT/bin/$PYTHON_APP_TOC $COMM_OPTS PYTHON_ARGS -c $BENV_SCENE_FILE -s $BENV_SCENE
else
  echo
#  (
    DATE_START=`date +%s`
    echo "Execution Starts on: `date -j -f '%s' ${DATE_START}`"
    echo "=================================================================="

    python $MUTRAFF_ROOT/bin/$PYTHON_APP_TOC $COMM_OPTS $PYTHON_ARGS -c $BENV_SCENE_FILE -s $BENV_SCENE

    DATE_END=`date +%s`
    echo "=================================================================="
    echo "Execution End    on: `date -j -f '%s' ${DATE_END}`"

    PROCESS_TIME=$(echo "${DATE_END} - ${DATE_START}" | bc)
    echo "Execution total time: ${PROCESS_TIME}"
#  ) 2>&1 | tee time.out
fi


