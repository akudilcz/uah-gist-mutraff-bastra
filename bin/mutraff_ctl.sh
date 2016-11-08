#!/bin/bash

cat <<EOF
==================================================================
			MUTRAFF CONTROLLER

			UAH - Universidad de Alcala
			alvaro.paricio@uah.es

Example: `basename $0` es.uah.gist.mutraff.toc_alvaro
==================================================================
EOF

function usage(){
cat <<EOF
*** USAGE ERROR ***
Usage: $0 MESSAGE_BROKER_NAME SCENARIO.
- MESSAGE_BUS is the selected busname for the communications.
EOF
exit 1
}

# ==================================================================
[ $# -lt 1 ] && { usage; }
COMM_OPTS="-x $1"

# ==================================================================
# Check environment
[ -z "$PYENV_ROOT" ] && {
  # echo "Setting PYENV vars"
  export PYENV_ROOT="$HOME/.pyenv"
  export PATH="$PYENV_ROOT/bin:$PATH"
}

PYTHON_VERSION=2.7.6
PYTHON_DEBUG="-m pdb"
PYTHON_DEBUG=""
# CURR_PYTHON="`python -V`"
# [ "$PYTHON_VERSION" != "$CURR_PYTHON" ] && { echo "ERROR: incorrect python version $CURR_PYTHON. Expected $PYTHON_VERSION."; exit 1; }

export PYTHONPATH=$PYTHONPATH:../libs

# echo "PYTHONPATH=$PYTHONPATH"

# This is your application name
PYTHON_APP_1="mutraff_ctl.py"

# Add here any arguments your applicaton needs.
PYTHON_ARGS_1=""

if [ ! -z "${PYTHON_DEBUG}" ]; then
  cat <<EOF
==================================================================
		DEBUGGING MODE is ON

Type "run" to execute, ctrl-C to stop, "c" to continue, etc.
==================================================================
EOF
  set -x
  python ${PYTHON_DEBUG} ../bin/$PYTHON_APP_1 $COMM_OPTS $PYTHON_ARGS
else
  # DATE_START=`date +%s`
  # echo "Execution Starts on: `date -j -f '%s' ${DATE_START}`"
  # echo "========================================================"

  python ../bin/$PYTHON_APP_1 $COMM_OPTS $PYTHON_ARGS

  # DATE_END=`date +%s`
  # echo "========================================================"
  # echo "Execution End    on: `date -j -f '%s' ${DATE_END}`"
fi
