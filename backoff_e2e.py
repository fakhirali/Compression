import math
from collections import defaultdict


def bitstream(data):
    for byte in data:
        bits = format(byte, '08b')
        for b in bits:
            yield b


enwik = open('enwik3', 'rb').read() + b'\x00'  # adding a byte to the end to make sure the last bit is written
enwik_zip = open('enwik3.zip', 'rb').read()
print(f'gzip compression factor {len(enwik) / len(enwik_zip)}')

compressed_data = ''
freqs = defaultdict(lambda: [1, 1])  # freqs[context] = [0s, 1s]
n = 17
context = '0' * n
low = 0
high = 255  # highest 8-bit number also the infinite stream of 1s
for bit in (bitstream(enwik)):
    min_n = 0
    while sum(freqs[context[min_n:]]) == 2 and min_n < n - 1:
        min_n += 1
    prob = freqs[context[min_n:]][0] / sum(freqs[context[min_n:]])
    r = high - low
    point = low + int(prob * r)
    if bit == '1':
        for i in range(n):
            freqs[context[i:]][1] += 1
        low = point + 1
    else:
        for i in range(n):
            freqs[context[i:]][0] += 1
        high = point
    context += bit
    context = context[-n:]
    while (high >> 7) == (low >> 7):
        minus = 0
        if high >> 7 == 1:
            minus = 256
        compressed_data += str(high >> 7)
        high = (high << 1) - minus + 1
        low = (low << 1) - minus
    assert high > low, f"{high}, {low}"

print(len(enwik)-1, math.ceil(len(compressed_data) / 8), len(enwik_zip))

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

uncompressed_data = ''
freqs = defaultdict(lambda: [1, 1])
context = '0' * n
low = 0
high = 255
i = 8
while i < len(compressed_data) * 8:
    min_n = 0
    while sum(freqs[context[min_n:]]) == 2 and min_n < n - 1:
        min_n += 1
    prob = freqs[context[min_n:]][0] / sum(freqs[context[min_n:]])
    r = high - low
    point = low + int(prob * r)
    if num > point:
        uncompressed_data += '1'
        for i in range(n):
            freqs[context[i:]][1] += 1
        low = point + 1
        context += uncompressed_data[-1]
    else:
        uncompressed_data += '0'
        for i in range(n):
            freqs[context[i:]][0] += 1
        high = point
        context += uncompressed_data[-1]
    context = context[-n:]
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

assert enwik == open('enwik.un', 'rb').read() + b'\x00'