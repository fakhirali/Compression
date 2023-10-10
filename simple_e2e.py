#simple char frequency encoder decoder
import numpy as np
from collections import defaultdict
import math
from tqdm import tqdm
import time


enwik6 = open('enwik6', 'rb').read()
enwik6_zip = open('enwik6.zip', 'rb').read()
print(f'gzip compression factor {len(enwik6) / len(enwik6_zip)}')

compressed_data = ''
counts = [1, 1]
low = 0
high = 1
for char in tqdm(enwik6):
    binary_num = format(char, '08b')
    for bit in binary_num:
        prob = counts[0] / sum(counts)
        r = high - low
        point = low + prob*r
        if bit == '1':
            counts[1] += 1
            low = point
        else:
            counts[0] += 1
            high = point
        while int(high*2) == int(low*2):
            compressed_data += format(int(high*2), 'b')
            high = (high*2) - int(high*2)
            low = (low*2) - int(low*2)
        assert high > low, f"{high}, {low}"

print(len(enwik6),  len(compressed_data)/8)

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
file.close()


#decompressing
compressed_data = open('enwik6.ht', 'rb').read()
binary_num = format(compressed_data[0], '08b')
float_num = int(binary_num, 2) / 2**8

uncompressed_data = ''
counts = [1, 1]
low = 0.0
high = 1.0
i = 1
progress_bar = tqdm(total=len(compressed_data))
while i < len(compressed_data):
    prob = counts[0] / sum(counts)
    r = high - low
    point = low + prob*r
    if float_num > prob:
        uncompressed_data += '1'
        counts[1] += 1
        low = point
    else:
        uncompressed_data += '0'
        counts[0] += 1
        high = point
    while int(high*2) == int(low*2):
        high = (high*2) - int(high*2)
        low = (low*2) - int(low*2)
        binary_num = format(compressed_data[i], '08b')
        float_num += int(binary_num, 2) / 2**(i*8)
        print(len(uncompressed_data) % 8)
        i += 1
        progress_bar.update(i)

file = open('enwik6.un', 'wb')
bytes_to_write = []
acc_bits = ''
for bit in uncompressed_data:
    if len(acc_bits) == 8:
        bytes_to_write.append(int(acc_bits, 2))
        acc_bits = ''
    acc_bits += bit
file.write(bytes(bytes_to_write))
file.close()



