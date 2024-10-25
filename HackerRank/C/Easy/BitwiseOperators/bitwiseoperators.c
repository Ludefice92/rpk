#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>
//Complete the following function.

//each value must be less than k for max and, or, xor
void calculate_the_maximum(int n, int k) {
  //Write your code here.
  int maxAnd = 0;
  int maxOr = 0;
  int maxXor = 0;
  
  for(int i=1; i<n; i++) {
      for(int j=i+1; j<=n; j++) {
          if((maxAnd < (i&j)) && (k > (i&j))) maxAnd = i & j;
          if((maxOr < (i|j)) && (k > (i|j))) maxOr = i | j;
          if((maxXor < (i^j)) && (k > (i^j))) maxXor = i ^ j;
      }
  }
  
  printf("%d\n",maxAnd);
  printf("%d\n",maxOr);
  printf("%d",maxXor);
}

int main() {
    int n, k;
  
    scanf("%d %d", &n, &k);
    calculate_the_maximum(n, k);
 
    return 0;
}
