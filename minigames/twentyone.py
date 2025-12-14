import random
import time

# ---------- UTILITIES ----------
def Print(text, delay=0.02):  # 0.02
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

# ---------- DISPLAY ----------
def show_cards(player_cards, villager_cards, target_score, inventory, enemy_name):
    Print("\n----- Cards -----")
    print(f"Your Cards: {', '.join(map(str, player_cards))} (Total: {sum(player_cards)})")
    revealed_villager_total = sum(villager_cards[1:])
    print(f"{enemy_name}'s Cards: {', '.join(['??'] + [str(card) for card in villager_cards[1:]])} "
          f"(Total: {revealed_villager_total})")
    print(f"\nTarget Score: {target_score}")
    print(f"Your Trump Cards: {', '.join(inventory) if inventory else 'None'}")

# ---------- TRUMP CARDS ----------
def trump_cards(inventory, target_score, player_cards, villager_cards, available_cards, enemy_name):
    if not inventory:
        Print("\nYou don't have any trump cards!")
        return target_score

    Print("\nYour trump cards:")
    for idx, card in enumerate(inventory, 1):
        Print(f"[{idx}] {card}")

    choice = input("\nChoose a trump card to use (or press Enter to skip): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(inventory):
        selected_card = inventory.pop(int(choice) - 1)

        if selected_card == "17":
            Print("\nYou used 'Change Target to 17'!")
            target_score = 17

        elif selected_card == "24":
            Print("\nYou used 'Change Target to 24'!")
            target_score = 24

        elif selected_card == "Recall Self":
            if player_cards:
                recalled = player_cards.pop()
                available_cards.append(recalled)
                Print(f"\nYou recalled your last card: {recalled}")
            else:
                Print("\nYou have no cards to recall!")

        elif selected_card == "Perfect Draw":
            current_total = sum(player_cards)
            best_card = None
            best_diff = float('inf')
            for card in available_cards:
                total_if = current_total + card
                if total_if <= target_score:
                    diff = abs(total_if - target_score)
                    if diff < best_diff:
                        best_diff = diff
                        best_card = card
            if best_card is not None:
                player_cards.append(best_card)
                available_cards.remove(best_card)
                Print(f"\nYou perfectly drew a {best_card}!")
            else:
                Print("\nNo suitable card found for Perfect Draw!")

        elif selected_card == "Recall Enemy":
            if len(villager_cards) > 1:
                recalled = villager_cards.pop()
                available_cards.append(recalled)
                Print(f"\nYou recalled {enemy_name}'s last visible card: {recalled}")
            else:
                Print(f"\n{enemy_name} has no visible cards to recall!")

        else:
            Print("\nUnknown trump card effect.")
    else:
        Print("\nNo trump card used.")
        return target_score

    return target_score

def draw_trump_card():
    trump_pool = ['17', '24', 'Recall Self', 'Perfect Draw', 'Recall Enemy']
    return random.choice(trump_pool)

# ---------- AI TRUMP USAGE ----------
def ai_use_trump_cards(difficulty, villager_cards, player_cards, target_score, villager_trumps, available_cards, enemy_name):
    if difficulty.lower() == "easy" or not villager_trumps:
        return target_score

    # Snapshot totals for decision logic
    current_total = sum(villager_cards)
    player_total = sum(player_cards)

    # Iterate over a copy so removal is safe
    for card in villager_trumps[:]:
        if difficulty.lower() == "medium":
            # If over target, try to fix
            if current_total > target_score:
                if card == "Recall Self" and len(villager_cards) > 1:
                    recalled = villager_cards.pop()
                    available_cards.append(recalled)
                    Print(f"The {enemy_name} used 'Recall Self' to remove {recalled}.")
                    villager_trumps.remove(card)
                    break
                elif card == "17":
                    target_score = 17
                    Print(f"The {enemy_name} used '17' to change the target score.")
                    villager_trumps.remove(card)
                    break

        elif difficulty.lower() in ("hard", "elite"):
            # Try to approach target smartly
            if card == "Perfect Draw":
                best_card = None
                best_diff = float('inf')
                for c in available_cards:
                    total_if = current_total + c
                    if total_if <= target_score:
                        diff = abs(total_if - target_score)
                        if diff < best_diff:
                            best_diff = diff
                            best_card = c
                if best_card is not None:
                    villager_cards.append(best_card)
                    available_cards.remove(best_card)
                    Print(f"The {enemy_name} used 'Perfect Draw' and got a {best_card}.")
                    villager_trumps.remove(card)
                    break

            if current_total > target_score and card == "Recall Self" and len(villager_cards) > 1:
                recalled = villager_cards.pop()
                available_cards.append(recalled)
                Print(f"The {enemy_name} used 'Recall Self' to remove {recalled}.")
                villager_trumps.remove(card)
                break

            if player_total > target_score - 3 and len(player_cards) > 1 and card == "Recall Enemy":
                recalled = player_cards.pop()
                available_cards.append(recalled)
                Print(f"The {enemy_name} used 'Recall Enemy' to remove your {recalled}.")
                villager_trumps.remove(card)
                break

            if card == "17" and target_score > 17 and current_total < 17 and player_total > 17:
                target_score = 17
                Print(f"The {enemy_name} used '17' to lower the target score.")
                villager_trumps.remove(card)
                break

            if card == "24" and target_score < 24 and current_total > 21 and player_total < 21:
                target_score = 24
                Print(f"The {enemy_name} used '24' to increase the target score.")
                villager_trumps.remove(card)
                break

    return target_score

# ---------- MAIN GAME ----------
def play_21(player_data, klare_data, difficulty, gold_bet, enemy_name, game_stats):

    # Balance check
    if player_data.get("gold", 0) < gold_bet:
        Print("You do not have enough gold to make that bet.")
        return player_data, klare_data, game_stats

    # Deduct bet upfront
    player_data["gold"] -= gold_bet
    Print("\n----- 21 Game -----")
    Print(f"Difficulty: {difficulty.capitalize()}")
    Print(f"Gold Bet: {gold_bet}")

    # Reset trump cards (per match)
    player_data["trump_cards"] = []

    # Best of three
    player_wins = 0
    villager_wins = 0

    while player_wins < 2 and villager_wins < 2:
        target_score = 21

        # Fresh deck each round
        available_cards = list(range(1, 14))
        player_cards = []
        villager_cards = []

        # Trump cards
        player_trump_cards = player_data.get("trump_cards", [])
        player_trump_cards.append(draw_trump_card())
        player_data["trump_cards"] = player_trump_cards

        villager_trump_cards = [draw_trump_card(), draw_trump_card()]

        Print("\nStarting a new round!")
        Print("\n----- Drawing Trump Cards -----")
        Print(f"\nYou draw the trump card: {', '.join(player_trump_cards)}")

        # Initial cards
        player_cards.append(random.choice(available_cards))
        available_cards.remove(player_cards[-1])

        villager_cards.append(random.choice(available_cards))
        available_cards.remove(villager_cards[-1])

        Print("\n----- Drawing Hidden Card -----")
        Print(f"\nYou draw your hidden card: {player_cards[0]}")
        Print(f"\n{enemy_name} draws their hidden card: ??")

        player_stands = False
        villager_stands = False

        while not (player_stands and villager_stands):

            # Player turn
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
                    if sum(player_cards) > target_score:
                        Print("You are currently over the target score.")

                elif choice == "2":
                    Print(f"\nYou stand with a total of {sum(player_cards)}")
                    player_stands = True

                elif choice == "3":
                    show_cards(player_cards, villager_cards, target_score, player_trump_cards, enemy_name)
                    continue

                elif choice == "4":
                    target_score = trump_cards(
                        player_trump_cards,
                        target_score,
                        player_cards,
                        villager_cards,
                        available_cards,
                        enemy_name
                    )
                    continue

                else:
                    Print("Invalid choice.")
                    continue

            # Villager turn
            if not villager_stands:
                target_score = ai_use_trump_cards(
                    difficulty,
                    villager_cards,
                    player_cards,
                    target_score,
                    villager_trump_cards,
                    available_cards,
                    enemy_name
                )

                vill_total = sum(villager_cards)
                player_total = sum(player_cards)
                diff = difficulty.lower()

                if diff == "easy":
                    need_draw = vill_total < 17
                elif diff == "medium":
                    need_draw = vill_total < 18
                elif diff == "hard":
                    need_draw = vill_total < 17 or vill_total < target_score - 2
                else:  # elite
                    if player_total > target_score:
                        need_draw = False
                    elif vill_total > target_score:
                        need_draw = False
                    elif vill_total < player_total:
                        need_draw = True
                    else:
                        need_draw = False

                if need_draw and available_cards:
                    new_card = random.choice(available_cards)
                    villager_cards.append(new_card)
                    available_cards.remove(new_card)
                    Print(f"{enemy_name} draws a {new_card}!")
                    player_stands = False
                else:
                    Print(f"\n{enemy_name} stands.")
                    villager_stands = True

        # Final hands
        Print("\nFinal hands:")
        Print(f"Your Cards: {', '.join(map(str, player_cards))} (Total: {sum(player_cards)})")
        Print(f"{enemy_name}'s Cards: {', '.join(map(str, villager_cards))} (Total: {sum(villager_cards)})")

        player_total = sum(player_cards)
        villager_total = sum(villager_cards)

        if player_total > target_score and villager_total > target_score:
            if abs(player_total - target_score) < abs(villager_total - target_score):
                Print("\nYou were closer to the target score! You win!")
                player_wins += 1
            elif abs(villager_total - target_score) < abs(player_total - target_score):
                Print(f"\n{enemy_name} was closer! They win!")
                villager_wins += 1
            else:
                Print("\nIt is a tie!")

        elif player_total > target_score:
            Print(f"\nYou went over! {enemy_name} wins.")
            villager_wins += 1

        elif villager_total > target_score:
            Print(f"\n{enemy_name} went over! You win.")
            player_wins += 1

        elif player_total == target_score:
            Print("\nYou hit the target exactly! You win!")
            player_wins += 1

        elif villager_total == target_score:
            Print(f"\n{enemy_name} hit the target exactly! They win!")
            villager_wins += 1

        else:
            if abs(target_score - player_total) < abs(target_score - villager_total):
                Print("\nYou were closer! You win!")
                player_wins += 1
            elif abs(target_score - villager_total) < abs(target_score - player_total):
                Print(f"\n{enemy_name} was closer! They win!")
                villager_wins += 1
            else:
                Print("\nIt is a draw!")

        Print(f"\nScore: You {player_wins} - {villager_wins} {enemy_name}\n")

    # Match end
    Print("Game Over!")
    game_stats['minigames_played'] += 1

    if player_wins > villager_wins:
        Print("You win the best of 3!")
        payout = gold_bet * 2
        player_data["gold"] += payout
        Print(f"You earn {payout} gold!")
        game_stats['gambles_won'] += 1

        diff_key = f"{difficulty.lower()}_beaten"
        if diff_key in klare_data and enemy_name not in klare_data[diff_key]:
            klare_data[diff_key].append(enemy_name)

    else:
        Print(f"{enemy_name} wins the best of 3.")
        Print(f"You lose your {gold_bet} gold.")
        game_stats['gambles_lost'] += 1

    return player_data, klare_data, game_stats

# ---------- STANDALONE TEST HARNESS ----------
def _placeholder_klare_data():
    return {
        "day_pass": False,
        "basic_pass": False,
        "premium_pass": False,
        "easy_beaten": [],
        "medium_beaten": [],
        "hard_beaten": [],
        "easy_pro_beaten": False,
        "medium_pro_beaten": False,
        "hard_pro_beaten": False,
    }

# Variable containing all the game stats (21 mvp)
game_stats = {
    "minigames_played": 0,
    "gambles_won": 0,
    "gambles_lost": 0,
    }

if __name__ == "__main__":
    # Placeholder data for standalone play
    player_data = {"gold": 150, "trump_cards": []}
    klare_data = _placeholder_klare_data()

    action = input("Enter difficulty\n[1] Easy\n[2] Medium\n[3] Hard\n[4] Elite\nEnter: ").strip().lower()

    if action == "1":
        difficulty = "easy"
    elif action == "2":
        difficulty = "medium"
    elif action == "3":
        difficulty = "hard"
    elif action == "4":
        difficulty = "elite"
    else:
        Print("Invalid difficulty. Defaulting to medium.")
        difficulty = "medium"

    try:
        gold_bet = int(input("Gold bet: ").strip())
    except ValueError:
        Print("Invalid number, defaulting bet to 10.")
        gold_bet = 10

    enemy_name = "Klara Dealer"
    player_data, klare_data = play_21(player_data, klare_data, difficulty, gold_bet, enemy_name, game_stats)
    Print(f"\nFinal gold: {player_data.get('gold', 0)}")
    Print(f"Beaten lists: easy={klare_data['easy_beaten']}, medium={klare_data['medium_beaten']}, hard={klare_data['hard_beaten']}")

# make using a trump card "unstand" the other player