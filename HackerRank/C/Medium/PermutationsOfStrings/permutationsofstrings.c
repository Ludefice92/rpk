#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int next_permutation(int n, char **s)
{
	/**
	* Complete this method
	* Return 0 when there is no next permutation and 1 otherwise
	* Modify array s to its next permutation
	*/
    int i = n-2;
    
    while(i>=0 && strcmp(s[i],s[i+1])>=0) i--;
    if(i==-1) return 0; //no new permutations
    
    //find the smallest element in the suffix greater than s[i], swap, then reverse suffix
    int j = n-1;
    while(strcmp(s[i],s[j])>=0) j--;
    char *tmp = s[i];
    s[i] = s[j];
    s[j] = tmp;
    
    for(int first=i+1, last = n-1; first < last; first++, last--) {
        char *tmp2 = s[first];
        s[first] = s[last];
        s[last] = tmp2;
    }
    
    return 1;
}

int main()
{
	char **s;
	int n;
	scanf("%d", &n);
	s = calloc(n, sizeof(char*));
	for (int i = 0; i < n; i++)
	{
		s[i] = calloc(11, sizeof(char));
		scanf("%s", s[i]);
	}
	do
	{
		for (int i = 0; i < n; i++)
			printf("%s%c", s[i], i == n - 1 ? '\n' : ' ');
	} while (next_permutation(n, s));
	for (int i = 0; i < n; i++)
		free(s[i]);
	free(s);
	return 0;
}