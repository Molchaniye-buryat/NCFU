#include <iostream>
#include <string>

using namespace std;

int main(int argc, char const *argv[])
{
	string text;
	cout<<"Enter text: ";
	getline(cin, text);

	cout<<"A words: "<<endl;
	string word = "";

	for (int i = 0; i <= text.length(); i++) {
		if (i == text.length() || text[i] == ' ') {
			if (word.length() > 0 && (word[0] == 'A' || word[0] == 'a')) {
				cout<<word<<endl;
			}
			word = "";
		}
		else {
			word += text[i];
		}
	}
}