import random
from collections import deque
import time

difficulty = 0
rounds = 0
player_history = deque(maxlen=5)  # Store last 5 moves
ai_rounds = 0  # Track rounds for AI drawing first 2 rounds
show_prediction = False # Show what AI thinks

def Print(text, delay=0.02): #0.02
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def play_rps(player_data, klare_data, difficulty, gold_bet, enemy_name, game_stats):
    # --- Check funds ---
    if player_data.get("gold", 0) < gold_bet:
        Print("You do not have enough gold to make that bet.")
        return player_data, klare_data, game_stats

    # Deduct the bet
    player_data["gold"] -= gold_bet
    Print(f"You placed a bet of {gold_bet} gold against {enemy_name}!")

    # --- Setup ---
    rounds = 5 if difficulty.lower() == "easy" else 7 if difficulty.lower() == "medium" else 11
    player_history.clear()
    playerscore = 0
    enemyscore = 0

    Print(f"\nDifficulty: {difficulty.capitalize()} | Best of {rounds}\n")

    choices = ["Rock", "Paper", "Scissors"]

    # --- Game Loop ---
    while rounds > 0:
        Print(f"\n-----Rounds left: {rounds}-----")

        predicted_move = predict_player_move()
        enemyrps = counter_move(predicted_move)

        playerrps = input("\nWhat will you pick? (Rock, Paper, Scissors): ").capitalize()
        if playerrps in ["R", "P", "S"]:
            playerrps = {"R": "Rock", "P": "Paper", "S": "Scissors"}[playerrps]
        if playerrps not in choices:
            Print("Invalid choice! Please enter Rock, Paper, or Scissors.")
            continue

        player_history.append(playerrps)
        Print(f"\nYou picked {playerrps} and {enemy_name} picked {enemyrps}!")

        # --- Determine Round Result ---
        if playerrps == enemyrps:
            Print("\nIt's a tie!")
        elif (playerrps == "Rock" and enemyrps == "Scissors") or \
             (playerrps == "Paper" and enemyrps == "Rock") or \
             (playerrps == "Scissors" and enemyrps == "Paper"):
            Print("\nYou win this round!")
            playerscore += 1
        else:
            Print("\nYou lose this round!")
            enemyscore += 1

        rounds -= 1
        print("\n------------------------------------------------------\n")

    # --- End of Match ---
    if playerscore > enemyscore:
        Print(f"You win the match! {playerscore}-{enemyscore}")
        player_data["gold"] += gold_bet * 2
        Print(f"You earn {gold_bet * 2} gold!")
        game_stats['gambles_won'] += 1

        diff_key = f"{difficulty.lower()}_beaten"
        if diff_key in klare_data and enemy_name not in klare_data[diff_key]:
            klare_data[diff_key].append(enemy_name)

    elif playerscore == enemyscore:
        Print(f"It's a draw! {playerscore}-{enemyscore}")
        player_data["gold"] += gold_bet  # refund
        Print(f"You get your {gold_bet} gold back.")
    else:
        Print(f"You lost the match. {enemyscore}-{playerscore}")
        Print(f"You lose your {gold_bet} gold.")
        game_stats['gambles_lost'] += 1

    game_stats['minigames_played'] += 1

    return player_data, klare_data, game_stats

def predict_player_move():
    if difficulty == "Easy":
        return random.choice(["Rock", "Paper", "Scissors"])  # Easy mode: pick randomly

    if difficulty == "Hard":
        # Hard Logic
        if len(player_history) < 2:
            return random.choice(["Rock", "Paper", "Scissors"])  # Pick randomly for first 2 guesses

        last_move = player_history[-1]
        second_last_move = player_history[-2]

        # **Pattern Recognition**
        if len(player_history) >= 3 and player_history[-3] == last_move == second_last_move:
            return random.choice(["Rock", "Paper", "Scissors"])

        if second_last_move == "Rock" and last_move == "Paper":
            return "Scissors"
        if second_last_move == "Paper" and last_move == "Scissors":
            return "Rock"
        if second_last_move == "Scissors" and last_move == "Rock":
            return "Paper"

        if last_move == second_last_move:
            return counter_move(last_move)

        return random.choice(["Rock", "Paper", "Scissors"])  # Fallback random choice

    if difficulty == "All Out":
        # Use advanced strategy for All Out mode
        if len(player_history) < 2:
            return random.choice(["Rock", "Paper", "Scissors"])  # Pick randomly for first 2 guesses
        
        last_move = player_history[-1]
        second_last_move = player_history[-2]

        # **Pattern Recognition for All Out Mode**
        if len(player_history) >= 3 and player_history[-3] == last_move == second_last_move:
            return random.choice(["Rock", "Paper", "Scissors"])

        if second_last_move == "Rock" and last_move == "Paper":
            return "Scissors"
        if second_last_move == "Paper" and last_move == "Scissors":
            return "Rock"
        if second_last_move == "Scissors" and last_move == "Rock":
            return "Paper"

        if last_move == second_last_move:
            return counter_move(last_move)

        # Advanced strategy for All Out mode
        if random.random() < 0.2:
            return last_move  # Try to draw based on last move (20% chance)

        # Analyze frequency of moves in player history
        move_frequency = {
            "Rock": player_history.count("Rock"),
            "Paper": player_history.count("Paper"),
            "Scissors": player_history.count("Scissors")
        }

        if move_frequency["Scissors"] < 2:
            return "Rock"  # Scissors is least played, so Rock counters it
        if move_frequency["Rock"] < 2:
            return "Paper"  # Rock is least played, so Paper counters it
        if move_frequency["Paper"] < 2:
            return "Scissors"  # Paper is least played, so Scissors counters it

        if random.random() < 0.7:
            if move_frequency["Scissors"] < 2:
                return "Rock"
            elif move_frequency["Rock"] < 2:
                return "Paper"
            elif move_frequency["Paper"] < 2:
                return "Scissors"

        if random.random() < 0.2:
            most_played = sorted(move_frequency.items(), key=lambda x: x[1], reverse=True)[:2]
            most_played_moves = [move for move, count in most_played]
            for move in most_played_moves:
                if move == "Rock":
                    return "Paper"
                elif move == "Paper":
                    return "Scissors"
                elif move == "Scissors":
                    return "Rock"

        if random.random() < 0.1:
            return random.choice(["Rock", "Paper", "Scissors"])  # Random choice fallback

        return random.choice(["Rock", "Paper", "Scissors"])  # Fallback random choice

def counter_move(move):
    # Return the counter to the given move.
    counters = {"Rock": "Paper", "Paper": "Scissors", "Scissors": "Rock"}
    if move not in counters:
        # Fallback: pick a random valid move if input is invalid
        return random.choice(["Rock", "Paper", "Scissors"])
    return counters[move]