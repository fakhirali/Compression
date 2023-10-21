Compression = Coding + Modelling

Coding: How to store symbols.  
Modelling: Which symbols are more probable.

We want to code the most probable symbols in the least amount of bits. And vice versa.

Coding is solved.
Modelling is proved unsolvable.

On first 1000 bytes of wikipedia  
gzip :: 508 bytes  
16 bit n-gram :: 522 bytes  
16 bit n-gram + backoff :: 513 bytes  
16 bit learned weighted n-gram :: 587 bytes

TODO:
- [ ] Code with more bits to improve precision

Results: 

 averaged on 3 random samples of 1000 bytes from enwik9

| Model | Compressed Size | Theoretical Compression |
| --- | --- | --- |
| zip | 382.6666666666667 | N/A |
| Ngram | 573.6666666666666 | 566.1230212214556 |
| Backoff | 556.0 | 549.1950639647857 |
| LearnedWeighted | 622.6666666666666 | 615.2785268782923 |
