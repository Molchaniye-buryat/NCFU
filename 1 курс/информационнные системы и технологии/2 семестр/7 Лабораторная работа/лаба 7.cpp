#include <iostream>
#include <string>

using namespace std;

enum Genre {ACTION, RPG, STRATEGY, SPORT};

struct Game
{
    string title;
    Genre genreType;
    int year;
    string developer;
};

int main(int argc, char const *argv[])
{
    Game myGame;
    cout<<"Enter game name: ";
    cin>>myGame.title;

    int genreChoice;
    cout<<"Choose genre (0 - Action, 1 - RPG, 2 - Strategy, 3 - Sport): ";
    cin>>genreChoice;
    myGame.genreType = static_cast<Genre>(genreChoice);

    cout<<"Enter year: ";
    cin>>myGame.year;

    cout<<"Enter developer: ";
    cin>>myGame.developer;

    cout<<endl;
    cout<<"GAME INFORMATION"<<endl;
    cout<<"Title: "<<myGame.title<<" | ";

    if (myGame.genreType == ACTION) cout<<"Genre: Action";
    else if (myGame.genreType == RPG) cout<<"Genre: RPG";
    else if (myGame.genreType == STRATEGY) cout<<"Genre: Strategy";
    else if (myGame.genreType == SPORT) cout<<"Genre: Sport";

    cout<<" | Year: "<<myGame.year;
    cout<<" | Developer: "<<myGame.developer<<endl;

    return 0;
}
```

/*
#include <iostream>
#include <string>

using namespace std;

enum Genre {ACTION, RPG, STRATEGY, SPORT};

string GenreString(Genre genre)
{
    if (genre == ACTION) return "Action";
    else if (genre == RPG) return "Genre: RPG";
    else if (genre == STRATEGY) return "Genre: Strategy";
    else if (genre == SPORT) return "Genre: Sport";
}

struct Game
{
    string title;
    Genre genre;
    int year;
    string developer;
    double rating;
};

int main(int argc, char const *argv[])
{
    const int SIZE = 5;
    Game games[SIZE];

    cout<<"Enter data for 5 games: "<<endl;
    for (int i = 0; i < SIZE; i++) {
        cout<<"Game ("<<i+1<<") ";
        cout<<"Title: ";
        cin>>games[i].title;

        int genreChoice;
        cout<<"Choose genre (0 - Action, 1 - RPG, 2 - Strategy, 3 - Sport): ";
        cin>>genreChoice;
        games[i].genre = static_cast<Genre>(genreChoice);

        cout<<"Enter year: ";
        cin>>games[i].year;

        cout<<"Enter developer: ";
        cin>>games[i].developer;

        cout<<"Enter rating (1-10): ";
        cin>>games[i].rating;
    }

    
    int needRate;
    cout<<"------SEARCH FOR GAME------"<<endl;
    cout<<"Enter rating: ";
    cin>>needRate;
    cout<<" "<<endl;

    cout<<"------GAMES------"<<endl;
    cout<<"-----------------"<<endl;
    for (int i = 0; i < SIZE; i++) {
        if (games[i].rating >= needRate) {
            cout<<"#"<<games[i].title<<" ("<<GenreString(games[i].genre)
                <<", "<<games[i].year<<") by "<<games[i].developer
                <<" | Rating: "<<games[i].rating<<endl;
        }
    }

    return 0;
}
*/