import numpy as np
from collections import defaultdict
import math
from tqdm import tqdm

enwik6 = open('enwik6', 'rb').read()
enwik6_zip = open('enwik6.zip', 'rb').read()
print(f'gzip compression factor {len(enwik6) / len(enwik6_zip)}')


# making a byte gram model
class Ngram_model:
    def __init__(self, n):
        self.n = n
        self.freqs = defaultdict(lambda: defaultdict(int))  # freqs[context][char] = count

    def get_bits(self, enwik):
        bits = 0
        context = enwik[:self.n]
        for byte in (enwik[self.n:]):
            prob = ((self.freqs[context][byte] + 1) / (sum(self.freqs[context].values()) + 256))
            bits += 1 + math.log2(1 / prob)
            self.freqs[context][byte] += 1
            context += bytes([byte])
            context = context[-self.n:]
        return bits


# Multiple Context Length model
class MultipleNgram:
    def __init__(self, n):
        """
        Uses the model with the maximum available context
        :param n: Max context length
        """
        self.n = n
        self.freqs = defaultdict(lambda: defaultdict(int))  # freqs[context][char] = count

    def get_bits(self, enwik):
        bits = 0
        context = enwik[:1]
        for byte in enwik[1:]:
            prob = 1 / 256
            for i in range(1, min(self.n + 1, len(context) + 1)):
                if self.freqs[context[:i]][byte] != 0:
                    prob = ((self.freqs[context[:i]][byte]) / (sum(self.freqs[context[:i]].values())))
                    self.freqs[context[:i]][byte] += 1
                else:
                    self.freqs[context[:i]][byte] += 1
            bits += 1 + math.log2(1 / prob)
            context += bytes([byte])
            context = context[-self.n:]
        return bits

models = [Ngram_model(i) for i in range(1, 5)]
compression_factors = len(enwik6) / (np.array([m.get_bits(enwik6) for m in models]) / 8)
for i, cf in enumerate(compression_factors):
    print(f"{i + 1}-gram compression factor {cf}")

# print()
# models = [MultipleNgram(i) for i in range(1, 5)]
# compression_factors = len(enwik6) / (np.array([m.get_bits(enwik6) for m in models]) / 8)
# for i, cf in enumerate(compression_factors):
#     print(f"multiple {i + 1}-gram compression factor {cf}")