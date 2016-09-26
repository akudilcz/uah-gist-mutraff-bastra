#!/bin/bash

cat <<EOF
==================================================================
			BASTRA
		MULTI-MAP INTENTION-AWARE SIMULATOR

		UAH - Universidad de Alcala
==================================================================
EOF

# ==================================================================
[ $# -lt 1 ] && { echo "Error. Must provide a simulation scenario name.Check scenes dir for available ones"; exit 1; }

SCENE_DIR="./scenes"
BASTRA_SCENE=$1
[ -d "${SCENE_DIR}/${BASTRA_SCENE}" ] || { echo "Error. Scenario ${SCENE_DIR}/${BASTRA_SCENE} doesn't exist"; exit 1; }
echo "Selected simulation scene: $BASTRA_SCENE"

# ==================================================================
# Check environment
[ -z "$SUMO_HOME" ] && {
  echo "Setting SUMO vars"
  export SUMO_HOME="$HOME/traffic/sumo"
  export SUMO_BIN=${SUMO_HOME}/bin
  export PATH=.:$HOME/bin:$PATH:$SUMO_BIN
}

[ -z "$PYENV_ROOT" ] && {
  echo "Setting PYENV vars"
  export PYENV_ROOT="$HOME/.pyenv"
  export PATH="$PYENV_ROOT/bin:$PATH"
}

# ==================================================================
DATE=`date +'%y%m%d_%H%M%S'`
DATA_ROOT=./data
DATA_DIR=${DATA_ROOT}_${BASTRA_SCENE}_${DATE}
echo "Data dirs setup: ${DATA_DIR}"
(
  unlink ${DATA_ROOT}
  unlink ${DATA_DIR}
  mkdir -p ${DATA_DIR}/logs
  mkdir -p ${DATA_DIR}/dumps
  mkdir -p ${DATA_DIR}/tmp
  mkdir -p ${DATA_DIR}/results
  ln -s ${DATA_DIR} ${DATA_ROOT}
) 2>/dev/null

cd ${DATA_ROOT}
# ==================================================================
BASTRA_SCENE_DIR=../scenes/$BASTRA_SCENE

PYTHON_VERSION=2.7.6
PYTHON_DEBUG="-m pdb"
PYTHON_DEBUG=""
# CURR_PYTHON="`python -V`"
# [ "$PYTHON_VERSION" != "$CURR_PYTHON" ] && { echo "ERROR: incorrect python version $CURR_PYTHON. Expected $PYTHON_VERSION."; exit 1; }

export PYTHONPATH=$PYTHONPATH:$SUMO_HOME/tools:./bastralib
echo "PYTHONPATH=$PYTHONPATH"

if [ ! -z "${PYTHON_DEBUG}" ]; then
  cat <<EOF
==================================================================
		DEBUGGING MODE is ON

Type "run" to execute, ctrl-C to stop, "c" to continue, etc.
==================================================================
EOF
  set -x
  python ${PYTHON_DEBUG} ../bastra.py -c $BASTRA_SCENE_DIR/bastra.conf.xml
else
  echo
  (
    DATE_START=`date +%s`
    echo "Simulation Starts on: `date -j -f '%s' ${DATE_START}`"

    python ../bastra.py -c $BASTRA_SCENE_DIR/bastra.conf.xml

    DATE_END=`date +%s`
    echo "Simulation End    on: `date -j -f '%s' ${DATE_END}`"

    PROCESS_TIME=$(echo "${DATE_END} - ${DATE_START}" | bc)
    echo "Simulation total time: ${PROCESS_TIME}"
  ) 2>&1 | tee time.out
fi


