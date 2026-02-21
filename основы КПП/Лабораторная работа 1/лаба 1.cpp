/*
#include <iostream>
#include <math.h>
using namespace std;
int main()
{
    double a, b, c, d, s1, s2, s3, y;

    printf("Enter a, b, c, d:\n");
    scanf("%lf%lf%lf%lf", &a, &b, &c, &d);
    
    s1 = pow(sin(c), 3);
    s2 = pow(cos(a), 2);
    s3 = pow(sin(b), d);
    y = (s1*s2)/(5*s3);

    printf("Result y=%lf\n", y);
    system("pause");
}
*/

#include <iostream>
#include <cmath>
using namespace std;
int main()
{
    double a, b, c, d, s1, s2, s3, y;

    cout<<"Enter a, b, c, d:"<<endl;
    cin>>a>>b>>c>>d;
    
    s1 = pow(sin(c), 3);
    s2 = pow(cos(a), 2);
    s3 = pow(sin(b), d);
    y = (s1*s2)/(5*s3);

    cout<<"Result y="<<y<<endl;
}