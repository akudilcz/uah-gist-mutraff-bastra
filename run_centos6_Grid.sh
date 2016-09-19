#!/bin/bash

cat <<EOF
==================================================================
			BASTRA
		INTENTION AWARE SIMULATOR

		UAH - Universidad de Alcala
==================================================================
EOF

# Check environment
[ -z "$SUMO_HOME" ] && {
  echo "Setting SUMO vars"
  export SUMO_HOME="$HOME/traffic/sumo"
  export SUMO_BIN=${SUMO_HOME}/bin
  export PATH=.:$HOME/bin:$PATH:$SUMO_BIN

  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
}

[ -z "$PYENV_ROOT" ] && {
  echo "Setting PYENV vars"
  export PYENV_ROOT="$HOME/.pyenv"
  export PATH="$PYENV_ROOT/bin:$PATH"
}

# ==================================================================
DATE=`date +'%y%m%d_%H%M%S'`
DATA_ROOT=./data
DATA_DIR=${DATA_ROOT}_${DATE}
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
BASTRA_SCENE=Grid
echo "Selected simulation scene: $BASTRA_SCENE"

BASTRA_SCENE_DIR=./scenes/$BASTRA_SCENE

PYTHON_VERSION=2.7.6
# CURR_PYTHON="`python -V`"
# [ "$PYTHON_VERSION" != "$CURR_PYTHON" ] && { echo "ERROR: incorrect python version $CURR_PYTHON. Expected $PYTHON_VERSION."; exit 1; }

export PYTHONPATH=$PYTHONPATH:$SUMO_HOME/tools:./bastralib
echo "PYTHONPATH=$PYTHONPATH"

echo
set -x
python bastra.py -c $BASTRA_SCENE_DIR/bastra.conf.xml
