#!/bin/python3

import math
import os
import random
import re
import sys




first_multiple_input = input().rstrip().split()

n = int(first_multiple_input[0])

m = int(first_multiple_input[1])

matrix = []

alphanum = "" #symbols/spaces between alphanum char are replaced with a single space ' '

for _ in range(n):
    matrix_item = input()
    matrix.append(matrix_item)

#Read column-wise
decoded_matrix = ''.join([matrix[row][col] for col in range(m) for row in range(n)])
#using regex to decode matrix
decoded_matrix = re.sub(r'(?<=\w)[^a-zA-Z0-9]+(?=\w)', ' ', decoded_matrix)
print(decoded_matrix)
