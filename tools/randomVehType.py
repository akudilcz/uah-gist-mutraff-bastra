import optparse
import sys
import os
from lxml import etree
import random


class Vehicle:
    id=""
    type=""
    accel=""
    decel=""
    length=""
    max_speed=""
    color=""
    route=""
    # depart=""
    depart=0
    departLane=""
    departPos=""
    departSpeed=""
    arrivalLane=""
    arrivalPos=""
    arrivalSpeed=""
    line=""
    personNumber=""
    containerNumber=""
    fromTaz=""
    toTaz=""

    def __init__(self):
        return

    def getId(self):
        return self.id
    def setId(self, id):
        self.id=id
        return
    def getType(self):
        return self.type
    def setType(self, type):
        self.type=type
        return
    def setAccel(self, accel):
        self.accel=accel
        return
    def getAccel(self):
        return self.accel
    def setDecel(self, decel):
        self.decel=decel
        return
    def getDecel(self):
        return self.decel
    def setLength(self, length):
        self.length=length
        return
    def getLength(self):
        return self.length
    def setMaxSpeed(self, max_speed):
        self.max_speed=max_speed
        return
    def getMaxSpeed(self):
        return self.max_speed
    def setColor(self, color):
        self.color=color
        return
    def getColor(self):
        return self.color
    def setroutes(self, routes):
        self.routes=routes
        return
    def getroutes(self):
        return self.routes
    def setDepart(self, depart):
        self.depart=float(depart)
        return
    def getDepart(self):
        return self.depart
    def getDepartLane(self):
        return self.departLane
    def setDepartLane(self, departLane):
        self.departLane=departLane
        return
    def getDepartPos(self):
        return self.departPos
    def setDepartPos(self, departPos):
        self.departPos=departPos
        return
    def getDepartSpeed(self):
        return self.departSpeed
    def setDepartSpeed(self, departSpeed):
        self.departSpeed=departSpeed
        return
    def getArrivalLane(self):
        return self.arrivalLane
    def setArrivalLane(self, arrivalLane):
        self.arrivalLane=arrivalLane
        return
    def getArrivalPos(self):
        return self.arrivalPos
    def setArrivalPos(self, arrivalPos):
        self.arrivalPos=arrivalPos
        return
    def getArrivalSpeed(self):
        return self.arrivalSpeed
    def setArrivalSpeed(self, arrivalSpeed):
        self.arrivalSpeed=arrivalSpeed
        return
    def getLine(self):
        return self.line
    def setLine(self, line):
        self.line=line
        return
    def getPersonNumber(self):
        return self.personNumber
    def setPersonNumber(self, personNumber):
        self.personNumber=personNumber
        return
    def getContainerNumber(self):
        return self.containerNumber
    def setContainerNumber(self, containerNumber):
        self.containerNumber=containerNumber
        return
    def getFromTaz(self):
        return self.fromTaz
    def setFromTaz(self, fromTaz):
        self.fromTaz=fromTaz
        return
    def getToTaz(self):
        return self.toTaz
    def setToTaz(self, toTaz):
        self.toTaz=toTaz
        return


