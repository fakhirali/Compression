import math
from collections import defaultdict
from utils import run_model


class Ngram:
    def __init__(self, n):
        self.n = n
        self.freqs = defaultdict(lambda: [1, 1])
        self.context = '0' * n

    def get_prob(self):
        return self.freqs[self.context][0] / sum(self.freqs[self.context])

    def update(self, bit):
        update_idx = 1 if bit == '1' else 0
        self.freqs[self.context][update_idx] += 1
        self.context += bit
        self.context = self.context[-self.n:]

    def reset(self):
        self.freqs = defaultdict(lambda: [1, 1])
        self.context = '0' * self.n


if __name__ == '__main__':
    n = 16
    ngram_model = Ngram(n)
    compressed_size, theoretical_compression = run_model(ngram_model)
    print(compressed_size, theoretical_compression)