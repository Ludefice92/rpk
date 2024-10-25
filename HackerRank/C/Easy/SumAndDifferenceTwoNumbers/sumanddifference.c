#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main()
{
	int w,x;
    float y,z;
    
    scanf("%d %d", &w, &x);
    scanf("%f %f", &y, &z);
    
    printf("%d %d\n",w+x,w-x);
    printf("%.1f %.1f",y+z,y-z);
    
    return 0;
}
