import time
import random
import os

RESET = '\033[0m'
PINK = '\033[95m'

def Print(text, delay=0.02):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def get_suffix(number):
    if 10 <= number % 100 <= 20:
        return 'th'
    return {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th')

def play_memory(player_data, game_stats, colours_left, memory_sequence, world_state):
    all_colours = ['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Orange', 'Pink']
    max_length = 6

    colours_left = world_state["colours_left"]
    memory_sequence = world_state["memory_sequence"]

    # Reset if starting a new game
    if colours_left == 0:
        memory_sequence.clear()

    Print(f"\n{PINK}-----Memory Game-----{RESET}")
    Print("\n[Mysterious Voice] Knight, it is imperative to your survival that you remember these colours...")
    time.sleep(2)

    next_colour = random.choice(all_colours)
    memory_sequence.append(next_colour)

    Print("The colours are: " + ", ".join(memory_sequence))
    time.sleep(3)

    os.system('cls' if os.name == 'nt' else 'clear')

    # Save progress back into world_state
    if len(memory_sequence) < max_length:
        return player_data, game_stats, world_state, colours_left, memory_sequence

    Print("\n[Mysterious Voice] Now... repeat the sequence to me, brave knight.")
    game_stats['minigames_played'] += 1
    time.sleep(1)

    correct = True

    for i, colour in enumerate(memory_sequence):
        Print(f"\nWhat was the {i + 1}{get_suffix(i + 1)} colour?")

        # Correct answer + 4 wrong answers
        wrong_options = [c for c in all_colours if c != colour]
        options = random.sample(wrong_options, 4)
        options.append(colour)
        random.shuffle(options)

        for idx, opt in enumerate(options, 1):
            Print(f"[{idx}] {opt}")

        while True:
            try:
                choice = int(input("Enter: "))
                if 1 <= choice <= len(options):
                    break
                Print("Please Enter a valid input")
            except ValueError:
                Print("Please Enter a valid input")

        if options[choice - 1] != colour:
            Print(f"\n[Mysterious Voice] Wrong! The correct answer was {colour}.")
            correct = False
            break

        Print("[Mysterious Voice] Correct.")

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
        Print(f"-{player_data['gold']} Gold\nMax Health and health set to 150")

        player_data['gold'] = 0
        player_data['max_health'] = 150
        player_data['health'] = 150
        game_stats['gambles_lost'] += 1

    # Fully reset saved memory state
    world_state["colours_left"] = 6
    world_state["memory_sequence"].clear()

    return player_data, game_stats, world_state