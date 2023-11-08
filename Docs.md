### Making a model

To make a model you need to write four functions


```python
class Model:
    def __init__(self):
        #set up stuff
        pass
    
    def get_prob(self):
        #return the probability of the next bit being 0 (float between 1 and 0)
        return 0.25
    
    def update(self, bit):
        #update the state given the bit
        pass
    
    def reset(self):
        #reset the state as it was after initialization
        pass
```

Here is an example of a simple Ngram model


```python
from collections import defaultdict

class Ngram:
    def __init__(self, n):
        self.n = n
        self.freqs = defaultdict(lambda: [1, 1])
        self.context = '0' * n

    def get_prob(self):
        return self.freqs[self.context][0] / sum(self.freqs[self.context])

    def update(self, bit):
        update_idx = 1 if bit == '1' else 0
        self.freqs[self.context][update_idx] += 1
        self.context += bit
        self.context = self.context[-self.n:]

    def reset(self):
        self.freqs = defaultdict(lambda: [1, 1])
        self.context = '0' * self.n
```

### Data
The get_random_enwik function gets a random segment of the english wikipedia.

However any sequence of bytes would work.


```python
from testing_models import get_random_enwik

data = get_random_enwik(size=int(1e3)) #100 bytes of random wikipedia
```


```python
print(data)
```

    b"rve an ancient Celtic practice of a trial marriage for a year and a day, which some traditions hold should be contracted on Lammas (Lughnasadh), although this is far from universal. This practice is attested from centuries ago in the fourth and fifth volumes of the [[Brehon]] law texts, which are compilations of the opinions and judgements of the Brehon class of Druids (in this case, Irish). The texts as a whole deal with a copious amount of detail for the ancient Celtic tribes in the [[British Isles|Isles]].(O'Donovan, 2000) When someone is being initiated into a coven, it is also traditional to study with the coven for a year and a day before their actual initiation into the religion, and some Solitary Wiccans choose to study for a year and a day before dedicating themselves to the religion. Wiccans can also be &quot;promoted&quot; into higher ranks such as head priestess or head priest. Rank can be shown through coloured cords{{fact}}. Initiation can include a dramatic aspect, like "


### Running the model


```python
from utils import compress, decompress
from coding import get_bytes_to_write

model = Ngram(n=8)
model.reset() #remember to reset the model before compression/decompression

compressed_data, theo = compress(model, data)
compressed_data = get_bytes_to_write(compressed_data)
```


```python
print(f"size of orignal data {len(data)} bytes")
print(f"size of compressed data {len(compressed_data)} bytes")
print(f"size of theoretically optimal compressed data {theo / 8:.2f} bytes")
```

    size of orignal data 1000 bytes
    size of compressed data 695 bytes
    size of theoretically optimal compressed data 691.56 bytes



