DIR_MAPS='alcalahenares'
MUTAZ_FILE='alcalahenares.mutaz.xml'
MUTAZ_FILE='alcalahenares.minicentro.mutaz.xml'
MUTAZ_FILE='alcalahenares2.mutaz.xml'
MUTAZ_FILE='alcalahenares.casco-chorrilo-juande.mutaz.xml'
MUTAZ_FILE='alcalahenares_emergency.mutaz.xml'
OUT_TAZ_FILE='alcalahenares.casco-chorrilo-juande.taz.xml'
OUT_TAZ_FILE='alcalahenares_emergency.taz.xml'
set -x
python mutraff_tazcalc.py \
  -net $DIR_MAPS/alcalahenares.net.xml \
  -nod $DIR_MAPS/alcalahenares.nod.xml \
  -edg $DIR_MAPS/alcalahenares.edg.xml \
  -mutaz $DIR_MAPS/$MUTAZ_FILE \
  -i 1120010 \
  -sumo_taz $OUT_TAZ_FILE


# python mutraff_tazcalc.py -net alcalahenares.net.xml -nod alcalahenares.nod.xml -edg alcalahenares.edg.xml -mutaz alcalahenares.mutaz.xml 
