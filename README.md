# MUTRAFF / BASTRA Multi-Map Traffic Simulation Tool

BASTRA is a new traffic simulation tool that extends the well-known traffic simulation tool SUMO.  Is part of the MUTRAFF Research Project (Multi-Map Route Guidance Systems for Intelligent Optimization of Urban Traffic Flow) at GIST-UAH.

BASTRA enables dynamic route modification according to any routing policy, that is, changing the established routes on the fly. This allows:
* Implementing dynamic traffic policies from the Traffic Operation Center.
* Implementing driver-side traffic policies, such as Intention-Aware decisions.

You should use this package as follows:
* Supported platforms
* Check the License and Use Terms section.
* Installation and setup.
* QuickStart (execute the out-of-the-box *Grid* scene).
* Clone the *Grid* scene and create your own.

## Contact info 
Bastra is part of the MUTRAFF traffic research project developed at the *[GIST Research Group (Telematic Services Engineering Group](https://portal.uah.es/portal/page/portal/grupos_de_investigacion/49/Presentacion/QuienesSomos)* at *[Universidad de Alcala](http://www.uah.es)* developed by:
* Prof. Dr. Miguel Angel Lopez Carmona. Traffic Group Leader. [Contact](mailto://miguellopez.carmona@uah.es)
* Phd. Alvaro Paricio Garcia. MUTRAFF Traffic Researcher [Contact](mailto://alvaro.paricio@uah.es).
* Eng. Valentin Alberti. Main developer.

## Supported Platforms

Bastra has been tested succesfully in the following platforms:
* Linux CentOS.6 x64
* OS X Darwin x64 (MAC)
* Windows 7

If you port the tool to a new platform, we will kindly appreciate your contribution.

## License and Use Terms

All rights belong to its creators. No total or partial distribution is allowed 
without previous written consent.

SUMO is licensed [GPL v3](https://gnu.org/licenses/gpl.html) as stated in [Sumo License](http://sumo.dlr.de/wiki/License) where all its dependencies are also listed.

## Installation and Setup

Install the related python and SUMO packages as described in [Installation Pre-Requisites](./BASTRA_INSTALLATION_REQUISITES.md).

To install Bastra, you have to downkload it from the repository:
```
$ git clone https://github.com/uahservtel/uah-gist-mutraff-bastra.git
$ cd uah-gist-mutraff-bastra
```
You will find the "bastra.py" simulator and the run scripts as described in the QuickStart Guide.

## QuickStart

### Create and configure your python 2.7 environment

Create a python 2.7 environment:
```
        $ pyenv install 2.7.6
```

Define a SUMO env under 2.7 virtual environment:
```
        $ pyenv virtualenv 2.7.6 sumo
```

Check that everything is ok:
```
        $ ls -l $HOME/.pyenv/versions/
        $ pyenv virtualenvs
```

Activate the sumo environment:
```
        $ pyenv activate sumo
```

You will see the "(sumo) " prompt before your shell cursor:
```
        (sumo) $
```

### Run a BASTRA simulation scene

Simulation scenes are pre-defined traffic scenarios (network maps, demand configurations, traffic policies to adopt) that enable to do a simulation.

The package includes some "run_[OS]_[SCENE].sh" scripts to run the experiment described by
scene [SCENE] under the [OS] operating system environment. For instance:
```
(sumo) $ ./run_darwin_Grid.sh
```
will run the "Grid" scene under the OS-X Darwing environment.

Please, note that BASTRA should run in a python VIRTUALENV as described in the *Installation and Setup* section.

Run the default simulation in MAC OS-X Darwin:
```
$ pyenv activate sumo
(sumo) $ ./run_darwin_Grid.sh
```

Run the default simulation in CentOS.6:
```
$ pyenv activate sumo
(sumo) $ ./run_centos6_Grid.sh
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
* << tbd >>

Also you will find in the [scripts directory](scripts/) several utilities to manage.

## Package structure
* __scenes__ : contain the simulation scenarios and policies.
* __bastralib__ : contains the classes and objects that conform the simulator.
* __docs__ : contains the project's documentation.
* __data__ : contains non volatile results of simulation such as logs and trip dumps.

## Documentation

Can be found in the [docs directory](docs/).
