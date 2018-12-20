#20.12.2018
#TODO: Poprawić wczytywanie dla arythmii

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


        commentsString = ''
        for comment in self.comments:
            commentsString += comment

        return 'Index: '+str(self.index)+'\nClassName: '+self.className+'\nArgs: '+argsString

class Instances(object):
    fileName = ''
    args_names = []
    comments = []
    instances = []

    def __init__(self):
        fileName = 'BRAK PLIKU'

    def __init__(self, fileName):
        self.fileName = fileName

    def __init__(self,fileName, args_Names, comments, instances):
        self.fileName = fileName
        self.args_names = args_Names
        self.comments = comments
        self.instances = instances

    def toString(self):
        argsNamesString = ''
        for argName in self.args_names:
            argsNamesString += argName.strip()+', '

        commentsString = ''
        for comment in self.comments:
            commentsString += comment

        return '\nFileName: ' + self.fileName +'\nArgs Names: '+ argsNamesString +'\nInstances Count: '+str(len(self.instances))+'\nComments: '+commentsString 


    def showInstances(self):
        for instance in self.instances:
            instanceString = ''
            for arg in instance.args:
                instanceString += str(arg) +'\t'
            print(instanceString)

def load_data(path):
    f = open(path,'r')
    f_content = f.readlines()
    index = 0
    comments = []
    instances = []

    for line in f_content:
        if line[0] == '#' or line.isspace():
            #to linia komentarza więc ignoruj ją albo dodaj do jakiego obiektu narazie olać
            comments.append(line)
        else:
            if index == 0:
                #ta linia to nazwy kolumn
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

                index += 1
                instances.append(instance)

    return Instances(f.name,args_names,comments,instances)

#read filepath from command prompt with no spaces
if len(sys.argv) > 1:
    filePath = sys.argv[1]

if not os.path.exists(filePath):
     raise Exception('File does not exists')

#filePath = "A:/IRISDAT.TXT"
io = load_data(filePath)
print(io.toString())

io.showInstances()