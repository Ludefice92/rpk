def merge_the_tools(string, k):
    # your code goes here
    for i in range(0,len(string),k):
        substr = string[i:i+k]
        prevchars = set()
        result = []
        for char in substr:
            if char not in prevchars:
                result.append(char)
                prevchars.add(char)
        print(''.join(result))

if __name__ == '__main__':
    string, k = input(), int(input())
    merge_the_tools(string, k)