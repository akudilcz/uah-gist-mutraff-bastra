# pygrep: a python grep utility
Copyright: alvaro.paricio@uah.es for Mutraff project

#usage

python pygrep [-h] -d DATA_FILE -f FILTER_FILE [-v]

optional arguments:
  -h, --help            show this help message and exit
  -d DATA_FILE, --data-file DATA_FILE
                        Input. Data file to be grep,ed
  -f FILTER_FILE, --filter-file FILTER_FILE
                        Input. Filter file, one filter per line
  -v, --v               Doesnt contain
# Example:
python pygrep.py -d data.in -f file.in -v
