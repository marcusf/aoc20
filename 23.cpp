#include <iostream>
#include <vector>


int find(std::vector<unsigned> &clock, unsigned value) {
    return std::find(clock.begin(), clock.end(), value) - clock.begin();
}

int main() {
    static const unsigned arr[] = {3,2,6,5,1,9,4,7,8};
    std::vector<unsigned> clock(arr, arr + sizeof(arr) / sizeof(arr[0]));
    
    // init the array.
    for (unsigned i = 10; i <= 1000000; i++) {
        clock.push_back(i);
    }

    // Main loop
    for (unsigned i = 0; i < 10000000; i++) {
        // unsigned pickup = clock[1:4]
        unsigned destval = clock[0]-1 >= 1 ? clock[0]-1 : 1000000;
        unsigned destination = find(clock, destval);
        unsigned decr = 1;
        while (destination >= 1 && destination <= 3) {
            destval = destval - decr;
            if (destval < 1)
                destval = 1000000;
            destination = find(clock, destval);
        }
        

    }
    
    return 0;
}
