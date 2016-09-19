# BASTRA Installation Requisites

SUMO Api usage requires python 2.7 compatible environments. Here you will find how to install and configure this environment.

Before installing Bastra you must check that the following software is installed and is accesible to be run:
* python.
* pyenv.
* SUMO simulator

## python
Check the python v2.7 is installed:
```
$ python -V

Python 2.7.6
```
If not found, check with oyur administrator how to install it or check your OS distribution help files.

## pip
Check the pip v2.7 is installed:
```
$ pip -V

pip 8.1.2 from /Library/Python/2.7/site-packages/pip-8.1.2-py2.7.egg (python 2.7)
```
If not found, check with oyur administrator how to install it or check your OS distribution help files.

## Aditional libraries

After creating the python sumo env, maybe some python packges would be rrequired for installation. You will use pip command.

Bastra requires the lxml python package. Install it with:
```
	(sumo) $ pip install lxml
	# !!! NOTE THE (sumo) prompt that indicates the activation of the pyenv !!!
```

## Python Virtual Environments

It is recommended as a best-practice that BASTRA runs in a python VIRTUALENV. For it, packages pyenv and pyenv-virtualenv are required.
To install them, follow the instructions as described in:
* [pyenv](https://github.com/yyuu/pyenv)
* [pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv)

# Check that your environment is properly installed and configured
### Create and configure your environment

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

## SUMO

Follow the instruction described in [SUMO installation guide](http://sumo.dlr.de/wiki/Installing) to install the package.

