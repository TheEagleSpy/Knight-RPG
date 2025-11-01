import random
import time

# Utility function to print text with a delay
def Print(text, delay=0.02):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

# Generate a new random number
def roll_new():
    return random.randint(1, 50)

# Main game logic
def play_higherlower(player_data):
    Print("\nWelcome to Higher or Lower Test Game!")
    Print("A random number will generate between 1 and 50 and you have to guess if the next number will be higher or lower.")
    Print("\nHere's 100 gold to get you started!")  # DEBUGGING
    player_data['gold'] += 100 # DEBUGGING
    
    while True:
        try:
            input_gold = int(input(f"\nHow much gold do you want to bet?\n\nYou have {player_data['gold']} Gold.\nBet: "))
            if input_gold <= 0:
                Print("Bet must be a positive number.")
                continue
            if player_data['gold'] >= input_gold:
                Print(f"\nYou bet {input_gold} gold.")
                current_number = roll_new()
                Print("\n-----Higher Or Lower Game-----")
                Print(f"The starting number is {current_number}.")
                break
            else:
                Print("You do not have enough gold.\n")
        except ValueError:
            Print("Invalid input! Please enter a number.\n")

    gold_multiplier = 1
    
    while True:
        guess = input(f"\nWill the next number be:\n\n[1] Higher\n[2] Lower\nEnter: ").strip()
        if guess not in ['1', '2']:
            Print("Invalid choice! Please type '1' or '2'.\n")
            continue

        next_number = roll_new()

        if (guess == '1' and next_number >= current_number) or \
           (guess == '2' and next_number <= current_number):
            gold_multiplier = round(gold_multiplier + 0.10)  # Round multiplier each time
            Print(f"\nCorrect! Your gold multiplier is now {gold_multiplier}")
                          
            action = input(f"Do you want to take your {gold_multiplier} multiplier on your {round(input_gold, 2)} bet?\n\n[1] Continue Guessing\n[2] Take Winnings\nEnter: ")
            
            if action == '1':
                Print(f"\nThe next number is {next_number}.")
                current_number = next_number
            
            elif action == '2':
                player_data['gold'] = round(player_data['gold'] * gold_multiplier, 0)  # Round after updating gold
                Print(f"\nCongratulations your new gold is {round(player_data['gold'], 0)}")
                break
            else:
                Print(f"\n{action} is not a answer between 1 and 2 so '1' will be pressed by default")
                Print(f"\nThe next number is {next_number}.\n")
                current_number = next_number
                 
        else:
            Print(f"\nThe next number is {next_number}.\n")
            Print(f"Wrong! Game over. You lost {round(input_gold, 2)} gold.\n")
            player_data['gold'] = round(player_data['gold'] - input_gold, 0)  # Round after subtracting gold
            action = input("Do you want to play again?\n[1] Yes\n[2] No\nEnter: ")
            if action == '1':
                play_higherlower(player_data)
            elif action == '2':
                break
            else:
                Print(f"\n{action} is not a answer between 1 and 2 so '1' will be pressed by default")
                play_higherlower(player_data)

# DEBUGGING
def main_player():
    player_data = {
        "gold": 3,  # Starting gold
    }
    return player_data

# DEBUGGING
if __name__ == "__main__":
    player_data = main_player()
    print("Testing: Player starts with", player_data['gold'], "extra gold.")
    play_higherlower(player_data)