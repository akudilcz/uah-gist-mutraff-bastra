#!/bin/bash
# ---------------------------------------------------------------------
# GENERATE MAPS WITH RANDOM NORMAL DISTRIBUTIONS
# ---------------------------------------------------------------------

mkdir grid16.maps
# python genmaps.bastra.py -c gmp.grid16.ref.conf
# python genmaps.bastra.py -c gmp.grid16.rand05.conf
# python genmaps.bastra.py -c gmp.grid16.rand2.conf
# python genmaps.bastra.py -c gmp.grid16.directedPenalty.1.conf
# python genmaps.bastra.py -c gmp.grid16.directedPenalty.2.conf
python genmaps.bastra.py -c gmp.grid16.incidentTWM.conf

