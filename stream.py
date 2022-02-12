import random
import numpy as np

class Stream:
    def __init__(self, n, k, seed = 101):
        self.n = n
        self.k = k
        random.seed(seed)
    
    def get_k_elements(self):
        if self.n == 0:
            return None
        elements = [random.random() for _ in range(min(self.k, self.n))]
        if self.n >= self.k:
            self.n -= self.k
            return elements
        
        self.n = 0
        for i in range(self.k - self.n):
            if i%2 == 0:
                elements.append(np.Inf)
            else:
                elements.append(np.NINF)
        return elements