class Type:
    id=""
    accel=""
    decel=""
    sigma=""
    tau=""
    length=""
    minGap=""
    maxSpeed=""
    speedFactor=""
    speedDev=""
    color=""
    vClass=""
    emissionClass=""
    guiShape=""
    width=""
    imgFile=""
    impatience=""
    laneChangeModel=""
    carFollowModel=""
    personCapacity=""
    containerCapacity=""
    boardingDuration=""
    loadingDuration=""
    latAlignment=""
    minGapLat=""
    maxSpeedLat=""
    weight=""

    def getId(self):
        return self.id
    def setId(self, id):
        self.id=id
        return
    def getAccel(self):
        return self.accel
    def setAccel(self, accel):
        self.accel=accel
        return
    def getDecel(self):
        return self.decel
    def setDecel(self, decel):
        self.decel=decel
        return
    def getSigma(self):
        return self.sigma
    def setSigma(self, sigma):
        self.sigma=sigma
        return
    def getTau(self):
        return self.tau
    def setTau(self, tau):
        self.tau=tau
        return
    def getLength(self):
        return self.length
    def setLength(self, length):
        self.length=length
        return
    def getMinGap(self):
        return self.minGap
    def setMinGap(self, minGap):
        self.minGap=minGap
        return
    def getMaxSpeed(self):
        return self.maxSpeed
    def setMaxSpeed(self, maxSpeed):
        self.maxSpeed=maxSpeed
        return
    def getSpeedFactor(self):
        return self.speedFactor
    def setSpeedFactor(self, speedFactor):
        self.speedFactor=speedFactor
        return
    def getSpeedDev(self):
        return self.speedDev
    def setSpeedDev(self, speedDev):
        self.speedDev=speedDev
        return
    def getColor(self):
        return self.color
    def setColor(self, color):
        self.color=color
        return
    def getVClass(self):
        return self.vClass
    def setVCLass(self, vClass):
        self.vClass=vClass
        return
    def getEmissionClass(self):
        return self.emissionClass
    def setEmissionClass(self, emissionClass):
        self.emissionClass=emissionClass
        return
    def getGuiShape(self):
        return self.guiShape
    def setGuiShape(self, guiShape):
        self.guiShape=guiShape
        return
    def getWidth(self):
        return self.width
    def setWidth(self, width):
        self.width=width
        return
    def getImgFile(self):
        return self.imgFile
    def setImgFile(self, imgFile):
        self.imgFile=imgFile
        return
    def getImpatience(self):
        return self.impatience
    def setImpatience(self, impatience):
        self.impatience=impatience
        return
    def getLaneChangeModel(self):
        return self.laneChangeModel
    def setLaneChangeModel(self, laneChangeModel):
        self.laneChangeModel=laneChangeModel
        return
    def getCarFollowModel(self):
        return self.carFollowModel
    def setCarFollowModel(self, carFollowModel):
        self.carFollowModel=carFollowModel
        return
    def getPersonCapacity(self):
        return self.personCapacity
    def setPersonCapacity(self, personCapacity):
        self.personCapacity=personCapacity
        return
    def getContainerCapacity(self):
        return self.containerCapacity
    def setContainerCapacity(self, containerCapacity):
        self.containerCapacity=containerCapacity
        return
    def getBoardingDuration(self):
        return self.boardingDuration
    def setBoardingDuration(self, boardingDuration):
        self.boardingDuration=boardingDuration
        return
    def getLoadingDuration(self):
        return self.loadingDuration
    def setLoadingDuration(self, loadingDuration):
        self.loadingDuration=loadingDuration
        return
    def getLatAlignment(self):
        return self.latAlignment
    def setLatAlignment(self, latAlignment):
        self.latAlignment=latAlignment
        return
    def getMinGapLat(self):
        return self.minGapLat
    def setMinGapLat(self, minGapLat):
        self.minGapLat=minGapLat
        return
    def getMaxSpeedLat(self):
        return self.maxSpeedLat
    def setMaxSpeedLat(self, maxSpeedLat):
        self.maxSpeedLat=maxSpeedLat
        return
    def setWeight(self, weight):
        self.weight=weight
        return
    def getWeight(self):
        return self.weight



def getConfig():
    parser = optparse.OptionParser()
    parser.add_option("-c", "--config", dest="config_file",
                    help="define the configuration file (mandatory)", type="string")
    (options, args) = parser.parse_args()
    return options


def readOption(option):
    try:
        tree=etree.parse(config_file)
        root=tree.getroot()
        l_config=root.findall("randvt")
        label=l_config[0].find(option)
        value=label.get("value")
    except:
        sys.exit("Configuration error: value for " + option + " in " + config_file + " not found.")

    return value

def load_config():
    dict_conf={}
    dict_conf["types_file"]=readOption("types_file")
    dict_conf["routes_file"]=readOption("routes_file")
    dict_conf["output"]=readOption("output")

    return dict_conf


