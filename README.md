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

You can test your models too! [Docs](Docs.ipynb) 


TODO:
- [ ] Code with more bits to improve precision

Results: 

 averaged on 3 random samples of 1000 bytes from enwik9

| Model | Compressed Size | Theoretical Compression |
| --- | --- | --- |
| zip | 532.3333333333334 | N/A |
| Ngram | 722.3333333333334 | 717.4846796689859 |
| Backoff | 685.0 | 680.7137133275579 |
| LearnedWeighted | 718.3333333333334 | 712.3682375572251 |
