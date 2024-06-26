# Notes

Things I've been reading:
- [Machine Super Intelligence](https://www.vetta.org/documents/Machine_Super_Intelligence.pdf)
  - Suggested by [Marcus Hutter](http://www.hutter1.net/ai/introref.htm)

### Neural Networks
Neural Network initialization would have to be deterministic. 
Same random seed will work? Neural Networks love more context.

### Ideas
[starlit](https://github.com/amargaritov/starlit#starlit-algorithm-description) was the latest winner that had
a new idea. It orders the articles based on mutual information using Doc2Vec. 
I like the submissions that have a new insight or idea with them instead of just 
being more computationally efficient, even though being efficient is also a big deal.
The winners all use [cmix](https://www.byronknoll.com/cmix.html).

data + null_char + data + null_char + data + null_char.
we know how many null_chars there are. The model will be able to learn the data 
much better given multiple passes. But compression would have to be done on all 3. (Not possible)

Compression is pretty much sorting. Something sorted can be very easily compressed. The more
random something is, the harder it is to compress. If a program can sort the data, it is the same as compressing it.
However sorting would have to be done so that it can be reversed. Maybe that is the difference.