def readTypes(types_file):
    r_types=[]
    tree=etree.parse(types_file)
    root=tree.getroot()
    l_types=root.findall("type")

    for type in l_types:
        new_type=Type()
        id=type.get("id")
        accel=type.get("accel")
        decel=type.get("decel")
        sigma=type.get("sigma")
        tau=type.get("tau")
        length=type.get("length")
        minGap=type.get("minGap")
        max_speed=type.get("max_speed")
        speedFactor=type.get("speedFactor")
        speedDev=type.get("speedDev")
        color=type.get("color")
        vClass=type.get("vClass")
        emissionClass=type.get("emissionClass")
        guiShape=type.get("guiShape")
        width=type.get("width")
        imgFile=type.get("imgFile")
        impatience=type.get("impatience")
        laneChangeModel=type.get("laneChangeModel")
        carFollowModel=type.get("carFollowModel")
        personCapacity=type.get("personCapacity")
        containerCapacity=type.get("ContainerCapacity")
        boardingDuration=type.get("boardingDuration")
        loadingDuration=type.get("loadingDuration")
        latAlignment=type.get("latAlignment")
        minGapLat=type.get("minGapLat")
        maxSpeedLat=type.get("maxSpeedLat")
        weight=type.get("weight")

        if id==None:
            print ("Error: Id value for a type is not defined (mandatory).\n")
            exit(1)
        else:
            new_type.setId(id)
        if accel is not None:
            new_type.setAccel(accel)
        if decel is not None:
            new_type.setDecel(decel)
        if sigma is not None:
            new_type.setSigma(sigma)
        if tau is not None:
            new_type.setTau(tau)
        if length is not None:
            new_type.setLength(length)
        if minGap is not None:
            new_type.setMinGap(minGap)
        if max_speed is not None:
            new_type.max_speed(max_speed)
        if speedFactor is not None:
            new_type.setSpeedFactor(speedFactor)
        if speedDev is not None:
            new_type.setSpeedDev(speedDev)
        if color is not None:
            new_type.setColor(color)
        if vClass is not None:
            new_type.setVCLass(vClass)
        if emissionClass is not None:
            new_type.setEmissionClass(emissionClass)
        if guiShape is not None:
            new_type.setGuiShape(guiShape)
        if width is not None:
            new_type.setWidth(width)
        if imgFile is not None:
            new_type.setImgFile(imgFile)
        if impatience is not None:
            new_type.setImpatience(impatience)
        if laneChangeModel is not None:
            new_type.setLaneChangeModel(laneChangeModel)
        if carFollowModel is not None:
            new_type.setCarFollowModel(carFollowModel)
        if personCapacity is not None:
            new_type.setPersonCapacity(personCapacity)
        if containerCapacity is not None:
            new_type.setContainerCapacity(containerCapacity)
        if boardingDuration is not None:
            new_type.setBoardingDuration(boardingDuration)
        if loadingDuration is not None:
            new_type.setLoadingDuration(loadingDuration)
        if latAlignment is not None:
            new_type.setLatAlignment(latAlignment)
        if minGapLat is not None:
            new_type.setMinGapLat(minGapLat)
        if maxSpeedLat is not None:
            new_type.setMaxSpeedLat(maxSpeedLat)
        if weight is None:
            print ("Error: weight for type " + new_type.getId() + " is not defined (mandatory).\n")
            exit(1)
        else:
            new_type.setWeight(weight)
        r_types.append(new_type)

    return r_types


def readVehicles(routes_file):
    r_vehicles=[]
    tree=etree.parse(routes_file)
    root=tree.getroot()
    l_vehicles=root.findall("vehicle")

    for vehicle in l_vehicles:
        new_vehicle=Vehicle()
        id=vehicle.get("id")
        type=vehicle.get("type")
        accel=vehicle.get("accel")
        decel=vehicle.get("decel")
        length=vehicle.get("length")
        max_speed=vehicle.get("max_speed")
        color=vehicle.get("color")
        l_routes=vehicle.find("route")
        routes=l_routes.get("edges")
        depart=vehicle.get("depart")
        departLane=vehicle.get("departLane")
        departPos=vehicle.get("departPos")
        departSpeed=vehicle.get("departSpeed")
        arrivalLane=vehicle.get("arrivalLane")
        arrivalPos=vehicle.get("arrivalPos")
        arrivalSpeed=vehicle.get("arrivalSpeed")
        line=vehicle.get("line")
        personNumber=vehicle.get("personNumber")
        containerNumber=vehicle.get("containerNumber")
        fromTaz=vehicle.get("fromTaz")
        toTaz=vehicle.get("toTaz")

        if id is None:
            print ("Error: Id value for a vehicle is not defined (mandatory).\n")
            exit(1)
        else:
            new_vehicle.setId(id)
        if type is not None:
            new_vehicle.setType(type)
        if accel is not None:
            new_vehicle.setAccel(accel)
        if decel is not None:
            new_vehicle.setDecel=decel
        if length is not None:
            new_vehicle.setLength(length)
        if max_speed is not None:
            new_vehicle.max_speed(max_speed)
        if color is not None:
            new_vehicle.setColor(color)
        if routes is None:
            print ("Error: routes for vehicle " + new_vehicle.getId() + " is not defined (mandatory).\n")
            exit(1)
        else:
            new_vehicle.setroutes(routes)
        if depart is not None:
            new_vehicle.setDepart(depart)
        if departLane is not None:
            new_vehicle.setDepartLane(departLane)
        if departPos is not None:
            new_vehicle.setDepartPos(departPos)
        if departSpeed is not None:
            new_vehicle.setDepartSpeed(departSpeed)
        if arrivalLane is not None:
            new_vehicle.setArrivalLane(arrivalLane)
        if arrivalPos is not None:
            new_vehicle.setArrivalPos(arrivalPos)
        if arrivalSpeed is not None:
            new_vehicle.setArrivalSpeed(arrivalSpeed)
        if line is not None:
            new_vehicle.setLine(line)
        if personNumber is not None:
            new_vehicle.setPersonNumber(personNumber)
        if containerNumber is not None:
            new_vehicle.setPersonNumber(personNumber)
        if fromTaz is not None:
            new_vehicle.setFromTaz(fromTaz)
        if toTaz is not None:
            new_vehicle.setToTaz(toTaz)

        r_vehicles.append(new_vehicle)

    return r_vehicles


