import pandas as pd
import os

class ExperimentCatalog:

  def __init__(self,name):
    print( "Created experiment catalog: "+name)
    self.name = name
    self.csv_file = ''
    self.experiments = {}
    self.papers = {}

  def addPaper(self,paper_ref):
    self.papers[paper_ref] = { 'experiments_id': [] }

  def getPapers(self):
    return self.papers

  def getPaperReferences( self, paper_ref ):
    if not paper_ref in self.experiments:
      return []
    return papers[paper_ref]['experiments_id']

  def addExperiments2Paper(self,paper_ref,exp_list):
    if not paper_ref in self.experiments:
      self.addPaper( paper_ref )
    self.papers[paper_ref]['experiments_id'].append( exp_list )

  def loadExperimentsFromCSV(self,csv_file):
    if not os.path.isfile(csv_file):
      print( "ERROR: file "+csv_file+" not found")
    print( "Loading experiment catalog from "+csv_file )
    self.csv_file = csv_file

    # From: https://www.quora.com/How-do-I-fix-a-Unicode-error-while-reading-a-CSV-file-with-a-pandas-library-in-Python-3-6
    data = pd.read_csv(csv_file, encoding='ISO-8859-1')
    for index, row in data.iterrows():
      # print("PUSHING: {}".format(row.to_dict) )
      self.pushExperimentAsDict( row['ID'], row.to_dict() )

  def pushExperiment(self,idx,prefix,group,label,twm,net,logit,demand,traffic,lanes,routing_algo,teleporting,twm_func,twm_size,expnum,other_features):
    self.experiments[idx] = {}
    self.experiments[idx]['FILE']		= prefix
    self.experiments[idx]['GROUP/OBJECTIVE']	= group
    self.experiments[idx]['LABEL']		= label
    self.experiments[idx]['TWM']		= twm
    self.experiments[idx]['NET']		= net
    self.experiments[idx]['LOGIT']		= logit
    self.experiments[idx]['DEMAND']		= demand
    self.experiments[idx]['TRAFFIC']		= traffic
    self.experiments[idx]['LANES']		= lanes
    self.experiments[idx]['ROUTE_ALGO']		= routing_algo
    self.experiments[idx]['TELEPORTING']	= teleporting
    self.experiments[idx]['TWM_FUNC']		= twm_func
    self.experiments[idx]['TWM_SIZE']		= twm_size
    self.experiments[idx]['EXPNUM']		= expnum
    self.experiments[idx]['SPECIAL FEATURE']	= other_features

  def pushExperimentBrief(self,idx,prefix,group,label):
    self.pushExperiment(idx,prefix,group,label,'','','','','','','','','','','','')
    
  def pushExperimentAsDict(self,idx,inDict):
    self.experiments[idx] = inDict

  def getExperiment(self,idx):
    if idx in self.experiments:
      return self.experiments[idx]
    else:
      print( "Experiment id not found")
      return None

  def getExperimentPrefix(self,idx):
    if idx in self.experiments:
      return self.experiments[idx]['FILE']
    else:
      print( "Experiment id not found")
      return 'NaN'

