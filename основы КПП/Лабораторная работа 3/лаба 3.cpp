/*
#include <iostream>
#include <cmath>

using namespace std;

int main(int argc, char const *argv[])
{
	double x, eps;
	cout<<"Enter x and eps: ";
	cin>>x>>eps;

	double F = 1.0, a = 1.0;
	int n = 0;

	while (fabs(a) >= eps) {
		n+=2;
		a *= -x * x / ((n-1)*n);
		F+=a;
	}
	cout<<"Approximate cos("<<x<<") = "<<F<<endl;
	cout<<"Exact cos("<<x<<") = "<<cos(x)<<endl;
}
*/

#include <iostream>
#include <cmath>

using namespace std;

int main(int argc, char const *argv[])
{
	double x, eps;
	cout<<"Enter x and eps: ";
	cin>>x>>eps;

	double F = 1.0, a = 1.0;
	int n = 0;

	do {
		n+=2;
		a *= -x * x / ((n-1)*n);
		F+=a;
	} while (fabs(a) >= eps);
	cout<<"Approximate cos("<<x<<") = "<<F<<endl;
	cout<<"Exact cos("<<x<<") = "<<cos(x)<<endl;
}