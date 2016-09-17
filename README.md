# BASTRA Multi-Map for SUMO simulation

BASTRA is a new traffic simulation tool that extends the well-known traffic simulation tool SUMO.

BASTRA enables dynamic route modification according to any routing policy, that is, changing the established routes on the fly. This allows:
* Implementing dynamic traffic policies from the TRaffic Operation CEnter.
* Implementing driver-side traffic policies, such as Intention-Aware decisions.

You should use this package as follows:
* Check the License and Use Terms section.
* Installation and setup.
* Quickstart (execute the out-of-the-box *Grid* scene).
* Clone the *Grid* scene and create your own.

## License and Contact info 
Bastra is a research project from the *[GIST Search Group (Telematic Services Engineering Group](https://portal.uah.es/portal/page/portal/grupos_de_investigacion/49/Presentacion/QuienesSomos)* at *[Universidad de Alcala](http://www.uah.es)* developed by:
* Prof. Dr. Miguel Angel Lopez Carmona. Traffic Group Leader. [Contact](mailto://miguellopez.carmona@uah.es)
* Phd. Alvaro Paricio Garcia. Main Traffic Researcher [Contact](mailto://alvaro.paricio@uah.es).
* Eng. Valentin Alberti. Main developer.

All rights belong to its creators. No total or partial distribution is allowed 
without previous written consent.

## Installation and Setup

<< to be written >>

## Quickstart

The package includes a "run.sh" script that contains the necessary steps to execute the __Grid__ simulation scene.

The simulator SHOULD RUN IN A python VIRTUALENV. You will find more info on how to install and use it in the *CREATE_PYTHON_ENVS.md* file.

Run the default simulation:
```
$ pyenv activate sumo
(sumo) $ ./run.sh
```

You will check in your screen how simulation is executed using a non-gui SUMO instance (as defined in the *grid* scene). The simulation will take some long time depending on your ecomputing resources and environment.

Execution results will create several files:
* statistics.csv : a CSV formatted report with execution results.
* data/dumps/... : dumps on each traffic routing iteration
* data/logs/... : logs about bastra execution

Execution results will create several files:
* statistics.csv : a CSV formatted report with execution results.
* data/dumps/* : dumps on each traffic routing iteration

## Tools

Bastra package is formed by several tools:
* *bastra.py* : Bastra simulator

Also you will find in the [scripts directory](scripts/) several utilities to manage.

## Package structure
* __scenes__ : contain the simulation scenarios and policies.
* __bastralib__ : contains the classes and objects that conform the simulator.
* __docs__ : contains the project's documentation.
* __data__ : contains non volatile results of simulation such as logs and trip dumps.

## Documentation

Can be found in the [docs directory](docs/).