def printTypes(type_list, file):
    for type in type_list:
        file.write ("\t<vType id=\"" + type.getId() + "\" ")
        if len(type.getAccel())>0:
            file.write("accel=\"" + type.getAccel() + "\" ")
        if len(type.getDecel())>0:
            file.write("decel=\"" + type.getDecel() + "\" ")
        if len(type.getSigma())>0:
            file.write("sigma=\"" + type.getSigma() + "\" ")
        if len(type.getTau())>0:
            file.write("tau=\"" + type.getTau() + "\" ")
        if len(type.getLength())>0:
            file.write("length=\"" + type.getLength() + "\" ")
        if len(type.getMinGap())>0:
            file.write("minGap=\"" + type.getMinGap() + "\" ")
        if len(type.getMaxSpeed()):
            file.write("maxSpeed=\"" + type.getMaxSpeed() + "\" ")
        if len(type.getSpeedFactor())>0:
            file.write("speedFactor=\"" + type.getSpeedFactor() + "\" ")
        if len(type.getSpeedDev())>0:
            file.write("speedDev=\"" + type.getSpeedDev() + "\" ")
        if len(type.getColor())>0:
            file.write("color=\"" + type.getColor() + "\" ")
        if len(type.getVClass())>0:
            file.write("vClass=\"" + type.getVClass() + "\" ")
        if len(type.getEmissionClass())>0:
            file.write("emissionClass=\"" + type.getEmissionClass() + "\" ")
        if len(type.getGuiShape())>0:
            file.write("guiShape=\"" + type.getGuiShape() + "\" ")
        if len(type.getWidth())>0:
            file.write("width=\"" + type.getWidth() + "\" ")
        if len(type.getImgFile())>0:
            file.write("imgFile=\"" + type.getImgFile() + "\" ")
        if len(type.getImpatience())>0:
            file.write("impatience=\"" + type.getImpatience() + "\" ")
        if len(type.getLaneChangeModel())>0:
            file.write("laneChangeModel=\"" + type.getLaneChangeModel() + "\" ")
        if len(type.getCarFollowModel())>0:
            file.write("carFollowModel=\"" + type.getCarFollowModel() + "\" ")
        if len(type.getPersonCapacity())>0:
            file.write("personCapacity=\"" + type.getPersonCapacity() + "\" ")
        if len(type.getContainerCapacity())>0:
            file.write("containerCapacity=\"" + type.getContainerCapacity() + "\" ")
        if len(type.getBoardingDuration())>0:
            file.write("boardingDuration=\"" + type.getBoardingDuration() + "\" ")
        if len(type.getLoadingDuration())>0:
            file.write("loadingDuration=\"" + type.getLoadingDuration() + "\" ")
        if len(type.getLatAlignment())>0:
            file.write("latAlignment=\"" + type.getLatAlignment() + "\" ")
        if len(type.getMinGapLat())>0:
            file.write("minGapLat=\"" + type.getMinGapLat() + "\" ")
        if len(type.getMaxSpeedLat())>0:
            file.write("maxSpeedLat=\"" + type.getMaxSpeedLat() + "\" ")
        file.writelines("/>\n")

    return


def getRule(type_list):
    rule=[]
    sum=0
    for type in type_list:
        sum=sum+float(type.getWeight())
    for type in type_list:
        per=float(type.getWeight())/sum
        rule.append((type.getId(), per))
    return rule


