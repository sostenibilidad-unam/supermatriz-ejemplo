import numpy as np
import csv


class SuperMatrix:
    def __init__(self, path):

        fileReader = csv.reader(open(path), delimiter=",")
        self.clustersNodos = []
        renglon = -1
        cluster = -1
        self.nodos = []
        for row in fileReader:
            renglon = renglon + 1
            if (renglon > 1):
                self.nodos.append(row[1])
                if (row[0] != ""):
                    cluster = cluster + 1
                    self.clustersNodos.append({'cluster':row[0], 'nodos':[row[1]]})
                else:
                    self.clustersNodos[cluster]['nodos'].append(row[1])
                    
        self.M = np.matrix(np.loadtxt(path, delimiter=',', skiprows=2, usecols=range(2, len(self.nodos)+2)))            
        self.eigenvector = self.converge()


    def equal(self, a, b, atol=0.0001):    
        """
        determines if two matrices are closer than certain tolerance
        """
        if np.allclose(a, b, atol=atol):
            return False
        else:
            return True


    def converge(self):
        """
        compute eigenvector
        """
        p = self.M.copy()
        n = self.M * self.M
        while not self.equal(p, n):
            p = n.copy()
            n *= n
            
        return n[:, [0]]



