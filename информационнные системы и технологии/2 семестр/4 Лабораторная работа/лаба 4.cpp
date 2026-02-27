/*
#include <iostream>
#include <cmath>

using namespace std;

int main(int argc, char const *argv[])
{
	int a, V;
	int* pa = &a;
	int* pV = &V;

	cout<<"Enter the len: ";
	cin>>*pa;

	*pV = pow(*pa, 3);

	cout<<"V = "<<*pV<<endl;
}
*/
/*
#include <iostream>

using namespace std;

int main(int argc, char const *argv[])
{
	int N = 8;
	int arr[N];
	int* ptr = arr;
	int* minptr = arr;

	cout<<"Enter "<<N<<" elements:";
	for (int i = 0; i<N; i++) {
		cin>>*(ptr + i);
	}

	for (int i = 1; i < N; i++) {
		if (*(ptr + i) < *minptr) {
			minptr = ptr + i;
		}
	}

	cout<<"Min: "<<*minptr<<endl;
}
*/

#include <iostream>

using namespace std;

int main(int argc, char const *argv[])
{
	int N = 5;
	int arr[N] = {10, 20, 30, 40, 50};
	int* ptr = arr;

	for (int i = 0; i < N; i++) {
		cout<<"arr["<<i<<"] ("<<ptr + i<<") ->";
		cout<<" arr["<<i+1<<"] ("<<ptr + i + 1<<"): ";
		cout<<(char*)(ptr + i + 1) - (char*)(ptr + i)<<" bytes"<<endl;
	}
}





