/*
#include <iostream>
#include <ctime>

using namespace std;

void fillArray(int* arr, int size) {
	for (int i = 0; i < size; i++) {
		arr[i] = rand()%100;
	}
}

int multy(int* arr, int size) {
	int a = 1;
	for (int i = 0; i < size; i++) {
		a *= arr[i];
	}
	return a;
}

int main(int argc, char const *argv[]) {
	srand(time(0));
	int n;

	cout<<"Enter size: ";
	cin>>n;

	int* myArray = new int[n];
	fillArray(myArray, n);

	for (int i = 0; i < n; i++) {
		cout<<myArray[i]<<" ";
	}
	cout<<endl;

	int totalPr = multy(myArray, n);
	cout<<"Result: "<<totalPr<<endl;

	delete[] myArray;

	return 0;
}
*/
/*
#include <iostream>

using namespace std;

int factorial(int n) {
	if (n<=1) {
		return 1;
	}
	return n*factorial(n-1);
}

int power(int x, int n) {
	if (n == 0) {
		return 1;
	}
	return x*power(x, n-1);
}

double res(int x, int n) {
	return x*power(x, n) / factorial(n);
}

int main(int argc, char const *argv[])
{
	int x, n;

	cout<<"Enter x, n: ";
	cin>>x>>n;

	cout<<"(x^n) / n! = "<<res(x, n)<<endl;


	return 0;
}
*/

#include <iostream>
#include <ctime>

using namespace std;

int main(int argc, char const *argv[])
{
	srand(time(0));

	int n;
	cout<<"Enter size: ";
	cin>>n;

	int* arr1 = new int[n];
	for (int i = 0; i < n; i++) {
		arr1[i] = rand()%200;
		cout<<arr1[i]<<" ";
	}
	cout<<endl;

	int cnt = 0;
	for (int i = 0; i < n; i++) {
		if (arr1[i] >= 10 && arr1[i] <= 99) {
			cnt++;
		}
	}

	if (cnt > 0) {
		int* arr2 = new int[cnt];
		int index = 0;

		for (int i = 0; i < n; i++) {
			if (arr1[i] >= 10 && arr1[i] <= 99) {
				arr2[index] = arr1[i];
				index++;				
			}
		}
		cout<<"Result: ";
		for (int i = 0; i < cnt; i++) {
			cout<<arr2[i]<<" ";
		}
		delete[] arr2;
	}

	else {
		cout<<"No 2-digit numbers"<<endl;
	}

	delete[] arr1;
	return 0;
}