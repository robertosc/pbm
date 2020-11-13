import sys
import yaml
from collections import OrderedDict

def find_neg_num(start, line): #Se busca un signo negativo en el archivo, se da una posición de inicio en la linea
    
    for i in range(start+1, len(line)-1):
        if(line[i] == "-"):
            #print(line[i])
            data = float(line[i:i+4])
            break
    return data
    
def extract_data(filename, no_params=1):
    f = open(filename, 'r')
    
    file_type = f.name.find(".log") #Se busca que el archivo sea .log
    if(file_type == -1):
        return #Si no es .log, se termina la función
    
    tag = -1
    x = 0  #Se define una etiqueta para llevar conteo
    a = f.name.find("Amb")
    data = []
    for i, line in enumerate(f):
        y = line.find(" 1 ") #Se busca la primera posición de datos
        if(y != -1):
            tag = 1
        if(tag != -1 and tag <= no_params):
            data.append(find_neg_num(y, line)) #Se busca el número negativo adelante del numero de posición
            tag+=1
    f.close()
    #a = {f.name[a:-4]:[data1, data2]}
    return f.name[a:-4], data
    
        
def multiples_archivos(argv):
    compuestos = {} #Se almacenan datos en diccionario
    for k in range(1, len(sys.argv)):
        filename = sys.argv[k]
        try:
            a, b = extract_data(filename, 4)
            print(a, b)
            for i in range(len(b)):
                compuestos[a+"_"+str(i)] = b[0]

        except:
            pass
    print(compuestos)
    compuestos = {k: v for k, v in sorted(compuestos.items(), key=lambda item: item[1])}
    return OrderedDict(compuestos)

def represent_dictionary_order(self, dict_data):
    return self.represent_mapping('tag:yaml.org,2002:map', dict_data.items())
    
def setup_yaml():
    yaml.add_representer(OrderedDict, represent_dictionary_order)
    
def formato_yaml(comp_dict): #Se genera una función para pasar el diccionario a formato .yaml
    setup_yaml()
    print(comp_dict)
    op = str(input("¿Deseas guardar con un nombre específico? y/n"))
    if(op == "n"):
        print("Se guardará bajo el nombre compuestos.yaml")
        filename = "compuestos.yaml"
    else:
        filename = str(input("Ingrese el nombre del archivo .yaml"))
        punto = filename.find(".") #Se busca un punto para evitar errores de nombre
        if(punto != -1):
            filename = filename[0:punto]+".yaml"
            print("Nombre del archivo: %s", filename)
        else:
            filename = filename+".yaml"
            print("Nombre del archivo: %s", filename)
    file = open(filename, 'w')
    
    yaml.dump(comp_dict, file)
    file.close() 


def main(argv):
    comp_ordenados = multiples_archivos(argv)
    print(type(comp_ordenados))
    formato_yaml(comp_ordenados)
    
main(sys.argv)