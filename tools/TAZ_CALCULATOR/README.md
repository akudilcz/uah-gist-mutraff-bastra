# MUTRAFF TAZ-CALCULATOR
```
                 _              __  __   _                     _      
                | |            / _|/ _| | |                   | |     
 _ __ ___  _   _| |_ _ __ __ _| |_| |_  | |_ __ _ _______ __ _| | ___ 
| '_ ` _ \| | | | __| '__/ _` |  _|  _| | __/ _` |_  / __/ _` | |/ __|
| | | | | | |_| | |_| | | (_| | | | |   | || (_| |/ / (_| (_| | | (__ 
|_| |_| |_|\__,_|\__|_|  \__,_|_| |_|    \__\__,_/___\___\__,_|_|\___|

                 MUTRAFF TAZ Calculator
```
Author: alvaro.paricio@uah.es

Given an XML taz definition file based on polygon coordinates in GPS format(lat,lon), generate the associated SUMO TAZ definiton file with the edges contained inside each taz polygon.

## Usage
```
usage: mutraff_tazcalc [-h] -net IN_NET -nod IN_NODES -edg IN_EDGES -mutaz
                       IN_MUTAZ [-sumo_taz OUT_SUMO_TAZ] [-p NET_PATH] [-v]
                       [-t] [-i TAZ_ID_SEED]
```

# Arguments
## Mandatory
  -nod IN_NODES, --in-nodes IN_NODES
                        Input. SUMOs XML nodes description file
  -edg IN_EDGES, --in-edges IN_EDGES
                        Input. SUMOs XML edges description file
  -mutaz IN_MUTAZ, --in-mutaz IN_MUTAZ
                        Input. MUTRAFF XML description file
## Optional
  -h, --help            show this help message and exit
  -net IN_NET, --in-net IN_NET
                        Input. SUMOs XML net description file
  -sumo_taz OUT_SUMO_TAZ, --out-sumo-taz OUT_SUMO_TAZ
                        Output. Generate output to SUMO TAZ XML description
                        file
  -p NET_PATH, --net-path NET_PATH
                        Input. Path to locate files
  -v, --verbose         Verbose output
  -t, --run-tests       Run tests
  -i TAZ_ID_SEED, --taz-id-seed TAZ_ID_SEED
                        USe this number as TAZ id numbering seed

# Examples
* Generate the TAZs associated to a given polygon:
```
    python mutraff_tazcalc.py -net alcalahenares.net.xml -nod alcalahenares.nod.xml -edg alcalahenares.edg.xml -mutaz alcalahenares.mutaz.xml -sumo_taz alcalahenares.taz.xml
```
