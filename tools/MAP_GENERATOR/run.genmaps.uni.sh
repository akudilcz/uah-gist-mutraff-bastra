#!/bin/bash
# ---------------------------------------------------------------------
# GENERATE MAPS WITH RANDOM UNIFORM DISTRIBUTIONS
# ---------------------------------------------------------------------

python genmaps.bastra.py -c gmp.grid16.uni1.conf
python genmaps.bastra.py -c gmp.grid16.uni3.conf

python genmaps.bastra.py -c gmp.radial16.uni1.conf
python genmaps.bastra.py -c gmp.radial16.uni3.conf
