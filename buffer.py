class Buffer:
    def __init__(self, k, elements, label = False, level = None):
        self.k = k
        self.elements = elements
        self.label = label
        self.level = level
        self.weight = 0
    
    def __str__(self):
        res = ""
        for elem in self.elements:
            res += str(elem) + " "
        return res

