#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main() {
	
    int n;
    scanf("%d", &n);
    //Complete the code to calculate the sum of the five digits on n.
    unsigned int sumDigits = 0;
    unsigned int remainder = 1;

    while (n>0) {
        if(n==10) {
            sumDigits++;
            break;
        }
        remainder = n % 10;
        n = n / 10;
        sumDigits += remainder;
    }
    
    printf("%d",sumDigits);
    
    return 0;
}
