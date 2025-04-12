# rock-paper-scissors game

import random

user_score = 0
computer_score = 0

while True:
    user_input = input("Enter your choice (rock, paper, scissors): ").lower()
    computer_input = random.choice(["rock", "paper", "scissors"])

    print("Computer chose:", computer_input)
    print("You chose:", user_input)

    if user_input == computer_input:
        print("It's a tie!")
        
    elif user_input == "rock":
        if computer_input == "scissors": 
            print("You win!")
            user_score += 1
        else:
            print("You lose!")
            computer_score += 1
    elif user_input == "paper":
        if computer_input == "rock":
            print("You win!")
            user_score += 1
        else:
            print("You lose!")
            computer_score += 1
    elif user_input == "scissors":
        if computer_input == "paper":
            print("You win!")
            user_score += 1
        else:
            print("You lose!")
            computer_score += 1
    else:
        print("Invalid input! Please enter rock, paper, or scissors.")

    print("YOUR Score:", user_score)
    print("COMPUTER Score:", computer_score)

    play_again = input("Do you  want to play another round (y/n): ").lower()
    if play_again != "y":
        if user_score > computer_score:
            print("Congratulations! You won the game!")
        elif user_score < computer_score:
            print("Sorry! You lost the game.")
        elif user_score == computer_score:
            print("It's a tie game!")
        else:
            print("Thanks for playing!")
        break
