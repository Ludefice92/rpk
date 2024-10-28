#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <set>
#include <algorithm>
using namespace std;


int main() {
    /* Enter your code here. Read input from STDIN. Print output to STDOUT */
    set<int> s;
    int Q;
    cin >> Q;
    
    for(int i=0; i<Q; i++) {
        int x,y;
        cin >> y >> x;
        
        if(y==1) {
            s.insert(x);
        } else if(y==2) {
            s.erase(x);
        } else if(y==3) {
            set<int>::iterator itr = s.find(x);
            if(itr!=s.end()) {
                cout << "Yes" << endl;
            } else {
                cout << "No" << endl;
            }
        }
    }
    
      
    return 0;
}



