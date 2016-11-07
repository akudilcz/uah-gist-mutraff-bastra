'''
Created on 27/09/2016

@author: Alvaro Paricio alvaro.paricio@uah.es
'''
try:    
  import thread 
except ImportError:
  import _thread as thread #Py3K changed it.
import re
import time
import numpy as np
import sys
import pika
from mutraffLib import MessageCounter

# Traffic Operations Center
class TrafficCenter:

  # -----------------------------------------
  def __init__(self, id, name, host, exchange):
    self.id    = id
    self.strId = "["+str(id)+"]"
    self.name  = name
    self.host  = host
    self.msg_counter = MessageCounter.MessageCounter(id)

    # Frecuency for publishing maps
    self.map_publish_frecuency = 60

    # If we want to limit number of publications (epochs)
    # <0 = unlimited
    self.map_publish_epochs = -1

    self.broker_connection = 0
    self.project_exchange    = exchange

    # I haven't fond yet why this routing is not working. TO BE SOLVED !!!
    # self.publish_maps_mq_key= "edu.uah.gist.mutraff.TWM"
    self.publish_maps_mq_key= "#TWM"
    self.publisher_channel  = 0

    self.subscriber_channel  = 0
    self.subscriber_mq_keys_VROU= [ "#VROU" ]
    self.subscriber_mq_keys_CTRL= [ "#CTRL" ]

    # ----------
    # Just for testing purposes: listen my own messages ...
    # self.subscriber_mq_keys_VROU= [ "#" ]
    # ----------

    print(self.strId, " Created ", name )
    print(self.strId, " [host:"+host+", exchange:"+exchange+"]" )

  # -----------------------------------------
  def getStrId(self):
    return self.strId

  # -----------------------------------------
  def getMapPublishFrecuency(self):
    return self.map_publish_frecuency

  # -----------------------------------------
  def setMapPublishFrecuency(self, freq):
    self.map_publish_frecuency = freq
    return self.map_publish_frecuency

  # -----------------------------------------
  def getMapPublishEpochs(self):
    return self.map_publish_epochs

  # -----------------------------------------
  def setMapPublishEpochs(self, num_epochs):
    self.map_publish_epochs = num_epochs
    return self.map_publish_epochs

  # -----------------------------------------
  def decrMapPublishEpochs(self):
    if( self.map_publish_epochs > 0 ):
      self.map_publish_epochs -= 1
    return self.map_publish_epochs

  # -----------------------------------------
  def getName(self):
    return self.name

  # -----------------------------------------
  def getHost(self):
    return self.host

  # -----------------------------------------
  def connectionsStart(self):
    out = True

    self.broker_connection = pika.BlockingConnection(pika.ConnectionParameters( host=self.host))

    # Publisher channels
    self.publisher_channel = self.broker_connection.channel()
    self.publisher_channel.exchange_declare(exchange=self.project_exchange, type='topic')

    # Subscriber channels
    self.subscriber_channel = self.broker_connection.channel()
    self.subscriber_channel.exchange_declare(exchange=self.project_exchange, type='topic')

    print( self.getStrId(), " comms started" )
    return out

  # -----------------------------------------
  def connectionsStop(self):
    out = True
    self.broker_connection.close();
    print( self.getStrId(), " comms stopped" )
    return out

  # -----------------------------------------
  def terminate(self):
    self.subscriber_channel.stop_consuming()

  # -----------------------------------------
  def messageSend(self, msg):
      print( self.getStrId(), "p:--> [key:"+self.publish_maps_mq_key+"] '"+ msg+ "'" )
      sys.stdout.flush()
      fields = { 'type':'TWM', 'format':'TWM_fmt' }
      self.publisher_channel.basic_publish(
        exchange=self.project_exchange, routing_key=self.publish_maps_mq_key,
        body=msg, properties = pika.BasicProperties( headers = fields )
	)

  # -----------------------------------------
  def mapBroadcast(self, epoch, desc):
      map = np.random.rand(3,2)
      st_re = re.sub(r'\[ ', '[', str(map))
      st_re = re.sub(r'[\n| ]+', ',', st_re)
      msg =  '{"id":"' + str(self.msg_counter.getNewMessageId()) + '", "desc":"' + desc + '", "map":"' + st_re +'"}'
      self.messageSend( msg )

  # ==========================================================================
  # ASYNCHRONOUS LOOP
  # BE CAREFULL: THIS FUNCTION RUNS IN A DIFFERENT THREAD
  # ==========================================================================
  def mapsLoop(self):
  # ==========================================================================
    out = True
    print( self.getStrId(), "p:publishing maps loop" )

    epoch = self.getMapPublishEpochs()
    while( epoch != 0 ):
      self.mapBroadcast( epoch, 'TWM/Traffic Weighted Map emission ')
      time.sleep( self.getMapPublishFrecuency() )
      epoch = self.decrMapPublishEpochs();

    print( self.getStrId(), "p:leaving publishing maps loop" )
    # Exit loops to finish
    self.terminate()
    return out


  # ==========================================================================
  # SYNCHRONOUS LOOP
  def receptionLoop(self):
  # ==========================================================================
    out = True
    print( self.getStrId(), "r:entering reception loop" )

    # -- Subscribe to the ROUTING messages queue
    queue_VROU = "VROU"
    result = self.subscriber_channel.queue_declare(queue=queue_VROU,exclusive=True)
    for binding_key in self.subscriber_mq_keys_VROU:
      print( self.getStrId(), "r:Listening at queue [exchange:"+self.project_exchange+", key:"+binding_key+", queue:"+queue_VROU+"]" )
      self.subscriber_channel.queue_bind(exchange=self.project_exchange, queue=queue_VROU, routing_key=binding_key
        )

    # -- Subscribe to the ROUTING messages queue
    queue_CTRL = "CTRL"
    result = self.subscriber_channel.queue_declare(queue=queue_CTRL,exclusive=True)
    for binding_key in self.subscriber_mq_keys_CTRL:
      print( self.getStrId(), "r:Listening at queue [exchange:"+self.project_exchange+", key:"+binding_key+", queue:"+queue_CTRL+"]" )
      self.subscriber_channel.queue_bind(exchange=self.project_exchange, queue=queue_CTRL, routing_key=binding_key
        )

    sys.stdout.flush()

    # -----------------------------------------
    # Inline callback for messages commands
    # -----------------------------------------
    def VROU_rxCallbackback(ch, method, properties, body):
      print( self.getStrId(), "r:<-- [VROU][key:"+method.routing_key+"] "+str(body) )
      # print( self.getStrId(), "METHOD:", method)
      # print( self.getStrId(), "CH:", ch)
      # print( self.getStrId(), "PROPS:", properties)

      # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      # INCLUDE HERE YOUR MESSAGE PARSING AND REACTION CODE !!!!
      # INCLUDE HERE YOUR MESSAGE PARSING AND REACTION CODE !!!!
      # INCLUDE HERE YOUR MESSAGE PARSING AND REACTION CODE !!!!
      # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

      sys.stdout.flush()

    # -----------------------------------------
    # Inline callback for CTRL commands
    # -----------------------------------------
    def CTRL_rxCallbackback(ch, method, properties, body):
      print( self.getStrId(), "r:<-- [CTRL][key:"+method.routing_key+"] "+str(body) )
      print( self.getStrId(), "METHOD:", method)
      print( self.getStrId(), "CH:", ch)
      print( self.getStrId(), "PROPS:", properties)

      if( body == "STOP".encode() ):
        print( "Stopping the system" )
        self.terminate()

      # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      # INCLUDE HERE YOUR CONTROL-MGT CODE !!!!
      # INCLUDE HERE YOUR CONTROL-MGT CODE !!!!
      # INCLUDE HERE YOUR CONTROL-MGT CODE !!!!
      # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

      sys.stdout.flush()

    # -----------------------------------------
    self.subscriber_channel.basic_consume(VROU_rxCallbackback, queue=queue_VROU, no_ack=True)
    self.subscriber_channel.basic_consume(CTRL_rxCallbackback, queue=queue_CTRL, no_ack=True)

    try:
      self.subscriber_channel.start_consuming()
    except KeyboardInterrupt:
      self.terminate()

    print( self.getStrId(), "r:leaving reception loop" )
    return out

  # ==========================================================================
  # MAIN GLOBAL LOOP
  # ==========================================================================
  def mainLoop(self):
  # ==========================================================================
    out = True
    print( self.getStrId(), " entering main loop" )

    # This MUST be launched in a different thread
    thread.start_new_thread( self.mapsLoop, ());

    # Blocking loop
    self.receptionLoop();

    print( self.getStrId(), " leaving main loop" )
    return out

