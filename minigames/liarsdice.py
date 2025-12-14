import random
import time
import os
import json
from math import comb
from collections import deque

GREEN = "\033[92m"
RESET = "\033[0m"

AI_MEMORY_FILE = "ai_memory.json"

def clear_cmd():
    os.system("cls" if os.name == "nt" else "clear")

def Print(text, delay=0.03, newline=True):
    for c in str(text):
        print(c, end="", flush=True)
        time.sleep(delay)
    if newline:
        print()

def press_to_continue(msg="\nPress Enter to continue: "):
    try:
        input(msg)
    except EOFError:
        pass

def render_turn_order(order, active_set, current, fast=False):
    seq = []
    seen = set()
    for name in list(order):
        if name in seen:
            continue
        seen.add(name)
        if name not in active_set:
            continue
        if name == current:
            seq.append(f"{GREEN}{name}{RESET}")
        else:
            seq.append(name)
    line = " -> ".join(seq)
    if fast:
        print(line)
    else:
        Print(line)
    return line

BASE_STATS = {
    "bluffs_caught": 0,
    "defended_success": 0,
    "bluffs_made": 0,
    "bluff_success": 0,
    "truths_made": 0,
    "truth_success": 0,
}

def _ensure_ai(mem, name):
    if name not in mem:
        mem[name] = {k: 0 for k in BASE_STATS}

def load_ai_memory(players):
    data = {}
    if os.path.exists(AI_MEMORY_FILE):
        try:
            with open(AI_MEMORY_FILE, "r", encoding="utf-8") as f:
                raw = json.load(f)
                for k, v in raw.items():
                    data[k] = {kk: int(v.get(kk, 0)) for kk in BASE_STATS}
        except Exception:
            data = {}
    for p in players:
        _ensure_ai(data, p)
    return data

def save_ai_memory(memory):
    try:
        with open(AI_MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=2)
    except Exception:
        pass

def merge_match_into_global(global_mem, match_mem):
    for name, stats in match_mem.items():
        _ensure_ai(global_mem, name)
        for k in BASE_STATS:
            global_mem[name][k] += stats.get(k, 0)

def prob_at_least(n, k, p=1/6):
    if n <= 0:
        return 1.0
    if n > k:
        return 0.0
    total = 0.0
    for i in range(n, k + 1):
        total += comb(k, i) * (p ** i) * ((1 - p) ** (k - i))
    return total

table_talk = {
    "pre_bid": [
        "[{name}] Hmm... let’s start with this...",
        "[{name}] Starting strong with {next_qty} {face}'s.",
        "[{name}] Don’t get too confident {target}.",
        "[{name}] Haha, good luck guys.",
        "[{name}] Let's start off slowly.",
        "[{name}] Well this is interesting...",
        "[{name}] I've already won this game.",
        "[{name}] Let’s get this started.",
        "[{name}] Careful, {target}. I’m watching you.",
        "[{name}] I can feel the tension in the air."
    ],
    "raise": [
        "[{name}] Let's go with {new_qty} {new_face}'s.",
        "[{name}] Aww scared are we?. {new_qty} {new_face}'s.",
        "[{name}] Haha, Try this, {new_qty} {new_face}'s.",
        "[{name}] Watch and learn... {new_qty} {new_face}'s.",
        "[{name}] Can you top that? {new_qty} {new_face}'s.",
        "[{name}] I raise it to {new_qty} {new_face}'s.",
        "[{name}] {new_qty} {new_face}'s.",
        "[{name}] Let’s see how you guys handle {new_qty} {new_face}'s.",
        "[{name}] This is the last truthful bid. {new_qty} {new_face}'s."
    ],
    "call_bluff": [
        "[{name}] Haha, thats a bluff",
        "[{name}] Bluff! No way that’s true.",
        "[{name}] I don’t buy it.",
        "[{name}] Let’s see what you’re hiding.",
        "[{name}] I’m calling you out!",
        "[{name}] You sure about that one?",
        "[{name}] Not convinced.",
        "[{name}] Let’s check those dice.",
        "[{name}] I think you’re fibbing.",
        "[{name}] Even you know that bid was too high."
    ]
    }

def assign_partners(players):
    n = len(players)
    if n >= 32:
        k = 3
        max_winners = 4
        split = [25, 25, 25, 25]
    elif n >= 18:
        k = 2
        max_winners = 3
        split = [34, 33, 33]
    else:
        k = 1
        max_winners = 2
        split = [50, 50]

    order = players[:]
    random.shuffle(order)

    # initialize everyone with empty partner lists
    partners = {p: [] for p in order}

    if k == 1:
        # Pair players evenly (A↔B, C↔D, etc.)
        for i in range(0, len(order) - 1, 2):
            a, b = order[i], order[i + 1]
            partners[a].append(b)
            partners[b].append(a)
        # if odd number of players, last one pairs with first
        if len(order) % 2 == 1:
            last, first = order[-1], order[0]
            partners[last].append(first)
            partners[first].append(last)

    elif k == 2:
        # Group players in triplets that all share each other as partners
        for i in range(0, len(order), 3):
            group = order[i:i + 3]
            for p in group:
                partners[p].extend([x for x in group if x != p])
        # Handle leftover players if not divisible by 3
        leftover = len(order) % 3
        if leftover and len(order) > 3:
            group = order[-leftover:]
            for p in group:
                partners[p].extend([x for x in group if x != p])

    elif k == 3:
        # Group players in fours that all share each other as partners
        for i in range(0, len(order), 4):
            group = order[i:i + 4]
            for p in group:
                partners[p].extend([x for x in group if x != p])
        # Handle leftovers (just pair them with last full group)
        leftover = len(order) % 4
        if leftover and len(order) > 4:
            group = order[-leftover:]
            for p in group:
                partners[p].extend([x for x in group if x != p])

    return partners, max_winners, split

