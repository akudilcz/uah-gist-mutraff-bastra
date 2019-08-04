
import optparse
import os
import sys
import random
import numpy

from lxml import etree

class connection:

    edge=""
    node1=""
    node2=""
    def __init__(self, edge, node1, node2):
        self.edge=edge
        self.node1=node1
        self.node2=node2

    def getNode1(self):
        return self.node1
    def getNode2(self):
        return self.node2
    def getEdge(self):
        return self.edge



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
        l_config=root.findall("gmb")
        label=l_config[0].find(option)
        value=label.get("value")
    except:
        sys.exit("Configuration error: value for " + option + " in " + config_file + " not found.")

    return value

def load_config():
    dict_conf={}
    dict_conf["mode"]=readOption("mode")
    dict_conf["net_file"]=readOption("net_file")
    dict_conf["output_prefix"]=readOption("output_prefix")
    dict_conf["output_dir"]=readOption("output_dir")
    dict_conf["weight_factor"]="1"
    dict_conf["weight_factor"]=readOption("weight_factor")
    dict_conf["weight_add"]="0"
    dict_conf["weight_add"]=readOption("weight_add")
    dict_conf["num_maps"]=readOption("num_maps")
    dict_conf["begin"]=readOption("begin")
    dict_conf["end"]=readOption("end")
    dict_conf["join_map"]=readOption("join_map")
    dict_conf["join_option"]=readOption("join_option")
    dict_conf["pen_edges"]=readOption("pen_edges")
    dict_conf["steps"]=readOption(("pen_edges_steps"))

    return dict_conf


def readSumoNet(net_file):

    dict_edges={}
    tree=etree.parse(net_file)
    root=tree.getroot()
    l_edges=root.findall("edge")

    for edge in l_edges:
        if not (edge.get("function")=="internal"):
            edge_id=edge.get("id")
            lane=edge.find("lane")
            speed=lane.get("speed")
            length=lane.get("length")
            traveltime=float(length)/float(speed)
            dict_edges[edge_id]=traveltime

    return dict_edges


def generateRandom(num_maps, name):
    iter=0
    maps=[]
    while iter < num_maps:
        name_map=config["output_dir"] + name + ".rand." + str(iter+1) + ".xml"
        maps.append(genRandMap(name_map))
        iter=iter+1

    return maps


def genRandMap(file_name):

    if os.path.isfile(file_name):
        os.remove(file_name)

    weight_factor=eval(config["weight_factor"])
    weight_add=eval(config["weight_add"])

    xml_file=open(file_name, "w+")
    xml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    xml_file.write("\n")
    xml_file.write("<meandata>\n")
    xml_file.write("\t<interval begin=\"" + config["begin"] + "\" end=\""
                        + config["end"] + "\" id=\"whatever\">\n")
    for edge in dict_edges.keys():
        weight=dict_edges[edge]
        weight=weight * weight_factor + weight_add
        if weight<=0:
            print("Configuration error: weight funtion with result of 0 or less")
            exit (1)
        xml_file.write("\t\t<edge id=\"" + edge
                                   + "\" traveltime=\"" + str(weight) + "\"/>\n")
    xml_file.write("\t</interval>\n")
    xml_file.write("</meandata>\n")
    xml_file.close()

    return file_name

def generateMapR():

    file_name= config["output_dir"] + prefix + ".mapR.xml"
    if os.path.isfile(file_name):
        os.remove(file_name)
    xml_file=open(file_name, "w+")
    xml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    xml_file.write("\n")
    xml_file.write("<meandata>\n")
    xml_file.write("\t<interval begin=\"" + config["begin"] + "\" end=\""
                        + config["end"] + "\" id=\"whatever\">\n")
    for edge in dict_edges.keys():
        weight=dict_edges[edge]
        xml_file.write("\t\t<edge id=\"" + edge
                                   + "\" traveltime=\"" + str(weight) + "\"/>\n")
    xml_file.write("\t</interval>\n")
    xml_file.write("</meandata>\n")
    xml_file.close()

    return file_name


def readConnections(net_file):
    connections=[]
    tree=etree.parse(net_file)
    root=tree.getroot()
    l_edges=root.findall("edge")

    for edge in l_edges:
        if not (edge.get("function")=="internal"):
            id=edge.get("id")
            node1=edge.get("from")
            node2=edge.get("to")
            connect=connection(id, node1, node2)
            connections.append(connect)

    return connections


