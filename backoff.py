from collections import defaultdict
from utils import run_model


class Backoff:
    def __init__(self, n):
        self.n = n
        self.freqs = defaultdict(lambda: [1, 1])
        self.context = '0' * n

    def get_prob(self):
        min_n = 0
        while sum(self.freqs[self.context[min_n:]]) == 2 and min_n < self.n - 1:
            min_n += 1
        return self.freqs[self.context[min_n:]][0] / sum(self.freqs[self.context[min_n:]])

    def update(self, bit):
        update_idx = 1 if bit == '1' else 0
        for i in range(self.n):
            self.freqs[self.context[i:]][update_idx] += 1
        self.context += bit
        self.context = self.context[-self.n:]

    def reset(self):
        self.freqs = defaultdict(lambda: [1, 1])
        self.context = '0' * self.n


if __name__ == '__main__':
    n = 16
    backoff_model = Backoff(n)
    compressed_size, theoretical_compression = run_model(backoff_model)
    print(compressed_size, theoretical_compression)
