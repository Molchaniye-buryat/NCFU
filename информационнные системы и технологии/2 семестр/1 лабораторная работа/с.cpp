#include <iostream>
#include <iomanip>
#include <cmath>

using namespace std;

int main()
{
	int a;
	int constanta = 16;
	cout<<"Number a:"<<endl;
	cin>>a;
	double r = (a*constanta)+(a%(5));
	cout<<"Result:"<<r<<endl;
}
