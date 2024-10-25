#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main() 
{

    int n;
    scanf("%d", &n);
  	// Complete the code to print the pattern.
    int numToIterate = (n*2) - 1;
    int lowVal, highVal;
    
    for(int i=0; i<numToIterate; i++) {
      for(int j=0; j<numToIterate; j++) {
        if(j<i) {
          lowVal = j;
        } else {
          lowVal = i;
        }
        int minDistToEdge = lowVal;
        minDistToEdge = minDistToEdge < numToIterate - i ? minDistToEdge : numToIterate - i - 1;
        minDistToEdge = minDistToEdge < numToIterate - j ? minDistToEdge : numToIterate - j - 1;
        
        printf("%d ",n-minDistToEdge);
      }
      printf("\n");
    }
    return 0;
}
