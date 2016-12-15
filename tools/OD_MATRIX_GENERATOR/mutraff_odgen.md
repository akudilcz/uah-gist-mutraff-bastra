# MuTRAFF ODGEN - Origin/Destination Matrix Calculus
                 _              __  __             _                  
                | |            / _|/ _|           | |                 
 _ __ ___  _   _| |_ _ __ __ _| |_| |_    ___   __| | __ _  ___ _ __  
| '_ ` _ \| | | | __| '__/ _` |  _|  _|  / _ \ / _` |/ _` |/ _ \ '_ \ 
| | | | | | |_| | |_| | | (_| | | | |   | (_) | (_| | (_| |  __/ | | |
|_| |_| |_|\__,_|\__|_|  \__,_|_| |_|    \___/ \__,_|\__, |\___|_| |_|
                                                      __/ |           
                                                     |___/            

                 MUTRAFF O/D Matrix generator
                    alvaro.paricio@uah.es

## Description
MuTRAFF Origin/Destination Demand Matrices generator.
Generates different kinds of O/D matrices from the SUMO simulation files: network and trip files.

Matrices generated show csv files where:
* Rows represent "FROM" trip starting point.
* Columns represent "TO" trip end point.

Available O/D matrices are:
* Trip counters 
* Edge weights for adjacencies from origins to destinations
* Edge ids at links from origins to destinations

## Usage
usage: mutraff_odgen [-h] -n IN_NET [-d IN_DEMAND] [-v] [-p OUT_PREFIX] [-A]
                     [-I] [-T] [-P] [-W] [-C] [-N] [-fti FILTER_TIME_INI]
                     [-fte FILTER_TIME_END]

Mandatory arguments:
  -n IN_NET, --in-net IN_NET
                        Input. SUMOs XML net description file

Optional arguments:
  -h, --help            show this help message and exit
  -d IN_DEMAND, --in-demand IN_DEMAND
                        Input. SUMOs trip file
  -v, --verbose         Verbose output
  -p OUT_PREFIX, --out-prefix OUT_PREFIX
                        Output. prefix for O/D generated files
  -A, --out-all         Output. Generate all the O/D matrices
  -I, --out-edge-ids    Output. Generate O/D matrix with edge ids
  -T, --out-edge-types  Output. Generate O/D matrix with edge types
  -P, --out-edge-priorities
                        Output. Generate O/D matrix with edge priorities
  -W, --out-weights     Output. Generate O/D matrix with edge weights
  -C, --out-trip-counters
                        Output. Generate O/D matrix with timeless trip
                        counters. Requires -d option enabled
  -N, --out-names       Output. Generate O/D matrix with street names
  -fti FILTER_TIME_INI, --filter-time-ini FILTER_TIME_INI
                        Filter. Dump trips from specified time
  -fte FILTER_TIME_END, --filter-time-end FILTER_TIME_END
                        Filter. Dump trips up to specified time

## Examples
Examples:
* Generate all matrices:
'''
> python mutraff_odgen.py -n alcalahenares.net.xml -d alcalahenares_L_Bastra_uni1x8_timeALL_fulltraffic_logit50.trip.xml -A
'''
* Generate time-filtered trip counters:
'''
> python mutraff_odgen.py -fti 1 -fte 2 -n alcalahenares.net.xml -C -d alcalahenares_L_Bastra_uni1x8_timeALL_fulltraffic_logit50.trip.xml
'''
