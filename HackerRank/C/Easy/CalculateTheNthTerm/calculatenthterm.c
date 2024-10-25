#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int recursion(int n, int a, int b, int c, int d) {
    
  if(d == n) {
    return a+b+c;
  } else {
    int tmp;
    tmp=c;
    c=a+b+c;
    a=b;
    b=tmp;
  }
  
  return recursion(n,a,b,c,d+1);
}

//Complete the following function.
int find_nth_term(int n, int a, int b, int c) {
  //Write your code here.
  if(n==1) {
    return a;
  } else if(n==2) {
    return b;
  } else if(n==3) {
    return c;
  }
  
  return recursion(n,a,b,c,4);
}

int main() {
    int n, a, b, c;
  
    scanf("%d %d %d %d", &n, &a, &b, &c);
    if(n<1 || n>20 || a<1 || a>100 || b<1 || b>100 || c<1 || c>100) {
      printf("One or more of the input values are illegal.\n"
           "a,b,c should be between 1 and 100. n should be between 1 and 20\n");
      return -1;
    }
    int ans = find_nth_term(n, a, b, c);
 
    printf("%d", ans); 
    return 0;
}
