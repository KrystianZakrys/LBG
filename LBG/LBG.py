#20.12.2018
#TODO: wczytywanie. Dane oddzielane spacją, przecinek na kropkę, czasem jest zapis [,2] co znacza 0.2 ostatnia kolumna to zawsze klasa. 
#TODO: Serializacja

#21.12.2018
#TODO: Algorytm 
#TODO: testy i raport
import csv
import sys
import os

class Instance(object):
    index = 0
    className = 'init'
    args = []
    args_names = []

    def __init__(self, index, className, args):
        self.index = index  
        self.className = className
        self.args = args
    
    def __init__(self, index):  
        self.index = index
        self.args = []
        self.args_names = []
    
    def toString(self):
        argsString = ''
        for arg in self.args:
            argsString += str(arg) + ' '

        argsNamesString = ''
        for argName in self.args_names:
            argsNamesString += argName +' '

        return 'Index: '+str(self.index)+'\nClassName: '+self.className+'\nArgs: '+argsString+'\nArgs_Names: '+argsNamesString

instances = []

def load_data(path):
    f = open(path,'r')
    f_content = f.readlines()
    index = 0
    for line in f_content:
        if line[0] == '#' or line.isspace():
            #to linia komentarza więc ignoruj ją albo dodaj do jakiego obiektu narazie olać
            print(' ')
        else:
            if index == 0:
                #ta linia to nazwy kolumn
                print(' ') 
                index += 1
                args_names = line.split('\t')
            else:
                instanceTemp = line.split('\t')
                lastElementIndex = len(instanceTemp)-1
                className = instanceTemp[lastElementIndex].strip()
                del instanceTemp[lastElementIndex]
                instance = Instance(index -1)
                for arg in instanceTemp:
                    x = arg.replace(',','.')
                    if x[0] == '.':
                        x = '0'+x
                    instance.args.append(float(x))
                instance.className = className
                instance.args_names = args_names
                index += 1
                instances.append(instance)


#read filepath from command prompt with no spaces
#if len(sys.argv) > 1:
#    filePath = sys.argv[1]

#if not os.path.exists(filePath):
#     raise Exception('File does not exists')
filePath = "A:/IRISDAT.TXT"
load_data(filePath)
for instance in instances:
    print(instance.toString())