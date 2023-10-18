#include <iostream>
#include <fstream>
using namespace std;


int main(){
    string line;
    ifstream fin("enwik6");
    while (getline(fin, line)){
        cout << line << endl;
    }
    return 0;
}