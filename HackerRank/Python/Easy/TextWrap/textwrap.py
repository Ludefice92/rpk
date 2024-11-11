import textwrap

def wrap(string, max_width):
    outStr = ""
    for i in range(0, len(string), max_width):
        outStr+=string[i:i+max_width] + '\n'
    return outStr 

if __name__ == '__main__':
    string, max_width = input(), int(input())
    result = wrap(string, max_width)
    print(result)