import math
from collections import defaultdict
from coding import bitstream, Encoder, Decoder, write_to_file


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


if __name__ == '__main__':
    filename = 'files/enwik3'
    enwik = open(f'{filename}', 'rb').read() + b'\x00'  # adding a byte to the end to make sure the last bit is written
    enwik_zip = open(f'{filename}.zip', 'rb').read()

    n = 16
    backoff = Backoff(n)
    theoretical_compression = 0
    encoder = Encoder()
    for bit in (bitstream(enwik)):
        prob = backoff.get_prob()
        encoder.encode(bit, prob)
        theoretical_compression += math.log2(1 / (1 - prob)) if bit == '1' else math.log2(1 / prob)
        backoff.update(bit)

    compressed_data = encoder.compressed_data
    print(len(enwik) - 1, math.ceil(len(compressed_data) / 8), len(enwik_zip), theoretical_compression / 8)

    # saving the compressed file
    write_to_file(f'{filename}.ht', compressed_data)

    # assert False
    # decompressing

    compressed_data = open(f'{filename}.ht', 'rb').read()
    bit_stream = bitstream(compressed_data)
    decoder = Decoder(bit_stream)

    backoff = Backoff(n)
    while True:
        prob = backoff.get_prob()
        next_bit = decoder.decode(prob)
        if next_bit is None:
            break
        backoff.update(next_bit)
    uncompressed_data = decoder.uncompressed_data
    write_to_file(f'{filename}.un', uncompressed_data)

    assert enwik == open(f'{filename}.un', 'rb').read()
