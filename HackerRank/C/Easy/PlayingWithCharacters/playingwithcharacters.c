#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main() 
{

    /* Enter your code here. Read input from STDIN. Print output to STDOUT */
    char c;
    char s[100]; //fewer than 100 chars always
    char sen[100]; //fewer than 100 chars always
    
    scanf("%c",&c);
    scanf("\n");
    scanf("%[^\n]%*c",s);
    scanf("\n");
    scanf("%[^\n]%*c",sen);
    
    printf("%c\n",c);
    printf("%s\n",s);
    printf("%s",sen);
       
    return 0;
}
