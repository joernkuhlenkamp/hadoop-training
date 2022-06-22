#!/usr/local/bin/python
import sys

cur_word = ""
cur_count = 0
for line in sys.stdin:
    word, count = line.strip().split('\t')
    count = int(count)
    if word == cur_word:
        cur_count += count
    else:
        if cur_word != "":
            print(f'{cur_word}\t{cur_count}')
        cur_word = word
        cur_count = count
            
print(f'{cur_word}\t{cur_count}')