def all_partner_dice(name, partners_map, active_players):
    dice = []
    for partner in partners_map.get(name, []):
        if partner in active_players:
            dice.extend(active_players[partner])
    return dice

# AI move calculation
def ai_take_turn(
    player,
    active_players,
    partners,
    current_bid,
    current_bidder,
    global_memory,
    difficulty,
    noise_gate=True
    ):
    diff = difficulty
    total_players_left = len(active_players)
    total_dice = sum(len(d) for d in active_players.values())
    dice = active_players[player]
    partner_dice_list = all_partner_dice(player, partners, active_players)

    # pacing
    time.sleep(0.015 if total_players_left > 20 else 0.1)

    # dialogue printing — never skip any AI dialogue
    def maybe_print(line):
        Print(line)

    _ensure_ai(global_memory, player)
    self_stats = global_memory[player]
    defend_success_self = (self_stats["defended_success"] /
                           max(1, self_stats["defended_success"] + self_stats["bluffs_caught"]))
    bluff_success_self = (self_stats["bluff_success"] / max(1, self_stats["bluffs_made"]))

    conf_windows = {
        "easy":   (0.28, 0.45),
        "medium": (0.50, 0.65),
        "hard":   (0.85, 0.95)
    }
    low, high = conf_windows.get(diff, (0.50, 0.65))

    # Opening bid
    if not current_bid:
        min_open = max(2, total_dice // 10)
        face_counts = {f: dice.count(f) for f in range(1, 7)}
        common_face = max(face_counts, key=face_counts.get)
        face_guess = common_face if random.random() < 0.7 else random.randint(2, 5)

        # Hard always considers partners, Medium often, Easy sometimes
        base_qty = dice.count(face_guess)
        if diff == "hard":
            base_qty += sum(1 for v in partner_dice_list if v == face_guess)
        elif diff == "medium" and random.random() < 0.6:
            base_qty += sum(1 for v in partner_dice_list if v == face_guess)
        elif diff == "easy" and random.random() < 0.35:
            base_qty += sum(1 for v in partner_dice_list if v == face_guess)

        base_qty = max(min_open, base_qty)
        confidence_factor = 1.0 + (bluff_success_self - 0.5) * (0.4 if diff == "hard" else 0.25)
        qty_guess = int(max(min_open, min(base_qty + random.choice([0, 1]) * confidence_factor, total_dice)))
        maybe_print(f"\n{random.choice(table_talk['pre_bid']).format(name=player, next_qty=qty_guess, face=face_guess, target='Knight')}")
        Print(f"{player} opens with {qty_guess} {face_guess}'s.\n")
        return (qty_guess, face_guess), player, False, None

    # Evaluate call vs raise
    qty, face = current_bid

    known_count = dice.count(face)
    # Hard always counts partners, Medium usually, Easy sometimes
    if diff == "hard" or (diff == "medium" and random.random() < 0.75) or (diff == "easy" and random.random() < 0.35):
        known_count += sum(1 for v in partner_dice_list if v == face)

    unknown_dice = total_dice - len(dice) - len(partner_dice_list)
    need = max(0, qty - known_count)
    p_true = prob_at_least(need, unknown_dice, p=1/6)

    estimate_factor = random.uniform(low, high)
    if total_players_left > 10:
        estimate_factor = min(0.9, max(0.7, estimate_factor - 0.05))
    if total_players_left <= 4:
        estimate_factor = random.uniform(0.9, 1.05)

    estimated_total = known_count + int(unknown_dice * estimate_factor) + random.randint(-1, 1)
    bluff_margin = qty - estimated_total

    call_chance = 0.06 + max(0, bluff_margin) * 0.10
    call_chance += (1.0 - p_true) * (0.60 if diff == "hard" else 0.40)

    # Additional large-table sanity: if qty is well below expectation, be reluctant to call
    expected = total_dice / 6.0
    variance = total_dice * (1/6) * (5/6)
    std = max(1.0, variance ** 0.5)
    if total_dice >= 60:
        if qty <= expected - 0.5 * std:
            call_chance *= 0.25
        elif qty <= expected:
            call_chance *= 0.5

    # Sanity floor
    if qty <= max(2, total_dice // 4) and p_true > 0.60:
        call_chance *= 0.10

    threshold_quarter = max(3, (total_dice + 4) // 4)
    if qty > threshold_quarter:
        call_chance += 0.12 * (qty - threshold_quarter)
    if qty > 8:
        call_chance += 0.08 + (qty - 8) * 0.02

    if diff == "easy":
        call_chance *= 0.75
    elif diff == "hard":
        call_chance *= 0.85

    bidder = current_bidder
    if bidder:
        _ensure_ai(global_memory, bidder)
        opp = global_memory[bidder]
        opp_defend_success_rate = (opp["defended_success"] /
                                   max(1, opp["defended_success"] + opp["bluffs_caught"]))
        opp_bluff_rate = (opp["bluffs_made"] / max(1, opp["truths_made"] + opp["bluffs_made"]))
        opp_bluff_success_rate = (opp["bluff_success"] / max(1, opp["bluffs_made"]))
        call_chance *= (1.0 + (opp_bluff_rate - 0.5) * (0.8 if diff == "hard" else 0.5))
        call_chance *= (1.0 - (opp_defend_success_rate - 0.5) * (0.5 if diff == "hard" else 0.3))
        call_chance *= (1.0 - (opp_bluff_success_rate - 0.5) * 0.15)

    # Partner friendliness: medium/hard 10–20% less likely to call partners
    if bidder and bidder in partners.get(player, []):
        if diff == "hard":
            call_chance *= 0.8
        elif diff == "medium":
            call_chance *= 0.85
        else:
            call_chance *= 0.95

    if total_players_left <= 4:
        call_chance *= 1.6

    call_chance = max(0.02, min(call_chance, 0.95))

    # Decision
    if random.random() < call_chance:
        return current_bid, current_bidder, True, player
    else:
        have = dice.count(face)
        partner_have = sum(1 for v in partner_dice_list if v == face)
        total_have = have + partner_have
        conservative = qty >= max(9, threshold_quarter)
        confidence_factor = 1.0 + (defend_success_self - 0.5) * (0.45 if diff == "hard" else 0.25) \
                                + (bluff_success_self - 0.5) * (0.30 if diff == "hard" else 0.20)
        if total_have >= 2 and not conservative:
            inc_raw = random.choice([1, 1, 2])
        else:
            inc_raw = 1 if conservative or random.random() < 0.9 else 0
        inc = max(1, int(round(inc_raw * confidence_factor)))
        new_qty = min(qty + inc, total_dice)
        face_bump_chance = 0.65 + (confidence_factor - 1.0) * 0.2
        new_face = face if random.random() < min(0.95, max(0.05, face_bump_chance)) else min(6, face + random.choice([0, 1]))
        maybe_print(f"\n{random.choice(table_talk['raise']).format(name=player, new_qty=new_qty, new_face=new_face)}\n")
        return (new_qty, new_face), player, False, None

# Main game loic
def play_liars_dice(player_data, klare_data, enemy_count, difficulty, game_stats, gold_bet, enemy_names, silent=None):
    diff = str(difficulty).strip().lower()
    if diff not in ("easy", "medium", "hard"):
        diff = "medium"

    game_stats['minigames_played'] += 1

    # for 15+ players we will prefer fast printing in some places
    def fast_print(*args, **kwargs):
        if not silent:
            print(*args, **kwargs)

    def slow_or_fast_print(text):
        if silent:
            return
        Print(text)

    if gold_bet is None:
        while True:
            try:
                gold_bet = int(input("Enter your gold bet per player: ").strip())
                if gold_bet > 0:
                    break
                Print("Enter a positive integer.")
            except ValueError:
                Print("That is not a number, try again.")

    enemy_count = max(1, int(enemy_count))
    enemy_names = list(enemy_names or [])
    enemy_names = enemy_names[:enemy_count]
    while len(enemy_names) < enemy_count:
        enemy_names.append(f"Opponent {len(enemy_names)+1}")
    players = ["Knight"] + enemy_names[:enemy_count]
    total_players = len(players)

    if player_data.get("gold", 0) < gold_bet:
        Print("You do not have enough gold to make that bet.")
        return player_data, klare_data
    player_data["gold"] -= gold_bet
    pot = gold_bet * len(players)

    active_players = {name: [] for name in players}

    partners, max_winners, split_rule = assign_partners(players)

    match_memory = {name: {k: 0 for k in BASE_STATS} for name in players}
    global_memory = load_ai_memory(players)

    beaten_this_game = set()
    elimination_order = []
    turn_order = deque(players)
    random.shuffle(turn_order)
    next_round_starter_name = None
    round_start_index = 0
    turn_counter = 0

    if max_winners == 2:
        slow_or_fast_print("Top 2 split the pot 50/50, if you and your partner are the final two, you receive 75 percent, your partner 25 percent.\n")
    elif max_winners == 3:
        slow_or_fast_print("Top 3 can win this match, pot splits 34/33/33.\n")
    else:
        slow_or_fast_print("Top 4 can win this match, pot splits 25/25/25/25.\n")

    # Watching / skipping controls after Knight elimination
    skip_to_results = False

    # main rounds
    while len(active_players) > max_winners:
        ordered_all = list(turn_order)
        alive_set = set(active_players.keys())

        starter = None
        if next_round_starter_name:
            if next_round_starter_name in ordered_all:
                idx_base = ordered_all.index(next_round_starter_name)
            else:
                idx_base = -1
            for step in range(1, len(ordered_all)+1):
                cand = ordered_all[(idx_base + step) % len(ordered_all)]
                if cand in alive_set:
                    starter = cand
                    break
            next_round_starter_name = None
        if starter is None:
            for _ in range(len(ordered_all)):
                cand = ordered_all[round_start_index % len(ordered_all)]
                round_start_index += 1
                if cand in alive_set:
                    starter = cand
                    break

        start_pos = ordered_all.index(starter)
        round_order = deque(ordered_all[start_pos:] + ordered_all[:start_pos])

        if not silent:
            press_to_continue("Press Enter to roll dice and begin the round: ")
            clear_cmd()

        use_fast = len(active_players) >= 15
        render_turn_order(round_order, alive_set, starter, fast=use_fast)

        # Roll dice
        for name in list(active_players.keys()):
            active_players[name] = [random.randint(1, 6) for _ in range(4)]

        if "Knight" in active_players:
            pd = active_players["Knight"]
            partner_names = partners.get("Knight", [])

            # Build partner dice text dynamically
            partner_texts = []
            for pn in partner_names:
                if pn in active_players:  # Partner still alive
                    partner_dice = active_players[pn]
                    partner_texts.append(f"{pn}'s Dice: {partner_dice}")

            # Decide what to print based on how many partners are alive
            if partner_texts:
                msg = "Your Dice: {} | {}".format(pd, " | ".join(partner_texts))
            else:
                msg = f"Your Dice: {pd}"

            # Print using correct style depending on player count
            if len(active_players) >= 15:
                print(msg)
            else:
                Print(msg)


        current_bid = None
        current_bidder = None
        round_over = False
        if use_fast:
            fast_print(f"\n{starter} starts the round.")
        else:
            slow_or_fast_print(f"\n{starter} starts the round.")
        caller_this_round = None

        # Track last-bid info only for success crediting; we no longer record "made" counters separately
        last_bid_info = None
        bids_in_round = 0

        while not round_over:
            for _ in range(len(round_order)):
                if round_over:
                    break
                player = round_order[0]
                round_order.rotate(-1)
                if player not in active_players:
                    continue

                turn_counter += 1
                if turn_counter % 40 == 0:
                    save_ai_memory(global_memory)

                total_players_left = len(active_players)
                total_dice = sum(len(d) for d in active_players.values())

                if player == "Knight":
                    if "Knight" not in active_players:
                        continue  # safety

                    while True and not silent:
                        current_bid_text = f"{current_bid[0]} {current_bid[1]}'s" if current_bid else "No bids yet"
                        partner_names = partners.get("Knight", [])
                        partner_dice_flat = []
                        for pn in partner_names:
                            if pn in active_players:
                                partner_dice_flat.extend(active_players[pn])

                        Print("\n---------------------------")

                        # Show Knight's and partners' dice
                        pd = active_players["Knight"]
                        partner_names = partners.get("Knight", [])

                        partner_texts = []
                        for pn in partner_names:
                            if pn in active_players:  # Only show surviving partners
                                partner_dice = active_players[pn]
                                partner_texts.append(f"{pn}'s Dice: {partner_dice}")

                        if partner_texts:
                            msg = "Your Dice: {} | {}".format(pd, " | ".join(partner_texts))
                        else:
                            msg = f"Your Dice: {pd}"

                        if len(active_players) >= 15:
                            print(msg)
                        else:
                            Print(msg)

                        Print(f"Players Left: {total_players_left} | Total Dice: {total_dice}")
                        Print(f"Current Bid: {current_bid_text}")
                        Print("[1] Up Bid")
                        Print("[2] Call Bluff")
                        action = input("Enter: ").strip()
                        Print("---------------------------")

                        if action not in ("1", "2"):
                            Print("Invalid choice, Enter 1 to Up Bid or 2 to Call Bluff.")
                            continue

                        if action == "2":
                            if not current_bid or not current_bidder:
                                Print("\nNo bid to call bluff on.")
                                continue

                            qty, face = current_bid
                            caller_this_round = "Knight"
                            Print(f"\n[Knight] I am calling your {current_bid[0]} {current_bid[1]}'s.")

                            # Reveal all dice (fast or slow)
                            if len(active_players) >= 15:
                                print("\n--- ALL DICE REVEALED ---")
                                for name, dice in active_players.items():
                                    print(f"{name}: {dice}")
                                print("--------------------------\n")
                            else:
                                Print("\n--- ALL DICE REVEALED ---")
                                for name, dice in active_players.items():
                                    Print(f"{name}: {dice}")
                                Print("--------------------------\n")

                            actual_count = sum(d.count(face) for d in active_players.values())
                            msg = f"The bid was {qty} {face}'s, there are {actual_count} {face}'s."
                            if len(active_players) >= 15:
                                fast_print(msg)
                            else:
                                Print(msg)

                            bidder = current_bidder
                            was_truth = actual_count >= qty

                            if last_bid_info and last_bid_info["bidder"] == bidder:
                                last_bid_info["resolved"] = True

                            _ensure_ai(global_memory, bidder)
                            _ensure_ai(match_memory, bidder)

                            if was_truth:
                                # caller out
                                out_name = caller_this_round
                                if len(active_players) >= 15:
                                    fast_print(f"{out_name} loses the bluff and is OUT!")
                                else:
                                    Print(f"{out_name} loses the bluff and is OUT!")
                                if out_name in active_players:
                                    del active_players[out_name]
                                    elimination_order.append(out_name)
                                    if "Knight" in active_players and out_name != "Knight":
                                        beaten_this_game.add(out_name)

                                # Update bidder stats
                                global_memory[bidder]["truths_made"] += 1
                                global_memory[bidder]["truth_success"] += 1
                                global_memory[bidder]["defended_success"] += 1
                                match_memory[bidder]["truths_made"] += 1
                                match_memory[bidder]["truth_success"] += 1
                                match_memory[bidder]["defended_success"] += 1

                            else:
                                # bidder out
                                if len(active_players) >= 15:
                                    fast_print(f"{bidder} was bluffing and is OUT!")
                                else:
                                    Print(f"{bidder} was bluffing and is OUT!")
                                if bidder in active_players:
                                    del active_players[bidder]
                                    elimination_order.append(bidder)
                                    if "Knight" in active_players and bidder != "Knight":
                                        beaten_this_game.add(bidder)

                                global_memory[bidder]["bluffs_made"] += 1
                                global_memory[bidder]["bluffs_caught"] += 1
                                match_memory[bidder]["bluffs_made"] += 1
                                match_memory[bidder]["bluffs_caught"] += 1

                            save_ai_memory(global_memory)
                            next_round_starter_name = caller_this_round
                            round_over = True
                            break

                        else:
                            # Knight raises
                            # Crediting success to previous bid if not already resolved
                            if last_bid_info and not last_bid_info.get("resolved"):
                                prev_bidder = last_bid_info["bidder"]
                                if last_bid_info["was_bluff_calc"]:
                                    global_memory[prev_bidder]["bluff_success"] += 1
                                elif last_bid_info["was_truth_actual"]:
                                    global_memory[prev_bidder]["truth_success"] += 1
                                save_ai_memory(global_memory)

                            while True:
                                bet = input("Enter Bid as 'quantity' of 'face' (eg. 3 4): ").strip().split()
                                if len(bet) != 2 or not all(x.isdigit() for x in bet):
                                    Print("Invalid format, example: 3 4")
                                    continue
                                qty, face = map(int, bet)
                                if not (1 <= face <= 6):
                                    Print("Face must be 1–6.")
                                    continue
                                if qty < 2 and not current_bid:
                                    Print("Minimum opening bid is 2 of a kind.")
                                    continue
                                if current_bid and (qty < current_bid[0] or (qty == current_bid[0] and face <= current_bid[1])):
                                    Print("Bid must be higher than current.")
                                    continue
                                if qty > total_dice:
                                    Print(f"Quantity too high, max is {total_dice}.")
                                    continue

                                current_bid = (qty, face)
                                current_bidder = "Knight"
                                bids_in_round += 1
                                # build last bid info
                                actual = sum(d.count(face) for d in active_players.values())
                                last_bid_info = {
                                    "bidder": "Knight",
                                    "bid": (qty, face),
                                    "was_bluff_calc": qty > actual,
                                    "was_truth_actual": qty <= actual,
                                    "resolved": False,
                                }

                                Print(f"\nKnight bids {qty} dice of {face}'s.")
                                break
                            break

                else:
                    result_bid, result_bidder, wants_reveal, caller = ai_take_turn(
                        player=player,
                        active_players=active_players,
                        partners=partners,
                        current_bid=current_bid,
                        current_bidder=current_bidder,
                        global_memory=global_memory,
                        difficulty=diff,
                        noise_gate=True
                    )

                    if wants_reveal:
                        caller_this_round = caller or player
                        # Bluff call line remains slow Print for drama
                        Print(f"\n{random.choice(table_talk['call_bluff']).format(name=caller_this_round)}\n")

                        qty, face = current_bid
                        # Reveal all dice (fast or slow)
                        if len(active_players) >= 15:
                            print("\n--- ALL DICE REVEALED ---")
                            for name, dice in active_players.items():
                                print(f"{name}: {dice}")
                            print("--------------------------\n")
                        else:
                            Print("\n--- ALL DICE REVEALED ---")
                            for name, dice in active_players.items():
                                Print(f"{name}: {dice}")
                            Print("--------------------------\n")

                        actual_count = sum(d.count(face) for d in active_players.values())
                        msg = f"The bid was {qty} {face}'s, there are {actual_count} {face}'s."
                        if len(active_players) >= 15:
                            fast_print(msg)
                        else:
                            Print(msg)

                        bidder = current_bidder
                        was_truth = actual_count >= qty

                        if last_bid_info and last_bid_info["bidder"] == bidder:
                            last_bid_info["resolved"] = True

                        _ensure_ai(global_memory, bidder)
                        _ensure_ai(match_memory, bidder)

                        if was_truth:
                            # caller out
                            out_name = caller_this_round
                            if len(active_players) >= 15:
                                fast_print(f"{out_name} loses the bluff and is OUT!")
                            else:
                                Print(f"{out_name} loses the bluff and is OUT!")
                            if out_name in active_players:
                                del active_players[out_name]
                                elimination_order.append(out_name)
                                if "Knight" in active_players and out_name != "Knight":
                                    beaten_this_game.add(out_name)

                            global_memory[bidder]["truths_made"] += 1
                            global_memory[bidder]["truth_success"] += 1
                            global_memory[bidder]["defended_success"] += 1
                            match_memory[bidder]["truths_made"] += 1
                            match_memory[bidder]["truth_success"] += 1
                            match_memory[bidder]["defended_success"] += 1

                        else:
                            # bidder out
                            if len(active_players) >= 15:
                                fast_print(f"{bidder} was bluffing and is OUT!")
                            else:
                                Print(f"{bidder} was bluffing and is OUT!")
                            if bidder in active_players:
                                del active_players[bidder]
                                elimination_order.append(bidder)
                                if "Knight" in active_players and bidder != "Knight":
                                    beaten_this_game.add(bidder)

                            global_memory[bidder]["bluffs_made"] += 1
                            global_memory[bidder]["bluffs_caught"] += 1
                            match_memory[bidder]["bluffs_made"] += 1
                            match_memory[bidder]["bluffs_caught"] += 1

                        save_ai_memory(global_memory)
                        next_round_starter_name = caller_this_round
                        round_over = True
                        break

                    else:
                        # AI raises; credit previous unresolved bid with success
                        if last_bid_info and not last_bid_info.get("resolved"):
                            prev_bidder = last_bid_info["bidder"]
                            if last_bid_info["was_bluff_calc"]:
                                global_memory[prev_bidder]["bluff_success"] += 1
                            elif last_bid_info["was_truth_actual"]:
                                global_memory[prev_bidder]["truth_success"] += 1
                            save_ai_memory(global_memory)

                        current_bid = result_bid
                        current_bidder = result_bidder
                        bids_in_round += 1

                        # update last bid info
                        qty2, face2 = current_bid
                        actual2 = sum(d.count(face2) for d in active_players.values())
                        last_bid_info = {
                            "bidder": result_bidder,
                            "bid": (qty2, face2),
                            "was_bluff_calc": qty2 > actual2,
                            "was_truth_actual": qty2 <= actual2,
                            "resolved": False,
                        }

        if not silent:
            press_to_continue()
            clear_cmd()

        # If Knight just got eliminated, offer skip option once
        if "Knight" not in active_players and not skip_to_results and not silent:
            Print("\nYou have been eliminated.")
            Print("[1] Watch the rest")
            Print("[2] Skip to final results")
            choice = input("Enter: ").strip()
            if choice == "2":
                skip_to_results = True
                silent = True  # suppress all drama/pauses going forward

    survivors = list(active_players.keys())
    slow_or_fast_print("\nFinal survivors reached.\n")

    # Show partner pairs (compact)
    if not silent:
        Print("Partner pairs this match:")
        seen = set()
        for a in players:
            if a in seen:
                continue
            ps = partners.get(a, [])
            group = [a] + ps
            for g in group:
                seen.add(g)
            Print(f"{a} ↔ {', '.join(ps) if ps else '-'}")

        Print("\nElimination order (first out -> last out):")
        Print(", ".join(elimination_order + survivors))

    # Payouts
    if "Knight" in survivors:
        if len(survivors) == 2:
            # special 75/25 if Knight and a partner are the last two
            other = [s for s in survivors if s != "Knight"][0]
            if other in partners.get("Knight", []):
                knight_reward = int(pot * 0.75)
                partner_reward = pot - knight_reward
                player_data["gold"] += knight_reward
                slow_or_fast_print(f"\nKnight and partner {other} survive together.")
                slow_or_fast_print(f"Knight receives {knight_reward} gold, {other} receives {partner_reward} gold.")
            else:
                # normal 50/50
                reward = (pot * split_rule[0]) // 100 if split_rule == [50, 50] else pot // 2
                player_data["gold"] += reward
                slow_or_fast_print(f"\nKnight survives to the final two and receives {reward} gold.")
            
        else:
            # 3 or 4 winners or unusual multiple survivors case
            if len(survivors) == 3 and split_rule == [34, 33, 33]:
                # allocate integer split by first 34 to someone; if Knight is among, give Knight 34%
                if "Knight" in survivors:
                    knight_reward = (pot * 34) // 100
                else:
                    knight_reward = (pot * 33) // 100
                player_data["gold"] += knight_reward
                slow_or_fast_print(f"\nThree winners. Knight receives {knight_reward} gold by rule (34/33/33).")
            elif len(survivors) == 4 and split_rule == [25, 25, 25, 25]:
                reward = (pot * 25) // 100
                player_data["gold"] += reward
                slow_or_fast_print(f"\nFour winners. Knight receives {reward} gold by rule (25% each).")
            else:
                # fallback: split equally among survivors
                reward = pot // max(2, len(survivors))
                player_data["gold"] += reward
                slow_or_fast_print(f"\nMultiple survivors. Knight receives {reward} gold by rule.")
        
        game_stats['gambles_won'] += 1

    else:
        game_stats['gambles_lost'] += 1

    diff_key = f"{diff}_beaten"
    if isinstance(klare_data, dict):
        klare_data.setdefault(diff_key, [])
        for name in sorted(beaten_this_game):
            if name != "Knight" and name not in klare_data[diff_key]:
                klare_data[diff_key].append(name)

    merge_match_into_global(global_memory, match_memory)
    save_ai_memory(global_memory)

    return player_data, klare_data, game_stats

# Klare data placeholder when this file is main
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

# Help menu
def liarsdice_help_menu():
    while True:
        press_to_continue()
        clear_cmd()
        print("===== LIAR'S DICE - HELP MENU =====\n")

        print("=== OBJECTIVE ===")
        print("The goal of Liar’s Dice is to outlast every other player by making accurate bids or calling out false ones. "
              "Each player secretly rolls dice, and on their turn they must either RAISE the current bid or CALL BLUFF. "
              "When a bluff is called, all dice are revealed and one player is eliminated.\n")

        print("=== BASIC TERMS ===")
        print("• Bid: A claim about how many dice of a specific face value exist across ALL players (e.g. '3 4's' means at least 3 dice show a 4).")
        print("• Raise: Increasing the current bid. You must either increase the quantity or raise the face while keeping the quantity the same.")
        print("• Caller: The player who chooses to call bluff on the current bidder’s claim.")
        print("• Current Bidder: The player who made the most recent bid.")
        print("• Round: A cycle of bidding and bluff-calling that ends when one player is eliminated.\n")

        print("=== TURN ORDER DISPLAY ===")
        print("At the start of each round, you’ll see a list of players in order of turns. "
              "The active player’s name is highlighted in green. As players are eliminated, they disappear from the list. "
              "Turn order rotates automatically each round, beginning with the player after whoever last called a bluff.\n")

        print("=== HOW TO MAKE A LEGAL BID ===")
        print("On your turn, you can choose to [1] Up Bid or [2] Call Bluff.\n")
        print("When choosing to Up Bid, you must type two numbers separated by a space, for example:")
        print("4 5")
        print("This means you are claiming there are at least 4 dice showing a face of 5 across the entire table.\n")
        print("A bid is only LEGAL if it increases the total quantity or, if the quantity stays the same, raises the face value.\n")
        print("Examples of LEGAL raises:")
        print("• From '3 5' to '4 5'  (quantity increased)")
        print("• From '4 4' to '4 6'  (face increased)")
        print("Examples of ILLEGAL raises:")
        print("• From '3 4' to '4 3'  (face decreased)")
        print("• From '4 4' to '3 5'  (quantity decreased)\n")

        print("=== CALLING A BLUFF ===")
        print("If you think the current bid is false, choose to Call Bluff. "
              "All dice are revealed and compared to the claim.\n")
        print("• If the bid was TRUE (enough dice matched), the CALLER is eliminated.")
        print("• If the bid was FALSE (not enough dice), the BIDDER is eliminated.\n")
        print("There are no retries or second chances... once eliminated, you are out of the match.\n")

        print("=== PARTNERS ===")
        print("You have one partner. "
              "Your partner’s dice will be visible to you each round while they are still in the game.\n")
        print("If you and your partner are the last survivors, you get more of the gold rewards. 75%/25% to be exact.\n")

        print("=== MATCH FLOW ===")
        print("1. All players roll dice.\n"
              "2. Starting player makes the first bid.\n"
              "3. Each player either raises the bid or calls bluff.\n"
              "4. When a bluff is called, dice are revealed and one player is eliminated.\n"
              "5. The person after the caller starts the next round.\n"
              "6. The game continues until the required number of survivors remain.\n")

        print("=== ELIMINATION AND ENDGAME ===")
        print("When you are called out correctly (your bid was false), you are eliminated immediately with no chance to continue. "
              "If your call was correct, the bidder is eliminated instead.\n")
        print("The match ends once the survivor count matches the number of winners for that player range (2, 3, or 4). "
              "Gold rewards are then distributed automatically according to the final survivor group.\n")

        print("=== QUICK REMINDERS ===")
        print("• Enter bids as two numbers: quantity then face (e.g., 3 5).\n"
              "• You cannot lower a bid’s quantity or face value.\n"
              "• You can always call bluff instead of raising.\n"
              "• The active player is highlighted in green at the top of the screen.\n"
              "• Eliminated players are permanently out, no respawns, no retries.\n")

        print("=====================================")
        print("Press Enter to return.")
        input("Enter: ").strip().lower()
        break  

# Update log
def updatelog():
    clear_cmd()
    Print("-----Current Version: V2-----")
    print("- Added standalone menu with Rules, Update Log, and Play options.")
    print("- Expanded player scaling beyond 8 participants; supports 2–32+ players.")
    print("- Added dynamic partner system:")
    print("   • 2–17 players → 1 partner, 2 total winners (50/50 or 75/25 split).")
    print("   • 18–31 players → 2 partners, 3 total winners (34/33/33 split).")
    print("   • 32+ players → 3 partners, 4 total winners (25% each).")
    print("- Introduced new probability balancing for large-table realism; AIs avoid early impossible calls.")
    print("- Added persistent AI memory saving to external JSON file (auto-saves during play).")
    print("- New difficulty tuning:")
    print("   • Easy: simplified reasoning, slower adaptation.")
    print("   • Medium: balanced confidence and partner use.")
    print("   • Hard: full probabilistic reasoning using partner dice and memory.")
    print("- Reworked turn pacing and AI noise gate for faster performance at 15+ players.")
    print("- Improved reveal and dice printing for large matches (fast print mode).")
    print("- Added post-elimination option to skip or watch remaining rounds.")
    print("- Integrated `klare_data` tracking for which AI names you've beaten by difficulty.")
    print("- Added structured gold payout system with dynamic split rules and proper rounding.")
    print("- Improved probability helper for more accurate bluff analysis.")
    print("- Rewrote partner assignment to ensure even distribution across large tables.")
    print("- Added emergent AI behaviors that evolve via saved statistics between sessions.")
    print("\n---Bugs/Changes---")
    print("- Fixed edge cases where bids could exceed total dice count.")
    print("- Fixed partner dice not counting properly on some AI difficulties.")
    print("- Fixed saved memory overwriting on corrupted files.")
    print("- Fixed crash when AI_MEMORY_FILE missing or malformed.")
    print("- Improved stability when the Knight is eliminated early.")
    print("- Adjusted AI call thresholds to prevent overly-aggressive play at large tables.")
    print("- Adjusted output pacing and formatting for better readability.")
    print("- Refined elimination order tracking and end-of-game summaries.")

if __name__ == "__main__":
    # Standalone menu
    while True:
        print("\nLIAR'S DICE – Standalone")
        print("[1] Play")
        print("[2] Rules")
        print("[3] Update Log")
        print("[4] Quit")
        choice = input("Enter: ").strip()
        if choice == "2":
            liarsdice_help_menu()
            clear_cmd()
            continue
        if choice == "3":
            updatelog()
            press_to_continue()
            clear_cmd()
            continue
        if choice == "4":
            raise SystemExit
        if choice != "1":
            print("Invalid choice.")
            continue

        player_data = {"gold": 500}
        klare_data = _placeholder_klare_data()

        try:
            enemy_count = int(input("How many opponents? ").strip())
        except ValueError:
            enemy_count = 7

        difficulty = input("Difficulty [easy/medium/hard]: ").strip().lower() or "medium"
        try:
            gold_bet = int(input("Gold bet per player: ").strip())
        except ValueError:
            gold_bet = 50

        default_names = ["Joe", "Bob", "Frank", "Sue", "Tom", "Lily", "Max", "Emma", "Nia", "Zed", "Kara", "Vince",
                         "Mira", "Ike", "Tess", "Odin", "Quinn", "Rhea", "Pax", "Uma", "Xan", "Yuri"]
        enemy_names = default_names[:enemy_count]

        Print(f"\nYou will play Liar's Dice against {enemy_count} opponents for {gold_bet} gold each.\n")
        player_data, klare_data = play_liars_dice(player_data, klare_data, enemy_count, difficulty, enemy_names, gold_bet)

        Print(f"\nFinal gold: {player_data.get('gold', 0)}")
        Print(f"Beaten lists: easy={klare_data['easy_beaten']}, medium={klare_data['medium_beaten']}, hard={klare_data['hard_beaten']}")

# Make it show the counted amount of each dice under the tabled revealed eg. 4 1s, 3 2s, 6 3s etc.
# make easy easier. (ai is less likely to call bluff)
# make ai better (ofc)
# fix skip to results not working. (make it do all the game but without printing it.)
# fix being able to bid higher count lower face.
# stop ais going from like 7 5s to 9 5s
# when ais raise to a higher face, they keep the amount the same eg 3 4s to 3 5s

# add nudging, where you can nudge your teammate by 20% to bluff or raise

# MAX IS A MADMAN WHAT (why did it happen?)
#[Tom] Let’s see how you guys handle 5 3's.
#[Max] This is the last truthful bid. 9 3's.
#[Frank] Let's go with 10 3's.