import random
import time

def Print(text, delay=0.02):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def roll_new():
    return random.randint(1, 50)

def play_higherlower(player_data, klare_data, difficulty, gold_bet, game_stats):

    # --- Check player balance ---
    if player_data.get("gold", 0) < gold_bet:
        Print("You do not have enough gold to make that bet.")
        return player_data, klare_data, game_stats

    # Deduct upfront
    player_data["gold"] -= gold_bet
    Print(f"\nYou placed a bet of {gold_bet} gold!")

    Print("\n----- Higher or Lower Game -----")
    Print("A random number between 1 and 50 will appear. Guess if the next number will be higher or lower than the 'Current number:'.\n")

    current_number = roll_new()
    Print(f"The starting number is {current_number}.")

    multiplier = 1.0
    rounds_played = 0
    keep_playing = True

    game_stats['minigames_played'] += 1

    while keep_playing:
        guess = input(f"\n--Current number: {current_number}--\nWill the next number be:\n[1] Higher\n[2] Lower\nEnter: ").strip()

        if guess not in ["1", "2"]:
            Print("Invalid input! Please type '1' or '2'.")
            continue

        next_number = roll_new()
        Print(f"\nThe next number is {next_number}.")

        # --- Win condition ---
        if (guess == "1" and next_number >= current_number) or \
           (guess == "2" and next_number <= current_number):

            rounds_played += 1
            multiplier += 0.25
            Print(f"Correct! Multiplier now: x{multiplier:.2f}")

            action = input(f"\nDo you want to keep going or cash out?\n[1] Continue\n[2] Cash Out\nEnter: ").strip()

            game_stats['gambles_won'] += 1

            if action == "2":
                winnings = int(gold_bet * multiplier)
                player_data["gold"] += winnings
                Print(f"\nYou cashed out and won {winnings} gold!")
                keep_playing = False
            else:
                current_number = next_number
                Print("\nContinuing...")

        # --- Lose condition ---
        else:
            Print(f"\nWrong! You lost the round and your {gold_bet} gold.")
            keep_playing = False

            game_stats['gambles_lost'] += 1

        # --- Optional round limits by difficulty ---
        if difficulty.lower() == "easy" and rounds_played >= 13:
            Print("Easy mode round limit reached! Auto cashout.")
            winnings = int(gold_bet * multiplier)
            player_data["gold"] += winnings
            keep_playing = False
        elif difficulty.lower() == "medium" and rounds_played >= 9:
            Print("Medium mode round limit reached! Auto cashout.")
            winnings = int(gold_bet * multiplier)
            player_data["gold"] += winnings
            keep_playing = False
        elif difficulty.lower() == "hard" and rounds_played >= 5:
            Print("Hard mode round limit reached! Auto cashout.")
            winnings = int(gold_bet * multiplier)
            player_data["gold"] += winnings
            keep_playing = False

    Print(f"\nYou now have {player_data['gold']} gold total.")
    return player_data, klare_data, game_stats