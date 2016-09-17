# BASTRA Multi-Map for SUMO simulation
# uah-gist-mutraff-bastra

<<< Abstract to be included >>

## Execute Bastra simulator

The package includes a "run.sh" script that contains the necessary steps to execute the __Grid__ simulation scene.

The simulator SHOULD RUN IN A python VIRTUALENV. You will find more info on how to install and use it in the *CREATE_PYTHON_ENVS.md* file.

Run the default simulation:
```
$ pyenv activate sumo
(sumo) $ ./run.sh
```

## Package structure
* __scenes__ : contain the simulation scenarios and policies.
* __bastralib__ : contains the classes and objects that conform the simulator.
* __docs__ : contains the project's documentation.
* __data__ : contains non volatile results of simulation such as logs and trip dumps.
## Documentation

Can be found inthe docs directory.
