#include <iostream>
#include <deque>
using namespace std;

void printKMax(int arr[], int n, int k){
	//Write your code here.
    deque<int> deq;
    int maxVal = INT_LEAST32_MIN, oldFront;
    //print as many numbers as there are combinations of k subarrays in arr
    //take max of every subarray
    for(int i=0; i<(n-k+1); i++) {
        if(i==0) {
            for(int j=0; j<k; j++) {
                if(maxVal < arr[j]) maxVal = arr[j];
                deq.push_back(arr[j]);
            }
        } else {
            oldFront = deq[0];
            deq.pop_front();
            deq.push_back(arr[i+k-1]);
            if(maxVal == oldFront) {
                //we need to check the whole deq to find the max
                maxVal = INT_LEAST32_MIN;
                for(int m=0; m<k; m++) {
                    if(maxVal < deq[m]) maxVal = deq[m];
                }
            } else {
                if(maxVal < deq[k-1]) maxVal = deq[k-1];
            }
        }

        cout << maxVal << " ";
    }
    cout << endl;
}

int main(){
  
	int t;
	cin >> t;
	while(t>0) {
		int n,k;
    	cin >> n >> k;
    	int i;
    	int arr[n];
    	for(i=0;i<n;i++)
      		cin >> arr[i];
    	printKMax(arr, n, k);
    	t--;
  	}
  	return 0;
}
