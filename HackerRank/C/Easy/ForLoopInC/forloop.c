#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

void printSingleDigit(int x) {
    if(x==1) {
        printf("one\n");
    } else if(x==2) {
        printf("two\n");
    } else if(x==3) {
        printf("three\n");
    } else if(x==4) {
        printf("four\n");
    } else if(x==5) {
        printf("five\n");
    } else if(x==6) {
        printf("six\n");
    } else if(x==7) {
        printf("seven\n");
    } else if(x==8) {
        printf("eight\n");
    } else if(x==9) {
        printf("nine\n");
    }
}

void printMultiDigit(int y) {
    if(y % 2 == 0) {
        printf("even\n");
    } else {
        printf("odd\n");
    }
}

int main() 
{
    int a, b;
    scanf("%d\n%d", &a, &b);
  	// Complete the code.
    for(int i=a; i<b+1; i++) {
        if(i<10) printSingleDigit(i);
        if(i>=10) printMultiDigit(i);
    }
    return 0;
}

