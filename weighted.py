import math
from collections import defaultdict
from coding import bitstream, Encoder, Decoder, write_to_file
import numpy as np
import TensionFlowFakhir.TensionFlow as tf #from pip install TensionFlowFakhir


class Weighted:
    def __init__(self, n, lr=1e-3):
        self.n = n
        self.lr = lr
        self.freqs = defaultdict(lambda: [1, 1])
        self.context = '0' * n
        # self.weights = np.linspace(0, 1, n + 1)[1:] ** 5
        self.weights = np.ones(n)
        self.weights = self.weights / self.weights.sum()  # so that the sum of weights is 1
        self.weights = self.weights[::-1]  # so that the first weight is the highest
        self.weights = tf.Neuron(self.weights)
        self.loss = None

    def get_prob(self):
        probs = []
        for i in range(self.n):
            probs.append(self.freqs[self.context[i:]][0] / sum(self.freqs[self.context[i:]]))
        probs = tf.Neuron(np.array(probs))
        prob_sum = (probs * self.weights).sum()
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
        self.weights.value = self.weights.value.clip(min=0) #relu?
        self.weights.value = self.weights.value / self.weights.value.sum()
        self.loss.backward_zero_grad()

if __name__ == '__main__':
    n = 16
    filename = 'files/enwik3'
    enwik = open(filename, 'rb').read() + b'\x00'  # adding a byte to the end to make sure the last bit is written
    enwik_zip = open(f'{filename}.zip', 'rb').read()

    weighted_contexts = Weighted(n)
    theoretical_compression = 0
    encoder = Encoder()
    for bit in (bitstream(enwik)):
        prob = weighted_contexts.get_prob()
        encoder.encode(bit, prob)
        weighted_contexts.update(bit)
        if bit == '1':
            theoretical_compression += math.log2(1 / (1 - prob))
        else:
            theoretical_compression += math.log2(1 / prob)

    compressed_data = encoder.compressed_data
    print(len(enwik) - 1, math.ceil(len(compressed_data) / 8), len(enwik_zip), theoretical_compression / 8)
    print("weights: ", weighted_contexts.weights.value)
    # saving the compressed file
    write_to_file(f'{filename}.ht', compressed_data)

    # decompressing
    compressed_data = open(f'{filename}.ht', 'rb').read()
    bit_stream = bitstream(compressed_data)
    decoder = Decoder(bit_stream)
    weighted_contexts = Weighted(n)
    while True:
        prob = weighted_contexts.get_prob()
        next_bit = decoder.decode(prob)
        if next_bit is None:
            break
        weighted_contexts.update(next_bit)
    uncompressed_data = decoder.uncompressed_data
    write_to_file(f'{filename}.un', uncompressed_data)

    assert enwik == open(f'{filename}.un', 'rb').read()
