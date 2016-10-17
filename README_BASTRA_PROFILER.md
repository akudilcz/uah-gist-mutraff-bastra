# Using BASTRA PROFILER

If you want to use the BASTRA profiler you must follow two steps:
* Activate the "PYTHON_PROFILER_OPTS" in the run script (run_darwin.sh". This will generate the bastra.profile file when it terminates.
* After terminating the simulation, go to the expermients directory and process the generated file:
```
cd experiments/tmp/data
python -m pstats bastra.profile 
```
This will open a new prompt.
You should then type:
```
% stats bastra
```
There are mayn other command options. Please check the python profiler user manual.
