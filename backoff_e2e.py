import math
from collections import defaultdict
from coding import bitstream, Encoder, Decoder, write_to_file


enwik = open('enwik3', 'rb').read() + b'\x00'  # adding a byte to the end to make sure the last bit is written
enwik_zip = open('enwik3.zip', 'rb').read()

freqs = defaultdict(lambda: [1, 1])  # freqs[context] = [0s, 1s]
n = 16
context = '0' * n
theoretical_compression = 0
encoder = Encoder()
for bit in (bitstream(enwik)):
    min_n = 0
    while sum(freqs[context[min_n:]]) == 2 and min_n < n - 1:
        min_n += 1
    prob = freqs[context[min_n:]][0] / sum(freqs[context[min_n:]])
    encoder.encode(bit, prob)
    if bit == '1':
        for i in range(n):
            freqs[context[i:]][1] += 1
        theoretical_compression += math.log2(1 / (1-prob))
    else:
        for i in range(n):
            freqs[context[i:]][0] += 1
        theoretical_compression += math.log2(1 / prob)
    context += bit
    context = context[-n:]

compressed_data = encoder.compressed_data
print(len(enwik)-1, math.ceil(len(compressed_data) / 8), len(enwik_zip), theoretical_compression / 8)

# saving the compressed file
write_to_file('enwik.ht', compressed_data)

# assert False
# decompressing

compressed_data = open('enwik.ht', 'rb').read()
bit_stream = bitstream(compressed_data)
decoder = Decoder(bit_stream)

freqs = defaultdict(lambda: [1, 1])
context = '0' * n
while True:
    min_n = 0
    while sum(freqs[context[min_n:]]) == 2 and min_n < n - 1:
        min_n += 1
    prob = freqs[context[min_n:]][0] / sum(freqs[context[min_n:]])
    next_bit = decoder.decode(prob)
    if next_bit is None:
        break
    if next_bit == '1':
        for i in range(n):
            freqs[context[i:]][1] += 1
        context += next_bit
    else:
        for i in range(n):
            freqs[context[i:]][0] += 1
        context += next_bit
    context = context[-n:]
uncompressed_data = decoder.uncompressed_data
write_to_file('enwik.un', uncompressed_data)

assert enwik == open('enwik.un', 'rb').read()