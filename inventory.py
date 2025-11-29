import os
import time

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

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

    # Select weapon to view stats
    selection = input("\nSelect a weapon to view stats or 'r' to return: ").strip().lower()
    if selection == 'r':
        return
    try:
        selection = int(selection)
        if 1 <= selection <= len(weapons_data):
            weapon = weapons_data[selection - 1]
            view_weapon_stats(player_data, weapon)
    except ValueError:
        print("Invalid input.")

# View Weapon Stats
def view_weapon_stats(player_data, weapon):
    print(f"\n-----{weapon['name']} Stats-----")
    print(f"Damage: {weapon['damage']}")
    print(f"Critical Chance: {weapon['crit_chance']}%")
    if 'special' in weapon:
        print(f"Enchantment: {weapon['special']}")

    equip = input("\nPress Enter to equip or 'r' to return: ").lower()
    if equip == "":
        if weapon['name'] in player_data['owned_weapons']:
            player_data['weapon_equipped'] = weapon['name']
            player_data['crit_chance'] = weapon['crit_chance']
            print(f"\nYou have equipped the {weapon['name']}!")
        else:
            print(f"\nYou do not own the {weapon['name']}.")
    elif equip == "r":
        return

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

    selection = input("\nSelect armour to view stats or 'r' to return: ").strip().lower()
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
    print(f"\n----- {selected_armour['name']} Stats -----")
    print(f"Defence: {selected_armour['defence']}")

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
    elif equip == "r":
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
    equipped_weapon_name = player_data['weapon_equipped']  # Get equipped weapon name
    
    # Search through all weapons to find the equipped weapon
    for weapon in weapons_data:
        if weapon['name'] == equipped_weapon_name:
            return weapon['damage']  # Return the damage of the equipped weapon
    return None