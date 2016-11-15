'''
Created on 23 de feb. de 2016
@author: Valentin
'''

import os
import datetime
import traci

class BastraLog:
    log_level=0
    log_dir=""
    file_name=""
    log_path=""
    verbose=False
    def __init__(self, configuration):
        self.log_level=configuration["log_level"]
        self.file_name=configuration["log_file"]
        self.dir=configuration["log_dir"]
        self.verbose=configuration["verbose"]
        self.log_path=self.dir+self.file_name
        if os.path.isfile(self.log_path):
            os.remove(self.log_path)
        log_file=open(self.log_path, "w")
        date=datetime.datetime.now()
        day=date.day
        month=date.month
        year=date.year
        hour=date.hour
        min=date.minute
        log_file.write("\t\t************* BaStra Log File - " + str(month) + "." + str(day) + "." + str(year) + "  -  " + str(hour) + ":" + str(min) + " *************\n\n\n")

        log_file.write("------------Configuration-------------\n")

        for key in configuration.keys():
            line="%% " + key + " : " + str(configuration[key]) + "\n"
            log_file.write(line)

        log_file.write("--------------------------------------\n\n\n")
        log_file.close()
        return

    def printLog(self, msg_level, str_message):
        log_file=open(self.log_path, "a")
        stime=traci.simulation.getCurrentTime()/1000
        log=str(stime) + ":" + str_message
        if int(self.log_level)>=msg_level:
            log_file.write(log)
        if (self.verbose) and (msg_level==1):
            print( log )
        log_file.close()
        return

    def printLogVeh(self, msg_level, vehId, str_message):
      self.printLog( msg_level, "veh="+str(vehId)+":"+str_message )

    def printLogEdge(self, msg_level, edgeId, str_message):
      self.printLog( msg_level, "edge="+str(edgeId)+":"+str_message )


