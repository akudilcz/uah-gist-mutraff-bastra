#!/bin/bash
# ---------------------------------------------------------------------
# GENERATE MAPS WITH RANDOM UNIFORM DISTRIBUTIONS FOR ALCALA HENARES
# ---------------------------------------------------------------------

mkdir madrid_retiro.maps
python genmaps.bastra.py -c gmp.madrid_retiro.ref.conf
python genmaps.bastra.py -c gmp.madrid_retiro.rand05.conf
# python genmaps.bastra.py -c gmp.madrid_retiro.uni1.conf
# python genmaps.bastra.py -c gmp.madrid_retiro.uni5.conf
# python genmaps.bastra.py -c gmp.madrid_retiro.directedPenalty.1.conf
# python genmaps.bastra.py -c gmp.madrid_retiro.directedPenalty.2.conf

mkdir madrid_las_tablas.maps
python genmaps.bastra.py -c gmp.madrid_las_tablas.ref.conf
python genmaps.bastra.py -c gmp.madrid_las_tablas.rand05.conf

mkdir madrid_barrio_salamanca.maps
python genmaps.bastra.py -c gmp.madrid_barrio_salamanca.ref.conf
python genmaps.bastra.py -c gmp.madrid_barrio_salamanca.rand05.conf
