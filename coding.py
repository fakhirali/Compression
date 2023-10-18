# simple char frequency encoder decoder
import numpy as np
from collections import defaultdict
import math
from tqdm import tqdm
import time


def bitstream(data):
    for byte in data:
        bits = format(byte, '08b')
        for b in bits:
            yield b


enwik = open('enwik3', 'rb').read() + b'\x00'  # adding a byte to the end to make sure the last bit is written
enwik_zip = open('enwik3.zip', 'rb').read()
print(f'gzip compression factor {len(enwik) / len(enwik_zip)}')

counts = [1, 1]


class Encoder:
    def __init__(self):
        self.low = 0
        self.high = 255
        self.compressed_data = ''

    def encode(self, bit, prob):
        r = self.high - self.low
        point = self.low + int(prob * r)
        if bit == '1':
            self.low = point + 1
        else:
            self.high = point
        while (self.high >> 7) == (self.low >> 7):
            minus = 0
            if self.high >> 7 == 1:
                minus = 256
            self.compressed_data += str(self.high >> 7)
            self.high = (self.high << 1) - minus + 1
            self.low = (self.low << 1) - minus
        assert self.high > self.low, f"{self.high}, {self.low}"


encoder = Encoder()
for bit in tqdm(bitstream(enwik)):
    prob = counts[0] / sum(counts)  # probability of a 0 next
    encoder.encode(bit, prob)
    if bit == '1':
        counts[1] += 1
    else:
        counts[0] += 1
compressed_data = encoder.compressed_data

print(len(enwik), math.ceil(len(compressed_data) / 8))

# saving the compressed file
file = open('enwik.ht', 'wb')
bytes_to_write = []
acc_bits = ''
for bit in compressed_data:
    if len(acc_bits) == 8:
        bytes_to_write.append(int(acc_bits, 2))
        acc_bits = ''
    acc_bits += bit
for i in range(8 - len(acc_bits)):
    acc_bits += '0'
bytes_to_write.append(int(acc_bits, 2))
file.write(bytes(bytes_to_write))
file.close()

# assert False
# decompressing

compressed_data = open('enwik.ht', 'rb').read()
bit_stream = bitstream(compressed_data)


class Decoder:
    def __init__(self, bit_stream):
        self.low = 0
        self.high = 255
        self.num = None
        self.i = 0
        self.uncompressed_data = ''
        self.bit_stream = bit_stream

    def decode(self, prob):
        if self.num is None:
            binary_num = ''
            for i in range(8):
                binary_num += next(self.bit_stream)
            self.num = int(binary_num, 2)
        r = self.high - self.low
        point = self.low + int(prob * r)
        if self.num > point:
            self.uncompressed_data += '1'
            self.low = point + 1
        else:
            self.uncompressed_data += '0'
            self.high = point
        while (self.high >> 7) == (self.low >> 7):
            minus = 0
            if self.high >> 7 == 1:
                minus = 256
            self.high = (self.high << 1) - minus + 1
            self.low = (self.low << 1) - minus
            if (self.num >> 7) == 1:
                minus = 256
            else:
                minus = 0
            next_bit = next(self.bit_stream, None)
            if next_bit is None:
                self.num = None
                return None
            self.num = (self.num << 1) - minus + int(next_bit)
        return self.uncompressed_data[-1]


counts = [1, 1]
decoder = Decoder(bit_stream)
while True:
    prob = counts[0] / sum(counts)
    next_bit = decoder.decode(prob)
    if next_bit is None:
        break
    if next_bit == '1':
        counts[1] += 1
    else:
        counts[0] += 1
uncompressed_data = decoder.uncompressed_data
file = open('enwik.un', 'wb')
bytes_to_write = []
acc_bits = ''
for bit in uncompressed_data:
    if len(acc_bits) == 8:
        bytes_to_write.append(int(acc_bits, 2))
        acc_bits = ''
    acc_bits += bit
for i in range(8 - len(acc_bits)):
    acc_bits += '0'
bytes_to_write.append(int(acc_bits, 2))
bytes_to_write = bytes_to_write[:-1]  # removing the last null char
file.write(bytes(bytes_to_write))
file.close()

assert enwik == open('enwik.un', 'rb').read() + b'\x00'