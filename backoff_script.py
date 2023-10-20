from collections import defaultdict
from coding import bitstream, Encoder, Decoder, write_to_file
import sys
import argparse


parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

if __name__ == '__main__':
    parser.add_argument('-f', '--file_name', help='file to compress')
    parser.add_argument('-n', '--n', help='n for backoff', type=int, default=16)
    parser.add_argument('-c', '--compress', help='compress', action='store_true')
    parser.add_argument('-d', '--decompress', help='decompress', action='store_true')
    args = parser.parse_args()
    file_name = args.file_name
    n = args.n
    if args.compress:
        data = open(file_name, 'rb').read() + b'\x00'  # adding a byte to the end to make sure the last bit is written
        freqs = defaultdict(lambda: [1, 1])  # freqs[context] = [0s, 1s]
        context = '0' * n
        encoder = Encoder()
        for bit in (bitstream(data)):
            min_n = 0
            while sum(freqs[context[min_n:]]) == 2 and min_n < n - 1:
                min_n += 1
            prob = freqs[context[min_n:]][0] / sum(freqs[context[min_n:]])
            encoder.encode(bit, prob)
            if bit == '1':
                for i in range(n):
                    freqs[context[i:]][1] += 1
            else:
                for i in range(n):
                    freqs[context[i:]][0] += 1
            context += bit
            context = context[-n:]
        compressed_data = encoder.compressed_data
        write_to_file(f'{file_name}.ht', compressed_data)
    if args.decompress:
        assert file_name.endswith('.ht'), "File name must end with .ht"
        compressed_data = open(file_name, 'rb').read()
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
        uncompressed_data = decoder.uncompressed_data[:-8]  # removing the null byte
        write_to_file(file_name.replace('.ht', ''), uncompressed_data)
