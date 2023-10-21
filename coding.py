def bitstream(data):
    for byte in data:
        bits = format(byte, '08b')
        for b in bits:
            yield b

def get_bytes_to_write(data):
    bytes_to_write = []
    acc_bits = ''
    for bit in data:
        if len(acc_bits) == 8:
            bytes_to_write.append(int(acc_bits, 2))
            acc_bits = ''
        acc_bits += bit
    for i in range(8 - len(acc_bits)):
        acc_bits += '0'
    bytes_to_write.append(int(acc_bits, 2))
    return bytes(bytes_to_write)

def write_to_file(file_name, data):
    file = open(file_name, 'wb')
    bytes_to_write = get_bytes_to_write(data)
    file.write(bytes_to_write)
    file.close()


class Encoder:
    def __init__(self):
        self.low = 0
        self.n_bits = 8
        self.high = (1 << self.n_bits)-1
        self.compressed_data = ''

    def encode(self, bit, prob):
        """
        :param bit:
        :param prob: of the bit being 0
        :return:
        """
        r = self.high - self.low
        point = self.low + int(prob * r)
        if bit == '1':
            self.low = point + 1
        else:
            self.high = point
        while (self.high >> (self.n_bits-1)) == (self.low >> (self.n_bits-1)):
            minus = 0
            if self.high >> (self.n_bits-1) == 1:
                minus = 1 << self.n_bits
            self.compressed_data += str(self.high >> (self.n_bits-1))
            self.high = (self.high << 1) - minus + 1
            self.low = (self.low << 1) - minus
        assert self.high > self.low, f"{self.high}, {self.low}"


class Decoder:
    def __init__(self, bit_stream):
        self.n_bits = 8
        self.low = 0
        self.high = (1 << self.n_bits)-1
        self.num = None
        self.uncompressed_data = ''
        self.bit_stream = bit_stream

    def decode(self, prob):
        if self.num is None:
            binary_num = ''
            for i in range(self.n_bits):
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
        while (self.high >> (self.n_bits-1)) == (self.low >> (self.n_bits-1)):
            minus = 0
            if self.high >> (self.n_bits-1) == 1:
                minus = 1 << self.n_bits
            self.high = (self.high << 1) - minus + 1
            self.low = (self.low << 1) - minus
            if (self.num >> (self.n_bits-1)) == 1:
                minus = 1 << self.n_bits
            else:
                minus = 0
            next_bit = next(self.bit_stream, None)
            if next_bit is None:
                return None
            self.num = (self.num << 1) - minus + int(next_bit)
        return self.uncompressed_data[-1]
