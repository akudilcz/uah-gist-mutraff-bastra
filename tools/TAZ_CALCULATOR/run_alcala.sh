MUTAZ_FILE='alcalahenares.mutaz.xml'
MUTAZ_FILE='alcalahenares.minicentro.mutaz.xml'
MUTAZ_FILE='alcalahenares2.mutaz.xml'
set -x
python mutraff_tazcalc.py \
  -net alcalahenares.net.xml \
  -nod alcalahenares.nod.xml \
  -edg alcalahenares.edg.xml \
  -mutaz $MUTAZ_FILE \
  -i 1000 \
  -sumo_taz alcalahenares.taz.xml 


# python mutraff_tazcalc.py -net alcalahenares.net.xml -nod alcalahenares.nod.xml -edg alcalahenares.edg.xml -mutaz alcalahenares.mutaz.xml 
