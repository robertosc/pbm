"""
University of Costa Rica
Lab: PRIS-Lab
Author: Roberto Sánchez Cárdenas
email: roberto.sanchezcardenas@ucr.ac.cr
Version: 1.0
Creation date: 2020.08.25
Last modification date: 2020.08.27
help: This is a script for the extraction and sorting of affinity parameters of the docking results from pyMOL, the data must have the
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

Usage: 
"""
import sys
import yaml
import csv
import glob
from collections import OrderedDict
import argparse

def find_neg_num(line): #Se busca un signo negativo en el archivo, se da una posición de inicio en la linea
	for i in range(len(line)-1):
		if(line[i] == "-"):
			#print(line[i])
			data = float(line[i:i+5])
			break
	return data

def numInput():
	while True:
		try:
			num = int(input("Enter the number of parameters you want to extract from each file: "))
			if isinstance(num, int):
				break
		except:
			print("Error! Input must be an integer.")
	return num

def extract_data(filename, num_params):
	f = open(filename, 'r')
	file_type = f.name.find(".log") #Se busca que el archivo sea .log
	if(file_type == -1):
		return #Si no es .log, se termina la función
		
	tag = -1 #Se define una etiqueta para llevar conteo
	a = f.name.find("Amb") #Se busca esta línea para extraer nombre de compuesto
	data = []

	for i, line in enumerate(f):
		if tag == -1:
			y = line.find(" 1 ") #Se busca la primera posición de datos
			if(y != -1):
				tag = 1
		if(tag != -1 and tag <= num_params):
			data.append(find_neg_num(line)) #Se busca el número negativo adelante del numero de posición
			tag+=1
	#print(data)
	f.close()
	print(f.name[a:-4], data)
	return f.name[a:-4], data
		
def multiples_archivos(path, num_params=0):
	compounds = {} #Se almacenan datos en diccionario
	if(num_params == 0):
		num_params = numInput() #Se pide el numero de datos a extraer
	try:
		files = glob.glob(path+"*.log", recursive=True)
	except:
		print("No .log files found")
		return
	#print(files)
	for k in range(len(files)):
		try:
			a, b = extract_data(files[k], num_params)
			for i in range(len(b)):
				compounds[a+"_"+str(i)] = b[i]
		except:
			pass
	compounds = {k: v for k, v in sorted(compounds.items(), key=lambda item: item[1])}
	return OrderedDict(compounds)

def multiples_archivos_1(argv, num_params=0):
	compounds = {} #Se almacenan datos en diccionario
	if(num_params == 0):
		num_params = numInput() #Se pide el numero de datos a extraer

	for k in range(1, len(sys.argv)):
		filename = sys.argv[k]
		try:
			a, b = extract_data(filename, num_params)
			for i in range(len(b)):
				compounds[a+"_"+str(i)] = b[i]
		except:
			pass
	compounds = {k: v for k, v in sorted(compounds.items(), key=lambda item: item[1])}
	return OrderedDict(compounds)

def represent_dictionary_order(self, dict_data):
	return self.represent_mapping('tag:yaml.org,2002:map', dict_data.items())
		
def setup_yaml():
	yaml.add_representer(OrderedDict, represent_dictionary_order)
		
def humanreadable_format(comp_dict, filename, format): #Function to write the dictionary in yaml or csv format
	while(format == None or format != "yaml" and format != "csv"):
		format = str(input("In what format do you want to save you data? [yaml/csv] "))

	if (filename == None):
		filename = "compounds"
	punto = filename.find(".") #Se busca un punto para evitar errores de nombre
	
	if(punto != -1):
		filename = filename[0:punto]+"."+str(format)
		print("File will be saved under the name: %s" % filename)
	else:
		filename = filename+"."+str(format)
		print("File will be saved under the name: %s" % filename)

	f = open(filename, 'w')
	if(format == "yaml"):
		setup_yaml()
		yaml.dump(comp_dict, f)
	else:
		w = csv.writer(f)
		w.writerow(comp_dict.keys())
		w.writerow(comp_dict.values())
	f.close()





def main():
	my_parser = argparse.ArgumentParser(description="This is a script for the extraction and sorting of affinity parameters of the docking results from pyMOL with .log format\
		\n Usage example: python3 data_extraction.py -i /home/user/logfiles/ -f yaml -o compounds -n 3\n\n Usage example extracts 3 data points from file found at /home/user/logfiles/\
		,saves them as compunds.yaml")
	my_parser.add_argument('-n', action='store', type=int, help="Number of parameters to extract")
	my_parser.add_argument('-f', action='store', type=str, help="Format of the savings file [yaml/csv]")
	my_parser.add_argument('-o', action='store', type=str, help="Name of the file where data will be saved")
	#my_parser.add_argument('-i', action='store', type=str, help="Path to the .log format files")
	
	requiredNamed = my_parser.add_argument_group('required named arguments')
	requiredNamed.add_argument('-i', action='store', type=str, help='Path to the .log format files', required=True)
	
	args = my_parser.parse_args()

	if(args.n == None):
		sorted_compounds = multiples_archivos(args.i)
	else:
		sorted_compounds = multiples_archivos(args.i, args.n)
	
	humanreadable_format(sorted_compounds, args.o, args.f)

main()