#/bin/bash

CITY="alcalahenares"
NETWORK="${CITY}.net.xml"

ODMAT_VEHICLES="${CITY}.odmat.VEHICLES.xml"
ODMAT_POLICEMEN="${CITY}.odmat.POLICEMEN.xml"
ODMAT_FIREMEN="${CITY}.odmat.FIREMEN.xml"

CONF_VEHICLES="${CITY}.VEHICLES.conf"
CONF_POLICEMEN="${CITY}.POLICEMEN.conf"
CONF_FIREMEN="${CITY}.FIREMEN.conf"

OUT_CITY="${CITY}.trips.xml"

# OJO: SIN PREFIJO
od2trips -c ${CONF_VEHICLES}
echo "<!-- xxxxxxxxxxxx VEHICLES XXXXXXXXXXXXXX -->" > out.${CITY}.VEHICLES.trip
grep "trip id" alcalahenares.trip.VEHICLES.xml >> out.${CITY}.VEHICLES.trip

# OJO AL PREFIJO 1100
od2trips -c ${CONF_POLICEMEN}
echo "<!-- xxxxxxxxxxxx POLICEMEN XXXXXXXXXXXXXX -->" > out.${CITY}.POLICEMEN.trip
grep "trip id" alcalahenares.trip.POLICEMEN.xml | sed -e 's/trip id=\"/trip id=\"1100/g' >> out.${CITY}.POLICEMEN.trip

# OJO AL PREFIJO 1200
od2trips -c ${CONF_FIREMEN}
echo "<!-- xxxxxxxxxxxx FIREMEN XXXXXXXXXXXXXX -->" > out.${CITY}.FIREMEN.trip
grep "trip id" alcalahenares.trip.FIREMEN.xml | sed -e 's/trip id=\"/trip id=\"1200/g' >> out.${CITY}.FIREMEN.trip

# --------------------------------------------------------
# --------------------------------------------------------
cat out.${CITY}.POLICEMEN.trip out.${CITY}.FIREMEN.trip out.${CITY}.VEHICLES.trip | sed 's/\(.*\)\(id="[0-9]*"\).*\(depart="[0-9]*\.[0-9]*"\)\(.*\)\/>/    <trip \3 \2 \4 \/>/'  > kk
cat head.xml kk tail.xml > ${OUT_CITY}
echo "Generated ${OUT_CITY}"

# ELIMINAR FICHEROS AUXILIARES
# --------------------------------------------------------
rm kk
rm alcalahenares.trip.VEHICLES.xml alcalahenares.trip.POLICEMEN.xml alcalahenares.trip.FIREMEN.xml
rm out.${CITY}.VEHICLES.trip out.${CITY}.POLICEMEN.trip out.${CITY}.FIREMEN.trip 
