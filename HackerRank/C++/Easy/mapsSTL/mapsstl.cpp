#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <set>
#include <map>
#include <algorithm>
using namespace std;


int main() {
    /* Enter your code here. Read input from STDIN. Print output to STDOUT */   
    int Q;
    cin >> Q;
    map <string, int> m;
    
    for(int i=0; i<Q; i++) {
        int type,mark;
        string name;
        cin >> type >> name;
        
        if(type==1) {
            cin >> mark;
            map<string,int>::iterator it = m.find(name);
            if(it!=m.end()) {
                m[name] += mark;                              
            } else {
                m.insert(make_pair(name,mark));                
            }
        } else if(type==2) {
            m.erase(name);
        } else if(type==3) {
            map<string,int>::iterator it = m.find(name);
            if(it!=m.end()) {
                cout << m[name] << endl;                
            } else {
                cout << 0 << endl;                
            }
        }
    }
    
    
    
    
    return 0;
}
