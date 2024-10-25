#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main() {
    /* Enter your code here. Read input from STDIN. Print output to STDOUT */ 
    int n;
    scanf("%d", &n);
    if(n<1 || n>1000) {
      printf("This array is too small or too large. 1<=n<=1000");
      return -1;
    }
    
    int *arr = (int*)malloc(n*sizeof(int));
    int sum = 0;
    int currentElement;
    for(int i=0; i<n; i++) {
      scanf("%d",&currentElement);
      arr[i] = currentElement;
      sum += arr[i];
    }
    
    free(arr);
    printf("%d",sum);   
    return 0;
}
