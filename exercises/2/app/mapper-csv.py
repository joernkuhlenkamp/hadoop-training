#!/usr/local/bin/python
import sys

for line in sys.stdin:
    words = line.strip().split(',')
    for word in words:
        word = word.lower()
        if word != '':
            print(f'{word}\t{1}')