def chooseType(veh,rules):
    if( veh.id.startswith("1100") ):
      return "POLICEMEN"
    if( veh.id.startswith("1200") ):
      return "FIREMEN"
    rand=random.random()
    acul=0
    for a_rule in rules:
        acul=acul+a_rule[1]
        if rand<acul:
            return a_rule[0]
    return


def printVehicles(vehicle_list, type_list, file):

    rule=getRule(type_list)
    # ---------------------------
    # Sort vehicles
    # ---------------------------
    # vehicle_list.sort(key=lambda x: x.count, reverse=True)
    vehicle_list.sort(key=lambda x: x.depart)

    # ---------------------------
    # Print vehicles
    # ---------------------------
    for veh in vehicle_list:
        file.write("\t<vehicle ")
        # if len(veh.getDepart())>0:
            # file.write("depart=\"" + veh.getDepart() + "\" ")
        file.write("depart=\"{}\" ".format( veh.getDepart() ))
        file.write("id=\"" + veh.getId() + "\" ")
        if len(veh.getAccel())>0:
            file.write("accel=\"" + veh.getAccel() + "\" ")
        if len(veh.getDecel())>0:
            file.write("decel=\"" + veh.getDecel() + "\" ")
        if len(veh.getLength())>0:
            file.write("length=\"" + veh.getLength() + "\" ")
        if len(veh.getMaxSpeed()):
            file.write("maxSpeed=\"" + veh.getMaxSpeed() + "\" ")
        if len(veh.getColor())>0:
            file.write("color=\"" + veh.getColor() + "\" ")
        if len(veh.getDepartLane())>0:
            file.write("departLane=\"" + veh.getDepartLane() + "\" ")
        if len(veh.getDepartPos())>0:
            file.write("departPos=\"" + veh.getDepartPos() + "\" ")
        if len(veh.getDepartSpeed())>0:
            file.write("departSpeed=\"" + veh.getDepartSpeed() + "\" ")
        if len(veh.getArrivalLane())>0:
            file.write("arrivalLane=\"" + veh.getArrivalLane() + "\" ")
        if len(veh.getArrivalPos())>0:
            file.write("arrivalPos=\"" + veh.getArrivalPos() + "\" ")
        if len(veh.getArrivalSpeed())>0:
            file.write("arrivalSpeed=\"" + veh.getArrivalSpeed() + "\" ")
        if len(veh.getLine())>0:
            file.write("line=\"" + veh.getLine() + "\" ")
        if len(veh.getPersonNumber())>0:
            file.write("personNumber=\"" + veh.getPersonNumber() + "\" ")
        if len(veh.getContainerNumber())>0:
            file.write("containerNumber=\"" + veh.getContainerNumber() + "\" ")
        if len(veh.getFromTaz())>0:
            file.write("fromTaz=\"" + veh.getFromTaz() + "\" ")
        if len(veh.getToTaz())>0:
            file.write("toTaz=\"" + veh.getToTaz() + "\" ")
        if len(veh.getType())>0:
            file.write("type=\"" + veh.getType() + "\" " )
        else:
            file.write("type=\"" + chooseType(veh,rule)+ "\" " )
        file.write(">\n\t\t<route edges=\"" + veh.getroutes() + "\"/>\n")
        file.write("\t</vehicle>\n")

    return


def printResult(vehicles, types):

    routes_file=open(config["routes_file"], "r")
    if os.path.isfile(config["output"]):
        os.remove(config["output"])
    file=open(config["output"], "w")

    line=routes_file.readline()
    while len(line)>0:
        if line.find("<vehicle")<0:
            file.writelines(line)
        else:
            break
        line=routes_file.readline()

    printTypes(type_list, file)
    printVehicles(vehicle_list, type_list, file)
    file.write("</routes>\n")
    file.close()

    return


if __name__ == '__main__':
    param=getConfig()
    if param.config_file is None:
        print("Parameter -c name.xml is needed")
        exit(1)
    config_file=param.config_file
    config=load_config().copy()

    if os.path.isfile(config["types_file"]):
        type_list=readTypes(config["types_file"])
    else:
        print ("Error: file " + config["types_file"] + " doesn't exists\n")
        exit(1)

    if os.path.isfile(config["routes_file"]):
        vehicle_list=readVehicles(config["routes_file"])
    else:
        print ("Error: file " + config["routes_file"] + " doesn't exists\n")
        exit(1)

    printResult(vehicle_list, type_list)




exit(0)
