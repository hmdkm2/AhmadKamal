#include <iostream> 
#include <string>
#include <cstdlib>

using namespace std;

struct Count{
    int choise =0;
    int wins =0;
    int equals =0;
    };

enum Type{ stone = 1, paper = 2, scissor = 3 };

int randomNumbers(int From, int To) {

    // Generate a random number between 0 and (To - From) using rand(),
    // then add From to shift the range to [From, To].
    int random = rand() % (To - From + 1) + From;
    return random;
}

int ReadPositiveNumber(string message) {
    int num = 0;
    do {
        cout << message;
        cin >> num;
    } while (num <= 0);
    return num;
}

void RoundResult(int roundNumber,Count& user, Count& computer) {
    cout << "\n__________________ Round [" << roundNumber << "] __________________\n" << endl;
    switch (user.choise)
    {
    case stone:
        cout << "Player1 choice : Stone" << endl;
        break;
    case paper:
        cout << "Player1 choice : Paper" << endl;
        break;
    case scissor:
        cout << "Player1 choice : Scissor" << endl;
        break;
    default:
        break;
    }
    switch (computer.choise)
    {
    case stone:
        cout << "Computer choice: Stone" << endl;
        break;
    case paper:
        cout << "Computer choice: Paper" << endl;
        break;
    case scissor:
        cout << "Computer choice: Scissor" << endl;
        break;
    default:
        break;
    }

    user.choise = Type(user.choise);
    computer.choise = Type(computer.choise);

    if (user.choise == computer.choise) {
        system("color 6F");
        cout << "Round Winner   : [No Winner] " << endl;
        user.equals += 1;
        computer.equals += 1;
    }
    else if ((user.choise == stone) && (computer.choise == scissor)) {
        system("color 2F");
        cout << "Round Winner   : [Player1] " << endl;
        user.wins += 1;
    }
    else if ((user.choise == paper) && (computer.choise == stone)) {
        system("color 2F");
        cout << "Round Winner   : [Player1] " << endl;
        user.wins += 1;
    }
    else if ((user.choise == scissor) && (computer.choise == paper)) {
        system("color 2F");
        cout << "Round Winner   : [Player1] " << endl;
        user.wins += 1;
    }
    else if ((computer.choise == stone) && (user.choise == scissor)) {
        system("color 4F");
        cout << "\a";
        cout << "Round Winner   : [Computer] " << endl;
        computer.wins += 1;
    }
    else if ((computer.choise == paper) && (user.choise == stone)) {
        system("color 4F");
        cout << "\a";
        cout << "Round Winner   : [Computer] " << endl;
        computer.wins += 1;
    }
    else if ((computer.choise == scissor) && (user.choise == paper)) {
        system("color 4F");
        cout << "\a";
        cout << "Round Winner   : [Computer] " << endl;
        computer.wins += 1;
    }
    cout << "________________________________________________" << endl;
}

void printResult(int rounds, Count user, Count computer) {
    cout << "                ______________________________________________________________________________\n" << endl;
    cout << "                                             +++ G a m e  O v e r +++                           " << endl;
    cout << "                ______________________________________________________________________________\n" << endl;
    cout << "                _________________________________[ Game Results ]_____________________________\n" << endl;

    cout << "                Game Rounds             : " << rounds << endl;
    cout << "                Player1 won times       : " << user.wins << endl;
    cout << "                Computer won times      : " << computer.wins << endl;
    cout << "                Draw times              : " << user.equals << endl;

    if (user.wins > computer.wins) {
        cout << "                Final Winner            : Player1" << endl;
    }
    else if (user.wins < computer.wins) {
        cout << "                Final Winner            : Computer" << endl;
    }
    else {
        cout << "                Final Winner            : No Winner" << endl;
    }
    cout << "                ______________________________________________________________________________\n" << endl;
}

void playingRounds(int rounds,Count & user,Count & computer) {
    for (int i = 1; i <= rounds; i++) {
        cout << "\nRound [" << i << "] begins:\n" << endl;
        cout << "Your Choise: [1]:Stone, [2]:Paper, [3]:Scissor ? ";
        cin >> user.choise;
        computer.choise = randomNumbers(1,3);
        RoundResult(i,user,computer);
    }
    printResult(rounds, user, computer);
}


int main() {

    srand((unsigned)time(NULL));

    bool play = true;
    char playAgain;
    while (play) {
        Count user, computer;
        int rounds = ReadPositiveNumber("How Many Rounds 1 to 10 ?\n");
        playingRounds(rounds, user, computer);
        cout << "                Do you want to play again? Y/N? ";
        cin >> playAgain;
        cout << endl;
        if (playAgain == 'Y' || playAgain == 'y')
        {
            play = true;
        }
        else {
            play = false;
        }
    }

    return 0;
}
