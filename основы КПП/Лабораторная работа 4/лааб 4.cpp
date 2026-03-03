#include <iostream>
#include <cmath>

using namespace std;
int main(int argc, char const *argv[])
{
 	const int SIZE = 15;
 	int arr[SIZE];
 	int cnt = 0;

 	for (int i = 0; i < SIZE; i++) {
 		cout<<"Ellement: "<<i+1<<": ";
 		cin>>arr[i];
 	}
 	cout<<"----------------------"<<endl;
 	for (int i = 0; i < SIZE; i++) {
 		if (arr[i]%2 == 0) {
 			cnt++;
 		}
 		if (arr[i] >= 1 && arr[i] <= 11 && arr[i] % 2 != 0) {
 			int orig = arr[i];
 			arr[i] = pow(orig, 2);
 			cout<<"Ellement: "<<orig<<"^2 = "<<arr[i]<<endl;
 		}
 	}

 	cout<<"Count: "<<cnt<<endl;
 	cout<<"Result: [";
 	for (int i = 0; i < SIZE; i++) {
 		cout<<arr[i]<<" ";

 	}
 	cout<<"]";
}