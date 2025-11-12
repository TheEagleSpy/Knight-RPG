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

def start_rps():
    global difficulty, rounds

    Print("Welcome to Rock Paper Scissors Minigame Test!")
    Print("\n-----Rock Paper Scissors Game-----")

    # Set Difficulty
    while True:
        difficulty = input("Do you want to vs the easy or difficult version?\n[1] Easy (1.25x)\n[2] Hard (2x)\n[3] All out (5x, 50 rounds and you have to win 15 of them)\nEnter: ")

        if difficulty == '1':
            difficulty = "Easy"
            break
        elif difficulty == '2':
            difficulty = "Hard"
            break
        elif difficulty == '3':
            difficulty = "All Out"  # All out mode selected
            rounds = 50
            break
        else:
            Print("Invalid input. Please enter 1, 2, or 3.")

    # Set amount of Rounds
    while True:
        if rounds == 50:
            break
        else:
            bestof = input("\nWhat should the match be best of?\n[1] Best of 5\n[2] Best of 7\n[3] Best of 11\n[4] Best of 15\n[5] Best of 21\nEnter: ")

            bestof_dict = {'1': 5, '2': 7, '3': 11, '4': 15, '5': 21}
            if bestof in bestof_dict:
                rounds = bestof_dict[bestof]
                break
            else:
                Print("Invalid input. Please enter a number from 1 to 5.")

    Print("\nGame Starting...")
    play_rps()

def predict_player_move():
    """ Predict the player's next move based on past patterns. """
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
    return counters[move]

def play_rps():
    global difficulty, rounds, ai_rounds, show_prediction
    
    playerscore = 0
    enemyscore = 0
    ai_last_move = None  # Track the AI's last move
    player_last_move = None  # Track the player's last move
    previous_ai_moves = []  # To keep track of AI's last moves
    
    choices = ["Rock", "Paper", "Scissors"]

    while rounds > 0:
        Print(f"\n-----Rounds left: {rounds}-----")
        
        if difficulty == "All out":
            # Detect patterns like Rock -> Rock -> Paper -> Paper -> Scissors
            if len(player_history) >= 5:
                # Check for alternating pattern (Rock -> Rock -> Paper -> Paper -> Scissors)
                if player_history[-5:] == ["Scissors", "Scissors", "Paper", "Paper", "Rock"]:
                    enemyrps = counter_move("Scissors")  # AI will counter Scissors
                    print("[AI] I see you're alternating Rock and Paper. I’ll counter with Scissors!")
                    
                elif player_history[-5:] == ["Rock", "Rock", "Paper", "Paper", "Scissors"]:
                    enemyrps = counter_move("Paper")  # AI will counter Paper (which will be next move)
                    print("[AI] I see you're alternating Rock and Paper. I’ll counter with Paper")
                    
                elif player_history[-5:] == ["Rock", "Rock", "Scissors", "Scissors", "Paper"]:
                    enemyrps = counter_move("Rock")  # AI will counter Rock
                    print("[AI] I see you're alternating Rock and Scissors. I’ll counter with rock!")
                    
        # Determine the AI's move
        if difficulty == "Hard":
            # In Hard mode, AI always counters the player's move to win
            predicted_move = predict_player_move()
            
            # After winning, the AI should adapt and avoid repeating
            if ai_last_move and ai_last_move == counter_move(player_last_move):
                # If AI won with the last counter move, force a new choice
                enemyrps = counter_move(counter_move(predicted_move))  # Avoid repeating same counter
            else:
                enemyrps = counter_move(predicted_move)  # AI counters its prediction to win

            # Make sure AI isn't repeating the same strategy for more than 2 rounds
            if len(previous_ai_moves) >= 2 and previous_ai_moves[-1] == previous_ai_moves[-2]:
                # If AI repeated the same move for the last two rounds, change it
                enemyrps = random.choice([counter_move("Rock"), counter_move("Paper"), counter_move("Scissors")])

            # Add current move to the AI history
            previous_ai_moves.append(enemyrps)
            
            if show_prediction == 'egg':
                print(f"[AI] I think you will play: {predicted_move}")  # DEBUGGING
                print(f"[AI] So I will play: {enemyrps}")  # DEBUGGING
        else:
            # For the first 2 rounds, the AI will try to draw
            if ai_rounds < 2:
                predicted_move = predict_player_move()  # AI predicts player move
                enemyrps = predicted_move  # AI chooses move to draw (match the prediction)
                ai_rounds += 1
                if show_prediction == 'egg':
                    print(f"[AI] I think you will play: {predicted_move}")  # DEBUGGING
            else:
                # After 2 rounds, the AI tries to win by predicting the player's move
                predicted_move = predict_player_move()
                enemyrps = counter_move(predicted_move)  # AI counters its prediction to win
                if show_prediction == 'egg':
                    print(f"[AI] I think you will play: {predicted_move}")  # DEBUGGING
                    print(f"[AI] So I will play: {enemyrps}")  # DEBUGGING

        # Player makes their move
        playerrps = input("\nWhat will you pick? (Rock, Paper, Scissors): ").capitalize()
        if playerrps == "R":
            playerrps = "Rock"
        elif playerrps == "P":
            playerrps = "Paper"
        elif playerrps == 'S':
            playerrps = "Scissors"
        if playerrps not in choices:
            Print("Invalid choice! Please enter Rock, Paper, or Scissors.")
            continue  # Ask again if input is invalid
        
        # Store player move in history
        player_history.append(playerrps)
        player_last_move = playerrps  # Update last player move

        Print(f"\nYou picked {playerrps} and the opponent picked {enemyrps}!")

        # Determine the winner
        if playerrps == enemyrps:
            Print("\nIt's a tie!")
        elif (playerrps == "Rock" and enemyrps == "Scissors") or \
             (playerrps == "Paper" and enemyrps == "Rock") or \
             (playerrps == "Scissors" and enemyrps == "Paper"):
            Print("\nYou win!")
            playerscore += 1
        else:
            Print("\nYou lose!")
            enemyscore += 1

        # Update AI's last move
        ai_last_move = enemyrps

        rounds -= 1  # Decrease rounds after each game
        print("\n------------------------------------------------------\n")
        
    # Get the winner
    if playerscore > enemyscore:
        Print(f"You win {playerscore}-{enemyscore}")
    elif playerscore == enemyscore:
        Print(f"It's a draw {playerscore}-{enemyscore}")
    else:
        Print(f"Opponent wins {enemyscore}-{playerscore}")

    
if __name__ == "__main__":
    show_prediction = input("")
    start_rps()
