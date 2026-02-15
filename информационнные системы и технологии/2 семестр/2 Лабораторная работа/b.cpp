/*
#include <iostream>
#include <cmath>

using namespace std;

int main(int argc, char const *argv[])
{
	double x, y;

	cout<<"Enter x:"<<endl;
	cin>>x;

	if (x<0){
		y = sin(x) + cos(x);
	}
	else if (x>=0 && x<5){
		y = pow(x, 2) - 4;
	}
	else {
		y = sqrt(x);
	}

	cout<<"Result:"<<y<<endl;
	return 0;
}
*/

/*
#include <iostream>
#include <cmath>
#include <iomanip>

using namespace std;

int main(int argc, char const *argv[])
{
	double a = 1, b = 4, h = 0.3, x;
	cout<<setw(10)<<"x"<<setw(15)<<"f(x)"<<endl;

	for (x = a; x <= b + h/10; x+=h){
		double f = sqrt(x)*cos(x);
		cout<<fixed<<setw(10)<<x<<setw(15)<<f<<endl;
	}
	
	return 0;
}
*/

/*
#include <iostream>

using namespace std;

int main(int argc, char const *argv[])
{
	int n;
	double sum = 0;
	int i = 1;
	cout<<"Enter n:"<<endl;
	cin>>n;

	while (i<=n){
		sum+=(i/(i+1.0));
		i+=1;
	}
	cout<<fixed<<sum<<endl;

	return 0;
}

*/

