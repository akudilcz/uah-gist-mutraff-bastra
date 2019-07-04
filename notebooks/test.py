from MutraffExperiments.ExperimentCatalog import ExperimentCatalog

theExps = ExperimentCatalog('default')
theExps.loadExperimentsFromCSV( 'CATALOGO DE EXPERIMENTOS.csv' )

print( theExps.experiments )
#  exp = xp.ExperimentSet("nene")