```python
print(compressed_data)
```

    b'w\x11e\x86B\xa8\xee,\xda\x90\xd2\x8a\xe8\xc4\x08\xec\x8eJ\x9f\x96u\x9a\x17~\x90G\xdd_d\xee\xea\x9cmZ\xe5\xf2W\xce\xa9\x92\x9a`<\x94\xdb\xd4\x98\x85\xa6[UE\xa7#\xe5\xa5\x0f2\xc2\xb4\x7f\xde\x04\x8d`B\xa8!\xf8\\\x93I\xaf8kH\x0e\xfc\xfd\x19\xf9\x9f\x94\xce\xa9\x08\x86\x86\xd3\'\xfc\xee\xad\xfd\xb1\xc6i\xad\x99\x1a\xb9\x7faH\x98\xd9\xe8(+=\xd7\xd9g/?\x95\xc0\x9d\x06\xd7\xe8ck]\x81\xd0\x10p\xb2!\xe5\x16M\x03}\xbf\x18\x8c\x85\xb7\xd3\xae\xe1\xa0B\x1b)\xd2\xe1\xac\xd1\xa3\xd7\xba\x10\xca\xf8\xc0\xb5\xdcdp\'\xb7x\x91\x94\x98\xb0\xc5\xd9\xb6:\xd6D\x06\x8e.\xff\xa3jw\x1d-R\xe217\xbd\xdf,\xefsF\x88uS\xbet,(\xc8\x8f\xa7\xa3\xd2\x9f:\x8cQG\xe7\xc3Yb\t\xdf2\xc6\xf2\x13E\x97GFG\x89\xcb\x84\xf86\xf9\xe8\xb0\x9f\x9c\xdc\xee!($h\xf2E%e\xb4s\xb0\n\xc2\x80\xba\xad\xb6\x171\xf8|1\x82\xa1d\x04r\x1a1\x85\xcb\xb3~\xe3\x9f&\x10\xc0\xe32%%\x06]\x92\x9a\x083@\xd6#\xbd\x11\xa7\x14c\xe6)\x87|yd\xc28\x13\x97\xd6\x82\xa2\x86Z\xb5#\xaa\x1a\x8d\xdc\xd8\xcd3*B\xae\x06^\x95\xe6\xcc\x1f\xebm\xd3x\x99O\xf3$\x91\xc2]\n\xb9d\x05{W5\xc3J\xd8\xf6\xa3\x96)\x9c\xcfF\x84i\x7f"\xcb\x12\xb3Ym\xe6\x89{\x82\xfa\x9d\xe6\xb5|.\xda\xd7{\'+$\x02\xf2\x88\x06\xe4\x96\xdc\x0f\xb6\x8eb\xf0\x98e\x1c:\xb8\xf5K<Sj6K(\xfc\xce\xfa#\xaa\xa1\xea\xcc;\x1e\xae\xef\x8caHy:\xd1\xb7\r\xf3\r\x8b\xf9\xf2\x1f\xb7\x7f\xd7*\x8eG\x99{\x9e\xcf\xe8\xda;\xb9?~i\x86\xe4\x1ft\x84 \xa6\x9d|\xa3\xd7\xc4Is\xde\xec\x1a\xf2O\xad\x8a\xed\x8b\x00\x92\x93\xaf\xed4\xbb\xfb\xe2b\xd5\x8f\\\xeb\xe4\x06/\xc6\x00\xc6\xb3\xa9"JL\xf43\xe2\xc8.,d"\x9b\x83Y\x8e1\xb7\x83\x19\xacE\xa3\x1c\xc0\xb33\xbdz\xc9\x18\xd1#\n\r<\x01\xab\xf3{n\xf5N\xfb\xb3\x9a\'(x\xbf\xf5\x00\x8e\xc5\xcbm\x0b!@6\xf2^\xc4\xcf\xc5oP\xddkwH\x90X\x8a\xcd\x9e;\x14m/\n\xa8I\xe8Y\xd5 \xaf\xb3\xa3\xdc"n\xe7\x0bo\xfd\x91\xdb\xc4\xa8\x95_\x8e;\x16\x9cN\x05\xb5\xe3[\xa9_ZJ\x90m:*%\xefoS\xad7D\x9c]<\xe5\xa0f\xe1\x98s\xf9[\xb5[\x07\x08\xa1\xc5\xc4\xae4\xd87|*\xb6\x86\xb5\xb4\xe9!Q\x99QBl:\r\xcb\xe5\xae\xda\x9c\xdf\\\xad\x10\'\x90\x13>\x03e/y\xad\xac\x8aa\x82\xa4a\x93\x8b\xec\xba\x1c\x06{\xd8(\x89\x01\x98\xe6t\x00'



```python
model.reset()
decompressed_data = decompress(model, compressed_data)
decompressed_data = get_bytes_to_write(decompressed_data)
```


```python
print(decompressed_data[:-1] == data) # last byte ends in a null byte
```

    True



```python
print(decompressed_data)
```

    b"rve an ancient Celtic practice of a trial marriage for a year and a day, which some traditions hold should be contracted on Lammas (Lughnasadh), although this is far from universal. This practice is attested from centuries ago in the fourth and fifth volumes of the [[Brehon]] law texts, which are compilations of the opinions and judgements of the Brehon class of Druids (in this case, Irish). The texts as a whole deal with a copious amount of detail for the ancient Celtic tribes in the [[British Isles|Isles]].(O'Donovan, 2000) When someone is being initiated into a coven, it is also traditional to study with the coven for a year and a day before their actual initiation into the religion, and some Solitary Wiccans choose to study for a year and a day before dedicating themselves to the religion. Wiccans can also be &quot;promoted&quot; into higher ranks such as head priestess or head priest. Rank can be shown through coloured cords{{fact}}. Initiation can include a dramatic aspect, like \x00"
