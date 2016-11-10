'''
Created on 27/09/2016

@author: Alvaro Paricio alvaro.paricio@uah.es
'''
import json
import time
import sys
import pika

# Simulation Controller
class Controller:

  # ----------------------------------------
  def __init__(self, host, exchange):
    self.id		= "Controller"
    self.strId		= "["+str(self.id)+"]"
    self.name		= "Controller"
    self.host		= host
    self.verbose	= 0

    self.broker_connection = 0
    self.project_exchange    = exchange

    # self.publish_ctrl_mq_key= "edu.uah.gist.mutraff.CTRL"
    self.publish_ctrl_mq_key= "#CTRL"
    self.publisher_channel  = 0

    print( self.strId, ": Created ", self.name )
    print( self.strId, " [host:"+host+", exchange:"+exchange+"]" )

  # ----------------------------------------
  # def __del__(self):
  # nothing

  # -----------------------------------------
  def getStrId(self):
    return self.strId

  # ----------------------------------------
  def getName(self):
    return self.name

  # ----------------------------------------
  def getHost(self):
    return self.host

  # ----------------------------------------
  def connectionsStart(self):
    out = True

    self.broker_connection = pika.BlockingConnection(pika.ConnectionParameters( host=self.host))
    self.publisher_channel = self.broker_connection.channel()
    self.publisher_channel.exchange_declare(exchange=self.project_exchange, type='topic')

    print( self.getStrId(), " comms started" )
    return out

  # ----------------------------------------
  def connectionsStop(self):
    out = True
    self.broker_connection.close();
    print( self.getStrId(), " comms stopped" )
    return out

  # -----------------------------------------
  def messageSend(self, type, fmt, msg):
      print( self.getStrId(), "p:--> [key:"+self.publish_ctrl_mq_key+"] '"+ msg+ "'" )
      sys.stdout.flush()
      fields = { 'type':type, 'format':fmt }
      self.publisher_channel.basic_publish(
        exchange=self.project_exchange, routing_key=self.publish_ctrl_mq_key,
        body=msg, properties = pika.BasicProperties( headers = fields )
	)


  # ----------------------------------------
  def mapPublish(self,mapfile):
    out = True
    args = { 'map': mapfile }
    self.messageSend( 'MAP', 'json', json.dumps(args, ensure_ascii=False) )
    return out

  # ----------------------------------------
  def incidentPublish(self, action, incName, edgeName):
    out = True
    args = { 'action': action, 'incident':incName, 'edge':edgeName }
    self.messageSend( 'INCIDENT', 'json', json.dumps(args, ensure_ascii=False) )
    return out

  # ----------------------------------------
  def edgePublish(self, edgeName, feature, value):
    out = True
    args = { 'edge':edgeName, feature:value }
    self.messageSend( 'EDGE', 'json', json.dumps(args, ensure_ascii=False) )
    return out

  # ----------------------------------------
  def globalwarnPublish(self, intensity, message):
    out = True
    args = { 'warntype':'global', 'entity':'all', 'intensity':intensity, 'message':message }
    self.messageSend( 'WARN', 'json', json.dumps(args, ensure_ascii=False) )
    return out

  # ----------------------------------------
  def edgewarnPublish(self, edgeName, intensity, message):
    out = True
    args = { 'warntype':'edge', 'entity':edgeName, 'intensity':intensity, 'message':message }
    self.messageSend( 'WARN', 'json', json.dumps(args, ensure_ascii=False) )
    return out

  # ----------------------------------------
  def verbosePublish(self, entity, level):
    out = True
    if( entity == 'Controller' ):
      self.verbose = int(level)
    args = { 'command':'verbose', 'entity':entity, 'level': level }
    self.messageSend( 'CTRL', 'json', json.dumps(args, ensure_ascii=False) )
    return out


  # ----------------------------------------
  def stopSimulation(self):
    out = True
    print( self.getStrId(), " Stop simulation" )

    # Repeat some times the STOP command
    MAX = 1
    SLEEPTIME = 1
    args = { 'command':'STOP' }
    for n in range(0, MAX):
      self.messageSend( 'CTRL', 'json', json.dumps(args, ensure_ascii=False) )
      time.sleep(SLEEPTIME)

    return out

