'''
Created on 27/09/2016

@author: Alvaro Paricio alvaro.paricio@uah.es
'''
try:    
  import thread 
except ImportError:
  import _thread as thread #Py3K changed it.
import json
import time
import sys
import pika

# MUTRAFF VEHICLE
class Vehicle:

  # -----------------------------------------
  def __init__(self, id, name, host, exchange):
    self.id    = id
    self.strId = "["+str(id)+"]"
    self.name  = name
    self.host  = host

    # Frecuency for publishing maps
    self.vroute_publish_frecuency = 60

    # If we want to limit number of publications (epochs)
    # <0 = unlimited
    self.vroute_publish_epochs = -1

    self.broker_connection = 0
    self.project_exchange    = exchange

    # I haven't fond yet why this routing is not working. TO BE SOLVED !!!
    # self.publish_vroutes_mq_key= "edu.uah.gist.mutraff.VROU"
    self.publish_vroutes_mq_key= "#VROU"
    self.publisher_channel  = 0

    self.subscriber_channel  = 0
    self.subscriber_mq_keys_TWM= [ "#TWM" ]
    self.subscriber_mq_keys_CTRL= [ "#CTRL" ]

    # ----------
    # Just for testing purposes: listen my own messages ...
    # self.subscriber_mq_keys_TWM= [ "#" ]
    # ----------

    print(self.strId, " Created ", name )
    print(self.strId, " [host:"+host+", exchange:"+exchange+"]" )

  # -----------------------------------------
  def getStrId(self):
    return self.strId

  # -----------------------------------------
  def getVRoutePublishFrecuency(self):
    return self.vroute_publish_frecuency

  # -----------------------------------------
  def setVRoutePublishFrecuency(self, freq):
    self.vroute_publish_frecuency = freq
    return self.vroute_publish_frecuency

  # -----------------------------------------
  def getVRoutePublishEpochs(self):
    return self.vroute_publish_epochs

  # -----------------------------------------
  def setVRoutePublishEpochs(self, num_epochs):
    self.vroute_publish_epochs = num_epochs
    return self.vroute_publish_epochs

  # -----------------------------------------
  def decrVRoutePublishEpochs(self):
    if( self.vroute_publish_epochs > 0 ):
      self.vroute_publish_epochs -= 1
    return self.vroute_publish_epochs

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
      print( self.getStrId(), "p:--> [key:"+self.publish_vroutes_mq_key+"] '"+ msg+ "'" )
      sys.stdout.flush()
      fields = { 'type':'VROU', 'format':'VROU_fmt' }
      self.publisher_channel.basic_publish(
        exchange=self.project_exchange, routing_key=self.publish_vroutes_mq_key,
        body=msg, properties = pika.BasicProperties( headers = fields )
	)

  # -----------------------------------------
  def vrouteBroadcast(self, epoch, map):
      msg = str(epoch)+":"+map
      self.messageSend( msg )

  # ==========================================================================
  # ASYNCHRONOUS LOOP
  # BE CAREFULL: THIS FUNCTION RUNS IN A DIFFERENT THREAD
  # ==========================================================================
  def mapsLoop(self):
  # ==========================================================================
    out = True
    print( self.getStrId(), "p:publishing maps loop" )

    epoch = self.getVRoutePublishEpochs()
    while( epoch != 0 ):
      self.vrouteBroadcast( epoch, 'VROU/Vehicle Route Notification')
      time.sleep( self.getVRoutePublishFrecuency() )
      epoch = self.decrVRoutePublishEpochs();

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
    queue_TWM = "TWM-"+str(self.id)
    result = self.subscriber_channel.queue_declare(queue=queue_TWM,exclusive=True)
    for binding_key in self.subscriber_mq_keys_TWM:
      print( self.getStrId(), "r:Listening at queue [exchange:"+self.project_exchange+", key:"+binding_key+", queue:"+queue_TWM+"]" )
      self.subscriber_channel.queue_bind(exchange=self.project_exchange, queue=queue_TWM, routing_key=binding_key
        )

    # -- Subscribe to the ROUTING messages queue
    queue_CTRL = "CTRL-"+str(self.id)
    result = self.subscriber_channel.queue_declare(queue=queue_CTRL,exclusive=True)
    for binding_key in self.subscriber_mq_keys_CTRL:
      print( self.getStrId(), "r:Listening at queue [exchange:"+self.project_exchange+", key:"+binding_key+", queue:"+queue_CTRL+"]" )
      self.subscriber_channel.queue_bind(exchange=self.project_exchange, queue=queue_CTRL, routing_key=binding_key
        )

    sys.stdout.flush()

    # -----------------------------------------
    # Inline callback for messages commands
    # -----------------------------------------
    def TWM_rxCallbackback(ch, method, properties, body):
      msg = body.decode("utf-8")
      print( self.getStrId(), "r:<-- [TWM][key:"+method.routing_key+"] "+msg)
      if( method.routing_key == "#TWM" ):
        jdata = json.loads(msg)
        twm_data = eval(jdata['map'])
        print( self.getStrId(), "MAP RECEIVED:", twm_data )
      else:
        print( self.getStrId(), "    INVALID MESSAGE FORMAT" )

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
    self.subscriber_channel.basic_consume(TWM_rxCallbackback, queue=queue_TWM, no_ack=True)
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

