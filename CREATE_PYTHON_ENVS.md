# CREATE AND USE PYTHON ENVIRONMENTS FOR SUMO

SUMO Api usage requires python 2.7 compatible environments. Here you will find how to install and configure this environment.

## Required packages installation

Packages pyenv and pyenv-virtualenv are required. Please, follow the instruction described in:
* https://github.com/yyuu/pyenv
* https://github.com/yyuu/pyenv-virtualenv

## Create and configure your environment

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

## Aditional packages

After creating the python sumo env, maybe some python packges would be rrequired for installation. You will use pip command.

For instance, the lxml python package would be required. Install it with:
```
	(sumo) $ pip install lxml
	# !!! NOTE THE (sumo) prompt that indicates the activation of the pyenv !!!
```

