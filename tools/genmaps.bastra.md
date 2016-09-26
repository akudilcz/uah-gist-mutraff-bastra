# genmaps.bastra : Map generator for Bastra simulations

This genmaps tool generates, according to some settings, a series of maps with weights that modify the weight values of certain network sections. It uses a xml configuration file.

## Usage
The program is invoked from the command line, accordingthe
```
> Genmaps.bastra.py -c <configFile>
```

When starting the program, it expects to receive as to parameter the location of the file <configFile>,in xML format, and the structure shown below:

## Configuration file
* The <gmb> indicates the start of the configuration options for the genmaps.bastra.pyprogram.
* The <mode> indicates the mode we want the applicationadopt. This is an enumerated type, consisting of the following strings:
** map_r.With this character string invoke the mode of operation of reference map, which we will see later in the section intended operating modes
** random:with this chain character look random mode operation, on which we stop later in the corresponding sectionkick.
** penalty: with this character string invoke functionality on sections penalty. We shall see later, in the section, which means this mode.
* The <net_file> stores the value of the location of network file format SUMO that we will use as a data source.
* The <output_prefix> stores a string we will use prefix characters when composing / name / s of the / the file / s output. Must meet the operating system requirements for file names.
* The <output_dir> stores the location of the directorywhich the program output is delivered either in one or more files.
* The <weight_function> stores the function thatdefine the factor by which the weight of the section is multiplied to obtain the new weight, in random operation modes and penalty on a stretch. Its syntax must be suitable for implementation in Python. They have been incorporatedlibraries random and numpy code tool to incorporate the functions of these libraries to those available for use as weight functions in this attribute.
* The <num_maps> stores an integer greater than zero representing the number of maps created with the execution of the application. This attribute is only effective in the shuffle mode operation.
* The <begin> stores the integer equalor greater than zero indicating the start of the simulation, this being directly printed value on / the map / s output, according with the syntactical requirements of map files weights in SUMO.
* The tag <end> stores the integer greater than zero signals the end of the simulation, and this directly printed value on / the map / s output, according with the syntactical requirements of map files weights in SUMO.
* The <join_map> stores the location of the file you wantmerge with our departure. It is not necessarydefine this attribute, meaning that the empty string indicates that no file you wantmerge. We'll see howworks in the section aimed at merging mapsfollowing:.
* The <join_option> stores a character string that can vary between the
** Add:the values of the weights of the sections penalized both the output map as in the map merge join. We'll see whatmeans in the section on operating modes later
** Max:When a section is penalized both on the map resulting from the application (not yet merged with the join_map)and the map to merge, the end result for stretch weight is calculated as the maximum between them. We'll see how it acts in the section on fusion functionality genmaps.bastra.py maps later.
* The <pen_edges> stored in a string sections (separated by space) we wantpenalize. The penalty for each of the sections will be the result of multiplying your weight (or traveltime)by the result of the evaluation of the function described in <weight_function>.If this is a constant, all weights of the sections that are penalized will be multiplied by the same number. Clarify the operation sections penalty on later in this document. If the label contains the empty string, a map file empty weight (which is the equivalent to working with the reference map) is generated.
* The <pen_edges_steps> indicates the "jumps", or more properly the connections with sections indicated in <pen_edges> theybe penalized in drawingthe map of weights. Accepts greater than or equal to 0. We stop at whole application in the explanatory section ofoperating mode Penalty section below.
  
## Operation modes.
As we have seen, the attribute <mode> configuration file genmaps.bastra.py determines the mode of operation we expect from the tool. There are three operating modes, which we explain in detail.

###  Reference Mode

Sometimes it is useful to recover the original weight values (by default, to SUMO and tools, such as Duarouter, travel time or traveltime nominal).
To this end we have designed the operating mode reference map ("map_r"in the attribute <mode>).
Genmaps.bastra.py generates a map file weights with reference values map selected in the configuration with the name <output_prefix> .mapR.xml. In this mode,other configuration parameters are obviated .

### Random mode
In this mode a series of maps of weights that contains the set of all sections of the network specified in the options is generated, and whose weights correspond toproduct of the traveltime originalof the sections, multiplied by the result of assess the weight function specified in <weight_function>.The number of maps generated corresponds to the value assigned to <num_maps>.The maps are dumped into files with the name <output_prefix> .rand. <N>.xml,where <n> is the sequential number indicating the generated map (1 to <num_maps>).

Because the result of genmaps.bastra.py execution will be effective in SUMO and tools to calculate routes, and to the unpredictability of its operation with negative values weights, do not allow thefunction <weight_function> resultsa lower value than 0. if so, the program ends,screen showing this circumstance. The function is evaluated for calculating each section, so that an expression whose result is uncertain provide factors random penalty.

As a corollary to its operation, note that if we want all sections are penalized in the same way, only we assign <weight_function> a constant value. If this value is equal to 1,obtain a map equivalent toreference map (seen in the previous section)Tranches.

### Penalty Mode on
In this mode (activated when <mode> contains the string"penalty")penalties are calculated as only the sections selected in theattribute <pen_edges> and those connected to them at a distance specified by the variable <pen_edges_steps>.

As an example of this calculation, if the variable <pen_edges_steps> is equal to 1, and the section assigned to < pen_edges> is"tramo1"(defined between"node1"and"node2"),the result is a file in which all sections that appear in its definition nodes have as well"node1"good"node2".If the value of <pen_edges_steps> is equal to 0, the resulting filecontain only the sections included in <pen_edges>.The penalty toapplied will be the factor resulting from the evaluation, for each of the function specified in the attribute <weight_function>.As we saw earlier, if we want the sections obtained by the process are penalized by the same percentage, assign the parameter <weight_function> a constant value.

Finally, note that the name of the resulting file will be <output_prefix> .pen.map.xml .

## Maps  fusion
Genmaps.bastra.py implements functionality as added to the map generation weights, which allows fusion(join)map resulting from its implementation with a previously built in SUMO map format. To do this, the map location we wantmerge with / the resulting / s genmaps.bastra.py the normal operation in the configuration variableshould be included <join_map>.

The procedure for this union depends on the option chosenin the Variable <join_option>.The program runs filesresult of the execution, retrieving the values of weights for each section, and then runs the file to merge. Then poured into a final file (or several, if the output of genmaps.bastra.py is a set of files) sections and their weights. If a section is reflected in both files, the final weight for the tranchedepend on the option chosen merger. If the string entered in <join_option> is"max",the weight for the same will be up to those contained in the maps tojoined. Conversely, if the chosen option is "add", the weight applicable totranche will correspond to the sum of each of the weights.

The file with the merger of the maps will be named as <output_prefix> .join_map_ <n>.xml,where <n> it is the sequence of the resulting files. Therefore, it is equal to 1 when only have an output file for the program in its normal operation (modes reference map and penalty tranche) and will correspond to the file corresponding sequence in the case of multiple output program (random).

Finally, note that both files resulting from the merger as it will be obtained prior to output the program.
    
