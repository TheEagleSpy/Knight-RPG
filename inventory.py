# Inventory
def inventory_display(player_data, weapons_data):  
    print("\n-----Inventory-----")
    
    # Combine all weapon types into a single list
    all_weapons = weapons_data

    owned_weapons = player_data['owned_weapons']
    
    # Display all weapons with ownership tags
    for index, weapon in enumerate(all_weapons, start=1):
        owned_tag = "(Owned)" if weapon['name'] in owned_weapons else "(Not Owned)"
        print(f"[{index}] {weapon['name']} {owned_tag}")
    
    # Allow player to select a weapon
    while True:
        try:
            weapon_select = input("\n[1-11] Select a weapon to view its stats\nPress 'r' to exit\nEnter: ").strip()
            
            if weapon_select.lower() == 'r':
                break
            
            weapon_select = int(weapon_select)  # Convert input to an integer
            
            if 1 <= weapon_select <= len(all_weapons):
                weapon = all_weapons[weapon_select - 1]
                view_weapon_stats(player_data, weapon)  # Pass the selected weapon only
                break
            else:
                print("Invalid Input, Please Try Again")
        except ValueError:
            print("\nInvalid input! Please Enter a number or 'r' to exit.")

# View Weapon Stats In Inventory
def view_weapon_stats(player_data, weapons_data):
    print(f"\n-----{weapons_data['name']} Stats-----")
    print(f"Damage: {weapons_data['damage']}")
    print(f"Critical Chance: {weapons_data['crit_chance']}%")
    if 'special' in weapons_data:
        print(f"Enchantment: {weapons_data['special']}")
    
    equip = input("\nPress Enter to equip this weapon or type 'r' to return:").lower().strip()
    if equip == "":
        if weapons_data['name'] in player_data['owned_weapons']:
            player_data['weapon_equipped'] = weapons_data['name']
            player_data['crit_chance'] = weapons_data['crit_chance']
            print(f"\nYou have equipped the {weapons_data['name']}!")
        else:
            print(f"\nYou do not own the {weapons_data['name']}.")
    elif equip == "r":
        inventory_display(player_data, weapons_data)

# Access Weapon Damage
def get_equipped_weapon_damage(player_data, weapons_data):
    equipped_weapon_name = player_data['weapon_equipped']  # Get equipped weapon name
    
    # Search through all weapons to find the equipped weapon
    for weapon in weapons_data:
        if weapon['name'] == equipped_weapon_name:
            return weapon['damage']  # Return the damage of the equipped weapon
    return None