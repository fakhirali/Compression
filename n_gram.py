import math
from collections import defaultdict
from coding import bitstream, Encoder, Decoder, write_to_file


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


if __name__ == '__main__':
    filename = 'files/enwik3'
    enwik = open(f'{filename}', 'rb').read() + b'\x00'  # adding a byte to the end to make sure the last bit is written
    enwik_zip = open(f'{filename}.zip', 'rb').read()

    n = 16
    ngram_model = Ngram(n)
    encoder = Encoder()
    theoretical_compression = 0
    for bit in (bitstream(enwik)):
        prob = ngram_model.get_prob()
        encoder.encode(bit, prob)
        ngram_model.update(bit)
        if bit == '1':
            theoretical_compression += math.log2(1 / (1-prob))
        else:
            theoretical_compression += math.log2(1 / prob)
    compressed_data = encoder.compressed_data
    print(len(enwik)-1, math.ceil(len(compressed_data) / 8), len(enwik_zip), theoretical_compression / 8)

    # saving the compressed file
    write_to_file(f'{filename}.ht', compressed_data)

    # decompressing
    compressed_data = open(f'{filename}.ht', 'rb').read()
    bit_stream = bitstream(compressed_data)
    decoder = Decoder(bit_stream)
    ngram_model = Ngram(n)
    while True:
        prob = ngram_model.get_prob()
        next_bit = decoder.decode(prob)
        if next_bit is None:
            break
        ngram_model.update(next_bit)
    uncompressed_data = decoder.uncompressed_data
    write_to_file(f'{filename}.un', uncompressed_data)
    assert enwik == open(f'{filename}.un', 'rb').read()