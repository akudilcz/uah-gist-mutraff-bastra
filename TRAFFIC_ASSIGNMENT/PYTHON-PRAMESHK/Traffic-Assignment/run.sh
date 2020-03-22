#!/bin/bash

NET_DIR="OW"
NET_DIR="GRID64_6F"
NET_DIR="Madrid_Retiro"
NET_DIR="Madrid_Tablas"
NET_DIR="Madrid_Salamanca"
NET_DIR="Madrid_Retiro_1F"
NET_DIR="Sioux Falls network"

MAX_ITER="1000"
PRECISION="0.001"
ALGORITHM="MSA"
LOADING="deterministic"

OUT="msa.out"
DEBUG="9"

set -x
time python3 TrafficAssignment.py -s "${NET_DIR}" -d ${DEBUG} -p ${PRECISION} -i ${MAX_ITER} -a ${ALGORITHM} -l ${LOADING} 2>&1 | tee ${OUT}
