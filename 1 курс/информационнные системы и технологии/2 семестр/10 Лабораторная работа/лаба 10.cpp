#include <iostream>
#include <string>

using namespace std;

class Furniture {
protected:
    string material;
    double cost;
public:
    Furniture(string m, double c) : material(m), cost(c) {
        cout<<"Furniture constructor called"<<endl;
    }

    void printInfo() {
        cout<<"Material: "<<material<<", Cost: "<<cost<<"$"<<endl;
    }
};

class Table : public Furniture {
private:
    int legsCount;
public:
    Table(string m, double c, int legs) : Furniture(m, c), legsCount(legs) {
        cout<<"Table constructor called"<<endl;
    }
    void printExtendedInfo() {
        printInfo();
        cout<<"Legs: "<<legsCount<<endl;
    }
    void showMaterial() {
        cout<<"Material (from protected): "<<material<<endl;
    }
};

int main(int argc, char const *argv[])
{
    Table myTable("Oak", 500, 4);
    cout<<"\nCalling printInfo"<<endl;
    myTable.printInfo();
    cout<<"\nCalling printExtendedInfo"<<endl;
    myTable.printExtendedInfo();
    cout<<"\nFrom protected"<<endl;
    myTable.showMaterial();
    //myTable.material; - ошибка

    return 0;
}