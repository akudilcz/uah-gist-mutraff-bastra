#!/bin/bash

NET_DIR="../transportation_networks"
NET="OW.net"
NET="GRID64_6F.net"
NET="Madrid_Retiro.net"
NET="Madrid_Tablas.net"
NET="Madrid_Salamanca.net"
NET="Madrid_Retiro_1F.net"
OUT="msa.out"
DEBUG="9"

set -x
time python3 successive_averages.py -f ${NET_DIR}/${NET} -d ${DEBUG} 2>&1 > ${OUT}
#time python3 successive_averages.py -f ${NET_DIR}/${NET} -d ${DEBUG} 2>&1 | tee ${OUT}

