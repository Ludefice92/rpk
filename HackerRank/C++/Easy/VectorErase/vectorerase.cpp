#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
using namespace std;


int main() {
    /* Enter your code here. Read input from STDIN. Print output to STDOUT */
    int N;
    cin >> N;
    vector<int> vect(N);
    
    for(int i=0; i<N; i++) {
        cin >> vect[i];
    }
    
    int firstIndexToErase, lastIndex;
    cin >> firstIndexToErase;
    vect.erase(vect.begin() + firstIndexToErase - 1);
    cin >> firstIndexToErase;
    cin >> lastIndex;
    vect.erase(vect.begin() + firstIndexToErase - 1, vect.begin() + lastIndex - 1);
    
    cout << vect.size() << endl;
    for(int k=0; k<vect.size(); k++) {
        cout << vect[k] << " ";
    }
    
    return 0;
}
