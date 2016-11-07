'''
Created on 27/09/2016

@author: Alvaro Paricio alvaro.paricio@uah.es
'''
import time
import sys
import pika

# Simulation Controller
class Controller:

  # ----------------------------------------
  def __init__(self, host, exchange):
    self.id    = "Controller"
    self.strId = "["+str(self.id)+"]"
    self.name  = "Controller"
    self.host  = host

    self.broker_connection = 0
    self.project_exchange    = exchange

    # self.publish_ctrl_mq_key= "edu.uah.gist.mutraff.CTRL"
    self.publish_ctrl_mq_key= "#CTRL"
    self.publisher_channel  = 0

    print( self.strId, ": Created ", self.name )
    print( self.strId, " [host:"+host+", exchange:"+exchange+"]" )

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
  def messageSend(self, msg):
      print( self.getStrId(), "p:--> [key:"+self.publish_ctrl_mq_key+"] '"+ msg+ "'" )
      sys.stdout.flush()
      fields = { 'type':'CTRL', 'format':'CTRL_fmt' }
      self.publisher_channel.basic_publish(
        exchange=self.project_exchange, routing_key=self.publish_ctrl_mq_key,
        body=msg, properties = pika.BasicProperties( headers = fields )
	)


  # ----------------------------------------
  def stopSimulation(self):
    out = True
    print( self.getStrId(), " Stop simulation" )

    self.connectionsStart()

	# Repeat some times the STOP command
    MAX = 3
    SLEEPTIME = 1
    for n in range(0, MAX):
      self.messageSend( 'STOP' )
      time.sleep(SLEEPTIME)

    self.connectionsStop()
    return out

