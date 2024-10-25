#include <stdio.h>
#include <stdlib.h>
#include <math.h>

struct triangle
{
	int a;
	int b;
	int c;
};

typedef struct triangle triangle;

double triArea(triangle tr) {
    double p = (tr.a + tr.b + tr.c)/2.0;
    return sqrt(p*(p-tr.a)*(p-tr.b)*(p-tr.c));
}

void swap(triangle *a, triangle *b) {
    triangle tmp = *a;
    *a = *b;
    *b = tmp;
}

void sort_by_area(triangle* tr, int n) {
	/**
	* Sort an array a of the length n
	*/
    int i;
    //double area[n];
    //for(i=0; i<n; i++) {
       // area[i] = triArea(tr[i]);
   // }
    for(i=0; i<n-1; i++) {
        for(int j=i+1; j<n; j++) {
            if(triArea(tr[i]) > triArea(tr[j])) {
                swap(&tr[i],&tr[j]);
                //swap(&tr[i].b,&tr[j].b);
                //swap(&tr[i].c,&tr[j].c);
            }
        }
    }
}

int main()
{
	int n;
	scanf("%d", &n);
	triangle *tr = malloc(n * sizeof(triangle));
	for (int i = 0; i < n; i++) {
		scanf("%d%d%d", &tr[i].a, &tr[i].b, &tr[i].c);
	}
	sort_by_area(tr, n);
	for (int i = 0; i < n; i++) {
		printf("%d %d %d\n", tr[i].a, tr[i].b, tr[i].c);
	}
	return 0;
}