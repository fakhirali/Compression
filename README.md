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
- [ ] Time testing
- [ ] Seeing how model scales with more data

Results: 

 averaged on 3 random samples of 1000 bytes from enwik9

| Model | Compressed Size | Theoretical Compression |
| --- | --- | --- |
| zip | 569.3333333333334 | N/A |
| Ngram | 741.3333333333334 | 736.5475483723066 |
| Backoff | 703.6666666666666 | 699.5420570161597 |
| LearnedWeighted | 731.3333333333334 | 725.454829890491 |
