import numpy as np


class SuperMatrix:
    def __init__(self, M=[]):
        self.M           = np.matrix(M)
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



