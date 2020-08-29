This code is meant to be used on files obtained from the docking of proteins in the pyMOL software. It is of interest to extract the most negative energy obtained from the docking. In order to do this, a set of patterns are searched in the .log files. When found, the desired number of data points are extracted. This data is then stored and sorted from most negative to less negative. This data is printed in a yaml or csv file.

In order to use this code, a command terminal and a set of .log files are needed.

In the CLI you must type:
`<$python3 data_extraction.py -i /path/ -f format[yaml/csv] -n number_of_parameters -o output>`


The path must be a the direction of a directory rather than the specific files. 
