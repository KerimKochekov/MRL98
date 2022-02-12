import numpy as np
from buffer import Buffer
from math import ceil
import time
import sys

#START of Operations MRL98
def unite(buffers):
    W = 0
    all_elements = []
    pointer, lengths = [], []
    
    for buffer in buffers:
        lengths.append(len(buffer.elements))
        pointer.append(0)
        W += buffer.weight
    
    total_length = sum(lengths)
    
    for _ in range(total_length):
        min_value = np.Inf
        index_value = -1
        for i in range(len(buffers)):
            if pointer[i] < lengths[i] and min_value > buffers[i].elements[pointer[i]]:
                min_value = buffers[i].elements[pointer[i]]
                index_value = i
        all_elements.extend(buffers[index_value].weight * [buffers[index_value].elements[pointer[index_value]]])
        pointer[index_value] += 1
    
    return all_elements, W

def new(buffer, level, elements):
    buffer.elements = elements
    buffer.elements.sort()
    buffer.weight = 1
    buffer.level = level
    buffer.label = True

def output(buffers, k, phi):
    all_elements, W = unite(buffers)
    return all_elements[ceil(phi*k*W)]

def collapse(buffers, level, k):
    all_elements, W = unite(buffers)
    offset = (W + 1) // 2

    buffers[0].elements = [all_elements[j*W + offset] for j in range(k)]
    buffers[0].level = level
    buffers[0].weight = W

    for i in range(1, len(buffers)):
        buffers[i].elements = []
        buffers[i].label = False
        buffers[i].level = None
        buffers[i].weight = 0

#END of Operations MRL98

#Approximate phi-quantile computing algorithm MRL98
#https://dl.acm.org/doi/pdf/10.1145/276305.276342 
def MRL98(b, k, phi, stream):
    start_time = time.time()
    all_buffers = [Buffer(k, []) for _ in range(b)] 

    taken_memory = 0
    stream_continues = True
    stream_elements = []
    
    while stream_continues:
        l = np.Inf
        empty_buffers = []
        for buffer in all_buffers:
            if buffer.label == True:
                l = min(l, buffer.level)
            else:
                empty_buffers.append(buffer)
        if len(empty_buffers) == 1: #exists exactly on empty buffer
            elements = stream.get_k_elements() 
            if elements == None:
                #Stream ends
                stream_continues = False
            else:
                stream_elements += elements
                new(empty_buffers[0], l, elements)

        elif len(empty_buffers) > 1: #exists at least two empty buffers
            for i in range(len(empty_buffers)):
                elements = stream.get_k_elements()
                if elements == None:
                    #Stream ends
                    stream_continues = False
                    break
                stream_elements += elements
                new(empty_buffers[i], 0, elements)

        else: #empty buffer not exists
            same_buffers = [buffer for buffer in all_buffers if buffer.level == l]
            collapse(same_buffers, l+1, k)
        
        taken_memory = max(taken_memory, sys.getsizeof(all_buffers))
    
    full_buffers = [buffer for buffer in all_buffers if buffer.label == True]
    element = output(full_buffers, k, phi)
    end_time = time.time()

    #Brute-force sort to derive error between aproximate quantile and original quantile
    stream_elements.sort()
    N = len(stream_elements)
    error = abs(ceil(len(stream_elements)*phi) - stream_elements.index(element)) / N

    return element, error, end_time - start_time, taken_memory
