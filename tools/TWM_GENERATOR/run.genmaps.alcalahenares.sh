#!/bin/bash
# ---------------------------------------------------------------------
# GENERATE MAPS WITH RANDOM UNIFORM DISTRIBUTIONS FOR ALCALA HENARES
# ---------------------------------------------------------------------

mkdir alcalahenares.maps
#python genmaps.bastra.py -c gmp.alcalahenares.ref.conf
#python genmaps.bastra.py -c gmp.alcalahenares.uni1.conf
#python genmaps.bastra.py -c gmp.alcalahenares.uni5.conf

# python genmaps.bastra.py -c gmp.alcalahenares.directedPenalty.1.conf
# python genmaps.bastra.py -c gmp.alcalahenares.directedPenalty.2.conf

# python genmaps.bastra.py -c gmp.alcalahenares.taz5-taz50S.incident.alfa5-step5.conf
# python genmaps.bastra.py -c gmp.alcalahenares.taz5-taz50S.incident.alfa5-step5-join.conf

# python genmaps.bastra.py -c gmp.alcalahenares.taz5-taz50S.incident2x1.join.conf
# python genmaps.bastra.py -c gmp.alcalahenares.taz5-taz50S.incident3x1.join.conf
# python genmaps.bastra.py -c gmp.alcalahenares.taz5-taz50S.incident2x8.join.conf
# python genmaps.bastra.py -c gmp.alcalahenares.taz5-taz50S.incident3x8.join.conf

# python genmaps.bastra.py -c gmp.alcalahenares.XL_top_used_edges.join.conf
set -x
#python genmaps.bastra.py -c gmp.alcalahenares.L.Emergency.Emergencies.conf
#python genmaps.bastra.py -c gmp.alcalahenares.L.Emergency.Vehicles.conf
python genmaps.bastra.py -c gmp.alcalahenares.L.Emergency.Vehicles_penalty.conf
