# MUTRAFF - A distributed TWM traffic control system

The MUTRAFF traffic control system uses Traffic Weighted Maps to dynamically or statically control traffic on a network.

## Components

* MUTRAFF TOC - Traffic Operations Center. It is the unit where the TWM maps areto be distributed.
* MUTRAFF Vehicle. It represents a mobile vehicle using TWM.
* MUTRAFF Fleet. It represents a fleet fo mobile vehicles using the network.
* MUTRAFF Controller - It provides a distributed console to be used in the system to analize events, congestions, etc. It provides several commands to interact with the platform.

## Scripts

* mutraff_ctl.sh - Launches the control console.
* mutraff_toc.sh - Launches the traffic control/operations system.
* mutraff_fleet.sh - Launches the fleets to be using Mutraff.
* mutraff_vehicle.sh - Launches a single vehicle using the network.
