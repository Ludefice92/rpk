def count_substring(string, sub_string):
    substringCount = 0
    for i in range(len(string)-len(sub_string)+1):
        compareStr = string[i:i+len(sub_string)]
        if sub_string == compareStr:
            substringCount+=1
    return substringCount

if __name__ == '__main__':
    string = input().strip()
    sub_string = input().strip()
    
    count = count_substring(string, sub_string)
    print(count)