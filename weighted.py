from collections import defaultdict
import numpy as np
import TensionFlowFakhir.TensionFlow as tf #from pip install TensionFlowFakhir
from utils import run_model


class LearnedWeighted:
    def __init__(self, n, lr=1e2):
        self.n = n
        self.lr = lr
        self.freqs = defaultdict(lambda: [1, 1])
        self.context = '0' * n
        self.weights = np.ones(n)
        self.weights = tf.Neuron(self.weights)
        self.loss = None

    def get_prob(self):
        probs = []
        for i in range(self.n):
            probs.append(self.freqs[self.context[i:]][0] / sum(self.freqs[self.context[i:]]))
        probs = tf.Neuron(np.array(probs))
        prob_sum = (probs * (self.weights / self.weights.sum()[0])).sum()
        self.loss = prob_sum
        return prob_sum.value[0]

    def update(self, bit):
        if bit == '1':
            for i in range(self.n):
                self.freqs[self.context[i:]][1] += 1
            self.loss = -((1 - self.loss).log2())
        else:
            for i in range(self.n):
                self.freqs[self.context[i:]][0] += 1
            self.loss = -(self.loss.log2())
        self.context += bit
        self.context = self.context[-self.n:]
        self.loss.backward()
        self.weights.value -= self.weights.grad * self.lr
        self.loss.backward_zero_grad()

    def reset(self):
        self.__init__(self.n, self.lr)


if __name__ == '__main__':
    n = 24
    lr = 1e3
    weighted_contexts = LearnedWeighted(n, lr)
    compressed_size, theoretical_compression = run_model(weighted_contexts)
    print(compressed_size, theoretical_compression)

