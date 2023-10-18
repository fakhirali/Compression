Compression = Coding + Modelling

Coding: How to store symbols.  
Modelling: Which symbols are more probable.

We want to code the most probable symbols in the least amount of bits. And vice versa.

Coding is solved.
Modelling is proved unsolvable.

On first 1000 bytes of wikipedia 
gzip :: 508 bytes
16 bit n-gram :: 522 bytes
17 bit n-gram + backoff :: 510 bytes
