#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>
#include <ctype.h>

int main() {

    /* Enter your code here. Read input from STDIN. Print output to STDOUT */
    char num[1000];
    unsigned int digitCount[10] = {0};
    unsigned int curNum;
    
    scanf("%s",num);
    
    for(int i=0; i<1000; i++) {
        if(num[i] == '\0') break;
        curNum = 22;
        if(isdigit(num[i])) curNum = num[i] - '0';
        if(curNum != 22) {
          for(int j=0; j<10; j++) {
              if(j==curNum) digitCount[j]++;
          }
        }
    }
    
    for(int k=0; k<10; k++) {
        printf("%d ",digitCount[k]);
    }
    
    return 0;
}
