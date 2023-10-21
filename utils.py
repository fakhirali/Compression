from coding import bitstream, Encoder, Decoder, write_to_file, get_bytes_to_write
import math


def run_model(model, data):
    data = data + b'\x00'
    theoretical_compression = 0
    encoder = Encoder()
    for bit in (bitstream(data)):
        prob = model.get_prob()
        encoder.encode(bit, prob)
        model.update(bit)
        if bit == '1':
            theoretical_compression += math.log2(1 / (1 - prob))
        else:
            theoretical_compression += math.log2(1 / prob)

    compressed_data = encoder.compressed_data
    # saving the compressed file
    compressed_size = math.ceil(len(compressed_data) / 8)

    compressed_data = get_bytes_to_write(compressed_data)
    # decompressing
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
    uncompressed_data = get_bytes_to_write(uncompressed_data)
    model.reset()
    assert data == uncompressed_data, "Decompressed file is not the same as the original file"
    return compressed_size, theoretical_compression / 8
