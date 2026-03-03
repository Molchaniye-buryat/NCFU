/*
#include <iostream>
#include <cmath>

using namespace std;

int main() {
    double a;
    double& aRef = a;
    cout<<"Enter a: ";
    cin>>aRef;
    cout<<"sqrt = "<<sqrt(aRef)<<endl;

}
*/
/*
#include <iostream>a

using namespace std;
int main() {
    int a = 15;
    int b = 2;
    const int* ptrA = &a;
    //*ptrA = 99999; - Ошибка
    ptrA = &b;
    cout<<"REsult: "<<*ptrA<<endl;
}
*/

#include <iostream>
using namespace std;
int main() {
    int a, b;
    cout<<"Enter a and b: ";
    cin>>a>>b;
    int& aref = a;
    int& bref = b;
    cout<<aref-bref;
}

