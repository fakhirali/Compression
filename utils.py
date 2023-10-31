from coding import bitstream, Encoder, Decoder, write_to_file, get_bytes_to_write
import math


def compress(model, data):
    '''
    Compresses the data using the model and returns the compressed data and theoretical compression
    :param model:
    :param data:
    :return: compressed data, theoretical compression
    '''
    data = data + b'\x00'
    encoder = Encoder()
    theoretical_compression = 0
    for bit in (bitstream(data)):
        prob = model.get_prob()
        encoder.encode(bit, prob)
        model.update(bit)
        if bit == '1':
            theoretical_compression += math.log2(1 / (1 - prob))
        else:
            theoretical_compression += math.log2(1 / prob)
    compressed_data = encoder.compressed_data
    return compressed_data, theoretical_compression


def decompress(model, compressed_data):
    '''
    Decompresses the compressed data using the model and returns the uncompressed data
    :param model:
    :param compressed_data:
    :return: uncompressed data
    '''
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
    return uncompressed_data


def run_model(model, data):
    compressed_data, theoretical_compression = compress(model, data)
    compressed_size = math.ceil(len(compressed_data) / 8)
    compressed_data = get_bytes_to_write(compressed_data)

    uncompressed_data = decompress(model, compressed_data)
    uncompressed_data = get_bytes_to_write(uncompressed_data)
    model.reset()
    assert data + b'\x00' == uncompressed_data, "Decompressed file is not the same as the original file"
    return compressed_size, theoretical_compression / 8
