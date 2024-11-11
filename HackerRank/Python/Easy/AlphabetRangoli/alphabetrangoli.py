def print_rangoli(size):
    # your code goes here
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    toprint = []
    for i in range(size):
        sliceToPrint = '-'.join(alphabet[size-1:size-i-1:-1] + alphabet[size-i-1:size])
        toprint.append(sliceToPrint.center(4*size - 3, '-'))
    
    print("\n".join(toprint + toprint[-2::-1]))    

if __name__ == '__main__':
    n = int(input())
    print_rangoli(n)