from mrl98 import MRL98
from stream import Stream

b = 10
k = 5000
n = 10**6
q = 0.6

quantile, error, time_taken, memory_taken = MRL98(b, k, q, Stream(n, k))
print("{}-quantile: {}\nError: {}\nTime: {} sec\nMemory: {} bytes\n".
    format(q, quantile, error, time_taken, memory_taken))