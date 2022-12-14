#!/bin/bash
# ---------------------------------------------------------------------
# GENERATE MAPS WITH RANDOM NORMAL DISTRIBUTIONS
# ---------------------------------------------------------------------

mkdir grid16.maps
python genmaps.bastra.py -c gmp.grid16.ref.conf
python genmaps.bastra.py -c gmp.grid16.rand05.conf
python genmaps.bastra.py -c gmp.grid16.rand2.conf
python genmaps.bastra.py -c gmp.grid16.directedPenalty.1.conf
python genmaps.bastra.py -c gmp.grid16.directedPenalty.2.conf

mkdir radial16.maps
python genmaps.bastra.py -c gmp.radial16.ref.conf
python genmaps.bastra.py -c gmp.radial16.rand05.conf
python genmaps.bastra.py -c gmp.radial16.rand2.conf
python genmaps.bastra.py -c gmp.radial16.directedPenalty.1.conf
python genmaps.bastra.py -c gmp.radial16.directedPenalty.2.conf

mkdir grid3.maps
python genmaps.bastra.py -c gmp.grid3.ref.conf
python genmaps.bastra.py -c gmp.grid3.rand05.conf
python genmaps.bastra.py -c gmp.grid3.rand2.conf
# python genmaps.bastra.py -c gmp.grid3.directedPenalty.1.conf
# python genmaps.bastra.py -c gmp.grid3.directedPenalty.2.conf

