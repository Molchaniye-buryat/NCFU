/*
#include <iostream>
#include <cmath>

using namespace std;

class Point3D
{
private:
    double x, y, z;

public:
     Point3D() : x(0.0), y(0.0), z(0.0) {
        cout<<"Default constructor (0, 0, 0) "<<endl;
     }

     Point3D(double x_val, double y_val, double z_val) : x(x_val), y(y_val), z(z_val) {
        cout<<"Parameterized constructor ("<<x<<", "<<y<<", "<<z<<")"<<endl;
     }

     Point3D(double x_val, double y_val) : x(x_val), y(y_val), z(0.0) {
        cout<<"Constructor with 2 Parameteres ("<<x<<", "<<y<<")"<<endl;
     }

     double getX() {
        return x;
     }
     double getY() {
        return y;
     }
     double getZ() {
        return z;
     }

     void display() {
        cout<<"Point3D("<<x<<", "<<y<<", "<<z<<")"<<endl;
     }
};

int main(int argc, char const *argv[])
{
    Point3D p1;
    Point3D p2(4.8, 5.1, 0.3);
    Point3D p3(7.1, 2.2);

    p1.display();
    p2.display();
    p3.display();

    return 0;
}
*/
/*
#include <iostream>
#include <ctime>

using namespace std;

class IntArray {
private:
    int* data;
    int size;
public:
    IntArray(int s) {
        size = 5;
        data = new int[size];
    }
    ~IntArray() {
        delete[] data;
        cout<<"Deteted"<<endl;
    }

    void randomFill() {
        srand(time(0));
        for (int i = 0; i < size; i++) {
            data[i] = rand();
        }
    }

    void display() {
        for (int i = 0; i < size; i++) {
            cout<<data[i]<<" ";
        }
        cout<<endl;
    }

};

int main(int argc, char const *argv[])
{
    IntArray arr(5);
    arr.randomFill();
    arr.display();
        
    return 0;
}
*/

#include <iostream>
using namespace std;

class Point {
private:
    int num;
    static int count;
public:
    Point() {
        count++;
        num = count;
        cout<<"Object "<<num<<" created"<<endl;
    }
    
    ~Point() {
        cout<<"Object " <<num<<" deleted"<< endl;
    }
};

int Point::count = 0;

int main() {
    cout<<"Start main"<< endl;
    
    cout<<"\nCreating 3 dynamic objects:"<<endl;
 
    Point* p1 = new Point();
    Point* p2 = new Point();
    Point* p3 = new Point();
    
    cout<<"\nDeleting objects:"<<endl;

    delete p1;
    delete p2;
    delete p3;
    
    cout<<"End main"<<endl;
    
    return 0;
}