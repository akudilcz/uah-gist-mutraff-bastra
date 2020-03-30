#!/bin/bash

NET_DIR="../transportation_networks"
NET_DIR="/Users/alvaro/Desktop/workspace/mutraff/uah-gist-mutraff-bastra/TRAFFIC_ASSIGNMENT/notebooks/maslab"
# ----------------------------------
NET="OW.net"
NET="GRID64_6F.net"
# ----------------------------------
NET="Madrid_Retiro.net"
NET="Madrid_Tablas.net"
NET="Madrid_Salamanca.net"
NET="Madrid_Retiro_1F.net"
# ----------------------------------
NET="madrid_las_tablas_od.net"
NET="madrid_barrio_salamanca_od.net"
NET="madrid_retiro_od.net"
# ----------------------------------
OUT="msa.out"
DEBUG="9"

set -x
time python3 successive_averages.py -f ${NET_DIR}/${NET} -d ${DEBUG} 2>&1 > ${OUT}
#time python3 successive_averages.py -f ${NET_DIR}/${NET} -d ${DEBUG} 2>&1 | tee ${OUT}

