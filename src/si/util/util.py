# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Vítor Pereira
# Created Date: 01-09-2021
# version ='0.0.1'
# ---------------------------------------------------------------------------
"""Utility module"""
# ---------------------------------------------------------------------------
import numpy as np

# Y is reserved to idenfify dependent variables
ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXZ'


def label_gen(n):
    import itertools
    """ Generates a list of n distinct labels similar to the ones
        on spreadsheets.
    """
    def _iter_all_strings():
        size = 1
        while True:
            for s in itertools.product(ALPHA, repeat=size):
                yield "".join(s)
            size += 1

    generator = _iter_all_strings()

    def gen():
        for s in generator:
            return s

    return [gen() for _ in range(n)]


def l1_distance(x, y):
    """Computes the manhatan distance of a point (x) to a set of
    points y.
    x.shape=(n,) and y.shape=(m,n)
    """
    import numpy as np
    dist = (np.absolute(x - y)).sum(axis=1)
    return dist


def l2_distance(x, y):
    """Computes the euclidean distance of a point (x) to a set of
    points y.
    x.shape=(n,) and y.shape=(m,n)
    """
    dist = ((x - y) ** 2).sum(axis=1)
    return dist


def train_test_split(dataset, split=0.8):
    from ..data import Dataset
    n = dataset.X.shape[0]
    m = int(split*n)
    arr = np.arange(n)
    np.random.shuffle(arr)
    train_mask = arr[:m]
    test_mask = arr[m:]

    train = Dataset(dataset.X[train_mask], dataset.y[train_mask], dataset._xnames, dataset._yname)
    test = Dataset(dataset.X[test_mask], dataset.y[test_mask], dataset._xnames, dataset._yname)
    return train, test


def add_intersect(X):
    return np.hstack((np.ones((X.shape[0], 1)), X))


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def to_categorical(y, num_classes=None, dtype='float32'):
    y = np.array(y, dtype='int')
    input_shape = y.shape
    if input_shape and input_shape[-1] == 1 and len(input_shape) > 1:
        input_shape = tuple(input_shape[:-1])
    y = y.ravel()
    if not num_classes:
        num_classes = np.max(y) + 1
    n = y.shape[0]
    categorical = np.zeros((n, num_classes), dtype=dtype)
    categorical[np.arange(n), y] = 1
    output_shape = input_shape + (num_classes,)
    categorical = np.reshape(categorical, output_shape)
    return categorical


def minibatch(X, batchsize=256, shuffle=True):
    N = X.shape[0]
    ix = np.arange(N)
    n_batches = int(np.ceil(N / batchsize))

    if shuffle:
        np.random.shuffle(ix)

    def mb_generator():
        for i in range(n_batches):
            yield ix[i * batchsize: (i + 1) * batchsize]

    return mb_generator(),
