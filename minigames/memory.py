import time
import random
import os

RESET = '\033[0m'
PINK = '\033[95m'

# Print text with delay fast
def Print(text, delay=0.02): #0.02 = 2ms
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def play_memory(player_data, game_stats, colours_left, memory_sequence):
    all_colours = ['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Orange', 'Pink']
    max_length = 6

    # Reset if starting a new game
    if colours_left == 6:
        memory_sequence = []

    Print(f"\n{PINK}-----Memory Game-----{RESET}")
    Print("\n[Mysterious Voice] Knight, it is imperative to your survival that you remember these colours...")
    time.sleep(2)

    # Add one new random colour to the sequence
    next_colour = random.choice(all_colours)
    memory_sequence.append(next_colour)

    # Show current sequence in one line
    Print("The colours are: " + ", ".join(memory_sequence))
    time.sleep(3)

    # Clear console for suspense (works on Windows/macOS/Linux)
    os.system('cls' if os.name == 'nt' else 'clear')

    # If we haven’t reached 6 yet, next call will continue the sequence
    if len(memory_sequence) < max_length:
        colours_left -= 1
        return player_data, game_stats, colours_left, memory_sequence

    # If we've reached 6, test the player's memory
    Print("\n[Mysterious Voice] Now... repeat the sequence to me, brave knight.")
    game_stats['minigames_played'] += 1
    time.sleep(1)

    correct = True
    for i, colour in enumerate(memory_sequence):
        Print(f"\nWhat was the {i+1}{get_suffix(i+1)} colour?")

        # Create 5 options (one correct + 4 random others)
        options = random.sample(all_colours, 4)
        if colour not in options:
            options[random.randint(0, 3)] = colour
        else:
            # ensure exactly one correct answer
            options = list(set(options))
            while len(options) < 5:
                options.append(random.choice(all_colours))
        random.shuffle(options)

        # Display options
        for idx, opt in enumerate(options, 1):
            Print(f"[{idx}] {opt}")

        # Get player input
        while True:
            try:
                choice = int(input("Enter: "))
                if 1 <= choice <= len(options):
                    break
                else:
                    Print("Please Enter a valid input")
            except ValueError:
                Print("Please Enter a valid input")

        if options[choice - 1] != colour:
            Print(f"\n[Mysterious Voice] Wrong! The correct answer was {colour}.")
            correct = False
            break
        else:
            Print("[Mysterious Voice] Correct.")

    # Result
    if correct:
        Print("\n[Mysterious Voice] Incredible! Your memory serves you well, knight.")
        Print(f"\n+{player_data['gold']} Gold!\n+50 Max Health\n+150 Health\n+1 Strength")
        player_data['gold'] *= 2
        player_data['max_health'] += 50
        player_data['health'] += 150
        player_data['strength'] += 1
        game_stats['gambles_won'] += 1

    else:
        Print("\n[Mysterious Voice] Alas... your memory fails you this time.")
        Print(f"-{player_data['gold']} Gold\nMax Health and health set to 100")
        player_data['gold'] = 0
        player_data['max_health'] = 150
        player_data['health'] = 150
        game_stats['gambles_lost'] += 1

    # Reset for next game
    colours_left = 6
    memory_sequence = []

    return player_data, game_stats, colours_left, game_stats, memory_sequence

def get_suffix(number):
    if 10 <= number % 100 <= 20:
        return 'th'
    else:
        return {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th')
