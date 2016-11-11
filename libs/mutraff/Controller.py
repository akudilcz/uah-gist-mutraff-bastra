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

    self.subscriber_mq_keys_TWM= [ "#TWM" ]
    self.subscriber_channel  = 0

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

    # Publisher channels
    self.publisher_channel = self.broker_connection.channel()
    self.publisher_channel.exchange_declare(exchange=self.project_exchange, type='topic')

    # Subscriber channels
    self.subscriber_channel = self.broker_connection.channel()
    self.subscriber_channel.exchange_declare(exchange=self.project_exchange, type='topic')

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

  # ==========================================================================
  # ASYNCHRONOUS LOOP
  def asynchReceptionLoop(self):
  # ==========================================================================
    out = True
    print( self.getStrId(), "r:entering asynch reception loop" )

    # -- Subscribe to the ROUTING messages queue
    queue_TWM = "TWM-"+str(self.id)
    result = self.subscriber_channel.queue_declare(queue=queue_TWM,exclusive=True)
    for binding_key in self.subscriber_mq_keys_TWM:
      print( self.getStrId(), "r:Listening at queue [exchange:"+self.project_exchange+", key:"+binding_key+", queue:"+queue_TWM+"]" )
      self.subscriber_channel.queue_bind(exchange=self.project_exchange, queue=queue_TWM, routing_key=binding_key
        )

    sys.stdout.flush()

    # -----------------------------------------
    # Inline callback for messages commands
    # -----------------------------------------
    def TWM_rxCallbackback(ch, method, props, body):
      msg = body.decode("utf-8")
      print( self.getStrId(), "r:<-- [TWM][key:"+method.routing_key+"] "+msg)
      if( False ):
        print( self.getStrId(), "METHOD:", method)
        print( self.getStrId(), "CH:", ch)
        print( self.getStrId(), "PROPS:", props)

        if( props.headers['format'] ):
          if( props.headers['format'] == 'json' ):
            jmsg = json.loads(msg)
            print( self.getStrId(), "RECEIVED:", msg )
          elif( props.headers['format'] == 'TWM_fmt' ):
          # if( method.routing_key == "#TWM" ):
            jdata = json.loads(msg)
            twm_data = eval(jdata['map'])
            print( self.getStrId(), "MAP RECEIVED:", twm_data )
          else:
            print( self.getStrId(), "UNDEF FMT RECEIVED:", msg )
        else:
          print( self.getStrId(), "NO FMT RECEIVED:", msg )

      # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      # INCLUDE HERE YOUR MESSAGE PARSING AND REACTION CODE !!!!
      # INCLUDE HERE YOUR MESSAGE PARSING AND REACTION CODE !!!!
      # INCLUDE HERE YOUR MESSAGE PARSING AND REACTION CODE !!!!
      # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      sys.stdout.flush()
      return True

    # -----------------------------------------
    self.subscriber_channel.basic_consume(TWM_rxCallbackback, queue=queue_TWM, no_ack=True)

    try:
      self.subscriber_channel.start_consuming()
    except Exception as e:
      print(self.getStrId(), "ERROR: error receiving messages: "+ str(e))

    print( self.getStrId(), "r:leaving reception loop" )
    return out

  # ==========================================================================
  def listenChannels(self):
    # This MUST be launched in a different thread
    thread.start_new_thread( self.asynchReceptionLoop, ());

