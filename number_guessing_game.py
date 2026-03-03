import random
import time

def start_game():
    print("\nWelcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    
    print("\nPlease select the difficulty level:")
    print("1. Easy (10 Chances)")
    print("2. Medium (5 Chances)")
    print("3. Hard (3 Chances)")
    
    while True:
        choice = input("\nEnter you choice (1, 2, or 3):")
        if choice  =="1":
            chances = 10
            level = "Easy"
            break
        elif choice =="2":
            chances = 5
            level = "Medium"
            break
        elif choice == "3":
            chances = 3
            level = "Hard"
            break
        else:
            print("Invalid choice. Please pick 1, 2, or 3.")
            
    print(f"\n Great! You have selected the {level} difficulty level.")
    print("Let's start the game!")
    
    secret_number = random.randint(1, 100)
    attempts = 0
    start_time = time.time()
    
    while attempts < chances:
        try:
            guess = int(input("\nEnter your guess: "))
        except ValueError:
            print("Please enter a valid number.")
            continue
        
        attempts += 1
        
        if guess == secret_number:
            end_time = time.time()
            time_taken = round(end_time - start_time, 2)
            print(f"Congratulations! You guessed the correct number in {attempts} attempts.")
            print(f"It took you {time_taken} seconds.")
            return attempts
        elif guess < secret_number:
            print(f"Incorrect! The number is greater than {guess}.")
        else:
            print(f"Incorrect! The number is less than {guess}.")
            
        remaining = chances - attempts
        if remaining > 0:
            print(f"You have {remaining} chances left.")
    print(f"\n Game Over! You've run out of chances. The number was {secret_number}.")
    return None
def main():
    high_score = float('inf')
    
    while True:
        score = start_game()
        
        if score and score < high_score:
            high_score = score
            print(f"New High Score! Fewest attempts: {high_score}")
            
        play_again = input("\nDo you want to play again? (yes/no): ").lower()
        if play_again != 'yes' and play_again != 'y':
            print("Thanks for playing! Goodbye.")
            break
        
if __name__ == "__main__":
    main()