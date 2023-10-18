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

compressed_data = ''
counts = [1, 1]
low = 0
high = 255  # highest 8-bit number also the infinite stream of 1s
for bit in tqdm(bitstream(enwik)):
    prob = counts[0] / sum(counts)  # probability of a 0 next
    r = high - low  # range of the current interval
    point = low + int(prob * r)  # the split point of the interval
    # print(low + int(prob * r))
    # not we need to find whether low moves up to the split point
    # or high moves down to the split point
    # if the bit is 1, then we move low up and if the bit is 0 we move high down
    if bit == '1':
        counts[1] += 1
        low = point + 1
    else:
        counts[0] += 1
        high = point
    # if the first two bits of low and high are the same, we can find this by multiplying by 2 and checking
    # if the integer part is the same (either 1 or 0)
    # if so we then strip this bit off the interval and add it to the compressed data
    # and shift the bits of the interval values to the left see "Arithmetic Coding"
    while (high >> 7) == (low >> 7):
        minus = 0
        if high >> 7 == 1:
            minus = 256
        compressed_data += str(high >> 7)
        high = (high << 1) - minus + 1
        low = (low << 1) - minus
    assert high > low, f"{high}, {low}"

print(len(enwik), len(compressed_data) / 8)

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
binary_num = ''
for i in range(8):
    binary_num += next(bit_stream)
num = int(binary_num, 2)
print(num)

uncompressed_data = ''
counts = [1, 1]
low = 0
high = 255
i = 8
progress_bar = tqdm(total=len(compressed_data) * 8)
while i < len(compressed_data) * 8:
    prob = counts[0] / sum(counts)
    r = high - low
    point = low + int(prob * r)
    if num > point:  # idk check this
        uncompressed_data += '1'
        counts[1] += 1
        low = point + 1
    else:
        uncompressed_data += '0'
        counts[0] += 1
        high = point
    progress_bar.set_description(f"{high}, {low}, {num}, {point}, {prob}, {len(uncompressed_data)}")
    while (high >> 7) == (low >> 7):
        minus = 0
        if high >> 7 == 1:
            minus = 256
        high = (high << 1) - minus + 1
        low = (low << 1) - minus
        if (num >> 7) == 1:
            minus = 256
        else:
            minus = 0
        next_bit = next(bit_stream, None)
        if next_bit is None:
            num = None
            break
        num = (num << 1) - minus + int(next_bit)

        i += 1
        progress_bar.update(i)
    if num is None:
        break
    # input()

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
