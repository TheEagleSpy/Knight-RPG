import os

# Inventory
def inventory_display(player_data, weapons_data, armour_data):
    os.system('cls')  # Clear CMD  

    owned_weapons = player_data['owned_weapons']
    
    # Display weapons
    print("-----Weapons-----")
    for index, weapon in enumerate(weapons_data, start=1):
        owned_tag = "(Owned)" if weapon['name'] in owned_weapons else "(Not Owned)"
        print(f"[{index}] {weapon['name']} {owned_tag}")

    # Display armor
    print("\n-----Armour-----")
    for index, armour in enumerate(armour_data, start=len(weapons_data) + 1):
        owned_tag = "(Owned)" if armour['name'] in player_data['owned_armour'] else "(Not Owned)"
        print(f"[{index}] {armour['name']} {owned_tag}")

    # Allow player to select a weapon or armor
    while True:
        try:
            selection = input("\nSelect an item to view stats\nPress 'r' to exit\nEnter: ").strip()
            
            if selection.lower() == 'r':
                break
            
            selection = int(selection)

            if 1 <= selection <= len(weapons_data):  # If selecting a weapon
                weapon = weapons_data[selection - 1]
                view_weapon_stats(player_data, weapon)
                break
            elif len(weapons_data) < selection <= len(weapons_data) + len(armour_data):  # If selecting armor
                selected_armour = armour_data[selection - len(weapons_data) - 1]  # Get selected armor dictionary
                view_armour_stats(player_data, selected_armour, armour_data)  # Pass the full list too
                break
            else:
                print("Invalid Input, Please Try Again")
        except ValueError:
            print("\nInvalid input! Please enter a number or 'r' to exit.")


# View Weapon Stats In Inventory
def view_weapon_stats(player_data, weapons_data):
    print(f"\n-----{weapons_data['name']} Stats-----")
    print(f"Damage: {weapons_data['damage']}")
    print(f"Critical Chance: {weapons_data['crit_chance']}%")
    if 'special' in weapons_data:
        print(f"Enchantment: {weapons_data['special']}")
    
    equip = input("\nPress Enter to equip this weapon or type 'r' to return: ").lower()
    if equip == "":
        if weapons_data['name'] in player_data['owned_weapons']:
            player_data['weapon_equipped'] = weapons_data['name']
            player_data['crit_chance'] = weapons_data['crit_chance']
            print(f"\nYou have equipped the {weapons_data['name']}!")
        else:
            print(f"\nYou do not own the {weapons_data['name']}.")
    elif equip == "r":
        return

# Access Weapon Damage
def get_equipped_weapon_damage(player_data, weapons_data):
    equipped_weapon_name = player_data['weapon_equipped']  # Get equipped weapon name
    
    # Search through all weapons to find the equipped weapon
    for weapon in weapons_data:
        if weapon['name'] == equipped_weapon_name:
            return weapon['damage']  # Return the damage of the equipped weapon
    return None

# Get Equipped Armour Defence
def get_equipped_armour_defence(player_data, armour_list):
    equipped_armour_name = player_data.get('armour_equipped', None)  # Get equipped armour name
    
    # Search through all armours to find the equipped one
    for armour in armour_list:  # Ensure we're looping over a list, not a single dictionary
        if armour['name'] == equipped_armour_name:
            return armour['defence']  # Return the defence of the equipped armour
    return 0  # Default to 0 if no armour is equipped
        
# Change the player defence when swapping armour         
def view_armour_stats(player_data, selected_armour, armour_list):
    print(f"\n----- {selected_armour['name']} Stats -----")
    print(f"Defence: {selected_armour['defence']}")

    equip = input("\nPress Enter to equip this armor or type 'r' to return: ").lower()
    if equip == "":
        if selected_armour['name'] in player_data['owned_armour']:
            # Get current defence before swapping
            current_defence = get_equipped_armour_defence(player_data, armour_list)

            # Remove current armour defence from player
            player_data['defence'] -= current_defence

            # Equip new armour
            player_data['armour_equipped'] = selected_armour['name']

            # Add new armour's defence
            player_data['defence'] += selected_armour['defence']

            print(f"\nYou have equipped {selected_armour['name']}!")
        else:
            print(f"\nYou do not own {selected_armour['name']}.")
    elif equip == "r":
        return
