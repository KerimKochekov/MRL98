# MRL98
The Python implementation of approximate quantile using the proposed solution of [Approximate medians and other quantiles in one pass and with limited memory](https://dl.acm.org/doi/pdf/10.1145/276305.276342).

## Brief defintions about the quantile concept and MRL98
A **quantile** is an element at a certain rank in the dataset after sort.

In classic methods of computing φ-quantile over a dataset of size N, where float φ ∈ (0, 1), first we sort all elements and then return the one ranking int(φN). Its time complexity is O(N logN) and space complexity is O(N) obviously.

There are 3 basic metrics to assess an approximate quantile algorithm.
1. Space complexity
2. Update time
3. Accuracy

Here I implemented the MRL98, which has variyng execution time and memory complexity for different parameters. Here I will not concentrate on accuracy part of the algorithm.

MRL98 is a *deterministic streaming* model, which has a limitation of that it needs to know the length of the data stream at first.

## Navigation
- `buffer.py` contains the class implementation of Buffer, which keeps the metadata(k, label, level, weight) and data(elements) of the buffer
- `mrl98.py` contains the algorithm implementation with its supporting operations (NEW, COLLAPSE, OUTPUT)
- `stream.py` contains the class implementation of Stream, which simulates the streaming with given metadata N(known as entire sequence length) and k.
- `test.py` calls`mrl98.py`with various hyperparameteres of N, k, b, and φ of tests.

## MRL98 algorithm
MRL98 requires prior knowledge of the length N of the data stream. 
1. It divides the data stream into b blocks, samples k elements from each block, and puts them into b buffers. 
2. Each buffer X is given a weight w(X), representing the number of elements covered by this buffer. 

Each buffer X is assigned a height l(X) and l is set to min_i l(X_i). h(X) is set as the following standard:
1. If only one buffer is empty, its height is set to l (**NEW** operation called).
2. If there are two or more empty buffers, their heights are set to 0 (**NEW** operations called).
3. Otherwise, buffers of height l are collapsed, generating a buffer of height l + 1 (**COLLAPSE** operation called).
4. In the end, once **OUTPUT** operation called.

## MRL98 operations
- **NEW**: Put the first bk elements into buffers successively and set their weights to 1.
- **COLLAPSE**: Compress elements from multiple buffers into one buffer. Specifically, each element from an input buffer Xi would be duplicated w(Xi) times. Then these duplicated elements are sorted and merged into a sequence, where k elements are selected at regular intervals and stored in the output buffer Y, whose weight w(Y) = sum(w(Xi))
- **OUTPUT**: Select an element as the quantile answer from b buffers.
![](https://github.com/KerimKochekov/MRL98/blob/main/images/MLR98.png)

# Results
## Time consumption
As we see from the graphs below, for constant N=10^5(data size), the variyng values of parameters of φ, b, and k do not matter much(time difference is less than 1 sec for big values for them, so it can be discarded).

![](https://github.com/KerimKochekov/MRL98/blob/main/images/quantile-time.png)
![](https://github.com/KerimKochekov/MRL98/blob/main/images/b-time.png)
![](https://github.com/KerimKochekov/MRL98/blob/main/images/k-time.png)

As conclusion, we can say that only N(data size) affects the execution time of algorithm, as we see below. Logically, it increase by N increases(more data, more time to process it and find quantile).

![](https://github.com/KerimKochekov/MRL98/blob/main/images/N-time.png)
 
## Memory consumption
Unlike time consumption, b parameter(number of buffers) definetely affects the memory consumption as you can see from the graph below.
![](https://github.com/KerimKochekov/MRL98/blob/main/images/b-memory.png)

# Github link
[https://github.com/KerimKochekov/MRL98](https://github.com/KerimKochekov/MRL98)
