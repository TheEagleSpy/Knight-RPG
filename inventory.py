import os
import time

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Compare old and new item stats
def stat_comparison(current_item, new_item, item_type):
    print("\n-----Item Comparison-----")

    def get_enchant_bonus(item):
        dmg_bonus = 0
        crit_bonus = 0
        if item and 'special' in item and item['special'] != "None":
            enchant = item['special']
            if enchant.startswith("Strength"):
                level = int(enchant.split()[1])
                dmg_bonus = {1: 0.35, 2: 0.75, 3: 1.50}[level]
            elif enchant.startswith("Precision"):
                level = int(enchant.split()[1])
                crit_bonus = level * 25
        return dmg_bonus, crit_bonus

    if item_type == "weapon":
        # Base stats
        curr_dmg = current_item['damage'] if current_item else 0
        new_dmg = new_item['damage']
        curr_crit = current_item['crit_chance'] if current_item else 0
        new_crit = new_item['crit_chance']

        # Enchant bonuses
        curr_dmg_bonus, curr_crit_bonus = get_enchant_bonus(current_item)
        new_dmg_bonus, new_crit_bonus = get_enchant_bonus(new_item)

        # Apply bonuses
        curr_total_dmg = curr_dmg + int(curr_dmg * curr_dmg_bonus)
        new_total_dmg = new_dmg + int(new_dmg * new_dmg_bonus)
        curr_total_crit = curr_crit + curr_crit_bonus
        new_total_crit = new_crit + new_crit_bonus

        # Differences
        dmg_diff = new_total_dmg - curr_total_dmg
        crit_diff = new_total_crit - curr_total_crit

        # Print current weapon
        print(f"Current Weapon: {current_item['name'] if current_item else 'None'}")
        print(f"  Damage: {curr_total_dmg}", end="")
        if curr_dmg_bonus > 0:
            print(f" (+{int(curr_dmg * curr_dmg_bonus)} from enchant)", end="")
        print()
        print(f"  Crit Chance: {curr_total_crit}%", end="")
        if curr_crit_bonus > 0:
            print(f" (+{curr_crit_bonus}% from enchant)", end="")
        print()
        print(f"  Enchantment: {current_item['special'] if current_item and 'special' in current_item else 'None'}")

        # Print new weapon
        dmg_color = GREEN if dmg_diff > 0 else RED if dmg_diff < 0 else RESET
        crit_color = GREEN if crit_diff > 0 else RED if crit_diff < 0 else RESET

        print(f"\nNew Weapon: {new_item['name']}")
        print(f"  Damage: {new_total_dmg}", end="")
        if new_dmg_bonus > 0:
            print(f" (+{int(new_dmg * new_dmg_bonus)} from enchant)", end="")
        print(f" {dmg_color}({'+' if dmg_diff > 0 else ''}{int(dmg_diff)}){RESET}")

        print(f"  Crit Chance: {new_total_crit}%", end="")
        if new_crit_bonus > 0:
            print(f" (+{new_crit_bonus}% from enchant)", end="")
        print(f" {crit_color}({'+' if crit_diff > 0 else ''}{int(crit_diff)}){RESET}")

        print(f"  Enchantment: {new_item['special'] if 'special' in new_item else 'None'}")

    else:  # Armour (no enchants)
        curr_def = current_item['defence'] if current_item else 0
        new_def = new_item['defence']
        def_diff = new_def - curr_def

        print(f"Current Armour: {current_item['name'] if current_item else 'None'}")
        print(f"  Defence: {curr_def}")
        print(f"  Enchantment: None")

        def_color = GREEN if def_diff > 0 else RED if def_diff < 0 else RESET
        print(f"\nNew Armour: {new_item['name']}")
        print(f"  Defence: {new_def} {def_color}({'+' if def_diff > 0 else ''}{def_diff}){RESET}")
        print(f"  Enchantment: None")

# Inventory Display
def inventory_display(player_data, weapons_data, armour_data):
    while True:
        time.sleep(0.15)
        os.system('cls')
        print("-----Inventory Menu-----")
        print("[1] Weapons")
        print("[2] Armour")
        print(f"[3] Use Health Potion ({player_data['health_potions']} left)")
        print("[r] Exit")

        choice = input("Enter: ").strip().lower()

        if choice == '1':
            display_weapons(player_data, weapons_data)
        elif choice == '2':
            display_armour(player_data, armour_data)
        elif choice == '3':
            use_health_potion(player_data)
            input("\nPress Enter to return to the menu: ")
        elif choice == 'r':
            break
        else:
            print("Invalid input. Please try again.")

# Display Weapons
def display_weapons(player_data, weapons_data):
    os.system('cls')
    print("-----Weapons-----")
    owned_weapons = player_data['owned_weapons']
    equipped_weapon = player_data.get('weapon_equipped', "")

    for index, weapon in enumerate(weapons_data, start=1):
        name = weapon['name']
        if name == equipped_weapon:
            tag = f"{YELLOW}(Equipped){RESET}"
        elif name in owned_weapons:
            tag = f"{GREEN}(Owned){RESET}"
        else:
            tag = f"{RED}(Not Owned){RESET}"
        print(f"[{index}] {name} {tag}")

    selection = input("\nSelect a weapon to view comparison or 'r' to return: ").strip().lower()
    if selection == 'r':
        return
    try:
        selection = int(selection)
        if 1 <= selection <= len(weapons_data):
            weapon = weapons_data[selection - 1]
            view_weapon_stats(player_data, weapon, weapons_data)
    except ValueError:
        print("Invalid input.")

