from coding import bitstream, Encoder, Decoder, write_to_file
import math


def run_model(model):
    filename = 'files/enwik3'
    enwik = open(filename, 'rb').read() + b'\x00'  # adding a byte to the end to make sure the last bit is written
    theoretical_compression = 0
    encoder = Encoder()
    for bit in (bitstream(enwik)):
        prob = model.get_prob()
        encoder.encode(bit, prob)
        model.update(bit)
        if bit == '1':
            theoretical_compression += math.log2(1 / (1 - prob))
        else:
            theoretical_compression += math.log2(1 / prob)

    compressed_data = encoder.compressed_data
    # saving the compressed file
    write_to_file(f'{filename}.ht', compressed_data)
    compressed_size = math.ceil(len(compressed_data) / 8)

    # decompressing
    compressed_data = open(f'{filename}.ht', 'rb').read()
    bit_stream = bitstream(compressed_data)
    decoder = Decoder(bit_stream)
    model.reset()
    while True:
        prob = model.get_prob()
        next_bit = decoder.decode(prob)
        if next_bit is None:
            break
        model.update(next_bit)
    uncompressed_data = decoder.uncompressed_data
    write_to_file(f'{filename}.un', uncompressed_data)
    assert enwik == open(f'{filename}.un', 'rb').read(), "Decompressed file is not the same as the original file"
    return compressed_size, theoretical_compression / 8
