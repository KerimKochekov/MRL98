from mrl98 import MRL98
from stream import Stream
import matplotlib.pyplot as plt

def plot_graph(x, y, name, xlabel, ylabel, title, file_name):
    for i in range(len(x)):
        #x[i] = [log10(val) for val in x[i]]
        plt.plot(x[i], y[i], name[i])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.savefig(file_name)
    plt.show()

tests = []
for x in range(1, 100):
    tests.append({"n": 10**5, "b": 100, "k":5000, "q": x/100.0})

x = []
y = []
for test in tests:
    quantile, error, time_taken, memory_taken = MRL98(test["b"], test["k"], test["q"], Stream(test["n"], test["k"]))
    print("{}-quantile: {}\nError: {}\nTime: {} sec\nMemory: {} bytes\n".
    format(test["q"], quantile, error, time_taken, memory_taken))
    x.append(test["q"])
    y.append(time_taken)

plot_graph([x], [y], [""], "φ", "Time, sec", "Time consumption for N=10^5", "quantile.png")