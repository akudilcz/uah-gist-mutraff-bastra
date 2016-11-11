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
# import numpy as np
import sys
import pika
import json
from mutraff    import MessageCounter
from mutraff	import Ruleset as Rules
from mutraffSim import MutraffSimulator

TR_ERROR	= -1
TR_ALWAYS	= 0
TR_INFO		= 1
TR_COMMS	= 2
TR_DEBUG	= 5
TR_MAX	= 10

# Traffic Operations Center
class TrafficCenter:

  # -----------------------------------------
  def __init__(self, args):
    self.status		= "ALIVE"
    self.id		= args['amqp_toc_id']
    self.strId		= "["+str(self.id)+"]"
    self.name		= args['amqp_toc_name']
    self.host		= args['amqp_host']
    self.verbose	= args['verbose']
    self.conf		= args
    self.msg_counter = MessageCounter.MessageCounter(self.id)
    self.simulator	= None

    # Frecuency for publishing maps
    self.map_publish_frecuency = 60

    # If we want to limit number of publications (epochs)
    # <0 = unlimited
    self.map_publish_epochs = -1

    self.broker_connection = 0
    self.project_exchange    = args['amqp_exchange_name']

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

    self.trace(TR_ALWAYS, " Created ", self.name )
    self.trace(TR_DEBUG, " [host:"+self.host+", exchange:"+self.project_exchange+"]" )

  # -----------------------------------------
  def isAlive(self):
    return (self.status == "ALIVE")

  # -----------------------------------------
  def trace(self, level, *args):
    if( level <= self.verbose ):
      if( level == TR_ERROR ):
        print('{:s}: ERROR: '.format(self.strId)+ ' '.join(args) )
      else:
        print('{:s}: '.format(self.strId)+ ' '.join(args) )

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

    self.trace(TR_COMMS, " comms started" )
    return out

  # -----------------------------------------
  def connectionsStop(self):
    out = True
    self.broker_connection.close();
    self.trace(TR_COMMS, " comms stopped" )
    return out

  # -----------------------------------------
  def terminate(self):
    self.subscriber_channel.stop_consuming()
    self.status = "TO_DIE"

  # -----------------------------------------
  def messageSend(self, msg):
      self.trace(TR_COMMS, "p:--> [key:"+self.publish_maps_mq_key+"] '"+ msg+ "'" )
      sys.stdout.flush()
      fields = { 'type':'TWM', 'format':'TWM_fmt' }
      self.publisher_channel.basic_publish(
        exchange=self.project_exchange, routing_key=self.publish_maps_mq_key,
        body=msg, properties = pika.BasicProperties( headers = fields )
	)

  # -----------------------------------------
  def mapBroadcast(self, epoch, desc):
