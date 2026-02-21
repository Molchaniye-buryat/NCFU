#include <iostream>

using namespace std;

int main(int argc, char const *argv[])
{

	double x, y;
	cout<<"Enter x and y: ";
	cin>>x>>y;

	if (y>=0 && y<=0.8 && x*x+y*y<1) {
		cout<<"Inside"<<endl;
	}
	else if (y<0 || y>0.8 || x*x+y*y>1){
		cout<<"Outside"<<endl;
	}
	else {
		cout<<"On the border"<<endl;
	}
}