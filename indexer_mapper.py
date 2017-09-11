#!/usr/bin/python

import sys
import re


for line in sys.stdin:
    data = line.strip().split(",")
    if len(data) == 2:
        url, text = data
        words = text.split()
        for word in words:
            if word.isalpha():
                print "{0}\t{1}".format(word, url)

