# -*- coding: utf-8 -*-

import csv

import numpy as np


def obtenNodos(nombreDelArchivoCsv):    
    fileReader = csv.reader(open(nombreDelArchivoCsv), delimiter=",")
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

def eigenVector(nombreDelArchivoCsv):
    
    with open(nombreDelArchivoCsv) as f:
        f.readline()
        f.readline()
        ncols = len(f.readline().split(','))
 
    laSuperMatriz = np.matrix(np.loadtxt(nombreDelArchivoCsv, delimiter=',', skiprows=2, usecols=range(2, ncols)))
    
    
    laAnterior = laSuperMatriz.copy()
    laSiguiente = laSuperMatriz * laSuperMatriz
     
     
     
    while sonDistintas(laAnterior, laSiguiente):
        laAnterior = laSiguiente.copy()
        laSiguiente = laSiguiente * laSiguiente
         
    
    columna = laSiguiente[:, [0]]
    return columna

print eigenVector("DF101215_GOV_AP.csv")   
estosNodos = obtenNodos("DF101215_GOV_AP.csv")
print estosNodos[1]['cluster']
print estosNodos[1]['nodos']

