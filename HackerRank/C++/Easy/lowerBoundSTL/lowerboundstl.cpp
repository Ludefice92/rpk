#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
using namespace std;


int main() {
    /* Enter your code here. Read input from STDIN. Print output to STDOUT */   
    int N, Q;
    cin >> N;
    vector<int> arr(N);
    for(int i=0; i<N; i++) {
        cin >> arr[i];
    }
    cin >> Q;
    int Y;
    for(int i=0; i<Q; i++) {
        cin >> Y;
        
        auto iterator = lower_bound(arr.begin(),arr.end(),Y);
        if (iterator != arr.end() && *iterator == Y) {
            cout << "Yes " << (iterator - arr.begin() + 1) << endl;
        } else {
            cout << "No " << (iterator - arr.begin() + 1) << endl;
        }
    }
    
    return 0;
}
