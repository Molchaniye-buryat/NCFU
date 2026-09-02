#include <iostream>

using namespace std;

void inputSIZE(int &m, int &n) {
	cout<<"Enter m and n: ";
	cin>>m>>n;
}

void inputMatrix(int M[100][100], int m, int n) {
	for (int i = 0; i < m; i++) {
		for (int j = 0; j < n; j++) {
			cout<<"Element ["<<i<<"]["<<j<<"] = ";
			cin>>M[i][j];
		}
	}
}

void printOrig(int M[100][100], int m, int n) {
	cout<<"ORIG MATRIX"<<endl;
	for (int i = 0; i < m; i++) {
		for (int j = 0; j < n; j++) {
			cout<<M[i][j]<<" ";
		}
		cout<<endl;
	} 
}

void printNotOrig(int M[100][100], int m, int n) {
	cout<<"NOT ORIG MATRIX"<<endl;
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < m; j++) {
			cout<<M[j][i]<<" ";
		}
		cout<<endl;
	} 
}


int main(int argc, char const *argv[])
{
	int m, n;
	int M[100][100];

	inputSIZE(m , n);
	inputMatrix(M, m, n);
	printOrig(M, m, n);
	printNotOrig(M, m, n);

	return 0;
}