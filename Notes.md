# Notes

Things I've been reading:
- [Machine Super Intelligence](https://www.vetta.org/documents/Machine_Super_Intelligence.pdf)
  - Suggested by [Marcus Hutter](http://www.hutter1.net/ai/introref.htm)


### Ideas
[starlit](https://github.com/amargaritov/starlit#starlit-algorithm-description) was the latest winner that had
a new idea. It orders the articles based on mutual information using Doc2Vec. 
I like the submissions that have a new insight or idea with them instead of just 
being more computationally efficient, even though being efficient is also a big deal.
The winners all use [cmix](https://www.byronknoll.com/cmix.html).

data + null_char + data + null_char + data + null_char.
we know how many null_chars there are. The model will be able to learn the data 
much better given multiple passes. But compression would have to be done on all 3. (Not possible)