#      map = np.random.rand(3,2)
#      st_re = re.sub(r'\[ ', '[', str(map))
#      st_re = re.sub(r'[\n| ]+', ',', st_re)
#      msg =  '{"id":"' + str(self.msg_counter.getNewMessageId()) + '", "desc":"' + desc + '", "map":"' + st_re +'"}'
#      self.messageSend( msg )
     return

  # ==========================================================================
  # SYNCHRONOUS LOOP
  # ==========================================================================
  def mainLoopTOC(self):
  # ==========================================================================
    out = True
    self.trace(TR_COMMS, "p:publishing maps loop" )

    epoch = self.getMapPublishEpochs()
    while( self.isAlive() and (epoch != 0) ):
      self.mapBroadcast( epoch, 'TWM/Traffic Weighted Map emission ')
      time.sleep( self.getMapPublishFrecuency() )
      epoch = self.decrMapPublishEpochs();

    self.trace(TR_COMMS, "p:leaving publishing maps loop" )
    # Exit loops to finish
    self.terminate()
    return out


  # ==========================================================================
  # ASYNCHRONOUS LOOP
  # BE CAREFULL: THIS FUNCTION RUNS IN A DIFFERENT THREAD
  def asynchReceptionLoop(self):
  # ==========================================================================
    out = True
    self.trace(TR_COMMS, "r:entering reception loop" )

    # -- Subscribe to the ROUTING messages queue
    queue_VROU = "VROU"
    result = self.subscriber_channel.queue_declare(queue=queue_VROU,exclusive=True)
    for binding_key in self.subscriber_mq_keys_VROU:
      self.trace(TR_COMMS, "r:Listening at queue [exchange:"+self.project_exchange+", key:"+binding_key+", queue:"+queue_VROU+"]" )
      self.subscriber_channel.queue_bind(exchange=self.project_exchange, queue=queue_VROU, routing_key=binding_key
        )

    # -- Subscribe to the ROUTING messages queue
    queue_CTRL = "CTRL"
    result = self.subscriber_channel.queue_declare(queue=queue_CTRL,exclusive=True)
    for binding_key in self.subscriber_mq_keys_CTRL:
      self.trace(TR_COMMS, "r:Listening at queue [exchange:"+self.project_exchange+", key:"+binding_key+", queue:"+queue_CTRL+"]" )
      self.subscriber_channel.queue_bind(exchange=self.project_exchange, queue=queue_CTRL, routing_key=binding_key
        )

    sys.stdout.flush()

    # -----------------------------------------
    # Inline callback for messages commands
    # -----------------------------------------
    def VROU_rxCallbackback(ch, method, props, body):
      self.trace(TR_COMMS, "r:<-- [VROU][key:"+method.routing_key+"] "+str(body) )
      self.trace(TR_COMMS, "METHOD:", str(method))
      self.trace(TR_COMMS, "CH:", str(ch))
      self.trace(TR_COMMS, "PROPS:", str(props))

      # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      # INCLUDE HERE YOUR MESSAGE PARSING AND REACTION CODE !!!!
      # INCLUDE HERE YOUR MESSAGE PARSING AND REACTION CODE !!!!
      # INCLUDE HERE YOUR MESSAGE PARSING AND REACTION CODE !!!!
      # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

      sys.stdout.flush()

    # -----------------------------------------
    # Inline callback for CTRL commands
    # -----------------------------------------
    def CTRL_rxCallbackback(ch, method, props, body):
      msg = body.decode("utf-8")
      self.trace(TR_COMMS, "r:<-- [CTRL][key:"+method.routing_key+"] "+msg)
      self.trace(TR_COMMS, "   METHOD:", str(method))
      self.trace(TR_COMMS, "   CH:", str(ch))
      self.trace(TR_COMMS, "   PROPS:", str(props))

      if( props.headers['format'] == 'json' ):
        jmsg = json.loads(msg)

      # -----------------------------------------------
      # CTRL commands
      # -----------------------------------------------
      if( props.headers['type'] == 'CTRL' ):
        if( jmsg['command'] == 'STOP' ):
          self.trace(TR_ALWAYS, "Stopping the system" )
          self.terminate()
        if( jmsg['command'] == 'verbose' ):
          self.verbose = int(jmsg['level'])
          self.trace(TR_INFO, "Set verbose level to", str(self.verbose) )

      # -----------------------------------------------
      # WARN commands
      # -----------------------------------------------
      if( props.headers['type'] == 'WARN' ):
          self.trace(TR_INFO, "=== WARN MESSAGE === ", "scope:", jmsg['entity'], "--> ", jmsg['level'] )

      # -----------------------------------------------
      # EDGE commands
      # -----------------------------------------------
      if( props.headers['type'] == 'EDGE' ):
          self.trace(TR_INFO, "=== EDGE COMMAND === ", msg )

      # -----------------------------------------------
      # INCIDENT commands
      # -----------------------------------------------
      if( props.headers['type'] == 'INCIDENT' ):
          self.trace(TR_INFO, "=== INCIDENT RECEIVED === ", msg )

      # -----------------------------------------------
      # MAP commands
      # -----------------------------------------------
      if( props.headers['type'] == 'MAP' ):
          self.trace(TR_INFO, "=== MAP RECONFIGURATION === ", msg )

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

    self.trace(TR_COMMS, "r:leaving reception loop" )
    return out

  # ==========================================================================
  # SYNCHRONOUS LOOP
  # ==========================================================================
  def mainLoopSimulator(self):
  # ==========================================================================
    out = True

    self.simulator = MutraffSimulator.MutraffSimulator( self.conf )
    
    if( not self.simulator.commandScheduleReadfile( self.conf["commands_file"] )):
      self.trace(TR_ERROR, "Cannot read commands file", self.conf["commands_file"] )

    err = self.simulator.start()
    if( err['errCode'] != 0 ):
      self.trace(TR_ERROR, str(err) )
      return False

    while( self.simulator.notFinished() ):
      # Important: do nothing before preStep in the Loop
      self.simulator.preStep()

      # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      # If we have to alter simulation behaviour, it SHOULD BE DONE HERE
      # If we have to alter simulation behaviour, it SHOULD BE DONE HERE
      # If we have to alter simulation behaviour, it SHOULD BE DONE HERE
      # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

      alerts = self.simulator.doSimulationStep()
      if( alerts ):
        for n in range(0,len(alerts)):
	  a = alerts[n]
	  print("{:d} ==> ALERT: {:s}/{:s}: {:s} ".format(a.getEpoch(), a.getClass(), a.getInstance(), a.getText()) )
      # Important: do nothing after doSimulationStep inside this loop
      # -- end of simulation loop ------------------------------

    self.simulator.stop()

    return out


  # ==========================================================================
  # MAIN GLOBAL LOOP
  # ==========================================================================
  def mainLoop(self):
  # ==========================================================================
    out = True
    self.trace(TR_DEBUG, " entering main loop" )

    # This MUST be launched in a different thread
    thread.start_new_thread( self.asynchReceptionLoop, ());

    # Blocking sinchronous loop
    if( self.conf['exec_mode'] == 'SIMULATION' ):
      self.mainLoopSimulator()
    elif( self.conf['exec_mode'] == 'STANDARD' ):
      self.mainLoopTOC();
    else:
      self.trace(TR_ALWAYS, "Unknown execution mode", self.conf['exec_mode'] )

    self.trace(TR_DEBUG, " leaving main loop" )
    return out

