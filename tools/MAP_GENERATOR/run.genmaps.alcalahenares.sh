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
python genmaps.bastra.py -c gmp.alcalahenares.taz5-taz50S.incident.alfa5-step5.conf
python genmaps.bastra.py -c gmp.alcalahenares.taz5-taz50S.incident.alfa5-step5-join.conf