# View Weapon Stats
def view_weapon_stats(player_data, weapon, weapons_data):
    os.system('cls')
    current_weapon_name = player_data.get('weapon_equipped', None)
    current_weapon = None
    for w in weapons_data:
        if w['name'] == current_weapon_name:
            current_weapon = w
            break

    stat_comparison(current_weapon, weapon, "weapon")

    equip = input("\nPress Enter to equip or 'r' to return: ").lower()
    if equip == "":
        if weapon['name'] not in player_data['owned_weapons']:
            print(f"\nYou do not own the {weapon['name']}.")
            return

        # Find old weapon before overwriting
        old_weapon_name = player_data.get('weapon_equipped', None)
        old_weapon_crit = 0

        if old_weapon_name:
            for w in weapons_data:
                if w['name'] == old_weapon_name:
                    _, old_crit_bonus = get_enchant_bonus(w)
                    old_weapon_crit = w.get('crit_chance', 0) + old_crit_bonus
                    break

        # Subtract old weapon crit
        player_data['crit_chance'] -= old_weapon_crit

        # Equip new weapon
        player_data['weapon_equipped'] = weapon['name']

        # Add new weapon crit
        _, new_crit_bonus = get_enchant_bonus(weapon)
        new_weapon_crit = weapon.get('crit_chance', 0) + new_crit_bonus

        player_data['crit_chance'] += new_weapon_crit

        print(f"\nYou have equipped the {weapon['name']}!")

    else:
        return

# Get Enchant Bonus
def get_enchant_bonus(item):
    dmg_bonus = 0
    crit_bonus = 0
    if item and 'special' in item and item['special'] != "None":
        enchant = item['special']
        if enchant.startswith("Strength"):
            level = int(enchant.split()[1])
            dmg_bonus = {1: 0.35, 2: 0.75, 3: 1.50}[level]
        elif enchant.startswith("Precision"):
            level = int(enchant.split()[1])
            crit_bonus = level * 25
    return dmg_bonus, crit_bonus

# Display Armour
def display_armour(player_data, armour_data):
    os.system('cls')
    print("-----Armour-----")
    owned_armour = player_data['owned_armour']
    equipped_armour = player_data.get('armour_equipped', "")

    for index, armour in enumerate(armour_data, start=1):
        name = armour['name']
        if name == equipped_armour:
            tag = f"{YELLOW}(Equipped){RESET}"
        elif name in owned_armour:
            tag = f"{GREEN}(Owned){RESET}"
        else:
            tag = f"{RED}(Not Owned){RESET}"
        print(f"[{index}] {name} {tag}")

    selection = input("\nSelect armour to view comparison or 'r' to return: ").strip().lower()
    if selection == 'r':
        return
    try:
        selection = int(selection)
        if 1 <= selection <= len(armour_data):
            selected_armour = armour_data[selection - 1]
            view_armour_stats(player_data, selected_armour, armour_data)
    except ValueError:
        print("Invalid input.")

# View Armour Stats
def view_armour_stats(player_data, selected_armour, armour_list):
    os.system('cls')
    current_armour_name = player_data.get('armour_equipped', None)
    current_armour = None
    for armour in armour_list:
        if armour['name'] == current_armour_name:
            current_armour = armour
            break

    stat_comparison(current_armour, selected_armour, "armour")

    equip = input("\nPress Enter to equip or 'r' to return: ").lower()
    if equip == "":
        if selected_armour['name'] in player_data['owned_armour']:
            current_def = get_equipped_armour_defence(player_data, armour_list)
            player_data['defence'] -= current_def
            player_data['armour_equipped'] = selected_armour['name']
            player_data['defence'] += selected_armour['defence']
            print(f"\nYou have equipped {selected_armour['name']}!")
        else:
            print(f"\nYou do not own {selected_armour['name']}.")
    else:
        return

# Get Equipped Armour Defence
def get_equipped_armour_defence(player_data, armour_list):
    equipped_armour_name = player_data.get('armour_equipped', None)
    for armour in armour_list:
        if armour['name'] == equipped_armour_name:
            return armour['defence']
    return 0

# Use Health Potion
def use_health_potion(player_data):
    if player_data['health_potions'] > 0:
        possible_health = player_data['max_health'] - player_data['health']
        if player_data['location'] == 'Forest':
            health_potion = 50
        elif player_data['location'] == 'Frozen Peaks':
            health_potion = 75
        elif player_data['location'] == "Swamplands":
            health_potion = 125
        else:
            print("You cannot use health potions here.")
            return

        if player_data['health'] < player_data['max_health']:
            healed = min(health_potion, possible_health)
            action = input(f"\nAre you sure you want to use a health potion? You will gain {healed} health.\nPress Enter to confirm or 'r' to return: ").strip().lower()
            if action == 'r':
                return
            else:
                player_data['health'] += healed
                print(f"\nYou drank the potion and gained {healed} Health!")
                player_data['health_potions'] -= 1
                print(f"\nYou have {player_data['health_potions']} health potions left.")
        else:
            print("\nYou're already at full health.")
    else:
        print("\nYou don't have any health potions.")

# Access Weapon Damage
def get_equipped_weapon_damage(player_data, weapons_data):
    equipped_weapon_name = player_data['weapon_equipped']
    for weapon in weapons_data:
        if weapon['name'] == equipped_weapon_name:
            return weapon['damage']
    return None