#!/bin/python3

import math
import os
import random
import re
import sys



if __name__ == '__main__':
    s = input()
    charmap = {}
    
    for i in range(len(s)):
        if s[i] not in charmap.keys():
            charmap[s[i]] = 1
        else:
            charmap[s[i]] += 1
    sorted_dict = sorted(charmap.items(), key=lambda item: (-item[1],item[0]))
    for j in range(3):
        print(f"{sorted_dict[j][0]} {sorted_dict[j][1]}")
