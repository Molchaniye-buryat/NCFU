/*
#include <iostream>

using namespace std;

int main(int argc, char const *argv[])
{
	const int SIZE = 10;
	int arr[SIZE];
	int cnt = 0;

	cout<<"Enter "<<SIZE<<" integers:";
	for (int i = 0; i < SIZE; i++) {
		cin>>arr[i];
		if (arr[i] % 2 == 0) {
			cnt++;
		}
	}
	cout<<"Result: "<<cnt<<endl;
}
*/

/*
#include <iostream>
#include <iomanip>

using namespace std;

int main(int argc, char const *argv[])
{
	int matrix[4][4];
	int cnt = 0;

	cout<<"Enter Matrix 4x4: "<<endl;
	for (int i = 0; i < 4; i++) {
		for (int j = 0; j < 4; j++) {
			cin>>matrix[i][j];
		}
	}
	for (int i = 0; i < 4; i++){
		for (int j = 0; j < 4; j++) {
			cout<<setw(5)<<matrix[i][j]<<" ";
		}

		cout<<endl;
	}
	for (int i = 0; i < 4; i++) {
		for (int j = 0; j < 4; j++) {
			if (matrix[i][j] == 0) {
				cnt++;
			}
		}
	}
	cout<<"Result: "<<cnt<<endl;
}
*/

#include <iostream>
#include <string>

using namespace std;

int main(int argc, char const *argv[])
{
	string text;
	int cnt = 1;
	cout<<"Massage: ";
	getline(cin, text);

	for (int i = 0; i < text.length(); i++) {
		if (text[i] == ' ') {
			cnt ++;
		}
	}
	cout<<"Words: "<<cnt<<endl;
}