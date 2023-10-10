#simple char frequency encoder decoder


import numpy as np
from collections import defaultdict
import math
from tqdm import tqdm


enwik6 = open('enwik6', 'rb').read()
enwik6_zip = open('enwik6.zip', 'rb').read()
print(f'gzip compression factor {len(enwik6) / len(enwik6_zip)}')

compressed_data = []
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
        while int(high*10) == int(low*10):
            compressed_data.append(int(high*10))
            high = (high*10) - int(high*10)
            low = (low*10) - int(low*10)
        assert high > low, f"{high}, {low}"
print(high, low)
print(len(enwik6),  len(compressed_data))
print(compressed_data[0:10])






