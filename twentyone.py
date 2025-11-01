import random
import time

# Utility function to print text with a delay
def Print(text, delay=0.02):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

# Shows known player and villager cards
def show_cards(player_cards, villager_cards, target_score, inventory):
    Print("\n----- Cards -----")
    print(f"Your Cards: {', '.join(map(str, player_cards))} (Total: {sum(player_cards)})")
    
    # Calculate total of revealed villager cards
    revealed_villager_total = sum(villager_cards[1:])
    print(f"Villager's Cards: {', '.join(['??'] + [str(card) for card in villager_cards[1:]])} (Total: {revealed_villager_total})")
    
    print(f"\nTarget Score: {target_score}")
    print(f"Your Trump Cards: {', '.join(inventory) if inventory else 'None'}")

# Function to handle trump  cards for player
def trump_cards(inventory, target_score):
    if not inventory:
        Print("You don't have any trump cards!")
        return target_score

    Print("Your trump cards:")
    for idx, card in enumerate(inventory, 1):
        Print(f"[{idx}] {card}")

    choice = input("Choose a trump card to use (or press Enter to skip): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(inventory):
        selected_card = inventory.pop(int(choice) - 1)
        if "17" in selected_card:
            Print("You used 'Change Target to 17'!")
            target_score = 17
        elif "24" in selected_card:
            Print("You used 'Change Target to 24'!")
            target_score = 24
    else:
        Print("No trump card used.")

    return target_score

# Function to draw 2 trump cards for both player and villager
def draw_trump_cards():
    trump_cards = ['17', '24']
    return random.sample(trump_cards, 2)

# Main game function
def play_21():
    Print("-----Welcome to the 21 Minigame Test!-----\n")
    Print("\n-----21 Game-----")
    # Initialize scores
    player_wins = 0
    villager_wins = 0

    # Play rounds until one side wins 3 games
    while player_wins < 3 and villager_wins < 3:
        target_score = 21

        # Reset regular cards and initialize new round
        available_cards = list(range(1, 14))
        player_cards = []
        villager_cards = []

        # Draw trump cards for player and villager
        player_trump_cards = draw_trump_cards()
        villager_trump_cards = draw_trump_cards()

        Print(f"Starting a new round!")
        Print("\n-----Drawing Trump Cards-----")
        Print(f"\nYou draw two trump cards: {', '.join(player_trump_cards)}.")
        {', '.join(villager_trump_cards)}

        # Draw initial regular cards
        player_cards.append(random.choice(available_cards))
        available_cards.remove(player_cards[-1])
        
        villager_cards.append(random.choice(available_cards))
        available_cards.remove(villager_cards[-1])

        Print("\n-----Drawing Hidden Card-----")
        Print(f"\nYou draw your hidden card: {player_cards[0]}")
        Print(f"\nThe villager draws their hidden card: ??")

        player_stands = False
        villager_stands = False

        while not (player_stands and villager_stands):
            
            # Player's turn
            if not player_stands:
                Print("\n[1] Draw\n[2] Stand\n[3] Show Cards\n[4] Use Trump Card")
                choice = input("Enter: ").strip()

                if choice == "1":
                    if available_cards:
                        new_card = random.choice(available_cards)
                        player_cards.append(new_card)
                        available_cards.remove(new_card)
                        Print(f"\nYou draw a {new_card}!")
                        villager_stands = False
                    else:
                        Print("No more cards available in the deck!")
                    if sum(player_cards) > target_score:
                        Print("You are currently over the target score")
                        
                elif choice == "2":
                    player_total = sum(player_cards)  # Calculate the total
                    Print(f"\nYou stand with a total of {player_total}")
                    player_stands = True

                elif choice == "3":
                    show_cards(player_cards, villager_cards, target_score, player_trump_cards)
                    continue
                
                elif choice == "4":
                    target_score = trump_cards(player_trump_cards, target_score)
                    
                else:
                    Print("Invalid choice. Please select 1, 2, 3, or 4.")
                    continue

            # Villager's turn
            if not villager_stands:
                if sum(villager_cards) < 17:
                    if available_cards:
                        new_card = random.choice(available_cards)
                        villager_cards.append(new_card)
                        available_cards.remove(new_card)
                        Print(f"The villager draws a {new_card}!")
                        player_stands = False
                    else:
                        Print("No more cards available in the deck!")
                else:
                    Print("\nThe villager stands.")
                    villager_stands = True

        # Show final hands
        Print("\nFinal hands:")
        Print(f"Your Cards: {', '.join(map(str, player_cards))} (Total: {sum(player_cards)})")
        Print(f"Villager's Cards: {', '.join(map(str, villager_cards))} (Total: {sum(villager_cards)})")

        # Determine the winner of the round
        player_total = sum(player_cards)
        villager_total = sum(villager_cards)

        # Both over the target score
        if player_total > target_score and villager_total > target_score:
            if abs(player_total - target_score) < abs(villager_total - target_score):
                Print("You were both over but you were closer to the target score! You win!")
                player_wins += 1
                
            elif abs(villager_total - target_score) < abs(player_total - target_score):
                Print("You were both over but the villager was closer to the target score! They win!")
                villager_wins += 1
                
            else:
                Print("You were both over and had the same score... It's a tie!")

        # One over the target score
        elif player_total > target_score:
            Print("You went over! The villager wins this round.")
            villager_wins += 1
            
        elif villager_total > target_score:
            Print("The villager went over! You win this round.")
            player_wins += 1

        # Exact target score
        elif player_total == target_score:
            Print(f"You got exactly {target_score} and won!")
            player_wins += 1
            
        elif villager_total == target_score:
            Print(f"The villager got exactly {target_score} and won!")
            villager_wins += 1

        # Both under the target score
        elif player_total < target_score and villager_total < target_score:
            
            if abs(target_score - player_total) < abs(target_score - villager_total):
                Print(f"You were closer to {target_score} and won!")
                player_wins += 1
                
            elif abs(target_score - villager_total) < abs(target_score - player_total):
                Print(f"The villager was closer to {target_score} and won!")
                villager_wins += 1
                
            else:
                Print("You both had the same score... It's a draw!")

        # Both have equal scores
        elif player_total == villager_total:
            Print("You both had the same score... Therefore the game is a draw")
 
        # Restarts game if there is a score error
        else:
            Print("An error has occured and the game is restarting")
            play_21()
            
            
        # Show current score
        Print(f"Score: You {player_wins} - {villager_wins} Villager\n")

    # End of game
    Print("Game Over!")
    if player_wins > villager_wins:
        Print("Congratulations! You win the best of 5!")
        action = input("Do you want to play again?\n\n[1] Yes\n[2] No Thanks\nEnter: ")
        if action == '1':
            play_21()
        elif action == '2':
            Print("\n-----Town----")
    else:
        Print("The villager wins the best of 5. Better luck next time!")
        Print("-----Main Game-----")

# Start the game
if __name__ == "__main__":
    play_21()