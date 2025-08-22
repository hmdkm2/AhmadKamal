#include <iostream>
#include <string>
#include <cstdlib>
using namespace std;

enum level { easy = 1, med = 2, hard = 3, mixLevel = 4 };
enum operationType { sum = 1, sub = 2, mul = 3, divop = 4, mixOp = 5 };

struct inforGame {
    int numOfQuestions = 0;
    int numOfRightAnswers = 0;
    int numOfWrongAnswers = 0;
    int levelOfQuestions = 0;
    int operationOfQuestions = 0;
};

int randomNumbers(int From, int To) {
    return rand() % (To - From + 1) + From;
}

int ReadPositiveNumber(string message) {
    int num = 0;
    do {
        cout << message;
        cin >> num;
    } while (num <= 0);
    return num;
}

int generateOperation(int operationOfQuestions) {
    if (operationOfQuestions == mixOp)
        return randomNumbers(1, 4);
    else
        return operationOfQuestions;
}

int generateNumberLevel(int levelOfQuestions) {

    if (levelOfQuestions == easy) {
        return randomNumbers(0, 10);
    }
    else if (levelOfQuestions == med) {
        return randomNumbers(11, 50);
    }
    else if (levelOfQuestions == hard) {
        return randomNumbers(51, 100);
    }
    else
        return randomNumbers(0, 100);
}

void getInformation(inforGame& user) {
    user.levelOfQuestions = ReadPositiveNumber("Enter Questions Level [1] Easy, [2] Med, [3] Hard, [4] Mix ? ");
    user.operationOfQuestions = ReadPositiveNumber("Enter Operation Type [1] Add, [2] Sub, [3] Mul, [4] Div, [5] Mix ? ");
}

bool checkAnswer(int correctAnswer, int userAnswer, inforGame& user) {
    if (correctAnswer == userAnswer) {
        system("color 2F");
        cout << "Correct answer :-)\n";
        user.numOfRightAnswers++;
        return true;
    }
    else {
        system("color 4F");
        cout << "\a";
        cout << "Wrong answer :-(\n" << "The right answer is: " << correctAnswer << endl;
        user.numOfWrongAnswers++;
        return false;
    }
}

string generateLevelWord(int levelOfQuestions) {
    switch (levelOfQuestions) {
    case easy:
        return "Easy";
        break;
    case med:
        return "Med";
        break;
    case hard:
        return "Hard";
        break;
    case mixLevel:
        return "Mix";
        break;
    }
}

string generateOperationWord(int operationOfQuestions) {
    switch (operationOfQuestions) {
    case sum:
        return "Sum";
        break;
    case sub:
        return "Sub";
        break;
    case mul:
        return "Mul";
        break;
    case divop:
        return "Div";
        break;
    case mixOp:
        return "Mix";
        break;
    }
}

void finalResult(inforGame user) {
    if (user.numOfRightAnswers > user.numOfWrongAnswers) {
        system("color 2F");
        cout << "\n\n\n------------------------------" << endl;
        cout << "Final Results is Pass :-)\n";
        cout << "------------------------------" << endl;
    }
    else if (user.numOfRightAnswers < user.numOfWrongAnswers) {
        system("color 4F");
        cout << "\a";
        cout << "\n\n\n------------------------------" << endl;
        cout << "Final Results is Fail :-(\n";
        cout << "------------------------------" << endl;
    }
    else {
        system("color 6F");
        cout << "\n\n\n------------------------------" << endl;
        cout << "Final Results is Equal :-|\n";
        cout << "------------------------------" << endl;
    }
    cout << "Number Of Questions: " << user.numOfQuestions << endl;
    cout << "Operations level: " << generateLevelWord(user.levelOfQuestions) << endl;
    cout << "Operations Type: " << generateOperationWord(user.operationOfQuestions) << endl;
    cout << "Number of Right answers: " << user.numOfRightAnswers << endl;
    cout << "Number of Wrong answers: " << user.numOfWrongAnswers << endl;
    cout << "------------------------------" << endl;
}

void answeringQuestions(inforGame& user) {
    int firstNum, secondNum, result, userAnswer, op;

    for (int i = 1; i <= user.numOfQuestions; i++) {
        cout << "\nQuestion [" << i << "/" << user.numOfQuestions << "]" << endl;

        firstNum = generateNumberLevel(user.levelOfQuestions);
        secondNum = generateNumberLevel(user.levelOfQuestions);
        op = generateOperation(user.operationOfQuestions);
        switch (op) {
        case sum:
            cout << firstNum << " + " << secondNum << " = ";
            result = firstNum + secondNum;
            break;
        case sub:
            cout << firstNum << " - " << secondNum << " = ";
            result = firstNum - secondNum;
            break;
        case mul:
            cout << firstNum << " * " << secondNum << " = ";
            result = firstNum * secondNum;
            break;
        case divop:
            while (secondNum == 0)
                secondNum = generateNumberLevel(user.levelOfQuestions);
            cout << firstNum << " / " << secondNum << " = ";
            result = firstNum / secondNum;
            break;
        }
        cin >> userAnswer;
        checkAnswer(result, userAnswer, user);
    }
}

void StartGame() {
    char playAgain = 'Y';
    do {
        inforGame user;
        user.numOfQuestions = ReadPositiveNumber("How Many Questions do you want to answer? ");
        getInformation(user);
        answeringQuestions(user);
        finalResult(user);
        cout << endl;
        cout << "Do you want to play again? Y/N? ";
        cin >> playAgain;
        cout << endl;
    } while (playAgain == 'Y' || playAgain == 'y');
}

int main() {
    srand((unsigned)time(NULL));
    StartGame();
    return 0;
}
