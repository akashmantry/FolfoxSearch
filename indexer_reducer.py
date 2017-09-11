#!/usr/bin/python

import sys

old_word = None
url_list = set()

for line in sys.stdin:
    data = line.strip().split("\t")
    if len(data) != 2:
        continue
    this_word, url = data
    if old_word and old_word != this_word:
        print old_word, "\t", url_list
        url_list.clear()

    old_word = this_word
    url_list.add(url)

if old_word != None:
    print this_word, "\t", url_list

