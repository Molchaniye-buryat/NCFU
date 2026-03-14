/*
#include <iostream>
#include <cmath>

using namespace std;

class Point2D
{
private:
    double x;
    double y;
public:
    Point2D(double xCoord = 0.0, double yCoord = 0.0) : x(xCoord), y(yCoord) {}

    void init(double xCoord, double yCoord) {
        x = xCoord;
        y = yCoord;
    }

    void moveTo(double newX, double newY) {
        x = newX;
        y = newY;
        cout<<"Point moved to ("<<x<<", "<<y<<")"<<endl;
    }

    double distanceToOrigin() {
        return sqrt(pow(x, 2) + pow(y, 2));
    }

    void display() {
        cout<<"Point coordinates ("<<x<<", "<<y<<")"<<endl;
    }
};

int main(int argc, char const *argv[])
{
    Point2D point;
    point.init(3.0, 4.0);
    point.display();
    cout<<"Distance to origin: "<<point.distanceToOrigin()<<endl;
    point.moveTo(5.0, 12.0);
    cout<<"----------------"<<endl;
    cout<<"After moving: ";
    point.display();
    cout<<"Distance to origin: "<<point.distanceToOrigin();

    return 0;
}
*/

#include <iostream>
#include <cmath>

using namespace std;

class Point2D
{
private:
    double x, y;
public:
   void inputPoint(int num) {
    cout<<"Point ("<<num<<") - enter x and y : ";
    cin>>x>>y;
   }

   double distanceToOrigin() {
    return sqrt(pow(x, 2) + pow(y, 2));
   }

   void display() {
    cout<<"("<<x<<", "<<y<<")";
   }

};

int main(int argc, char const *argv[])
{   
    const int SIZE = 3;
    Point2D points[SIZE];

    for (int i = 0; i < SIZE; i++) {
        points[i].inputPoint(i+1);
    }

    int nearest = 0;
    double minDistance = points[0].distanceToOrigin();

    for (int i = 0; i < SIZE; i++) {
        double dist = points[i].distanceToOrigin();
        if (dist < minDistance) {
            minDistance = dist;
            nearest = i;
        }
    }
    cout<<"Nearest point: ";
    points[nearest].display();
    cout<<" with distance: "<<minDistance<<endl;

    return 0;
}