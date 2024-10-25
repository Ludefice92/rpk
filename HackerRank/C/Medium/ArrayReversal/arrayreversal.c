#include <stdio.h>
#include <stdlib.h>

int main()
{
    int num, *arr, i;
    scanf("%d", &num);
    int tmpArr[num];
    arr = (int*) malloc(num * sizeof(int));
    for(i = 0; i < num; i++) {
        scanf("%d", arr + i);
        tmpArr[num - i - 1] = *(arr+i);
    }


    /* Write the logic to reverse the array. */

    for(i = 0; i < num; i++) {
        *(arr+i) = tmpArr[i];
        printf("%d ", *(arr + i));
    }
    
    return 0;
}
