#simple char frequency encoder decoder


import numpy as np
from collections import defaultdict
import math
from tqdm import tqdm


enwik6 = open('enwik6', 'rb').read()
enwik6_zip = open('enwik6.zip', 'rb').read()
print(f'gzip compression factor {len(enwik6) / len(enwik6_zip)}')

compressed_data = ''
counts = [1, 1]
low = 0
high = 1
bits = 0
for char in tqdm(enwik6):
    binary_num = format(char, '08b')
    for bit in binary_num:
        prob = counts[0] / sum(counts)
        r = high - low
        point = low + prob*r
        if bit == '1':
            counts[1] += 1
            bits += 1 + math.log2(1 / (1-prob))
            low = point
        else:
            counts[0] += 1
            bits += 1 + math.log2(1 / prob)
            high = point
        while int(high*10) == int(low*10):
            compressed_data += format(int(high*10), 'b')
            high = (high*10) - int(high*10)
            low = (low*10) - int(low*10)
        assert high > low, f"{high}, {low}"

print(len(enwik6),  len(compressed_data)/8)
print(len(enwik6)*8 / len(compressed_data))
print(len(compressed_data)/8, bits/8)
print(counts[1]/sum(counts))

#saving the compressed file
file = open('enwik6.ht', 'wb')
bytes_to_write = []
acc_bits = ''
for bit in compressed_data:
    if len(acc_bits) == 8:
        bytes_to_write.append(int(acc_bits, 2))
        acc_bits = ''
    acc_bits += bit
file.write(bytes(bytes_to_write))





