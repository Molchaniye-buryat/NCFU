#include <iostream>

using namespace std;
int main(int argc, char const *argv[])
{
	int m, n;

	cout<<"Enter m and n: ";
	cin>>m>>n;

	int M[m][n];

	for (int i = 0; i < m; i++) {
		for (int j = 0; j < n; j++) {
			cout<<"Ellement: ["<<i<<"]["<<j<<"]: ";
			cin>>M[i][j];
		}
	}
	cout<<"Original Matrix"<<endl;
	for (int i = 0; i < m; i++) {
		for (int j = 0; j < n; j++) {
			cout<<M[i][j]<<" ";
		}
		cout<<endl;
	}

	cout<<"Not original Matrix"<<endl;
	for (int i = 0; i < m; i++) {
		for (int j = 0; j < n; j++) {
			cout<<M[j][i]<<" ";
		}
		cout<<endl;
	}
}