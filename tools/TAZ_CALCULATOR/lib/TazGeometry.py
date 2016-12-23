# ----------------------------------------------------------------
# Author: Alvaro Paricio Garcia, alvaro.paricio@uah.es
# TAZ CALCULATION BASED ON THE RAY CASTING ALGORYTHM
# FROM : http://rosettacode.org/wiki/Ray-casting_algorithm#Python
# ----------------------------------------------------------------
from collections import namedtuple
from collections import defaultdict
from pprint import pprint as pp
import sys
import os.path
from lxml import etree
import pandas as pd
 
TazPt      = namedtuple('TazPt', 'x, y')               # Point
TazEdge    = namedtuple('TazEdge', 'a, b')           # Taz edge from a to b
TazPolygon = namedtuple('TazPolygon', 'name, edges')    # TazPolygon
 
_eps = 0.00001
_huge = sys.float_info.max
_tiny = sys.float_info.min
 
# ===================================================================
def error( code, text ):
   print("ERROR: "+text)
   sys.exit(code)
 
# ===================================================================
# PART 1: ALGORITHM
# ===================================================================
def rayintersectseg(p, edge):
    ''' takes a point p=TazPt() and an edge of two endpoints a,b=TazPt() of a line segment returns boolean
    '''
    a,b = edge
    if a.y > b.y:
        a,b = b,a
    if p.y == a.y or p.y == b.y:
        p = TazPt(p.x, p.y + _eps)
 
    intersect = False
 
    if (p.y > b.y or p.y < a.y) or (
        p.x > max(a.x, b.x)):
        return False
 
    if p.x < min(a.x, b.x):
        intersect = True
    else:
        if abs(a.x - b.x) > _tiny:
            m_red = (b.y - a.y) / float(b.x - a.x)
        else:
            m_red = _huge
        if abs(a.x - p.x) > _tiny:
            m_blue = (p.y - a.y) / float(p.x - a.x)
        else:
            m_blue = _huge
        intersect = m_blue >= m_red
    return intersect
 
def _odd(x): return x%2 == 1
 
def taz_contains_pt(tazpoly, pt):
    ln = len(tazpoly)
    return _odd(sum(rayintersectseg(pt, edge)
                    for edge in tazpoly.edges ))
 
def taz_pp(tazpoly):
    print ("\n  TazPolygon(name='%s', edges=(" % tazpoly.name)
    print ('   ', ',\n    '.join(str(e) for e in tazpoly.edges) + '\n    ))')

def taz_test():
    Tazs = [
      TazPolygon(name='square', edges=(
        TazEdge(a=TazPt(x=0, y=0), b=TazPt(x=10, y=0)),
        TazEdge(a=TazPt(x=10, y=0), b=TazPt(x=10, y=10)),
        TazEdge(a=TazPt(x=10, y=10), b=TazPt(x=0, y=10)),
        TazEdge(a=TazPt(x=0, y=10), b=TazPt(x=0, y=0))
        )),
      TazPolygon(name='square_hole', edges=(
        TazEdge(a=TazPt(x=0, y=0), b=TazPt(x=10, y=0)),
        TazEdge(a=TazPt(x=10, y=0), b=TazPt(x=10, y=10)),
        TazEdge(a=TazPt(x=10, y=10), b=TazPt(x=0, y=10)),
        TazEdge(a=TazPt(x=0, y=10), b=TazPt(x=0, y=0)),
        TazEdge(a=TazPt(x=2.5, y=2.5), b=TazPt(x=7.5, y=2.5)),
        TazEdge(a=TazPt(x=7.5, y=2.5), b=TazPt(x=7.5, y=7.5)),
        TazEdge(a=TazPt(x=7.5, y=7.5), b=TazPt(x=2.5, y=7.5)),
        TazEdge(a=TazPt(x=2.5, y=7.5), b=TazPt(x=2.5, y=2.5))
        )),
      TazPolygon(name='strange', edges=(
        TazEdge(a=TazPt(x=0, y=0), b=TazPt(x=2.5, y=2.5)),
        TazEdge(a=TazPt(x=2.5, y=2.5), b=TazPt(x=0, y=10)),
        TazEdge(a=TazPt(x=0, y=10), b=TazPt(x=2.5, y=7.5)),
        TazEdge(a=TazPt(x=2.5, y=7.5), b=TazPt(x=7.5, y=7.5)),
        TazEdge(a=TazPt(x=7.5, y=7.5), b=TazPt(x=10, y=10)),
        TazEdge(a=TazPt(x=10, y=10), b=TazPt(x=10, y=0)),
        TazEdge(a=TazPt(x=10, y=0), b=TazPt(x=2.5, y=2.5))
        )),
      TazPolygon(name='exagon', edges=(
        TazEdge(a=TazPt(x=3, y=0), b=TazPt(x=7, y=0)),
        TazEdge(a=TazPt(x=7, y=0), b=TazPt(x=10, y=5)),
        TazEdge(a=TazPt(x=10, y=5), b=TazPt(x=7, y=10)),
        TazEdge(a=TazPt(x=7, y=10), b=TazPt(x=3, y=10)),
        TazEdge(a=TazPt(x=3, y=10), b=TazPt(x=0, y=5)),
        TazEdge(a=TazPt(x=0, y=5), b=TazPt(x=3, y=0))
        )),
      ]
    testpoints = (TazPt(x=5, y=5), TazPt(x=5, y=8),
                  TazPt(x=-10, y=5), TazPt(x=0, y=5),
                  TazPt(x=10, y=5), TazPt(x=8, y=5),
                  TazPt(x=10, y=10))
 
    print ("\n TESTING WHETHER POINTS ARE WITHIN POLYGONS")
    for taz in Tazs:
        taz_pp(taz)
        print('   \t'.join("%s: %s" % (p, taz_contains_pt(taz, p))
                               for p in testpoints[:3]))
        print('   \t'.join("%s: %s" % (p, taz_contains_pt(taz, p))
                               for p in testpoints[3:6]))
        print('   \t'.join("%s: %s" % (p, taz_contains_pt(taz, p))
                               for p in testpoints[6:]))

