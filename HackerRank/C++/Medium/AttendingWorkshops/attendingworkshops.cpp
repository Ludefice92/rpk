#include<bits/stdc++.h>

using namespace std;

//Define the structs Workshops and Available_Workshops.
//Implement the functions initialize and CalculateMaxWorkshops
struct Workshops {
    int start_time;
    int duration;
    int end_time;
};

struct Available_Workshops {
    int n;
    Workshops* ws;
};

Available_Workshops* initialize(int start_time[], int duration[], int n) {
    Available_Workshops* av_ws = new Available_Workshops();
    av_ws->n = n;
    av_ws->ws = new Workshops[n];
    for(int i=0; i<n; i++) {
        Workshops ws;
        ws.start_time = start_time[i];
        ws.duration = duration[i];
        ws.end_time = start_time[i] + duration[i];
        av_ws->ws[i] = ws;
    }
    
    return av_ws;
}

int CalculateMaxWorkshops(Available_Workshops* av_ws) {
    std::sort(av_ws->ws, av_ws->ws + av_ws->n, [](const Workshops& a, const Workshops& b) {
        return a.end_time < b.end_time;
    });;
    int attendableWorkshops = 0, lastEndTime = -1;
    for(int i=0; i<av_ws->n; i++) {
        if(av_ws->ws[i].start_time>=lastEndTime) {
            attendableWorkshops++;
            lastEndTime = av_ws->ws[i].end_time;
        }
    }
    
    return attendableWorkshops;
}

int main(int argc, char *argv[]) {
    int n; // number of workshops
    cin >> n;
    // create arrays of unknown size n
    int* start_time = new int[n];
    int* duration = new int[n];

    for(int i=0; i < n; i++){
        cin >> start_time[i];
    }
    for(int i = 0; i < n; i++){
        cin >> duration[i];
    }

    Available_Workshops * ptr;
    ptr = initialize(start_time,duration, n);
    cout << CalculateMaxWorkshops(ptr) << endl;
    return 0;
}
