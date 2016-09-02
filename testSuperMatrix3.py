# -*- coding: utf-8 -*-

import csv
import codecs

import numpy as np
from idlelib.IOBinding import encoding

def obtenNodos(nombreDelArchivoCsv):
    fileReader = csv.reader(open(nombreDelArchivoCsv, encoding='utf8'), delimiter=",")
    nodos = []
    renglon = -1
    
    for row in fileReader:
        renglon = renglon + 1
        if (renglon > 1):
            nodos.append(row[1])
                   
    return nodos

def obtenClustersNodos(nombreDelArchivoCsv):    
    fileReader = csv.reader(open(nombreDelArchivoCsv, encoding='utf8'), delimiter=",")
    clustersNodos = []
    renglon = -1
    cluster = -1
    for row in fileReader:
        renglon = renglon + 1
        if (renglon > 1):
            if (row[0] != ""):
                cluster = cluster + 1
                clustersNodos.append({'cluster':row[0], 'nodos':[row[1]]})
            else:
                clustersNodos[cluster]['nodos'].append(row[1])
                   
    return clustersNodos
    
def sonDistintas(a, b):    
    if np.allclose(a, b, atol=0.0001):
        return False
    else:
        return True
    
def laMatrizDeValores(nombreDelArchivoCsv):
    with open(nombreDelArchivoCsv, encoding='utf8') as f:
        f.readline()
        f.readline()
        ncols = len(f.readline().split(','))
#     with open(nombreDelArchivoCsv, encoding='utf8') as f:
#         f.readline()
#         f.readline()
        
    with codecs.open(nombreDelArchivoCsv, encoding="utf-8") as s:
    
        laSuperMatriz = np.loadtxt(s, dtype=float, delimiter=',', skiprows=2, usecols=range(2, ncols))
 
    # laSuperMatriz = np.matrix(np.loadtxt(nombreDelArchivoCsv, delimiter=',', skiprows=2, usecols=range(2, ncols), converters={0: lambda x: x.decode('utf-8')}, dtype='<U2'))
    return laSuperMatriz

def eigenVector(nombreDelArchivoCsv):
 
    laSuperMatriz = np.matrix(laMatrizDeValores(nombreDelArchivoCsv))
    laAnterior = laSuperMatriz.copy()
    laSiguiente = laSuperMatriz * laSuperMatriz

    while sonDistintas(laAnterior, laSiguiente):
        print ("son distintas")
        laAnterior = laSiguiente.copy()
        laSiguiente = laAnterior * laAnterior
         
    
    columna = laSiguiente[:, [0]]
    return columna


print (eigenVector("DF101215_GOV_AP.csv"))
#  
estosNodos = obtenClustersNodos("DF101215_GOV_AP.csv")
print (estosNodos[0]['cluster'])
print (estosNodos[0]['nodos'])
print(obtenNodos("DF101215_GOV_AP.csv"))
# print (laMatrizDeValores("DF101215_GOV_AP.csv")[:, [0]])
print (laMatrizDeValores("DF101215_GOV_AP.csv"))


