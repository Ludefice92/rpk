#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the solve function below.
def solve(s):
    names = s.split(" ")
    updatedStr = ""
    for name in names:
        if name:
            updatedStr += name[0].upper()
            if len(name) > 1: updatedStr += name[1:]
        updatedStr += " "
    
    return updatedStr.rstrip()

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    s = input()

    result = solve(s)

    fptr.write(result + '\n')

    fptr.close()