def generatePenEdges(edges_list):

    connections=readConnections(config["net_file"])
    for edge in edges_list:
        algo(edge, connections, int(config["steps"]))

    weight_factor=eval(config["weight_factor"])
    weight_add=eval(config["weight_add"])

    new_dict_edges={}
    for edge in new_pen_edges:
        # ALVARO: Patched on 02/06/19
        # if not new_dict_edges.has_key(edge):
        if not edge in new_dict_edges:
            weight=dict_edges[edge] * weight_factor + weight_add
            new_dict_edges[edge]=weight

    file_name=config["output_dir"] + prefix + ".pen.map.xml"
    if os.path.isfile(file_name):
        os.remove(file_name)
    xml_file=open(file_name, "w+")
    xml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    xml_file.write("\n")
    xml_file.write("<meandata>\n")
    xml_file.write("\t<interval begin=\"" + config["begin"] + "\" end=\""
                       + config["end"] + "\" id=\"whatever\">\n")
    for edge in new_dict_edges.keys():
        weight=new_dict_edges[edge]
        xml_file.write("\t\t<edge id=\"" + edge
                           + "\" traveltime=\"" + str(weight) + "\"/>\n")
    xml_file.write("\t</interval>\n")
    xml_file.write("</meandata>\n")
    xml_file.close()

    return file_name


def algo(edge, connections, dist):

    if dist==0:
        if edge not in new_pen_edges:
            new_pen_edges.append(edge)
        return
    else:
        for connect in connections:
            if connect.getEdge()==edge:
                node1=connect.getNode1()
                node2=connect.getNode2()

                for conn2 in connections:
                    if (conn2.getNode1()==node1 or conn2.getNode1()==node2) or (conn2.getNode2()==node1 or conn2.getNode2()==node2):
                        algo(conn2.getEdge(), connections, dist-1)

    return


def join(list_maps, map_file):
    index=0
    new_dict_edges={}
    for map in list_maps:
        tree=etree.parse(map)
        root=tree.getroot()
        interval=root.find("interval")
        l_edges=interval.findall("edge")

        for edge in l_edges:
            edge_id=edge.get("id")
            traveltime=float(edge.get("traveltime"))
            # ALVARO: Patched on 02/06/19
            # if not new_dict_edges.has_key(edge_id):
            if not edge_id in new_dict_edges:
                new_dict_edges[edge_id]=traveltime
            else:
                if config["join_option"]=="add":
                    new_dict_edges[edge_id]=new_dict_edges[edge_id]+traveltime
                elif config["join_option"]=="max":
                    if new_dict_edges[edge_id]< traveltime:
                        new_dict_edges[edge_id]=traveltime
                else:
                    print ("Config error: no correct option for join in " + config_file)
                    exit(1)

        tree=etree.parse(map_file)
        root=tree.getroot()
        interval=root.find("interval")
        l_edges=interval.findall("edge")

        for edge in l_edges:
            edge_id=edge.get("id")
            traveltime=float(edge.get("traveltime"))
            # ALVARO: Patched on 02/06/19
            # if not new_dict_edges.has_key(edge_id):
            if not edge_id in new_dict_edges:
                new_dict_edges[edge_id]=traveltime
            else:
                if config["join_option"]=="add":
                    new_dict_edges[edge_id]=new_dict_edges[edge_id]+traveltime
                elif config["join_option"]=="max":
                    if new_dict_edges[edge_id]< traveltime:
                        new_dict_edges[edge_id]=traveltime
                else:
                    print ("Config error: no correct option for join in " + config_file)
                    exit(1)

        file_name=config["output_dir"] + prefix + ".join_map_" + str(index+1) + ".xml"
        if os.path.isfile(file_name):
            os.remove(file_name)
        xml_file=open(file_name, "w+")
        xml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        xml_file.write("\n")
        xml_file.write("<meandata>\n")
        xml_file.write("\t<interval begin=\"" + config["begin"] + "\" end=\""
                       + config["end"] + "\" id=\"whatever\">\n")
        for edge in new_dict_edges.keys():
            weight=new_dict_edges[edge]
            xml_file.write("\t\t<edge id=\"" + edge
                           + "\" traveltime=\"" + str(weight) + "\"/>\n")
        xml_file.write("\t</interval>\n")
        xml_file.write("</meandata>\n")
        xml_file.close()
        new_dict_edges.clear()
        index=index+1


if __name__ == '__main__':

    param=getConfig()
    if param.config_file is None:
        print("Parameter -c name.xml is needed")
        exit(1)
    config_file=param.config_file
    config=load_config().copy()

    dict_edges=readSumoNet(config["net_file"])
    num_maps=int(config["num_maps"])
    prefix=config["output_prefix"]
    maps=[]
    if config["mode"]=="map_r":
        maps.append(generateMapR())
    elif config["mode"]=="random":
        maps.extend(generateRandom(num_maps, prefix))
    elif config["mode"]=="penalty":
        if len(config["pen_edges"])>0:
            str_pen_edges=config["pen_edges"]
            list_pen_edges=str_pen_edges.split(' ')
            new_pen_edges=[]
            maps.append(generatePenEdges(list_pen_edges))
        else:
            print ("Configuration error: edge for penalty mode not supplied")

    if len(config["join_map"])>0:
        if os.path.isfile(config["join_map"]):
            join(maps, config["join_map"])
        else:
            print ("Error opening map file " + config["join_map"])


exit(0)
