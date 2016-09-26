# randomVehType : Demand generator for vehicle types

RandomVehType.py takes a definition file of vehicles and routes (with ".rou.xml" extension) without set types and assign vehicles types randomly (defined in another file).
Distribution responds responding to a ratio defined as "weights" of each type.

Call the program from the command line with:
```
$ randomVehType.py -c<configFile>
```
 
## Usage

 When starting the program, it expects to receive as parameter the name of a file in XML format, very simple that contains the application settings.

## Configuration File
```
<?xml version="1.0" encoding="UTF-8"?>

<!-- generated on 08/15/16 09:09:57 by SUMO duarouter Version 0.23.0
<?xml version="1.0" encoding="UTF-8"?>
<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/duarouterConfiguration.xsd">
    <input>
        <net-file value="grid.net.xml"/>
        <trip-files value="grid.trip.xml"/>
    </input>
    <output>
        <output-file value="grid.rou.xml"/>
    </output>
    <processing>
        <remove-loops value="true"/>
    </processing>
    <time>
        <begin value="0"/>
        <end value="1000"/>
    </time>
</configuration>
-->

<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">
	<vType id="motorcycle" vClass="motorcycle" />
	<vType id="car" vClass="passenger" />
	<vehicle id="2304" depart="0.19" departLane="best" departSpeed="0.00" fromTaz="99" toTaz="99" type="car" >
		<route edges="1/11to2/11 2/11to3/11 3/11to4/11 4/11to5/11 5/11to6/11 6/11to7/11 7/11to8/11 8/11to9/11 9/11to10/11 10/11to10/10 10/10to10/9 10/9to10/8 10/8to10/7 10/7to10/6 10/6to10/5 10/5to10/4 10/4to10/3 10/3to11/3 11/3to12/3"/>
	[...]
	</vehicle>
	<vehicle id="3126" depart="0.38" departLane="best" departSpeed="0.00" fromTaz="99" toTaz="99" type="motorcycle" >
		<route edges="bottom7to7/0 7/0to8/0 8/0to9/0 9/0to10/0 10/0to10/1 10/1to10/2 10/2to10/3 10/3to10/4 10/4to10/5 10/5to10/6 10/6to10/7 10/7to10/8 10/8to10/9 10/9to10/10"/>
	</vehicle>
</routes>
```

* The <config> indicates the start of the configuration options.
* The label <randvt> indicates that from this point the specific settings for the program are defined randVehType.py.
* the <route_file> stores the value of the location of the file paths that we will use as a data source.
* thetag <type_file> stores the location of the file type definition. Explore the contents of this file below.
* The <output> stores the location and file name exit routes, which will already type mapping vehicles.
  
The content of file types <type_file>in xml format is a standard type definition according its semantics in SUMO to which attribute (adds weight to specify the relative probability that the vehicles defined in traffic demand<route-file>)belong to each type.
We should note that, unlike how the label is named in SUMO(<vtype>),this type definition uses the <type>.The <vTypes> is used to encompass all defined types.

A list of available attributes (besides the aforementioned weight)can be found in the "Types" section previously discussed in the chapter on traffic demand in this document. The contents of a file sample  is(types.xml)shown.
   
```
<?xml version="1.0" encoding="UTF-8"?>

<vTypes>
  <type id="motorcycle" vClass="motorcycle" weight="1" />
  <type id="car" vClass="passenger" weight="4" />
</vTypes>
```

## Notes

We want to remark that the program is designed to assign (defined in a separate) types randomly to traffic demand without established types.
If the definition file andoriginal routes of vehicles have already types and these are assigned to a vehicle anddefined in thefile, .rou.xml original  the program respect the class assigned to vehicle, but not retrieve the type information file routes. The user could, in any case, edit the file resulting from the implementation of the program to add the type (labeled <vtype>).


