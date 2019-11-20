# Using MAPS coordinates and images

## How to get a valid PNG for map.

Go to the page: www.openstreetmap.org and introduce your LAT-LONG coordinates here. You will receive a map view.
To close-up, render to PNG opening the "share" button in the right side, and the image format you need.
You will find the necessary lat,long cooridnates in the OSM map files and/or in the SUMO .net file.
For instance, for Alcala de Henares you will find:
```
<bounds minlat="40.462099" minlon="-3.4088516" maxlat="40.5187581" maxlon="-3.3123779"/>
```

Alternatively, you can open the openstreetmap to get a valid cookie (token) that enables a direct https request for the map you need.

Initial request:
> https://www.openstreetmap.org/#map=15/40.5065/-3.6990

Later requests:
> https://render.openstreetmap.org/cgi-bin/export?bbox=MINLONG,MINLAT,MAXLONG,MAXLAT&scale=13157&format=png

> Las Tablas:
> https://render.openstreetmap.org/cgi-bin/export?bbox=-3.708271980285645,40.493828843512766,-3.6790895462036137,40.51918229003526&scale=13157&format=png

> Barrio Salamanca:
> https://render.openstreetmap.org/cgi-bin/export?bbox=-3.6907196,40.4200307,-3.6689186,40.4389778&scale=13157&format=png

> Retiro:
> https://render.openstreetmap.org/cgi-bin/export?bbox=-3.691492,40.4204881,-3.679862,40.4258134&scale=13157&format=png

> Alcala de Henares:
> https://render.openstreetmap.org/cgi-bin/export?bbox=-3.4088516,40.462099,-3.3123779,40.5187581&scale=13160&format=png
> A mayor resolucion:
>  https://render.openstreetmap.org/cgi-bin/export?bbox=-3.4088516,40.462099,-3.3123779,40.5187581&scale=6580&format=png
> https://render.openstreetmap.org/cgi-bin/export?bbox=-3.4088516,40.462099,-3.3123779,40.5187581&scale=6580&format=png

## Where you should put the map
The received maps must have the city map name for the MuTraff platform, and must be saved at [MUTRAFF_HOME]/scenes/TEMPLATES/cities/[CITY_MAP]/images/[CITY_MAP].png
