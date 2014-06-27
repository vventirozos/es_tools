#!/usr/bin/python
import itertools
import random
from random import shuffle
def grouper(n, iterable):
    it = iter(iterable)
    while True:
       chunk = tuple(itertools.islice(it, n))
       if not chunk:
           return
       yield chunk

file = open('book.txt', 'r')
words = list(file.read().split())
shuffle(words)
for chunk in grouper(100, words): 
	print ' '.join(chunk)

