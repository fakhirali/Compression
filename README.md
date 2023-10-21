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

Results: 

 averaged on 5 random samples of 1000 bytes from enwik9

| Model | Compressed Size | Theoretical Compression |
| --- | --- | --- |
| zip | 576.2 | N/A |
| Ngram_16 | 751.6 | 747.0501653413878 |
| Backoff_16 | 715.4 | 711.4384452676097 |
| LearnedWeighted_16 | 737.8 | 732.9907825118808 |
