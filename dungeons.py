import time
import random
from twentyone import play_21
from higherlower import play_higherlower
from rps import start_rps

def Print(text, delay=0.02):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def determine_difficulty():
    roll = random.randint(1, 100)
    if roll <= 45:
        return "Easy", random.choice(["Tomas the Timid", "Lazy Luke", "Beginner Bob"])
    elif roll <= 80:
        return "Medium", random.choice(["Grumpy Greg", "Strategic Steve", "Midrange Max"])
    else:
        return "Hard", random.choice(["Vicious Valen", "Cruel Cassandra", "Unforgiving Ulric"])

def get_random_game():
    game = random.choice(["21", "HigherLower", "RPS"])
    if game == "21":
        return play_21, "21 Card Game", True
    elif game == "HigherLower":
        return play_higherlower, "Higher or Lower", False
    else:
        return start_rps, "Rock Paper Scissors", False

def dungeons(player_data, dungeons_reason):
    Print("[Knight] Well... What do I do now???")
    time.sleep(1)

    escape_cost = 2000 if dungeons_reason == 'queen' else 1000

    while True:
        Print("\n--- DUNGEON MENU ---")
        Print(f"You have {player_data['gold']} gold.")
        Print("[1] Play a minigame for your freedom")
        Print(f"[2] Pay {escape_cost} gold to escape")
        Print("[3] Give up")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            while True:
                try:
                    bet = int(input("Enter how much gold you'd like to bet: "))
                    if bet <= 0:
                        Print("You must bet at least 1 gold.")
                    elif bet > player_data['gold']:
                        Print("You don't have that much gold.")
                    else:
                        break
                except ValueError:
                    Print("Please enter a valid number.")

            while True:
                difficulty, enemy_name = determine_difficulty()
                minigame_func, game_name, needs_data = get_random_game()

                Print(f"\nYou are about to play **{game_name}** against {enemy_name} ({difficulty} difficulty).")
                Print("[1] Play this match")
                Print("[2] Skip for 100 gold")

                match_choice = input("Choose: ").strip()
                if match_choice == "2":
                    if player_data['gold'] >= 100:
                        player_data['gold'] -= 100
                        Print("You paid 100 gold to skip. Rerolling opponent and game...")
                        time.sleep(1)
                        continue
                    else:
                        Print("You don't have enough gold to skip.")
                        continue
                elif match_choice == "1":
                    break
                else:
                    Print("Invalid input.")

            # Call the minigame with correct args
            if needs_data:
                result = minigame_func(difficulty=difficulty, enemy_name=enemy_name, gold_bet=bet, player_data=player_data)
            else:
                result = minigame_func(difficulty=difficulty, enemy_name=enemy_name)

            if result == "win":
                reward = int(bet * 1.5)
                player_data['gold'] += reward
                Print(f"You defeated {enemy_name}! You won {reward} gold.")
            else:
                player_data['gold'] -= bet
                Print(f"You lost to {enemy_name}... You lost {bet} gold.")

            if player_data['gold'] <= 0:
                Print("You're out of gold. You remain in the dungeon...")
                break

        elif choice == '2':
            if player_data['gold'] >= escape_cost:
                player_data['gold'] -= escape_cost
                Print(f"You paid {escape_cost} gold and escaped the dungeon!")
                break
            else:
                Print("You don't have enough gold to escape.")

        elif choice == '3':
            Print("You gave up... and rot in the dungeon forever.")
            break
        else:
            Print("Invalid choice. Try again.")

if __name__ == "__main__":
    player_data = {
        'gold': 1500,
    }

    dungeons_reason = 'queen'
    dungeons(player_data, dungeons_reason)