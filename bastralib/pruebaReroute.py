
import traci
import subprocess
import sys
import os
from sumolib import checkBinary
import time


if __name__ == '__main__':

    try:
        sys.path.append(os.path.join(os.path.dirname(
            __file__), '..', '..', '..', '..', "tools"))
        sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
            os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in doc
    except ImportError:
        sys.exit("please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")


    sumoBinary = checkBinary('sumo-gui')
    sumoProcess = subprocess.Popen([sumoBinary, "-c", "../prueba.sumocfg", "--remote-port",  "2081", "-l", "prueba_log"], stdout=sys.stdout, stderr=sys.stderr)

    traci.init(2081)

    while traci.simulation.getMinExpectedNumber() > 0:
        print ("time: " + str(traci.simulation.getCurrentTime()/1000))

        option=raw_input("Opcion: ")
        if option=="c":
            traci.simulationStep()
        elif option=="i":
            id=raw_input("ID del vehiculo: ")
            print ("Ruta prevista: " + str(traci.vehicle.getRoute(id)) + "\n")
            edge=raw_input("edge de la ruta: ")
            edge_list=[]
            while edge<>"f":
                edge_list.append(edge)
                edge=raw_input("edge de la ruta: ")
            traci.vehicle.setRoute(id, edge_list)
            print (traci.vehicle.getRoute(id))

    print "Fin de la simulacion"