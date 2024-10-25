#include <stdio.h>

void update(int *a,int *b) {
    // Complete this function    
    int tmpa = *a;
    int tmpb = *b;
    *a = tmpa + tmpb;
    if(tmpb>tmpa) {
        *b = tmpb-tmpa;
    } else {
        *b = tmpa - tmpb;
    }
}

int main() {
    int a, b;
    int *pa = &a, *pb = &b;
    
    scanf("%d %d", &a, &b);
    update(pa, pb);
    printf("%d\n%d", a, b);

    return 0;
}
