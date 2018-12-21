#TODO: Pozostałe metody obliczania odległości
#TODO: Poprawić wczytywanie dla arythmii
#TODO: Żeby działało na obiektach a nie tablicach
#TODO: Usprawnienie wyświetlania
#TODO: Zliczenie poprawnie sklasyfikowanych obiektów ( potrzeba obiektów lub przypisania współrzędnych do klasy ) 
#TODO: testy i raport

import csv
import sys
import os
from sklearn import preprocessing #dla normalizacji... będzie trzeba wywalić po zrobieniu raportu
from copy import deepcopy
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


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

    def getClasses(self):
        classes = []
        sum = 0
        for instance in self.instances:
            if len(classes) <= 0:
                    classes.append(instance.className)
                    sum += 1
            if  not instance.className in classes and instance.className != 'init':
                classes.append(instance.className)
                sum += 1
        return {'count':sum,'classes':classes}

    def getNumberOfRowsForClass(self, classes):
        for instance in self.instances:
            temp = classes[instance.className]
            temp += 1
            classes[instance.className] = temp
        return classes 

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

#TODO: będzie trzeba zaimplementować swoje
def normalizeMinMax(args):
    minmaxscaler = preprocessing.MinMaxScaler(feature_range=(0,1))
    args_scaler = minmaxscaler.fit_transform(args)
    print(args_scaler)
    return args_scaler
    

#read filepath from command prompt with no spaces
#if len(sys.argv) > 1:
#    filePath = sys.argv[1]

#if not os.path.exists(filePath):
#     raise Exception('File does not exists')

filePath = "A:/IRISDAT.TXT"
io = load_data(filePath)
print(io.toString())

io.showInstances()
classesDictionary = io.getClasses()


k = classesDictionary['count']



tempArgs = []
for instance in io.instances:
      tempArgs.append(instance.args)

normalizedData = normalizeMinMax(tempArgs)

i = 0
for args in normalizedData:
    io.instances[i].args = args
    i+=1

for instance in io.instances:
    print('Klasa ',instance.className,'\n', instance.args)
    
plt.rcParams['figure.figsize']=(16,9)
plt.style.use('ggplot')


f1 = []
f2 = []

for arg in normalizedData:
     f1.append(arg[0])
     f2.append(arg[1])

X = np.array(list(zip(f1,f2)))

#Euclidean Distance Calculator
def dist (a, b, ax=1, control='e'):
    if control == 'e':
        return np.linalg.norm(a - b, axis = ax)
    if control == 'l1':
        return  np.linalg.norm((a - b), ord=1)
   
maxX =np.max(X)
C_x = np.random.uniform(0, np.max(X), size=k)
C_y = np.random.uniform(0,np.max(X),size=k)

C = np.array(list(zip(C_x,C_y)), dtype=np.float)
print(C)

plt.scatter(f1,f2,c='black', s=7)

colors = {0:'r',1:'g',2:'b',3:'y',4:'c',5:'m',6:'orange',7:'mediumspringgreen',8:'dodgerblue',9:'indigo',10:'blueviolet',11:'lime',12:'saddlebrown',13:'darkolivegreen',14:'khaki',15:'slategrey',16:'crimson'}

i = 0
for _class in classesDictionary['classes']:
    plt.scatter(C_x[i], C_y[i], marker='x', s=120,c=colors[i])
    i += 1

C_old = np.zeros(C.shape)
clusters = np.zeros(len(X))
error = dist(C, C_old, None)
while error != 0:
    for i in range(len(X)):
        distances = dist(X[i], C)
        cluster = np.argmin(distances)
        clusters[i] = cluster
    C_old = deepcopy(C)
    for i in range(k):
        points = [X[j] for j in range(len(X)) if clusters[j] == i]
        C[i] = np.mean(points, axis= 0)
    print(C, 'printuje z whilea')
    error = dist(C, C_old, None)

fig, ax = plt.subplots()
i = 0
classesPoints = {}
for _class in classesDictionary['classes']:
    points = np.array([X[j] for j in range(len(X)) if clusters[j]==i])
    classesPoints[_class] = points
    ax.scatter(points[:,0],points[:,1], s=7, c=colors[i])
    print('Printuje C:\n' ,C)
    ax.scatter(C[i,0],C[i,1], marker='x', s=120, c=colors[i])
    i += 1

for _class in classesDictionary['classes']:
    print('KLASA ', _class, '\n',classesPoints[_class])


zgodne = 0
niezgodne = 0
#for instance in io.instances:
#    for point in classesPoints[instance.className]:
classDict = {}
for _class in classesDictionary['classes']:
    classDict[_class] = 0
classInfo = io.getNumberOfRowsForClass(classDict)

print('Klasyfikacja wczytana z pliku: ')
for info in classInfo:
    print(info, classInfo[info])
        
print('\nPo grupowaniu k-means:')
for _class in classesDictionary['classes']:
    print( _class,str(len(classesPoints[_class])))
plt.show()