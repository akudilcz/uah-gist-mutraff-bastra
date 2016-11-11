# --------------------
# Run Ruleset.example() to learn how it works.
#   import Rules
#   Rules.Ruleset.example()
# --------------------

# ============================================================
class RuleMatch:
# ============================================================
  def __init__(self,epoch,mode,inclass,instance,feature,value,match,rule,text):
    self.epoch = epoch
    self.mode = mode
    self.inclass = inclass
    self.instance = instance
    self.feature = feature
    self.value = value
    self.match = match
    self.rule = rule
    self.text = text

  def getEpoch(self):
    return self.epoch

  def getMode(self):
    return self.mode

  def getClass(self):
    return self.inclass

  def getInstance(self):
    return self.instance

  def getFeature(self):
    return self.feature

  def getValue(self):
    return self.value

  def getMatch(self):
    return self.match

  def getRule(self):
    return self.rule

  def getText(self):
    return self.text

  def dumpMatch(self):
      print("RULE MATCHED: {'time':{:d}, 'mode':{:s}, 'class':{:s}, 'instance':{:s}, 'feature':{:s}, 'value':{:s}, 'match':{:s}, 'rule':{:s}, 'text':{:s} }".format(
      	self.epoch,self.mode,self.inclass,self.instance,self.feature,str(self.value),self.match,self.rule,self.text) )

  @classmethod
  def dump( cls, matches ):
    for m in range(0,len(matches)):
      r = matches[m]
      r.dumpMatch()

# ============================================================
class Measure:
# ============================================================
  def __init__(self,inclass,instanceName,**values):
    self.type = inclass
    self.instance = instanceName
    self.values = {}
    if( values ):
      self.values = values.copy()

  def setValue(self, feature, value ):
    self.values[feature] = value

  def setValues(self, *hash ):
    for f in hash:
      self.values[f] = hash[f]

  def getValue(self, feature ):
    try:
      return self.value[feature]
    except:
      return None

  def getInstance(self):
    return self.instance

  def getClass(self):
    return self.type

  def getValues(self):
    return self.values

# ============================================================
class Ruleset:
# Rule format is : "x = 4 if b > 8 else 9"
# ============================================================
  theRules = {}

  # --------------------
  def __init__(self):
    self.theRules = {}

  # --------------------
  def printRules(self):
    print( self.theRules )

  # --------------------
  def addRule( self, inclass, feature, rulename, cond, text ):
    if( not inclass in self.theRules ):
      self.theRules[inclass] = {}
      self.theRules[inclass][feature] = [ { 'name': rulename, 'cond': cond, 'text':text } ]
      return
      
    if( feature in self.theRules[inclass] ):
      self.theRules[inclass][feature] += [ { 'name': rulename, 'cond': cond, 'text':text } ]
    else:
      self.theRules[inclass][feature] =  [ { 'name': rulename, 'cond': cond, 'text':text } ]
    # print( self.theRules[feature] )

  # --------------------
  def fire( self, epoch, inclass, instance, feature, value ):
    matches = []
    if( inclass in self.theRules and feature in self.theRules[inclass] ):
      for rule in self.theRules[inclass][feature]:
        # print( "--> "+ feature+": Check rule "+ rule['name'] )
        expr1 = rule['cond'].format(float(value))
        expr = "True "+expr1+" else False"
        try:
          if( eval(expr) ):
		newMatch = RuleMatch(epoch,'MATCH',inclass,instance,feature,value,expr1,rule['name'],rule['text'])
		matches += [newMatch]
		# matches += [{'time':epoch, 'class':inclass, 'instance':instance, 'rule':rule['name'], 'text':rule['text'], 'feature':feature, 'match':expr1, 'value':value }]
          # print("      {:s} ==> {:s}".format(expr1,str(out)) )
        except:
          print( "Rule syntax error at rule '"+expr1+"': ignored") 
    return matches

  # --------------------
  def fireOnMeasure( self, measure ):
    matches = []
    name = measure.getInstance()
    type = measure.getClass()
    vals = measure.getValues()

    time = 0
    if( 'time' in vals ):
      time = vals['time']

    for f in vals:
      if( f != 'time' ):
        matches += self.fire( time, type, name, f, vals[f] )
        # print( self.fire( time, type, name, f, vals[f] ) )
    return matches

  # --------------------
  @classmethod
  def example(cls):
    # ---------
    rules = Ruleset()
    rules.theRules = {
      'edge': {
        'attrib1' : [
    	  {'name':'rule-1.1', 'cond':'if {:f} < 1.5', 'text':'xxx' },
    	  {'name':'rule-1.2', 'cond':'if {:f} > 2.0', 'text':'xxx' },
	  ],
        'attrib2' : [
      	  {'name':'rule-2.1', 'cond':'if {:f} < 1.5', 'text':'xxx' },
    	  {'name':'rule-2.2', 'cond':'if {:f} > 2.0', 'text':'xxx' },
    	  {'name':'rule-2.3', 'cond':'if( {:f} < 1.5)', 'text':'xxx' },
    	  {'name':'rule-2.4', 'cond':'if( {:f} > 2.0)', 'text':'xxx' },
    	  {'name':'rule-2.5', 'cond':'if( {:f} = 3.0)', 'text':'xxx' }, # ERROR!
    	  {'name':'rule-2.6', 'cond':'if( {:f} == 3.0)', 'text':'xxx' },
    	  {'name':'rule-2.7', 'cond':'if( {:f} == 3)', 'text':'xxx' },
    	  {'name':'rule-2.8', 'cond':'if 0 < {:f} < 5', 'text':'xxx' },
    	  {'name':'rule-2.9', 'cond':'if not 0 < {:f} < 5', 'text':'xxx' },
    	  {'name':'rule-2.10', 'cond':'if {:f} in [2,4,6,8]', 'text':'xxx' },
    	  {'name':'rule-2.11', 'cond':'if not {:f} in [2,4,6,8]', 'text':'xxx' },
	  ],
        'attrib3' : [
    	  {'name':'rule-3.1', 'cond':'if {:f} < 1.5', 'text':'xxx' },
    	  {'name':'rule-3.2', 'cond':'if {:f} > 2.0', 'text':'xxx' },
	  ],
      }
    }

    # ---------
    type = 'edge'
    instance = 'edge345'
    var = 'attrib2'
    val = 3

    time = 0
    matches = rules.fire( time, type, instance, var, val )
    RuleMatch.dump( matches )
    # printMatches( matches )

    rules.addRule( type, var, 'evenNumber', 'if {:f} in [2,4,6,8]', 'Is even number' )

    time += 1
    matches = rules.fire( time, type, instance, var, 4.7 )
    RuleMatch.dump( matches )

    edge1 = Measure( 'edge', 'edge666' )
    matches = rules.fireOnMeasure( edge1 )
    RuleMatch.dump( matches )

    edge2 = Measure( 'edge', 'edge777', attrib1=3.0, attrib2=22.22, attrib3=45 )
    # edge2 = Measure( 'edge', 'edge777', **{'attrib1':3.0, 'attrib2': 22.22, 'attrib3':45} )
    matches = rules.fireOnMeasure( edge2 )
    RuleMatch.dump( matches )

    attrib1 = 3.0
    edge3 = Measure( 'TRONKO', 'tronko000', attrib1=attrib1, attrib2=22.22, attrib3=45 )
    matches = rules.fireOnMeasure( edge3 )
    RuleMatch.dump( matches )
