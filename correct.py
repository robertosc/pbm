#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
University of Costa Rica
Lab: PRIS-Lab
Author: Roberto Sánchez Cárdenas
email: roberto.sanchezcardenas@ucr.ac.cr
Version: 1.0
Creation date: 2020.08.25
Last modification date: 2020.08.27
help: This is a script for the extraction and sorting of affinity parameters of the docking results from pyMOL, the data MUST have the
following format

mode |   affinity | dist from best mode
     | (kcal/mol) | rmsd l.b.| rmsd u.b.
-----+------------+----------+----------
   1         -8.8      0.000      0.000
   2         -8.3      1.060      1.930
   3         -7.9      2.381      9.433
   4         -7.5      3.149      9.765
   5         -7.5      2.507      9.687
   6         -7.4      3.043      7.100
   7         -7.3      4.204     11.952
   8         -7.3      1.598      2.341
   9         -7.3      1.687      2.251

Usage: $python3 data_extraction.py -i /path/ -f format -n num_parameters -o output

2020-08-29 Fabian Mora fmorac@prislab
 * Fixed .log file parsing, before this change it was only parsing negative affinitys  
 * Added JSON format for ouput 
"""

import time
import csv
import glob
import json
import argparse
import re
import os
import math
import yaml
from collections import OrderedDict

def num_input():
    while True:
        try:
            num = int(input("Enter the number of parameters you want to extract from each file: "))
            if isinstance(num, int):
                break
        except:
            print("Error! Input must be an integer.")
    return num


def parse_line(line):
    valid = re.search(r"^\s*[-+]?[0-9]+\s", line)
    #print(valid)
    if valid != None:
        tmp = line.split()[:2]
        #print(tmp)
        return [int(tmp[0]), float(tmp[1])]
    return None


def extract_data(filename, num_params):
    f = open(filename, "r")
    file_type = f.name.find(".log")  # Searching .log files only
    if file_type == -1:
        return  # If not .log, end def

    tag = 0  # Se define una etiqueta para llevar conteo
    name = re.sub(r"(_out)?.log", "", os.path.basename(f.name))  # Se busca esta línea para extraer nombre de compuesto
    values = [math.inf] * num_params

    for i, line in enumerate(f):
        if tag >= num_params:
            break
        tmp = parse_line(line)
        if tmp != None:
            values[tag] = tmp[1]
            tag += 1
    f.close()
    data = None
    if tag == 0:
        print("Error in file %s, values not found" % filename)
    else:
        values = sorted(values)
        data = {"name": name, "path": f.name, "score": min(values), "values": values}
    return data


def process_folder(path, num_params=0):
    if num_params == 0:
        num_params = num_input()  # Se pide el numero de datos a extraer
    try:
        files = glob.glob(path + "*.log", recursive=True)
    except:
        print("No .log files found")
        return
    compounds = [None] * len(files)  # Se almacenan datos en diccionario
    pos = 0
    for k in range(len(files)):
        try:
            data = extract_data(files[k], num_params)
            if data != None:
                compounds[pos] = data
                pos += 1
        except:
            print("File data from %s couldn't be extracted" % files[k])
    compounds = sorted(compounds[0:pos], key=lambda x: x["score"])
    return compounds


def human_readable_format(data, filename, frmt):
    try:
        if frmt == "json":
            with open(filename, "w") as data_file:
                json.dump(data, data_file, indent=2, sort_keys=True, ensure_ascii=False)
        elif frmt == "csv":
            columns = ["name", "score", "values", "path"]
            with open(filename, "w") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=columns)
                writer.writeheader()
                for data in data:
                    writer.writerow(data)
        elif frmt == "yaml":
            with open(filename, "w") as data_file:
                tmp = OrderedDict()
                for v in data:
                    tmp[v["name"]] = {"score": v["score"], "path": v["path"], "values": v["values"]}
                yaml.dump(tmp, data_file)
    except IOError:
        print("I/O error")


def main():
    parser = argparse.ArgumentParser(
        description="This is a script for the extraction and sorting of affinity parameters of the docking results from pyMOL with .log format\
		\n Usage example: python3 data_extraction.py -i /home/user/logfiles/ -f yaml -o compounds -n 3\n\n Usage example extracts 3 data points from file found at /home/user/logfiles/\
		,saves them as compunds.yaml"
    )
    parser.add_argument("-n", action="store", type=int, default=1, help="Number of parameters to extract")
    parser.add_argument("-f", action="store", type=str, choices=["yaml", "csv", "json"], default="json", help="Format of the savings file [yaml/csv/json]")
    parser.add_argument("-o", action="store", type=str, default="scores.json", help="Name of the file where data will be saved")
    parser.add_argument("-i", action="store", type=str, help="Path to the .log format files", required=True)

    args = parser.parse_args()

    if args.n == None:
        sorted_compounds = process_folder(args.i)
    else:
        sorted_compounds = process_folder(args.i, args.n)
    human_readable_format(sorted_compounds, args.o, args.f)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