# ===================================================================
# PART 2: ALGEBRA
# ===================================================================
class MuTazCalculator:

  # -----------------------------------------------
  def __init__(self,opts):
    self.opts = opts
    self.nodes = []
    self.edges = {}
    self.net = []
    self.mutazs = []
    self.flag_create_dataframes = False
    self.geometry = {}
    self.geo_nodes = {}
    self.verbose = opts['verbose']

  # -----------------------------------------------
  def vprint(self,txt):
    if( self.verbose ):
      print( txt )

  # -----------------------------------------------
  def loadNodes(self,file):
    self.vprint( "Start parsing nodes file" );

    root = {}
    n=0
    try:
      tree=etree.parse(file)
      root=tree.getroot()
    except:
      error(2,"Parsing "+file+" file. Exception: "+str(sys.exc_info()) )

    if self.flag_create_dataframes:
        # Two steps parsings: row count + row fill
        n=0
        for elem in root.iter():
          try:
            if( elem.tag ):
              if ( elem.tag == 'node' ):
                n += 1
          except:
            error(3,"Error parsing XML tree. Exception: "+str(sys.exc_info()))

        self.vprint( "Detected "+str(n)+" nodes" );
        self.nodes = pd.DataFrame(index=np.arange(n), columns=['id','x','y','type'] )
        
    n=0
    for elem in root.iter():
      try:
        if( elem.tag ):
          if ( elem.tag == 'node' ):
            if self.flag_create_dataframes:
                self.nodes.loc[n]=[elem.attrib['id'],elem.attrib['x'],elem.attrib['y'],elem.attrib['type']]
                n += 1
            self.geo_nodes[elem.attrib['id']]={}
            self.geo_nodes[elem.attrib['id']]['pt'] = TazPt(x=float(elem.attrib['x']),y=float(elem.attrib['y']))
      except:
        error(3,"Error parsing XML tree. Exception: "+str(sys.exc_info()))

    # if self.flag_create_dataframes:
    #    print( self.geo_nodes )
    self.vprint( "End parsing nodes file" );


  # -----------------------------------------------
  def loadEdges(self,file):
    self.vprint( "Start parsing edges file" );
    root = {}
    try:
      tree=etree.parse(file)
      root=tree.getroot()
    except:
      error(2,"Parsing "+file+" file. Exception: "+str(sys.exc_info()) )

    if self.flag_create_dataframes:
        # Two steps parsings: row count + row fill
        n=0
        for elem in root.iter():
          try:
            if( elem.tag ):
              if ( elem.tag == 'edge' ):
                n += 1
          except:
            error(3,"Error parsing XML tree. Exception: "+str(sys.exc_info()))

        self.vprint( "Detected "+str(n)+" edges" );
        self.edges = pd.DataFrame(index=np.arange(n),
                              columns=['id','from','to','prio','type','numLanes','speed'] )
    n=0
    for elem in root.iter():
      try:
        if( elem.tag ):
          if ( elem.tag == 'edge' ):
            if self.flag_create_dataframes:
                self.edges.loc[n]=[elem.attrib['id'],elem.attrib['from'],elem.attrib['to'],
                                   elem.attrib['priority'],elem.attrib['type'],
                                   elem.attrib['numLanes'],elem.attrib['speed']]
                n += 1
            edge_name = ''
            if 'name' in elem.attrib:
                edge_name = elem.attrib['name'].encode('utf8')
            self.edges[elem.attrib['id']] ={ 'from':elem.attrib['from'],
                                             'to': elem.attrib['to'],
                                             'prio': elem.attrib['priority'],
                                             'type': elem.attrib['type'],
                                             'numLanes': elem.attrib['numLanes'],
                                             'speed': elem.attrib['speed'],
                                             'name': edge_name
                                           }
            
      except:
        error(3,"Error parsing XML tree. Exception: "+str(sys.exc_info()))

    # if self.flag_create_dataframes:
    #    print( self.edges )

    self.vprint( "End parsing edges file" );

  # -----------------------------------------------
  def loadMUTaz(self,file):
    self.vprint( "Start parsing MuTaz file" );
    root = {}
    try:
      tree = etree.parse(file)
      root=tree.getroot()
    except:
      error(2,"Parsing "+file+" file. Exception: "+str(sys.exc_info()) )

    if self.flag_create_dataframes:
        # Two steps parsings: row count + row fill
        n=0
        for elem in root.iter():
          # etree.dump(elem)
          try:
            if( elem.tag ):
              if ( elem.tag == 'vertex' ):
                n += 1
          except:
            error(3,"Error parsing XML tree. Exception: "+str(sys.exc_info()))

        self.vprint( "Detected "+str(n)+" mutazs" );
        self.mutazs = pd.DataFrame(index=np.arange(n), columns=['mutaz','vertex','x','y'] )
        
    n=0
    curr_mutaz = ''
    for elem in root.iter():
      try:
        if( elem.tag ):
          if( elem.tag == 'mutaz' ):
            # print( elem.attrib )
            curr_mutaz = elem.attrib['id']
            self.geometry[curr_mutaz] = {'contained_nodes':{},
                                         'contained_edges':{},
                                         'taz_vertices':[],
                                         'taz_edges':[],
                                         'taz_poligon': None }
          if ( elem.tag == 'vertex' ):
            # print( elem.attrib )
            if self.flag_create_dataframes:
                self.mutazs.loc[n]=[curr_mutaz,elem.attrib['id'],elem.attrib['x'],elem.attrib['y']]
                n += 1
            self.geometry[curr_mutaz]['taz_vertices'].append( TazPt(x=float(elem.attrib['x']),y=float(elem.attrib['y'])))
      except:
        error(3,"Error parsing XML tree. Exception: "+str(sys.exc_info()))
    
    # Geometry calculus
    for taz in self.geometry:
        for n in range(0,len(self.geometry[taz]['taz_vertices'])-1):
            self.geometry[taz]['taz_edges'].append( TazEdge(a=self.geometry[taz]['taz_vertices'][n], b=self.geometry[taz]['taz_vertices'][n+1]) )
        self.geometry[taz]['taz_edges'].append( TazEdge(a=self.geometry[taz]['taz_vertices'][n+1], b=self.geometry[taz]['taz_vertices'][0]) )
        self.geometry[taz]['taz_poligon'] = TazPolygon(name=taz, edges=tuple(self.geometry[taz]['taz_edges']) )
    # self.vprint( self.geometry[taz]['taz_poligon'] )
    self.vprint( "End parsing MuTaz file" );

  # -----------------------------------------------------------
  def loadData(self):
    if not os.path.isfile(self.opts['in_nodes']):
      error(2,'Nodes file doesnt exist')
    if not os.path.isfile(self.opts['in_edges']):
      error(3,'Edges file doesnt exist')
    if not os.path.isfile(self.opts['in_mutaz']):
      error(3,'Taz-XML file doesnt exist')

    self.loadNodes(self.opts['in_nodes'])
    self.loadEdges(self.opts['in_edges'])
    self.loadMUTaz(self.opts['in_mutaz'])

  def calculateTazs(self):
    for taz in self.geometry:
        poly = self.geometry[taz]['taz_poligon']
        self.vprint( "******** TAZ "+taz+" ********")
        
        # STEP 1: Check which nodes are contained inside the MUTAZ polygon
        self.vprint( " NODES CONTAINED:")
        for pt in self.geo_nodes:
            if taz_contains_pt(poly, self.geo_nodes[pt]['pt']):
                self.geometry[taz]['contained_nodes'][pt] = True
                # self.vprint( "--> "+pt)
                
        for pt in self.geometry[taz]['contained_nodes']:
            if self.geometry[taz]['contained_nodes'][pt]:
                self.vprint( "--> "+pt)
                
        # STEP 2: Check which edges have both nodes included inside the MUTAZ polygon
        self.vprint( " EDGES CONTAINED (FULL/PARTIAL):")
        for edge in self.edges:
            if( self.edges[edge]['from'] in self.geometry[taz]['contained_nodes'] ):
                if( self.edges[edge]['to'] in self.geometry[taz]['contained_nodes'] ):
                    self.geometry[taz]['contained_edges'][edge] = True
                    self.vprint( "--> FULL: "+edge)
                else:
                    self.vprint( "--> PARTIAL (not included): "+edge)

  def dumpTazFile_v1(self):
    disclaimer='<!-- Generated by mutraff_tazcalc. alvaro.paricio@uah.es -->'
    if 'out_sumo_taz' in self.opts and self.opts['out_sumo_taz']:
	outF = open(self.opts['out_sumo_taz'], 'w')
	outF.write( disclaimer+'\n' )
	outF.write( '  -->\n')
        outF.write( '<tazs>\n')
	n = int(self.opts['taz_id_seed'])
        for taz in self.geometry:
            outF.write( '  <taz id="'+str(n)+'"><!-- name="'+taz+'" -->\n')
            weight=1/len(self.geometry[taz]['contained_edges'])
            for edge in self.geometry[taz]['contained_edges']:
                outF.write( '    <!-- name="'+self.edges[edge]['name']+'" -->\n')
                outF.write( '    <tazSource id="'+edge+'" weight="'+str(weight)+'"/>\n')
                outF.write( '    <tazSink id="'+edge+'" weight="'+str(weight)+'"/>\n')
            outF.write( '  </taz>\n')
	    n += 1
        outF.write( '</tazs>\n')
	outF.close()
	print("Generated file: "+self.opts['out_sumo_taz'] )
    else:
	print( disclaimer )
        print( '<tazs>')
        for taz in self.geometry:
            print( '  <taz id="'+taz+'">')
            weight=1/len(self.geometry[taz]['contained_edges'])
            for edge in self.geometry[taz]['contained_edges']:
                print( '    <!-- name="'+self.edges[edge]['name']+'" -->')
                print( '    <tazSource id="'+edge+'" weight="'+str(weight)+'">')
                print( '    <tazSink id="'+edge+'" weight="'+str(weight)+'">')
            print( '  </taz>')
        print( '</tazs>')


  def dumpTazFile(self):
    disclaimer='<!-- Generated by mutraff_tazcalc. alvaro.paricio@uah.es -->'
    n = int(self.opts['taz_id_seed'])
    if 'out_sumo_taz' in self.opts and self.opts['out_sumo_taz']:
	outF = open(self.opts['out_sumo_taz'], 'w')
	outF.write( disclaimer+'\n' )
	outF.write( '  -->\n')
        outF.write( '<tazs>\n')
        for taz in self.geometry:
	    edges = ' '.join(self.geometry[taz]['contained_edges'].keys())
            outF.write( '  <!-- name="'+taz+'" -->\n')
            outF.write( '  <taz id="'+str(n)+'" edges="' + edges + '" />\n' )
	    n += 1
        outF.write( '</tazs>\n')
	outF.close()
	print("Generated file: "+self.opts['out_sumo_taz'] )
    else:
	print( disclaimer )
        print( '<tazs>')
        for taz in self.geometry:
	    edges = ' '.join(self.geometry[taz]['contained_edges'].keys())
            print( '  <!-- name="'+taz+'" -->')
            print( '  <taz id="'+str(n)+'" edges="' + edges + '" />\n' )
        print( '</tazs>')

