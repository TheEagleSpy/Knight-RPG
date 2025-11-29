# Modules
import time
import random
import sys
import json
import os

# Mechanics
from inventory import inventory_display
from inventory import get_equipped_weapon_damage
from tips import display_random_tip

# Minigames
from twentyone import play_21
from higherlower import play_higherlower
from rps import start_rps
from dungeons import dungeons
from geniewish import geniewish

SAVE_FILE = "savegame.json"

# Player Actions
healed_today = True
upgraded_armour = False

# Enemies

# -- Forest --
fight_boss = False
fight_caveman = False
fight_campfire_bandit = False
fight_bandit_outpost = False
fight_ghost = False
fight_merchant = False
fight_black_knight = False
fight_endless_road_skeleton = False
fight_bandit_leader = False
fight_villager = False

# -- Frozen Peaks --
fight_elder_yeti = False
fight_caravan = False

# Game Actions

# -- Forest --
viewed_map = False
encounter_1 = True
encounter_2 = False
helped_bob = False
seen_bob = False
seen_bounty_hunter = False
seen_hermit = False

# -- Frozen Peaks --
colours_left = 6
storm_power = 0
picked_events_left = 0

# Print text with delay fast
def Print(text, delay=0.02): #0.02 = 2ms
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()
    
# Print text with slow delay
def PRint(text, delay=0.03): #0.03 = 3ms
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

# Makes the game run (dont touch)
def start_game():
    # Sets up player data
    player_data = main_player()
    # Goes to next part of game one the previous is done
    start_prologue(settings)
    start_story(player_data, settings)
    start_ending()

# Starting Player Stats
def main_player():
    player_data = {
        "max_health": 100,
        "health": 100,
        "strength": 0,
        "defence": 0,
        "gold": 0,
        "day": 1,
        "location": 'Forest',
        "health_potions": 0,
        "armour_equipped": 'No Armour',
        "weapon_equipped": 'Bronze Sword',
        "crit_chance": 2,
        "owned_weapons": ["Bronze Sword"],
        "owned_armour": ["No Armour"],
        "companion": 0,
        "slime_kingdom": False,
    }
    return player_data

# Display player stats
def stat_display(player_data):
    os.system('cls') # Clear CMD
    print("-----Character Stats-----")
    print(f"Max Health: {player_data['max_health']}")
    print(f"Health: {player_data['health']}")
    print(f"Strength: {player_data['strength']}")
    print(f"Defence: {player_data['defence']}")
    print(f"Gold: {player_data['gold']}")
    print(f"Day: {player_data['day']}")
    print(f"Location: {player_data['location']}")
    print(f"Weapon: {player_data['weapon_equipped']}")
    print(f"Companions: {player_data['companion']}")
    print("\n-------------------------------------------------------------------------")

# Weapons Data
def weapons():
    weapons_data = [
        # Swords
        {"name": "Bronze Sword", "damage": 8, "crit_chance": 9, "special": "None"},
        {"name": "Iron Sword", "damage": 21, "crit_chance": 14, "special": "None"},
        {"name": "Steel Sword", "damage": 43, "crit_chance": 22, "special": "None"},
        {"name": "Flame Sword", "damage": 60, "crit_chance": 30, "special": "None"},
        {"name": "Frost Sword", "damage": 85, "crit_chance": 39, "special": "None"},
        {"name": "Shadow Blade", "damage": 145, "crit_chance": 25, "special": "Life Steal 1"},
        {"name": "Dragon Blade", "damage": 450, "crit_chance": 0, "special": "None"},
        # Bows
        {"name": "Hunting Bow", "damage": 25, "crit_chance": 5, "special": "None"},
        {"name": "Elven Bow", "damage": 45, "crit_chance": 11, "special": "None"},
        {"name": "Dragon Bow", "damage": 130, "crit_chance": 0, "special": "None"},
        # Spears
        {"name": "Eagle Spear", "damage": 35, "crit_chance": 100, "special": "None"},
    ]
    return weapons_data

# Sets up weapon data
weapons_data = weapons()

# Defence of armour
def armour():
    armour_data = [
        # Armour
        {"name": "No Armour", "defence": 0},
        {"name": "Cloth Armour", "defence": 4},
        {"name": "Iron Armour", "defence": 10},
        {"name": "Yeti Armour", "defence": 19},
        {"name": "Titanium Armour", "defence": 31},
        {"name": "Adamantium Armour", "defence": 40},
        {"name": "Dragonite Armour", "defence": 55},
        {"name": "Dragon Armour", "defence": 70},
    ]
    return armour_data

# Sets up Armour Data
armour_data = armour()

# Gives the player's current sword an enchant
def enchant_equipped_weapon(weapon):
    enchantments = {
        "Strength 1": {"type": "damage", "value": 35, "rarity": 0.3},
        "Strength 2": {"type": "damage", "value": 75, "rarity": 0.2},
        "Strength 3": {"type": "damage", "value": 150, "rarity": 0.1},
        "Precision 1": {"type": "crit", "value": 25, "rarity": 0.3},
        "Precision 2": {"type": "crit", "value": 50, "rarity": 0.2},
        "Life Steal 1": {"type": "lifesteal", "value": 10, "rarity": 0.3},
        "Life Steal 2": {"type": "lifesteal", "value": 15, "rarity": 0.2},
        "Life Steal 3": {"type": "lifesteal", "value": 20, "rarity": 0.1}
    }

    if "Sword" in weapon['name']:
        print(f"\nYour current enchantment is: {weapon['special']}")
        enchantment_pool = []
        for enchant, data in enchantments.items():
            enchantment_pool.extend([enchant] * int(data['rarity'] * 100))
        chosen_enchant = random.choice(enchantment_pool)
        answer = input(f"\nDo you want to replace it with '{chosen_enchant}' on your {weapon['name']}?\n[1] Yes\n[2] No\nEnter: ")
        if answer.startswith('1'):
            weapon['special'] = chosen_enchant
            print(f"\n{weapon['name']} has been enchanted with {chosen_enchant}!")
        else:
            print("\nEnchantment discarded.")
    else:
        print("\nThis weapon cannot be enchanted.")

# Selects the random sword Enchant
def random_enchant(player_data, weapons_data):
    weapon = next((i for i in weapons_data if i['name'] == player_data['weapon_equipped']), None)
    if weapon:
        enchant_equipped_weapon(weapon)

# Function to load settings from the JSON file
def load_settings(file_name):
    default_settings = {
        "skip_battles": False,
        "debugging": False,
        "skip_intro": False,
        "enter_to_continue": True,
    }

    if not os.path.exists(file_name) or os.path.getsize(file_name) == 0:
        print("New Save File Generated")
        # Save default settings to file
        with open(file_name, 'w') as save_file:
            json.dump(default_settings, save_file, indent=4)
        return default_settings

    try:
        with open(file_name, 'r') as save_file:
            settings = json.load(save_file)
        return settings
    except json.JSONDecodeError:
        print("Save file corrupted or invalid JSON. Resetting to default.")
        with open(file_name, 'w') as save_file:
            json.dump(default_settings, save_file, indent=4)
        return default_settings
    except Exception as e:
        print(f"Unexpected error loading settings: {e}")
        return default_settings

# Displays Settings    
def settings_display(settings):
    while True:
        os.system('cls')  # Clear CMD
        print("-----Settings-----")    
        print(f"[1] Skip Battles: {'True' if settings['skip_battles'] else 'False'}")
        print(f"[2] Skip Intro: {'True' if settings['skip_intro'] else 'False'}")
        print(f"[3] Press Enter After Events: {'True' if settings['enter_to_continue'] else 'False'}")
        print("[r] Exit")

        try:
            settings_choice = input("\nEnter: ").lower()
            if settings_choice == '1':
                settings["skip_battles"] = not settings["skip_battles"]
            elif settings_choice == '2':
                settings["skip_intro"] = not settings["skip_intro"]
            elif settings_choice == '3':
                settings["enter_to_continue"] = not settings["enter_to_continue"]
            elif settings_choice == 'r':
                print("\n-------------------------------------------------------------------------")
                break
            else:
                print("Invalid option. Please try again.")

            # Write the updated settings to file
            with open('savedata.json', 'w') as save_file:
                json.dump(settings, save_file, indent=4)

        except ValueError:
            print("Invalid input! Please Enter a number.")

# List of settings        
settings = {
    "skip_battles": False,
    "debugging": False,
    "skip_intro": False,
    "enter_to_continue": True,
}

# Sets the game settings as the saved settings
settings = load_settings('savedata.json')

# Saves the settings to a JSON file
save_data = {key: f"{key} = {value}" for key, value in settings.items()}

# Uses a health potion if allowed
def use_health_potion(player_data):
    possible_health = player_data['max_health'] - player_data['health'] 
    if player_data['location'] == 'Forest':
        health_potion = 50
        if player_data['health'] < player_data['max_health']:
            healed = min(health_potion, possible_health)
            player_data['health'] += healed
            Print(f"You drank the potion and gained {healed} Health")
        else:
            Print("You're already at full health.")
    elif player_data['location'] == 'Frozen Peaks':
        health_potion = 75
        if player_data['health'] < player_data['max_health']:
            healed = min(health_potion, possible_health)
            player_data['health'] += healed
            Print(f"You drank the potion and gained {healed} Health")
        else:
            Print("You're already at full health.")
    elif player_data['location'] == "Swamplands":
        health_potion = 125
        if player_data['health'] < player_data['max_health']:
            healed = min(health_potion, possible_health)
            player_data['health'] += healed
            Print(f"You drank the potion and gained {healed} Health")
        else:
            Print("You're already at full health.")
    else:
        Print("You cannot use health potions here")

# Function to generate random effects
def random_berry_effect(player_data):
    effect_type = random.choice(["increase", "increase", "decrease", "decrease", "decrease"])  # Randomly decide if the effect is positive or negative
    if player_data['location'] == "Forest":
        stat = random.choice(["max_health", "health", "gold"])  # Randomly choose a stat
        amount = random.randint(1, 3)  # Random effect amount
    else:
        stat = random.choice(["max_health", "health", "gold", "crit_chance", "defence"])  # Randomly choose a stat
        amount = random.randint(2, 7)  # Random effect amount for other locations
    
    # Apply effect
    if effect_type == "increase":
        player_data[stat] += amount
        return f"increases your {stat.replace('_', ' ')} by {amount}!"
    else:
        player_data[stat] -= amount
        check_death(player_data)
        return f"decreases your {stat.replace('_', ' ')} by {amount}."
        
# Slime Kingdom with blacksmith and shop
def slime_kingdom(player_data):
    os.system('cls')
    Print("You head towards the slime kingdom")
    while True:
        action = input("\n---Slime Kingdom---\n[1] Merchant\n[2] Blacksmith\n[r] Leave\nEnter: ")
        if action == '1':
            forest_merchant(player_data)
        elif action == '2':
            forest_blacksmith(player_data, weapons_data, armour_data)
        elif action == 'r':
            break
        else:
            Print("Please Enter a number between 1 and 2")

# -- Forest -- #

# Forest Enemies list
def enemy_data_forest():
    # Easy
    rock = {"name": "Pet Rock", "health": 5, "strength": -5, "gold": 5}
    weak_goblin = {"name": "Weak Goblin", "health": 10, "strength": 3, "gold": 25}
    strong_goblin = {"name": "Strong Goblin", "health": 19, "strength": 7,  "gold": 40}
    orc = {"name": "Orc", "health": 30, "strength": 8, "gold": 25}
    weak_bandit = {"name": "Weak Bandit", "health": 50, "strength": 5, "gold": 35}
    skeleton = {"name": "Skeleton", "health": 20, "strength": 6, "gold": 5}
    wild_dog = {"name": "Wild Dog", "health": 30, "strength": 9, "gold": 5}
    strong_orc = {"name": "Strong Orc", "health": 35, "strength": 13, "gold": 20}
    treasure_chest = {"name": "Treasure Chest", "health": 5, "strength": -5, "gold": 100}
    # Medium
    fly = {"name": "Fly", "health": 10, "strength": 90, "gold": 30}
    albert = {"name": "Albert (homeless)", "health": 50, "strength": 9, "gold": 5}
    defensive_bird = {"name": "Defensive Bird", "health": 25, "strength": 9, "gold": 10}
    wolf = {"name": "Wolf", "health": 40, "strength": 6, "gold": 15}
    cursed_spirit = {"name": "Cursed Spirit", "health": 35, "strength": 15, "gold": 30}
    tree_ent = {"name": "Tree Ent", "health": 65, "strength": 8, "gold": 120}
    sword_skeleton = {"name": "Sword Skeleton", "health": 20, "strength": 20, "gold": 50}
    # Hard
    giant_orc = {"name": "Giant Orc", "health": 65, "strength": 17, "gold": 50}
    metal_skeleton = {"name": "Metal Skeleton", "health": 60, "strength": 16, "gold": 60}
    strong_bandit = {"name": "Strong Bandit", "health": 100, "strength": 13, "gold": 85}
    distorted_figure = {"name": "Distorted Figure", "health": 40, "strength": 35, "gold": 65}
    # Boss
    howler = {"name": "Howler", "health": 300, "strength": 25, "gold": 300}
    # Random encounter enemies
    caveman = {"name": "Cave Man", "health": 30, "strength": 8, "gold": 40}
    campfire_bandit = {"name": "Bandit", "health": 40, "strength": 7, "gold": 30}
    ghost = {"name": "Ghost", "health": 70, "strength": 10, "gold": 50}
    merchant = {"name": "Merchant", "health": 100, "strength": 3, "gold": 125}
    black_knight = {"name": "Black Knight", "health": 150, "strength": 11, "gold": 0}
    endless_road_skeleton = {"name": "Old Skeleton", "health": 21, "strength": 6, "gold": 5}
    bandit_leader = {"name": "Bandit Leader", "health": 75, "strength": 11, "gold": 85}
    villager = {"name": "Villager", "health": 35, "strength": 6, "gold": 0}
    
    global fight_boss, fight_caveman, fight_campfire_bandit, fight_bandit_outpost, fight_ghost, fight_merchant, fight_black_knight, fight_endless_road_skeleton, fight_bandit_leader, fight_villager

    if fight_boss == True:
        current_enemy = howler
    elif fight_caveman == True:
        current_enemy = caveman
    elif fight_campfire_bandit == True:
        current_enemy = campfire_bandit
    elif fight_bandit_outpost == True:
        enemy_type = random.random()
        if enemy_type <= 0.65: # 65%
            current_enemy = weak_bandit
        else: # 35%
            current_enemy = strong_bandit
    elif fight_ghost == True:
        current_enemy = ghost
    elif fight_merchant == True:
        current_enemy = merchant
    elif fight_black_knight == True:
        current_enemy = black_knight
    elif fight_endless_road_skeleton == True:
        current_enemy = endless_road_skeleton
    elif fight_bandit_leader == True:
        current_enemy = bandit_leader
    elif fight_villager == True:
        current_enemy = villager
    
    else:
        enemy_type = random.random()
        if enemy_type <= 0.60: # Easy Enemies (60%)
            random_enemy = random.random()
            if random_enemy <= 0.05: # 5%
                current_enemy = rock
            elif random_enemy <= 0.20: # 15%
                current_enemy = weak_goblin
            elif random_enemy <= 0.35: # 15% 
                current_enemy = strong_goblin
            elif random_enemy <= 0.45: # 10%
                current_enemy = orc
            elif random_enemy <= 0.55: # 10%
                current_enemy = weak_bandit
            elif random_enemy <= 0.70: # 15%
                current_enemy = skeleton
            elif random_enemy <= 0.80: # 10%
                current_enemy = wild_dog
            elif random_enemy <= 0.95: # 15%
                current_enemy = strong_orc
            else:
                current_enemy = treasure_chest
        elif enemy_type <= 0.90: # Medium Enemies (25%)
            random_enemy = random.random()
            if random_enemy <= 0.05: # 5%
                current_enemy = fly
            elif random_enemy <= 0.10: # 5%
                current_enemy = albert
            elif random_enemy <= 0.40: # 30%
                current_enemy = defensive_bird
            elif random_enemy <= 0.60: # 20%
                current_enemy = wolf
            elif random_enemy <= 0.85: # 25%
                current_enemy = cursed_spirit
            elif random_enemy <= 0.95: # 10%
                current_enemy = tree_ent
            else:
                current_enemy = sword_skeleton # 5%
        else: # Hard Enemies (10%)
            random_enemy = random.random()
            if random_enemy <= 0.20: # 20%
                current_enemy = giant_orc
            elif random_enemy <= 0.60: # 30%
                current_enemy = metal_skeleton
            elif random_enemy <= 0.85: # 25%
                current_enemy = strong_bandit
            else: # 15%
                current_enemy = distorted_figure

    return current_enemy

# Player explores forest
def explore_forest(player_data, weapons_data):
    global viewed_map,fight_boss, fight_caveman, fight_campfire_bandit, fight_ghost, helped_bob, seen_bob, seen_bounty_hunter, seen_hermit, upgraded_armour, fight_merchant, fight_black_knight, fight_endless_road_skeleton, fight_bandit_leader, fight_villager
    exploration_time = random.randint(3, 6) # How many events the player in encounter
    
    while True:
        if exploration_time > 0:
            if settings['debugging'] == False:
                exploration = random.random()
                
            else:
                try:
                    exploration = float(input("0 Exploration, 0.6 Shrine, 0.7 Trap, 0.95 Enemy, 1 Merchant\nExploration value: "))
                except ValueError:
                    exploration = random.random()
                    
            # Random Events
            # Main Exploration
            if exploration <= 0.50:
                
                Print("\n-----Wilderness Exploration-----")
                if settings['debugging'] == False:
                    random_event = random.random()
                    
                else: # if player enables debug they can change the event
                    try:
                        print("0.05 Cave, 0.10 House, 0.15 Sunny Field, 0.20 Elf, 0.25 Campsite, 0.30 Animal Attack, 0.35 Strength Plant, 0.40 Lost Villager, 0.45 Endless Road, 0.50 Bandit Outpost")
                        print("0.55 Catapiller Queen, 0.60 Encounter Bob, 0.65 Bounty Hunters, 0.70 Dark Witch, 0.75 Friendly Enemy, 0.80 Gotton Lost, 0.85 Berries, 0.90 Slime Kingdom, 0.95 Blacksmith, 1 Nothing")
                        random_event = float(input("Exploration value: "))
                    except ValueError:
                        random_event = random.random()
                        
                if random_event <= 0.05: # Cave event
                    Print("You find a cave that looks lived in...\n\n[Knight] I hope they aren't nearby")
                    cave_event = random.random()
                    
                    if cave_event <= 0.25:
                        Print("[Knight] Eww it stinks in here, wait, is that?")
                        time.sleep(2)
                        Print("\nYou see a half eaten human corspe and leave immediately")
                        
                    elif cave_event <= 0.50:
                        while True:
                            action = input("You find a potion on the table\n\n[1] Drink\n[2] Leave\nEnter: ")
                            
                            if action == '1':
                                Print("\n[Knight] Ooh a weird potion, I shall drink it!")
                                time.sleep(2)
                                potion_effect = random.random()
                                
                                if potion_effect <= 0.20:
                                    Print("[Knight] I don feel so goo-")
                                    Print("\nYou pass out...")
                                    time.sleep(2)
                                    Print("\n[Goblin] Haha your gold is now mine")
                                    Print(f"-{player_data['gold']} Gold")
                                    player_data['gold'] = 0
                                    
                                elif potion_effect <= 0.60:
                                    Print("[Knight] This tastes interesting")
                                    Print("\nYou suddenly feel warm...")
                                    time.sleep(2)
                                    Print("+30 Health")
                                    player_data['health'] += 30
                                    
                                elif potion_effect <= 0.80:
                                    Print("[Knight] Give me another! This is tastes awesome\n+20 Max Health\n+50 Health")
                                    player_data['max_health'] += 20
                                    player_data['health'] += 50
                                    
                                else:
                                    Print("[Knight] I sure do love me some water")
                                    Print("+10 Health")
                                    player_data['health'] += 10
                                break           
                            elif action == '2':
                                Print("You break the potion on the floor and leave the house before anything weird happens")
                                break
                            else:
                                Print("Please enter a number between 1 and 2")
                                
                    elif cave_event <= 0.75:
                        Print("You checked every corner and found nothing")
                        Print("[Knight] Well that was a waste of time")
                        
                    else:
                        Print("You checked every corner and found nothing")
                        Print("You leave...")
                        time.sleep(2)
                        Print("[Knight] Gah! Who are you?")
                        fight_caveman = True
                        battle(player_data)
                        fight_caveman = False
                        
                elif random_event <= 0.10: # House Event
                    Print("You stumble into a run down wooden house amoung the trees")
                    
                    while True:
                        action = input("\n[Knight] This doesn't look dangerous at all\n\n[1] Investigate\n[2] Leave\nEnter: ")
                        if action == '1':
                            
                            house_event = random.random()
                            
                            if house_event <= 0.25:
                                Print("You see a ghost and it starts swinging at you")
                                fight_ghost = True
                                battle(player_data)
                                fight_ghost = False
                                
                            elif house_event <= 0.50:
                                Print("\n[Knight] The door wont open... guess I'll continue on")
                                
                            elif house_event <= 0.75:
                                Print("\nYou walk up to the door and it opens. You look around for danger then head inside")
                                house_luck = random.random()
                                if house_luck <= 0.33:
                                    chest_reward = random.randint(35, 300)
                                    Print(f"After exploring around the house for while you find a chest with {chest_reward} Gold.\n\n[Knight] It has an ominous glow...")
                                    time.sleep(2)
                                    action = input("\n[1] Take Chest\n[2] Leave House\nEnter: ")
                                    if action == '1':
                                        player_data['health'] -= 10
                                        Print("You take the chest and lose 10 Health")
                                        check_death(player_data)
                                        Print(f"+{chest_reward} Gold!")
                                        player_data['gold'] += chest_reward
                                    elif action == '2':
                                        Print("You continue looking and find nothing so you leave")
                                    else:
                                        Print("\nPlease Enter a number between 1 and 2")
                                    break
                                elif house_luck <= 0.66:
                                    Print(f"\nAfter checking the downstairs you head into the attic finding a mysterious book. You open it and in a sudden flash of light it takes the {player_data['weapon_equipped']} out of your hand and enchants it:") # NOT FINISHED
                                    random_enchant(player_data, weapons_data)
                                else:
                                    Print("Suddenly you fall into the floor getting your foot stuck\n-5 Health")
                                    player_data['health'] -= 5
                            
                            else:
                                Print("\nYou find armour plating\n+2 Armour Defence")
                                for armour in armour_data:
                                    if armour['name'] == player_data['armour_equipped']:
                                        armour['defence'] += 2
                                        player_data['defence'] += 2
                            break
                        
                        elif action == '2':
                            Print("You leave the house safely")
                            break
                    
                elif random_event <= 0.15: # Plant Event
                    Print("You come across a flower field and the sun starts shining\n+5 Max Health\n+10 Health\n+1 Strength\n+1 Weapon Damage\n+1 Armour Toughness\n+20 Gold")
                    player_data['max_health'] += 5
                    player_data['health'] += 10
                    player_data['gold'] += 20
                    Print("\n[Knight] Its a good day today")
                    if player_data['health'] > 0:
                        for armour in armour_data:
                            if armour['name'] == player_data['armour_equipped']:
                                armour['defence'] += 1
                                player_data['defence'] += 1
                    
                    elif player_data['health'] > 0:
                        for weapon in weapons_data:
                            if weapon['name'] == player_data['weapon_equipped']:
                                weapon['damage'] += 1
                
                elif random_event <= 0.20: # Elf Event
                    Print("You walk into a mystical clearing filled with crystals and tall flowers surrounding it")
                    Print("\n[Kind Elf] Welcome...")
                    time.sleep(1.5)
                    Print("[Kind Elf] I see you struggling and I wish to grant you something of your choosing\n")
                    time.sleep(1.5)
                    elf_luck = random.random()
                    if elf_luck <= 0.33:
                        while True:
                            action = input(f"[1] Double your current Gold, Current Gold: {player_data['gold']}\n[2] Sharper Sword (+3 Attack)\n[3] +30 Max Health\nEnter: ")
                            if action == '1':
                                player_data['gold'] *= 2
                                Print(f"\n[Kind Elf] Your wish has been granted you now have: {player_data['gold']} Gold!")
                                break
                            elif action == '2':
                                for weapon in weapons_data:
                                    if weapon['name'] == player_data['weapon_equipped']:
                                        weapon['damage'] += 3
                                        Print(f"\n[Kind Elf] I believe this will do you well:\n+3 Damage!")
                                break
                            elif action == '3':
                                player_data['max_health'] += 30
                                player_data['health'] += 30
                                Print("\n[Kind Elf] You are now stronger than ever, go complete your quest\n+30 Max Health")
                                break
                            else:
                                Print("\nPlease Enter a number between 1 and 3")
                            
                    elif elf_luck <= 0.66:
                        while True:
                            action = input("[1] Random Enchantment\n[2] Free Steel Sword\n[3] 60% Crit rate with current weapon\nEnter: ")
                            if action == '1':
                                random_enchant(player_data, weapons_data)
                                break
                            elif action == '2':
                                player_data['owned_weapons'].append("Steel Sword")
                                player_data['weapon_equipped'] = "Steel Sword"
                                Print("\n[Kind Elf] Well here is your new ☆ Steel Sword ☆... Enjoy")
                                break
                            elif action == '3':
                                Print("\n[Kind Elf] Now you can deal more damage more often!")
                                for weapon in weapons_data:
                                    if weapon["name"] == player_data["weapon_equipped"]:  
                                        weapon["crit_chance"] += 60
                                        player_data['crit_chance'] += 60
                                        break
                                break
                            else:
                                Print("\nPlease Enter a number between 1 and 3")

                    else:
                        while True:
                            action = input(f"[1] +3 Weapon Damage\n[2] +125 Gold\n[3] Set Max Health between 75 and 165\nEnter: ")
                            if action == '1':
                                Print("\nYour Sword's blade shines against the sun")
                                for weapon in weapons_data:
                                    if weapon["name"] == player_data["weapon_equipped"]:  
                                        weapon["damage"] += 3
                                        break
                                break
                            elif action == '2':
                                Print("\nYour money bag starts to fill up as 125 gold coins are placed into it")
                                player_data['gold'] += 125
                                break
                            elif action == '3':
                                player_data['max_health'] = random.randint(75, 165)
                                Print(f"\n[Kind Elf] your new max health is {player_data['max_health']}!")
                                break
                            else:
                                Print("\nPlease Enter a number between 1 and 3")            

                elif random_event <= 0.25: # Campsite Event
                    Print("You stumbled upon an abandoned campsite.")
                    Print("The campsite seems deserted, but it might have valuable resources.")

                    while True:
                        action = input("\n[1] Loot Campsite\n[2] Rest without looting\n[3] Continue on your journey\nEnter: ")
                        if action == "1":
                            Print("\nYou carefully search the campsite for anything useful.\n")
                            campsite_event = random.random()

                            if campsite_event < 0.4:
                                old_gold = player_data['gold']
                                player_data['gold'] += random.randint(10, 50)
                                new_gold = player_data['gold'] - old_gold
                                Print(f"You found some gold coins hidden under a pile of ashes!\n+{new_gold} Gold")
                                
                                
                            elif campsite_event < 0.7:
                                for armour in armour_data:
                                    if armour['name'] == player_data['armour_equipped']:
                                        Print("You found an old piece of wood that you stick to your armour for extra defence\n+1 Defence")
                                        armour['defence'] += 1
                                        player_data['defence'] += 1
                                
                            else:
                                old_health = player_data['health']
                                player_data['health'] -= random.randint(5, 15)
                                new_health = old_health - player_data['health']
                                Print(f"While searching, you disturbed a snake and got bitten!\n-{new_health} Health")
                            break   

                        elif action == "2":
                            Print("\nYou decide to rest at the campsite.\n")
                            campsite_event = random.random()

                            if campsite_event < 0.5:
                                Print("After a long rest your health is restored to max")
                                player_data['health'] = player_data['max_health']
                            else:
                                fight_campfire_bandit = True
                                Print("You were attacked by bandits during your rest.")
                                battle(player_data)
                                fight_campfire_bandit = False
                            break
                        
                        elif action == "3":
                            Print("You decide to leave the campsite alone. Better safe than sorry.")
                            
                            break
                        else:
                            Print("Please Enter a number between 1 and 3")
                elif random_event <= 0.30: # Animal Attack
                    Print("A wild animal attacks you unexpectedly!")
                    Print("It does 15 Damage!")
                    player_data['health'] -= 15
                    check_death(player_data)
                    Print("However you manage to kill it before it does anything else")

                elif random_event <= 0.35: # Edible Plants Event
                    Print("You found a rare edible plant and decide to eat it")
                    Print("+2 Strength")
                    player_data['strength'] += 2

                elif random_event <= 0.40: # Lost Villager
                    Print("You encounter a lost looking villager on the side of the path")

                    action = input("\n[Knight] Should I go and investigate?\n\n[1] Walk up to him\n[2] Walk the other way\nEnter: ")

                    if action == "1":
                        Print("\nYou cautiously approach the villager, who notices you and looks relieved.")
                        Print("\n[Villager] Oh, thank the heavens! I’ve been wandering for hours...")
                        choice = input("\n[1] Help out\n[2] Rob\nEnter: ")

                        if choice == "1":
                            Print("[Knight] What happened to you?")
                            Print("\n[Villager] My village was raided by bandits, and I got separated from my family...")
                            time.sleep(1.5)
                            outcome = random.random()

                            if outcome < 0.3:
                                Print("The villager bursts into tears and hands you a family heirloom, insisting you keep it for protection.\n+2 Defence")
                                player_data['defence'] += 2
                            elif outcome < 0.6:
                                Print("The villager gives you some money and says to meet him back here if you ever find his family.\n+25 Gold")
                                player_data['gold'] += 25
                            else:
                                Print("[Villager] May I please come with you along your adventure as word is that you are going to travel through the village or Klare.")
                                Print("\n[Knight] Yes, you may... as long as you help me")
                                Print("\n[Villager] I promise to, good knight")
                                player_data['companion'] += 1
                                
                        elif choice == '2':
                            Print("\n[Knight] Give me all your money!")
                            Print("\n[Villager] No please, I have just lost my family as my village was raided by bandits")
                            Print("\n[Knight] Well that sounds unfortunate")
                            Print("[Knight] I'll just take this and be on my way\n+25 Gold\n\nYou found a defence charm\n+2 Defence")
                            player_data['defence'] += 2
                            player_data['gold'] += 25
                            Print("\n[Villager] No you wont! 😭")
                            fight_villager = True
                            battle(player_data)
                            fight_villager = False
                            
                        else:
                            Print("Please Enter a number between 1 and 2")
                    elif action == '2':
                        Print("You head the other way as he aimlessly stumbles around")
                    else:
                        Print("Please Enter a number between 1 and 2")
                        
                elif random_event <= 0.45: # Endless Road Event
                    
                    escape_chance = 0  # Initial escape chance percentage

                    Print("Welcome to the Endless Road! Can you find your way out?")
                    while True:
                        # Escape once escape chance hits 100
                        Print(f"\n---You are currently {escape_chance}% of the way escaped from the road---\n")
                        if escape_chance >= 100:
                            Print("\nYou found the way out! Congratulations!\n+125 Gold")
                            player_data['gold'] += 125
                            break

                        # Random event
                        road_luck = random.random()
                        
                        if road_luck <= 0.15:  # Go left or right
                            Print("You find a fork in the road.")

                            while True:
                                action = input("Which way do you go?\n\n[1] Left\n[2] Right\n[3] Straight\nEnter: ")
                                
                                if action == '1':
                                    if viewed_map:
                                        Print("After following the directions on the map you make your way off the road!")
                                        escape_chance = 100     
                                    Print("You encounter a strange glowing crystal. It hums with energy.\n+1 Strength\n-1 Defence")
                                    player_data['strength'] += 1
                                    for armour in armour_data:
                                        if armour['name'] == player_data['armour_equipped']:
                                            armour['defence'] -= 1
                                            player_data['defence'] -= 1
                                    escape_chance += 5
                                    break

                                elif action == '2':
                                    Print("A dense fog surrounds you, and you hear whispers from all around.\n-10 Health")
                                    player_data['health'] -= 10
                                    escape_chance -= 5
                                    break

                                elif action == '3':
                                    random_event = random.random()
                                    
                                    if random_event <= 0.10:
                                        Print("You fall into a hole with a clock which takes you back to Day 1 with all your stats and past decisions with extra defence and strength\nDay = 1\n+3 Strength\n+3 Defence")
                                        time.sleep(2)
                                        player_data['day'] = 1
                                        exploration_time = 0
                                        player_data['defence'] += 3
                                        player_data['strength'] += 3
                                        escape_chance = 100
                                        player_data['health'] += 10
                                        break
                                    
                                    elif random_event <= 0.35:
                                        Print("You Brush past the bushes and find...")
                                        time.sleep(2)
                                        Print("Absolutely nothing")
                                        
                                    elif random_event:
                                        Print("You Brush past the bushes and find...")
                                        time.sleep(2)
                                        Print("A skeleton that gets up and attacks you!")
                                        fight_endless_road_skeleton = True
                                        battle(player_data)
                                        fight_endless_road_skeleton = False
                                        check_death(player_data)
                                    break
                                else:
                                    Print("You are unsure, so you spin in a circle and walk forward")
                                    action = '2'

                        elif road_luck <= 0.25:  # Abandoned Camp
                            Print("You stumble across an abandoned campsite.")
                            while True:
                                action = input("What do you do?\n\n[1] Search the camp\n[2] Move on\nEnter: ")
                                if action == '1':
                                    Print("You find some food on the campfire, but the air feels ominous.")
                                    print("+25 Health")
                                    player_data['health'] += 25
                                    Print("\n[Knight] I better get out of here before something bad happens")
                                    break
                                elif action == '2':
                                    Print("You leave the camp behind and continue on your journey.")
                                    escape_chance += 15
                                    break

                        elif road_luck <= 0.35:  # Hermit Event
                            Print("You come across a Hermit sitting by a fire next to the path.")
                            while True:
                                action = input("What do you do?\n\n[1] Talk to him\n[2] Ignore him\nEnter: ")
                                if action == '1':
                                    if seen_hermit == False:
                                        PRint("[Hermit] Another wanderer, lost in the endless road. Sit. Listen.")
                                        time.sleep(2)
                                        PRint("[Knight] What is it you want, hermit?")
                                        time.sleep(2)
                                        PRint("[Hermit] I once walked as you do, blade in hand, fire in my heart. Until... I hunted the Howler.")
                                        PRint("[Knight] The Howler? That's just a myth.")
                                        time.sleep(1)
                                        PRint("[Hermit] That's what I thought... until I heard its cry in the dead of night. A sound that tears through you, a wail that breaks the mind. And then I saw it.")
                                        time.sleep(7)
                                        PRint("\nThe Hermit's voice breaks, his eyes hollow as if reliving the moment.\n")
                                        time.sleep(3)
                                        PRint("[Hermit] A beast born from nightmares. Eyes like burning coals. A mouth that stretched too wide, too many teeth. Its flesh swallowed my arrows, its skin turned my sword to dust.")
                                        PRint("[Knight] And how are you here talking to me?")
                                        PRint("[Hermit] I learned its secret. It fears itself. The reflection turns its power inward, shattering its form like brittle glass.")
                                        time.sleep(8)
                                        PRint("\nA gust of wind runs through the ruins around you. The fire crackles, and shadows quickly move along the hermit's face.\n")
                                        time.sleep(3)
                                        PRint("[Knight] So you defeated it?")
                                        PRint("[Hermit] No such victory is ever so easy. I lured it to the stillest pool I could find. It peered into the water, and for the first time, it saw itself. The scream it unleashed—")
                                        time.sleep(2)
                                        PRint("\nThe Hermit grips his sword, knuckles white. His breath turns shallow.\n")
                                        time.sleep(2)
                                        PRint("[Hermit] It was not pain. It was recognition. It saw what it was. What it had become. And for a single, trembling second, it hesitated.")
                                        PRint("[Knight] And you struck.")
                                        PRint("[Hermit] I plunged the remaining of my blade into its heart... I felt it die by my hands. And yet…")
                                        time.sleep(5)
                                        PRint("\nThe fire dims.\n")
                                        time.sleep(4)
                                        PRint("[Knight] Yet what?")
                                        PRint("[Hermit] I'm here. I have tried to leave, countless times. But the Howler was no ordinary beast. When I killed it, something took its place.")
                                        time.sleep(4)
                                        PRint("[Knight] What do you mean?")
                                        PRint("[Hermit] The Howler is not a creature. It is a curse. A hunter must always remain. It watches, waits, and when the path is dark… it returns.")
                                        time.sleep(3)
                                        PRint("[Knight] Are you saying—")
                                        time.sleep(1)
                                        PRint("[Hermit] One day, you too may hear its cry. When you do, pray you are ready.")
                                        time.sleep(4)
                                        PRint("\nThe Hermit's eyes fill with something unspoken. A weight settles in your chest, but also a fire.\n")
                                        seen_hermit = True
                                        
                                    Print("+1 Strength\n+10 Max Health\n+20 Health")
                                    player_data['strength'] += 1
                                    player_data['max_health'] += 10
                                    player_data['health'] += 20
                                    escape_chance += 5
                                    break

                                elif action == '2':
                                    Print("The hermit slowly shakes his head as you walk away.")
                                    escape_chance += 10
                                    break

                                else:
                                    Print("Please Enter a number between 1 and")

                        elif road_luck <= 0.45: # Storm
                            Print("A sudden storm rages around you, making it hard to see.")
                            while True:
                                action = input("What do you do?\n\n[1] Wait for the storm to pass\n[2] Push on\nEnter: ")
                                if action == '1':
                                    Print("The storm passes, but you feel like you lost precious time.")
                                    escape_chance -= 10
                                    break
                                elif action == '2':
                                    Print("You brave the storm but emerge exhausted and injured.\n-5 Max Health\n-5 Health")
                                    player_data['max_health'] -= 5
                                    player_data['health'] -= 5
                                    escape_chance += 10
                                    check_death(player_data)
                                    break
                                else:
                                    Print("Please Enter a number between 1 and 2")
                                
                                
                        elif road_luck <= 0.60:  # River Event
                            Print("You hear a distant sound of rushing water.")
                            while True:
                                action = input("What do you do?\n\n[1] Investigate\n[2] Stay on the path\nEnter: ")
                                if action == '1':
                                    Print("You discover a river that seems to block your path.")
                                    river_event = random.randint(1, 4)
                                    if river_event == 1:
                                        Print("You find a bridge and cross safely.")
                                        escape_chance += 10
                                    elif river_event == 2 or 3:
                                        Print("You swim across, but the current is strong.\n-5 Health")
                                        player_data['health'] -= 5
                                        escape_chance += 10
                                    elif river_event == 4:
                                        Print("You slip and fall in! It takes time to get out so you continue on the path now cold.\n-10 Health")
                                        escape_chance -= 10
                                        player_data['health'] -= 10
                                    break
                                elif action == '2':
                                    Print("You stay on the path, avoiding danger.")
                                    escape_chance += 10
                                    break
                                else:
                                    Print("Please Enter a number between 1 and 2")
                                check_death(player_data)

                        elif road_luck <= 0.75: # Find map
                            Print("You find an old map on the ground.")
                            while True:
                                action = input("What do you do?\n\n[1] Study the map\n[2] Leave it\nEnter: ")
                                if action == '1':
                                    Print("\nYou stare at the blank paper for a while, after turning it over it says 'Right is for the weak, Left is for the Strong and if you go straight you might run into a bomb'")
                                    viewed_map == True
                                    break
                                elif action == '2':
                                    Print("You ignore the map and continue on.")
                                    escape_chance += 15
                                    break
                                else:
                                    Print("Please Enter a number between 1 and 2")
                        elif road_luck >= 0.90:  # Lost Villager Event
                            Print("A strange shadow follows you silently.")
                            while True:
                                action = input("What do you do?\n\n[1] Confront it\n[2] Ignore it\nEnter: ")
                                if action == '1':
                                    villager_event = random.randint(1, 3)
                                    if villager_event <= 1:
                                        Print("The shadow reveals itself to be a lost villager who is grateful for your help.")
                                        Print("They hand you a small bag of gold.\n+50 Gold")
                                        player_data['gold'] += 50
                                    elif villager_event == 2:
                                        Print("The person begs for food. You give them a berry you found, and they give you a map in return.")
                                        viewed_map = True
                                    elif villager_event == 3:
                                        Print("As you step closer, the shadow lunges at you! It's a bandit!\n-20 Health")
                                        player_data['health'] -= 20
                                    check_death(player_data)
                                    break
                                elif action == '2':
                                    Print("The shadow fades into the darkness.")
                                    break
                                else:
                                    Print("Please Enter a number between 1 and 2")
                        else:
                            Print("You come across a tower and decide to climb it allowing you to see most of the way to the exit")
                            escape_chance += 35
                            
                        escape_chance += 5
                        if escape_chance <= 99:
                            player_data['health'] -= 10
                            Print("\nYou lose 10 Health due to starvation")
                            check_death(player_data)


                elif random_event <= 0.50: # Bandit camp with 3 enemies
                    while True:
                        action = input("You come across a bandit outpost with a bunch of enemies! (VERY DIFFICULT) Do you wish to enter?\n\n[1] Enter\n[2] Walk around it and continue on\nEnter: ")
                        if action == '1':
                            global fight_bandit_outpost
                            fight_bandit_outpost = True
                            battle(player_data)
                            battle(player_data)
                            battle(player_data)
                            battle(player_data)
                            fight_bandit_outpost = False
                            
                            Print("\nYou make your way to their treasure...")
                            time.sleep(2)
                            treasure = random.random()
                            
                            if treasure <= 0.25:
                                Print("You open the chest and find a bunch of random items!\n\n-----Items-----\nYou found a health ring made by the Eagles!\n+20 Max Health\nYou found a bag of gold!\n+35 Gold\nYou found a Flame Sword!!!")
                                player_data['max_health'] += 20
                                player_data['gold'] += 35
                                if "Flame Sword" in player_data['owned_weapons']:
                                    Print("\nUnfortunately you already have a flame sword so it has been UPGRADED to a FROST SWORD!!!!!")
                                    player_data['owned_weapons'].append("Frost Sword")
                                else:
                                    player_data['owned_weapons'].append("Flame Sword")
                                    
                            elif treasure <= 0.50:
                                Print("The chest pops open and you see a glowing item sitting in the corner!\n\n-----Items-----\nYou found a Frost Orb!!!")
                                Print("\n[Knight] I thought those were from the Frozen Peaks... Who are these guys?")
                                Print(f"\n---Rewards---\nx1.50 Max Health\nx1.75 Health")
                                player_data['max_health'] = int(player_data['health'] * 1.5)
                                player_data['health'] = int(player_data['health'] * 1.75)

                            elif treasure <= 0.75:
                                PRint("You open the chest to find a bunch of junk...\n\n-----Items-----\nJunk\nJunk\nJunk\nYou found a health potion!\n+1 Health Potion\nJunk\nYou found a Forest Orb!\n+100 Gold\n+4 Defence\n-1 Strength")
                                Print("\n[Knight] Ooh a Forest Orb")
                                Print("The Forest Orb merges with your armour and sword")
                                player_data['gold'] += 100
                                player_data['strength'] -= 1
                                for armour in armour_data:
                                    if armour['name'] == player_data['armour_equipped']:
                                        armour['defence'] += 4
                                        player_data['defence'] += 4
                              
                            else:
                                Print(f"As you get closer to the treasure, your {player_data['weapon_equipped']} begins to glow\n\n-----Items-----\nEnchanted book!!!")
                                random_enchant(player_data, weapons_data)

                            break

                        elif action == '2':
                            Print("You walk around the bandit outpost and continue on")
                            break
                elif random_event <= 0.55: # Encounter caterpiller princess
                    Print("After wandering through the forest")

                    # Caterpillar Princess discovery dialogue options
                    discovery_dialogues = [
                        "You spot a perculiar shimmer on a giant leaf ahead.",
                        "A soft voice hums a melody, drawing your attention to a leaf.",
                        "A strange glow of leaves illuminate the forest floor, leading your gaze to a large leaf.",
                        "You hear tiny laughter and look up to find a Caterpillar with a crown on a leaf."
                    ]

                    # Caterpillar Princess greeting dialogue options
                    greetings = [
                        "[Caterpillar Princess] Greetings, brave Knight! I am the Caterpillar Princess.",
                        "[Caterpillar Princess] Hello, Knight. You have found me, the Caterpillar Princess!",
                        "[Caterpillar Princess] Ah, a Knight! I am the Caterpillar Princess. How delightful to meet you!",
                        "[Caterpillar Princess] Welcome, good Knight. I am the Caterpillar Princess, watcher of this forest."
                    ]

                    # Knight's response options
                    knight_responses = [
                        "[Knight] It is an honor to meet you, Princess. Your forest is truly enchanting.",
                        "[Knight] I did not expect to find royalty here. How may I serve you?",
                        "[Knight] Your Highness, I am but a humble knight seeking adventure.",
                        "[Knight] Caterpillar Princess, your reputation precedes you. I am at your service."
                    ]

                    # Second dialogue options
                    second_dialogues = [
                        "[Caterpillar Princess] I have been watching over this forest for ages. Few find me, but you have.",
                        "[Caterpillar Princess] It is rare to see such a Knight venture so deep into the woods.",
                        "[Caterpillar Princess] This leaf is my throne, and from here I observe all who pass through.",
                        "[Caterpillar Princess] Tell me, knight, do you seek wisdom, fortune, or simply adventure?"
                    ]
                    
                    # Rewards for the knight
                    rewards = [
                        {"item": "Armour Plates", "description": "Gives armour Defence."},
                        {"item": "Potion of Strength", "description": "A potion that will make you bigger and stronger"},
                        {"item": "Caterpillar Charm", "description": "A charm said to allow you to hit critical hits more often."},
                        {"item": "Forest Jewel", "description": "A gem that massively increases Max Health"}
                    ]
                    
                    # Randomly select discovery dialogue
                    Print(random.choice(discovery_dialogues))
                    time.sleep(3)
                    # Randomly select greeting
                    Print("\n" + random.choice(greetings))
                    time.sleep(3)
                    # Randomly select knight's response
                    Print("\n" + random.choice(knight_responses))
                    time.sleep(3)
                    # Randomly select second dialogue
                    Print("\n" + random.choice(second_dialogues))
                    time.sleep(3)
                    Print("[Caterpillar Princess] I know of your journey to fight the dragon, I also know that you arent currently strong enough to beat him yet, so take this:")
                    reward = random.choice(rewards)
                    Print(f"\nThe Caterpillar Princess hands you a {reward['item']}.")
                    Print(f"Description: {reward['description']}")
                    if reward['item'] == "Armour Plates":
                        Print("You use the armour plates\n+5 Defence")
                        for armour in armour_data:
                                if armour['name'] == player_data['armour_equipped']:
                                    armour['defence'] += 5
                                    player_data['defence'] += 5
                        
                    elif reward['item'] == "Potion of Strength":
                        Print("\n--You drink the potion--\n\n+15 Max Health\n+20 Health\n+3 Strength")
                        player_data['max_health'] += 15
                        player_data['health'] += 20
                        player_data['strength'] += 3
                    
                    elif reward['item'] == "Caterpillar Charm":
                        Print("\n--You wear the charm around your wrist--\n\n+20 Critical Hit Chance")
                        for weapon in weapons_data:
                                if weapon['name'] == player_data['weapon_equipped']:
                                    weapon['crit_chance'] += 20
                                    player_data['crit_chance'] += 20
                        
                    else:
                        Print("\n--You use the Jewel--\n\n+65 Max Health")
                        player_data['max_health'] += 65
                        
                    Print("\nYou thank the Caterpillar Princess and continue on your journey, feeling enpowered by the encounter.")
                    
                elif random_event <= 0.60:  # Encounter Bob // Bob Reward // Meet an Old Lady

                    if not seen_bob:  # First time meeting Bob
                        action = input("[Bob] Hello stranger, I am heading to the castle to steal from their vault. If you tell me the way to the castle, I will give you a cut.\n\n[1] Tell Him\n[2] Start Capping\nEnter: ")

                        seen_bob = True  # Marks Bob as encountered

                        if action == '1':  # Helping Bob
                            Print("\n[Knight] I don't exactly remember the way, but if you head to the clearing that way, you should be able to see the castle.")
                            Print("\n[Bob] Thanks man, I shall give you the rewards if I am to see you again.")
                            helped_bob = True

                        elif action == '2':  # Rejecting Bob
                            Print("\n[Knight] I have got no idea, I'm from the town in that direction.")
                            Print("\n[Bob] Okay, well, I shall continue on my adventure then.")
                            helped_bob = False

                    elif helped_bob:  # Bob returns with reward
                        Print("\n[Bob] Hey! I found you again! I made it into the vault, and I appreciate your help. Here, take this as thanks!\n+1000 Gold")
                        player_data["gold"] += 1000
                        helped_bob = False

                    else:  # Old lady event if Bob was ignored
                        Print("\n[Old Lady] Oh, hello there... Can you spare some time? My carriage is stuck in the mud...")
                        while True:
                            action = input("\n[1] Help her\n[2] Ignore her\nEnter: ")
                            if action == '1':
                                Print("You walk over to her and use your strength to lift it out\n-10 Max Health")
                                Print("\n[Old Lady] Thank you, kind soul! Here, take this potion for your troubles.\n+1 Health Potion")
                                player_data['max_health'] -= 10
                                player_data['health_potions'] += 1
                                use_health_potion(player_data)
                                break
                            elif action == '2':
                                Print("\n[Old Lady] May fortune still find you, even if kindness does not...")
                                break

                elif random_event <= 0.65:  # Bounty hunter event
                    if seen_bounty_hunter == False:
                        Print("[Bounty Hunter] Have you seen this little guy called Bob wandering around robbing places and 'giving you a cut' of what he steals?")

                        seen_bounty_hunter = True

                        action = input("\n[1] Yes, I know where he is\n[2] I have never seen him before\nEnter: ")

                        if action == '1':  # Telling on Bob
                            if helped_bob:
                                Print("\n[Knight] He is heading towards my castle to rob it!")
                                time.sleep(1.5)
                                Print("\n[Bounty Hunter] Well, I hate to tell you this, but he was asking where the castle was and it appears you have told him.")
                                time.sleep(3)
                                Print("-----Castle-----")
                                time.sleep(0.5)
                                Print("\n[Queen] Why, Knight, did you betray me like this?")
                                time.sleep(1)
                                Print("\n[Knight] I'm sorry, my queen.")
                                Print("\n[Queen] It's okay, Knight. I shall just require you to pay a small amount of the vault back...")

                                while True:
                                    action = input("\n[1] Pay\n[2] Go to the dungeons\nEnter: ")
                                    if action == '1':
                                        Print("\n[Queen] 2000 GOLD! Guards, empty his pockets.")
                                        if player_data['gold'] >= 2000:
                                            Print("\n-2000 Gold")
                                            player_data['gold'] -= 2000
                                            break
                                        else:
                                            Print("\n[Knight] But my Queen, I do not have 2000 gold.")
                                            Print("\n[Queen] Well then... it is... OFF TO THE DUNGEONS for you.")
                                            dungeons_reason = "queen"
                                            dungeons(player_data, dungeons_reason)
                                            break
                                    elif action == '2':
                                        Print("\n[Knight] I would rather go to the dungeons than pay you!")
                                        Print("\n[Queen] Then, your wish is granted")
                                        dungeons_reason = "queen"
                                        dungeons(player_data, dungeons_reason)
                                        break

                            elif seen_bob and not helped_bob:  # Told bounty hunters after rejecting Bob
                                Print("\n[Knight] Well, when I said I know where he is... I mean I sent him off in that direction.")
                                Print("\n[Bounty Hunter] Thanks! We will be on our way. Just so you know, he was never going to give back that gold. Here's a thanks :) \n+250 Gold")
                                player_data['gold'] += 250

                            else:  # Lying about seeing Bob
                                Print("\n[Knight] Haha, just kidding. I have no idea who or where this guy is.")

                        elif action == '2':  # Lying to protect Bob
                            if helped_bob:
                                Print("\n[Bounty Hunter] Haha, well you see, Bob... is this the guy who gave you directions?")
                                Print("\n[Bob] Never *winks*")
                                Print("\nHe gestures you with his head over to the trees... once the bounty hunters leave with bob you scurry over to the trees and find a chest filled with gold\n+1000 Gold!!!")
                                player_data['gold'] += 1000
                            else:
                                Print("\n[Bounty Hunter] Well, if you ever see him, let us know, and we will pay you highly.")
                    else:
                        Print("[Bounty Hunter] I assume you still haven't seen him...\n\n[Knight] No I have not")
                            
                elif random_event <= 0.70: # witch that sets player stats to original but doubles a random stat
                    Print("You stumble into a mysterious forest")
                    Print("\n[Unknown] Hello Knight,")
                    time.sleep(1)
                    Print("\n[Knight] Uhm, Hello mysterious voice...")
                    time.sleep(1)
                    Print("\n[Unknown] Do you wish to gain ultimate power?")
                    time.sleep(1)

                    while True:
                        action = input("\n[1] Yes\n[2] No\nEnter: ")

                        if action == '1':
                            Print("\n[Knight] Yes, I do")
                            starting_stat = None
                            changed_stat = None
                            random_stat = random.randint(1, 3)
                            
                            if random_stat == 1:  # Max Health
                                changed_stat = "Max Health"
                                starting_stat = player_data['max_health']
                            elif random_stat == 2:  # Health
                                changed_stat = "Health"
                                starting_stat = player_data['health']
                            elif random_stat == 3:  # Gold
                                changed_stat = "Gold"
                                starting_stat = player_data['gold']
                            
                            new_stat = starting_stat * 2

                            if changed_stat == "Max Health":
                                player_data['max_health'] = new_stat
                                player_data['health'] = 100
                                player_data['gold'] = 0
                            elif changed_stat == "Health":
                                player_data['max_health'] = new_stat
                                player_data['health'] = new_stat
                                player_data['gold'] = 0
                            elif changed_stat == "Gold":
                                player_data['max_health'] = 100
                                player_data['health'] = 100
                                player_data['gold'] = new_stat

                            player_data['weapon_equipped'] = "Bronze Sword"
                            player_data['owned_weapons'] = ["Bronze Sword"]
                            weapons()

                            Print(f"\n[Dark Witch] I have reset your Max Health, Health, Gold and taken all your Weapons but doubled your {changed_stat}.")
                            Print(f"[Dark Witch] Old: {changed_stat} {starting_stat}, New: {changed_stat} {new_stat}.")
                            
                            if not player_data['companion']:
                                Print("[Dark Witch] I have also summoned a companion for your adventures.")
                                player_data['companion'] += 1
                            break

                        elif action == '2':
                            Print("\n[Knight] No thanks,")
                            break

                        else:
                            Print("\n[Unknown] Invalid choice. The voice fades away.")
                        
                elif random_event <= 0.75: # Meet a friendly orc, rock or albert
                    friendly_enemy = [
                        "Orc",
                        "Rock",
                        "Albert"
                    ]

                    friendly_dialogue = {
                        "Orc": "\nThe Orc grunts, Hey there, heavily armoured human! You need help smashing something?",
                        "Rock": ["\nThe Rock just sits silently... but somehow you feel enriched by its presence."],
                        "Albert": "\nAlbert adjusts his hole filled shirt.\n\n[Albert] Sit down with me young man, let me tell you about my glory days"
                    }
                    
                    friendly_enemy = random.choice(friendly_enemy)
                    Print(f"[Knight] Hello there... {friendly_enemy}")
                    Print(friendly_dialogue[friendly_enemy])
                    if friendly_enemy == 'Orc':
                        Print("[Knight] I am on a quest to defeat the dragon, and I wish for you to join me")
                        player_data['companion'] += 1
                    else:
                        Print("\n+1 Strength")
                        player_data['strength'] += 1

                elif random_event <= 0.80:  # Makes exploration 2-3 events longer
                    print("You seem to have gotten lost, which way do you go to get back?")
                    extra_exploration = 0

                    while True:
                        correct_way = random.randint(1, 3)
                        action = input("\n[1] Left\n[2] Right\n[3] Straight\nEnter: ")
                        
                        if action == '1' and correct_way == 1:
                            Print(f"\nYou safely got back on track and continued on, encountering {extra_exploration} more events")
                            break
                        
                        elif action == '1' and (correct_way == 2 or correct_way == 3):
                            Print("\nYou go to the left but now the path looks even more unfamiliar")
                            exploration_time += 1
                            extra_exploration += 1

                        elif action == '2' and correct_way == 2:
                            Print(f"\nYou safely got back on track and continued on, encountering {extra_exploration} more events")
                            break
                        
                        elif action == '2' and (correct_way == 1 or correct_way == 3):
                            Print("\nYou go to the right but now the path looks even more unfamiliar")
                            exploration_time += 1
                            extra_exploration += 1

                        elif action == '3' and (correct_way == 1 or correct_way == 2):
                            Print("\nYou go Straight but now the path looks even more unfamiliar")
                            exploration_time += 1
                            extra_exploration += 1

                        elif action == '3' and correct_way == 3:
                            Print(f"\nYou safely got back on track and continued on, now having to encounter {extra_exploration} extra events")
                            break

                        else:
                            Print("Please enter a number between 1 and 3")
              
                elif random_event <= 0.85:

                    Print("Since you are running low on food you decide to go and hunt for some berries")
                    
                    berries_left = random.randint(6, 11)
                    
                    # List of available berries
                    berries = [
                        "Brown", 
                        "Green", 
                        "Blue", 
                        "Purple", 
                        "Red", 
                        "Orange", 
                        "Light Blue", 
                        "Yellow"
                    ]

                    # Infinite loop for berry hunting
                    while True:
                        # Randomly select a berry
                        berry = random.choice(berries)
                        
                        # Ask for the player's action
                        action = input(f"\nDo you want to eat the {berry} berry?\n\n[1] Yes\n[2] No\nEnter: ")
                        
                        if action == '1':
                            # Generate and apply a random effect
                            effect = random_berry_effect(player_data)
                            Print(f"You eat the {berry} berry! It {effect}")
                            berries_left -= 1
                            
                            action = input("\nDo you want to continue looking?\n\n[1] Yes\n[2] No\nEnter: ")
                            
                            if berries_left == 0:
                                Print("You couldnt find anymore berries to eat")
                                break
                            
                            if action == '1':
                                Print("You continue looking and find another berry!")
                                
                            elif action == '2':
                                Print("You decide you are full and stop looking")
                                break
                            
                        elif action == '2':
                            Print(f"You decide not to eat the {berry} berry and continue looking.")
                            berries_left -= 1
                        else:
                            Print("Invalid choice. Please choose [1] Yes or [2] No.")
                        
                elif random_event <= 0.90: # save slime king and lets you visit his kingdom anytime during your forest and frozen peak adventure
                    if player_data['slime_kingdom'] == True:
                        Print("You found nothing")
                    else:
                        Print("You hear a faint cry for help and decide to investigate\nA small slime soldier runs up to you and asks that you defend their kingdom.")
                        while True:
                            action = input("\n[1] Help (HARD)\n[2] Ignore\nEnter: ")
                            if action == '1':
                                Print("You follow the slime soldier to the kingdom and see a massive slime king being attacked by a group of bandits")
                                fight_campfire_bandit = True
                                battle(player_data)
                                battle(player_data)
                                battle(player_data)
                                fight_campfire_bandit = False
                                fight_bandit_leader = True
                                battle(player_data)
                                fight_bandit_leader = False
                                Print("After you slay the final bandit, the slime king thanks you and offers you a home in his kingdom anytime you wish")
                                player_data['slime_kingdom'] = True
                                break
                            elif action == '2':
                                Print("\n[Knight] Sorry little guys, I'm just not strong enough to save you right now.")
                                break
                            else:
                                Print("Please Enter a number between 1 and 2")

                elif random_event <= 0.95: # meet blacksmith to sharpen sword, and improve armour for gold
                    Print("You spot a blacksmith store and decide to enter")
                    upgraded_armour = False
                    forest_blacksmith(player_data, weapons_data, armour_data)

                else:
                    print("You found nothing")
                            
            # Player finds a shrine
            elif exploration <= 0.60:
                Print("\n-----Hidden Shrine-----")
                Print("You uncover a mysterious shrine!")
                
                while True:
                    action = input("\n[1] Investigate\n[2] Leave\nEnter: ")

                    if action == '1':
                        shrine_luck = random.random()  # What happens when the player touches the shrine

                        if shrine_luck <= 0.20:  # Positive Shrine Effect 20%
                            Print("\nYou feel a warm sensation cover your body +35 Health +5 Max Health")
                            player_data['max_health'] += 5
                            player_data['health'] += 35

                        elif shrine_luck <= 0.40:  # Negative Shrine Effect 20%
                            Print("\nYou feel a figure touch your shoulder...")
                            time.sleep(2)
                            Print("\nBefore you can catch a glimpse, it disappears into the trees, and you hope that nothing bad happened")
                            player_data['max_health'] -= 10

                        elif shrine_luck <= 0.55:  # Ancient Well 15%
                            Print("You stumble upon an old, moss-covered well.")
                            well_luck = random.random()
                            if well_luck <= 0.33:
                                Print("\nYou find a small pouch at the bottom\n+50 Gold")
                                player_data['gold'] += 50
                            elif well_luck <= 0.66:
                                Print("\nThe well seems to whisper to you, filling you with confidence and Strength\n+1 Strength")
                                player_data['strength'] += 1
                            else:
                                Print("\nYou slip and fall!\n-20 Health")
                                player_data['health'] -= 20

                        elif shrine_luck <= 0.75:  # Lost Merchant 20%
                            Print("A Merchant sits by the shrine with a broken cart, looking distressed.")
                            while True:
                                action = input("\n[1] Help him fix his cart\n[2] Rob him\n[3] Ignore\nEnter: ")

                                if action == '1':
                                    Print("\nYou lend a hand and repair the cart draining your energy. The Merchant thanks you.\n+50 Gold\n-10 Health")
                                    player_data['gold'] += 50
                                    player_data['health'] -= 10
                                    check_death(player_data)
                                    break

                                elif action == '2':
                                    Print("\nYou threaten the merchant and take his gold, but not without a fight.")
                                    fight_merchant = True
                                    battle(player_data)
                                    fight_merchant = False
                                    break
                                elif action == '3':
                                    Print("[Knight] I don't feel like dealing with that right now")
                                    break
                                else:
                                    Print("Please Enter a number between 1 and 3")
                        

                        elif shrine_luck <= 0.90:  # Sleeping Bear 15%
                            Print("You spot a massive bear sleeping on the path.")
                            action = input("\n[1] Sneak past\n[2] Attack\n[3] Turn back\nEnter: ")

                            if action == '1':
                                if random.random() <= 0.50:
                                    Print("\nYou successfully sneak past!")
                                else:
                                    Print("\nThe bear wakes up and swipes at you! -25 Health")
                                    player_data['health'] -= 25

                            elif action == '2':
                                Print("\nYou battle the bear fiercely, and as you slash through it's bones it somehow sharpens your sword\n+1 Damage\n-35 Health")
                                for weapon in weapons_data:
                                    if weapon['name'] == player_data['weapon_equipped']:
                                        weapon['damage'] += 1
                                player_data['health'] -= 35
                                check_death(player_data)

                        elif shrine_luck <= 0.95:  # Cursed Knight 5%
                            Print("\nA knight in black armor approaches, appearing to want to protect the shrine.")
                            fight_black_knight = True
                            battle(player_data)
                            fight_black_knight = False

                        else:  # Golden Deer 5%
                            Print("\nA golden deer appears in the clearing, its fur shimmering.")
                            time.sleep(2)
                            Print("You follow the deer mesmerised...")
                            time.sleep(1)
                            Print("\nIt slowly walks up to a chest and rubs it's nose against it")
                            time.sleep(1)
                            Print("You walk up to the chest to find it full of coins!\n+100 Gold")
                            player_data['gold'] += 100   
                        break
                    
                    elif action == '2':
                        Print("You leave the shrine alone")
                        break
                    else:
                        Print("Please Enter a valid number")
                        
            # Player walks into a trap
            elif exploration <= 0.70:
                Print("\nYou walked into a trap!")
                time.sleep(1)
                trap_luck = random.random()
                if trap_luck <= 0.25:
                    Print("You fall into a hole and took 10 Damage")
                    player_data['health'] -= 10
                    
                elif trap_luck <= 0.60:
                    Print("You got hit by a falling log and took 20 Damage")
                    player_data['health'] -= 20

                elif trap_luck <= 0.80:
                    Print("You step on a tree branch and roll your ankle taking 15 Damage")
                    player_data['health'] -= 15
                else:
                    Print("Haha just kidding there was no trap there but you did find an apple + 5 Health")
                    player_data['health'] += 5
                
                check_death(player_data)
                    
            # Player finds an enemy
            elif exploration <= 0.95:
                battle(player_data)
                
            # Player encounters the merchant
            else:
                forest_merchant(player_data)
            exploration_time -= 1
            
            if settings['enter_to_continue']:
                input("\nPress Enter to continue ")                   
        else:
            player_data['day'] += 1
            if player_data['day'] == 15:
                Print("\n[Knight] There is nothing left here... I think its time I continue onto the Frozen Peaks, MIGHTY DRAGON HERE I COME")
                Print("\nYou hike through the rest of the forest and just before you exit you are stopped by the HOWLER")
                fight_boss = True
                battle(player_data)
                fight_boss = False
                player_data['location'] = 'Frozen Peaks'
            break

# Forest Merchant Encounter
def forest_merchant(player_data):
    print("\n-------------------------------------------------------------------------")
    Print("\n[Merchant] Hello I am a merchant what would you like to buy?")
    while True:
        
        if player_data['weapon_equipped'] not in player_data['owned_weapons']:
            player_data['owned_weapons'].append(player_data['weapon_equipped'])
        if player_data['armour_equipped'] not in player_data['owned_armour']:
            player_data['owned_armour'].append(player_data['armour_equipped'])
                
        Print(f"\nYou have {player_data['gold']} Gold")
        print("\n-----Swords-----\n\n[1] Iron Sword --100 Gold--\n[2] Steel Sword --300 Gold--\n\n-----Bows-----\n\n[3] Hunting bow --225 Gold--\n\n-----Armour-----\n\n[4] Cloth Armour --300 Gold--\n[5] Iron Armour --550 Gold--")
        action = input("\n-----Potions/Crystals-----\n\n[6] Health Potion --100 Gold--\n[7] Health Crystal --350 Gold--\n\n-----Items-----\n\n[8] Enchant Book --750 Gold--\n\n[r] Exit\nEnter: ").lower()
        if action == '1':
            if player_data['gold'] >= 100:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    if "Iron Sword" in player_data['owned_weapons']:
                        Print("\n[Merchant] You don't need another Iron Sword I see one on your back")
                    else:
                        Print("\n[Knight] I would like an ☆ Iron Sword ☆ Please")
                        time.sleep(1)
                        Print("\n-100 Gold")
                        player_data['gold'] -= 100
                        player_data['weapon_equipped'] = "Iron Sword"
                        time.sleep(1)
                        Print("\n[Merchant] Here you go young one")
            else:           
                Print("[Merchant] Sorry but you can't afford this item")
            
        elif action == '2':
            if player_data['gold'] >= 300:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    if "Steel Sword" in player_data['owned_weapons']:
                        Print("\n[Merchant] You don't need another Steel Sword I see one on your back")
                    else:
                        Print("\n[Knight] Can I have a ☆ Steel Sword ☆ Please")
                        Print("\n-300 Gold")
                        player_data['gold'] -= 300
                        player_data['weapon_equipped'] = "Steel Sword"
                        time.sleep(0.5)
                        Print("\n[Merchant] I believe you can kill anything with this!")
            else:
                Print("[Merchant] Sorry but you can't afford this item")

        elif action == '3':
            if player_data['gold'] >= 225:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    if "Hunting Bow" in player_data['owned_weapons']:
                        Print("You already own this")
                    else:
                        Print("\n[Knight] Can I have a ☆ Hunting Bow ☆ Please")
                        Print("\n-225 Gold")
                        time.sleep(0.5)
                        Print("\n[Merchant] Thats a good choice! Hope it does you well")
                        player_data['gold'] -= 225
                        player_data['weappon_equipped'] = "Hunting Bow"
                        time.sleep(0.5)
                        Print("[Merchant] Good luck")
            else:
                Print("[Merchant] Sorry but you can't afford this item")
            
        elif action == '4':
            if player_data['gold'] >= 300:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    if "Cloth Armour" in player_data['owned_armour']:
                        Print("You already own this")
                    else:
                        for armour in armour_data:
                            if armour['name'] == player_data['armour_equipped']:
                                player_data['defence'] -= armour['defence']
                                Print("\n[Knight] Can I have some ☆ Cloth Armour ☆ ?")
                                Print("\n-300 Gold")
                                time.sleep(0.5)
                                Print("\n[Merchant] Thats not a bad idea, hope to see you back here soon for Iron Armour!")
                                player_data['defence'] += 4
                                player_data['gold'] -= 300
                                player_data['armour_equipped'] = "Cloth Armour"
                                time.sleep(0.5)
                                Print("[Merchant] Good luck. Knight. I wish you the best")
                                break
            else:            
                Print("[Merchant] Sorry but you can't afford this item")
            
        elif action == '5':
            if player_data['gold'] >= 550:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    if "Iron Armour" in player_data['owned_armour']:
                        Print("You already own this")
                    else:
                        for armour in armour_data:
                            if armour['name'] == player_data['armour_equipped']:
                                player_data['defence'] -= armour['defence']
                                Print("\n[Knight] Can I have some ☆ Iron Armour ☆ ?")
                                time.sleep(0.5)
                                Print("\nThe merchant gives a slow and approving nod")
                                time.sleep(1)
                                Print("\n-550 Gold")
                                player_data['defence'] += 10
                                player_data['gold'] -= 550
                                player_data['armour_equipped'] = "Iron Armour"
                                time.sleep(0.5)
                                Print("\n[Merchant] Good luck in the Frozen Peaks knight 😉")
                                break
                        
            else:            
                Print("[Merchant] Sorry but you can't afford this item")
            
        elif action == '6':
            if player_data['gold'] >= 100:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    Print("\n[Knight] One health potion Merchant!")
                    Print("\n-100 Gold")
                    Print("\n[Merchant] Here you go! Did you know that if you die but have a health potion in your inventory it will use the potion and keep you alive instead? All for 100 gold")
                    Print("\n[Merchant] Is there anything else I can get for you?")
                    player_data['gold'] -= 100
                    player_data['health_potions'] += 1
                    use_health_potion(player_data)
                    
            else:            
                Print("[Merchant] Sorry but you can't afford this item")  
                     
        elif action == '7':
            if player_data['gold'] >= 350:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    Print("\n[Knight] Can I have the Health Crystal Please?")
                    Print("\n-350 Gold")
                    Print("\n[Merchant] Sure thing, now you should be ready for anything!")
                    Print("\nYou stare into the crystal.\n+20 Max Health\n+30 Health")
                    player_data['gold'] -= 350
                    player_data['max_health'] += 20
                    player_data['health'] += 20   
            else:        
                Print("[Merchant] Sorry but you can't afford this item")
                
        elif action == '8':
            if player_data['gold'] >= 750:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    Print("\n[Knight] Can I an enchant book please?")
                    Print("\n[Merchant] Sure thing")
                    Print("\n-750 Gold")
                    random_enchant(player_data, weapons_data) 
                    player_data['gold'] -= 750
                    Print("\n[Merchant] I hope you enjoy your new enchantment")

        elif action == 'r':
            Print("\n[Merchant] I shall see you soon")
            print("\n-------------------------------------------------------------------------")
            if player_data['weapon_equipped'] not in player_data['owned_weapons']:
                player_data['owned_weapons'].append(player_data['weapon_equipped'])
            if player_data['armour_equipped'] not in player_data['owned_armour']:
                player_data['owned_armour'].append(player_data['armour_equipped'])
            break

        elif action == 'rps':
            start_rps()

        else:
            Print("Please Enter a valid option") 

# Blacksmith Shop
def forest_blacksmith(player_data, weapons_data, armour_data):
    
    global upgraded_armour

    Print("\n-----Blacksmith-----")
    Print("[Blacksmith] Hello Knight, what would ya like?")
    while True:
        Print(f"\nGold: {player_data['gold']}")
        action = input("\n[1] Shop\n[2] Sharpnen Sword\n[3] Upgrade Armour (free)\n[r] Leave\nEnter: ").lower()
        if action == '1':
            Print("\n[Knight] I would like to look at your shop please!")
            time.sleep(2)
            os.system('cls')
            Print("-----Blacksmith Shop-----")
            Print("\n[Blacksmith] Welcome to me shop")
            while True:
                
                if player_data['weapon_equipped'] not in player_data['owned_weapons']:
                    player_data['owned_weapons'].append(player_data['weapon_equipped'])
                if player_data['armour_equipped'] not in player_data['owned_armour']:
                    player_data['owned_armour'].append(player_data['armour_equipped'])
                
                Print("What can I get ya?")
                Print(f"\nYou have {player_data['gold']} Gold")
                action = input("\n-----Swords-----\n\n[1] Iron Sword --75 Gold--\n[2] Steel Sword --200 Gold--\n\n-----Armour-----\n\n[3] Iron Armour --475 Gold--\n[r] Leave\nEnter: ").lower()
                if action == '1':
                    if player_data['gold'] >= 75:
                        confirmation = input("Press Enter to confirm or ' r ' to Return ")
                        if confirmation == '':
                            if "Iron Sword" in player_data['owned_weapons']:
                                Print("\n[Blacksmith] You don't need another Iron Sword I see one on your back")
                            else:
                                Print("\n[Knight] I would like an ☆ Iron Sword ☆ Please")
                                time.sleep(1)
                                Print("\n-75 Gold")
                                player_data['gold'] -= 75
                                player_data['weapon_equipped'] = "Iron Sword"
                                time.sleep(1)
                                Print("\n[Blacksmith] I always got the best deals just for you")
                                    
                    else:
                        Print("[Blacksmith] Sorry man you can't afford this") 
                        
                elif action == '2':
                    if player_data['gold'] >= 200:
                        confirmation = input("Press Enter to confirm or ' r ' to Return ")
                        if confirmation == '':
                            if "Steel Sword" in player_data['owned_weapons']:
                                Print("\n[Blacksmith] You don't need another Steel Sword I see one on your back")
                            else:
                                Print("\n[Knight] Can I have a ☆ Steel Sword ☆ Please")
                                Print("\n-200 Gold")
                                player_data['gold'] -= 200
                                player_data['weapon_equipped'] = "Steel Sword"
                                time.sleep(0.5)
                                Print("\n[Blacksmith] I believe you can kill anything with this!")
                    else:
                        Print("[Blacksmith] Sorry man you can't afford this") 

                elif action == '3':
                    if player_data['gold'] >= 475:
                        confirmation = input("Press Enter to confirm or ' r ' to Return ")
                        if confirmation == '':
                            if "Iron Armour" in player_data['owned_armour']:
                                Print("You already own this")
                            else:
                                for armour in armour_data:
                                    if armour['name'] == player_data['armour_equipped']:
                                        player_data['defence'] -= armour['defence']
                                        Print("\n[Knight] Can I have some ☆ Iron Armour ☆ ?")
                                        time.sleep(0.5)
                                        Print("\nHe heads to the back of the shop and grabs out the Iron armour")
                                        time.sleep(1)
                                        Print("\n-475 Gold")
                                        player_data['defence'] += 10
                                        player_data['gold'] -= 475
                                        player_data['armour_equipped'] = "Iron Armour"
                                        time.sleep(0.5)
                                        Print("\n[Blacksmith] Here you go knight! Come back soon")
                                        break   
                    else:
                        Print("[Blacksmith] I'm truly sorry but you can't afford this")

                elif action == 'r':
                    Print("\n[Blacksmith] Come back soon for another armour upgrade!")
                    print("\n-------------------------------------------------------------------------")
                    if (player_data['weapon_equipped']) not in player_data['owned_weapons']:
                        player_data['owned_weapons'].append(player_data['weapon_equipped'])
                    if player_data['armour_equipped'] not in player_data['owned_armour']:
                        player_data['owned_armour'].append(player_data['armour_equipped'])
                    break
                else:
                    Print("Please Enter a valid option")
            
        elif action == '2':
            if player_data['weapon_equipped'] == "Bronze Sword" or "Iron Sword":
                input("\n250 Gold for 3 Extra Damage\nPress Enter to confirm: ")
                if player_data['gold'] >= 250:
                    Print("\n-250 Gold\n+3 Damage")
                    player_data['gold'] -= 250
                    for weapon in weapons_data:
                        if weapon['name'] == player_data['weapon_equipped']:
                            weapon['damage'] += 3
                else:
                    Print("\n[Blacksmith] That is unfortunately not enough to upgrade your sword")
                    
            elif player_data['weapon_equipped'] == "Flame Sword":
                input("\n400 Gold for 3 Extra Damage\nPress Enter to confirm: ")
                if player_data['gold'] >= 425:
                    Print("\n-425 Gold\n+3 Damage")
                    player_data['gold'] -= 425
                    for weapon in weapons_data:
                        if weapon['name'] == player_data['weapon_equipped']:
                            weapon['damage'] += 1
                else:
                    Print("\n[Blacksmith] That is unfortunately not enough to upgrade your sword")         
            else:
                Print("\n[Blacksmith] Sorry, I don't know how to upgrade that sword")
                
        elif action == '3':
            if upgraded_armour == False:
                if player_data['armour_equipped'] == "No Armour" or "Cloth Armour":
                    Print("\n[Blacksmith] How am I meant to upgrade your armour if you don't have any?")
                else:
                    Print("\n[Knight] Can you upgrade my armour?")
                    time.sleep(1)
                    Print("\n[Blacksmith] Hand it over and I'll be back to you in a minute")
                    time.sleep(2)
                    Print("\n[Knight] Sure")
                    time.sleep(2)
                    Print("\n*tink *tink")
                    time.sleep(0.6)
                    Print("*bink *bam")
                    Print("\n[Blacksmith] Here ya go\n+2 Armour Defence\n")
                    upgraded_armour = True
                    for armour in armour_data:
                        if armour['name'] == player_data['armour_equipped']:
                            armour['defence'] += 2
                            player_data['defence'] += 2    
            else:
                Print("\n[Blacksmith] Sorry, I cant upgrade it any further")
                
        elif action == 'r':
            Print("\n[Blacksmith] See you next time!")
            if player_data['weapon_equipped'] not in player_data['owned_weapons']:
                player_data['owned_weapons'].append(player_data['weapon_equipped'])
            if player_data['armour_equipped'] not in player_data['owned_armour']:
                player_data['owned_armour'].append(player_data['armour_equipped'])
            break
             
# -- Frozen Peaks -- #

# Frozen Peaks Enemies list
def enemy_data_frozen_peaks():
    # Easy   
    frost_orc = {"name": "Frost Orc", "health": 60, "strength": 28, "gold": 25}
    ice_wraith = {"name": "Ice Wraith", "health": 65, "strength": 32, "gold": 30}
    snow_hunter = {"name": "Snow Hunter", "health": 85, "strength": 37, "gold": 40}
    shade = {"name": "Shade", "health": 55, "strength": 35, "gold": 75}
    golem = {"name": "Golem", "health": 350, "strength": 30, "gold": 80}
    frost_wraith = {"name": "Frost Wraith", "health": 55, "strength": 38, "gold": 45}
    ice_elemental = {"name": "Ice Elemental", "health": 70, "strength": 30, "gold": 50}
    wolf_pack = {"name": "Wolf Pack", "health": 90, "strength": 35, "gold": 35}
    # Medium
    frozen_knight = {"name": "Frozen Knight", "health": 120, "strength": 30, "gold": 70}
    cursed_shade = {"name": "Cursed Shade", "health": 100, "strength": 50, "gold": 90}
    snow_titan = {"name": "Snow Titan", "health": 150, "strength": 32, "gold": 100}
    yeti = {"name": "Yeti", "health": 260, "strength": 35, "gold": 120}
    frost_yeti = {"name": "Frost Yeti", "health": 200, "strength": 40, "gold": 150}
    ice_ghost = {"name": "Ice Ghost", "health": 170, "strength": 45, "gold": 130}
    frost_giant = {"name": "Frost Giant", "health": 250, "strength": 45, "gold": 200}
    wendigo = {"name": "Wendigo", "health": 230, "strength": 60, "gold": 250}
    # Hard
    blizzard_golem = {"name": "Blizzard Golem", "health": 425, "strength": 35, "gold": 300}
    ancient_wraith = {"name": "Ancient Wraith", "health": 270, "strength": 50, "gold": 275}
    snow_serpant = {"name": "Snow Serpent", "health": 255, "strength": 55, "gold": 320}
    baby_bigfoot = {"name": "Baby Bigfoot", "health": 285, "strength": 70, "gold": 350}
    snow_beast = {"name": "Snow Beast", "health": 280, "strength": 65, "gold": 400}
    # Boss
    bigfoot = {"name": "Bigfoot", "health": 650, "strength": 90, "gold": 700}
    # Event Enemies
    elder_yeti = {"name": "Elder Yeti", "health": 350, "strength": 75, "gold": 500}
    caravan = {"name": "Unknown Enemy", "health": 115, "strength": 35, "gold": 100}
    
    global fight_boss
    if fight_boss == True:
        current_enemy = bigfoot
    elif fight_elder_yeti == True:
        current_enemy = elder_yeti
    elif fight_caravan == True:
        current_enemy = caravan
    else:
        enemy_type = random.random()
        if enemy_type <= 0.60: # Easy Enemies (60%)
            random_enemy = random.random()
            if random_enemy <= 0.10: # 10%
                current_enemy = ice_wraith
            elif random_enemy <= 0.20: # 10%
                current_enemy = frost_orc
            elif random_enemy <= 0.30: # 20% 
                current_enemy = snow_hunter
            elif random_enemy <= 0.50: # 20%
                current_enemy = shade
            elif random_enemy <= 0.55: # 5%
                current_enemy = golem
            elif random_enemy <= 0.70: # 15%
                current_enemy = frost_wraith
            elif random_enemy <= 0.80: # 10%
                current_enemy = ice_elemental
            else:
                current_enemy = wolf_pack

        elif enemy_type <= 0.90: # Medium Enemies (25%)
            random_enemy = random.random()
            if random_enemy <= 0.15: # 15%
                current_enemy = frozen_knight
            elif random_enemy <= 0.25: # 10%
                current_enemy = cursed_shade
            elif random_enemy <= 0.40: # 15%
                current_enemy = snow_titan
            elif random_enemy <= 0.50: # 10%
                current_enemy = yeti
            elif random_enemy <= 0.65: # 15%
                current_enemy = frost_yeti
            elif random_enemy <= 0.80: # 10%
                current_enemy = ice_ghost
            elif random_enemy <= 0.90: # 10%
                current_enemy = wendigo
            else:
                current_enemy = frost_giant # 10%
        else: # Hard Enemies (10%)
            random_enemy = random.random()
            if random_enemy <= 0.20: # 20%
                current_enemy = blizzard_golem
            elif random_enemy <= 0.60: # 30%
                current_enemy = ancient_wraith
            elif random_enemy <= 0.80: # 20%
                current_enemy = snow_serpant
            elif random_enemy <= 0.95: # 15%
                current_enemy = snow_beast
            else: # 5%
                current_enemy = baby_bigfoot

    return current_enemy

# Player explores frozen peaks
def explore_frozen_peaks(player_data):
    global colours_left, fight_elder_yeti, storm_power, fight_boss, healed_today, fight_caravan, picked_events_left, seen_hermit, upgraded_armour, viewed_map
    exploration_time = random.randint(4, 7) # How many events the player will encounter

    while True:
        if exploration_time > 0:
            if settings['debugging'] == False:
                exploration = random.random()
            
            elif picked_events_left > 0:
                try:
                    action = input("\n---Encounter Menu---\n[1] Exploration\n[2] Memory Game\n[3] Enemy Encounter\n[4] Merchant\nEnter: ")
                    if action == '1':
                        exploration = 0.45
                    elif action == '2':
                        exploration = 0.55
                    elif action == '3':
                        exploration = 0.95
                    elif action == '4':
                        exploration = 1

                    picked_events_left -= 1

                except ValueError:
                    exploration = random.random()
                
            else: # if player enables debug they can change the event
                try:
                    exploration = float(input("0 Exploration, 0.55 Memory, 0.65 Trap, 0.93 Enemy, 1 Merchant\nExploration value: "))
                except ValueError:
                    exploration = random.random()
                    
            # Main Exploration
            if exploration <= 0.45:
                Print("\n-----Snow Exploration-----")
                
                if settings['debugging'] == False:
                    random_event = random.random()
                
                elif picked_events_left > 0:
                    try:
                        print("\n---Exploration Menu---\n[1] Find Elder Yeti\n[2] Caveman 21 Game\n[3] Tombstone Dungeon\n[4] Storm Power Increase\n[5] Abandond Wooden Shack\n[6] Snow Safe Circle\n[7] Caravan Escort\n[8] Defence and Strength Swap")
                        print("[9] Aurora In The Sky\n[10] Find a Companion\n[11] Endless Storm\n[12] Ice Cave\n[13] Blacksmith\n[14] Merchant")
                        action = input("Enter: ")
                        if action == '1':
                            random_event = 0.05
                        elif action == '2':
                            random_event = 0.10
                        elif action == '3':
                            random_event = 0.15
                        elif action == '4':
                            random_event = 0.30
                        elif action == '5':
                            random_event = 0.40
                        elif action == '6':
                            random_event = 0.45
                        elif action == '7':
                            random_event = 0.50
                        elif action == '8':
                            random_event = 0.55
                        elif action == '9':
                            random_event = 0.60
                        elif action == '10':
                            random_event = 0.65
                        elif action == '11':
                            random_event = 0.75
                        elif action == '12':
                            random_event = 0.80
                        elif action == '13':
                            random_event = 0.90
                        elif action == '14':
                            random_event = 0.99
                        else:
                            Print("Please Enter a number between 1 and 16")
                    except ValueError:
                        random_event = 0.60

                else:
                    try:
                        random_event = float(input("Enter: "))
                    except ValueError:
                        random_event = random.random()

                if random_event <= 0.05:
                    while True:
                        action = input("As you turn the corner of the ice spike you see a Elder Yeti... Do you wish to challenge it?\n\n[1] Yes\n[2] No\nEnter: ")
                        if action == '1':
                            fight_elder_yeti = True
                            battle(player_data)
                            fight_elder_yeti = False
                            Print("\nYou have defeated the Elder Yeti!!\n+10 Damage\nRandom Enchantment")
                            for weapon in weapons_data:
                                if weapon['name'] == player_data['weapon_equipped']:
                                    weapon['damage'] += 10
                            random_enchant(player_data, weapons_data)
                            break
                        elif action == '2':
                            Print("You quickly and quietly turn back around the ice spike and head the other way")
                            break
                        else:
                            Print("Please enter a number between 1 and 2")

                elif random_event <= 0.10:
                    Print("You find a small cave and decide to enter... When suddenly you hear a voice.")
                    time.sleep(1)
                    gold_bet = int(player_data['gold'] / 2)
                    while True:
                        action = input(f"\n[Middle Aged Man] Hello, Knight... Want to play a game of 21 worth {gold_bet} Gold?\n[1] Yes\n[2] No\nEnter: ")
                        if action == '1':
                            Print("\n[Knight] Sure, I could use some extra Gold")
                            action = input("[Middle Aged Man] Do you wish to know the rules?\n\n[1] Yes\n[2] No\nEnter: ")
                            if action == '1':
                                Print("[Middle Aged Man] The rules aren't as simple as you have to get as close to 21 as possible without going over") 
                                Print("[Middle Aged Man] There are trump cards, which are cards that can allow you to change the target goal to another number such as 24")
                                Print("[Middle Aged Man] Now however I could then use a 17 trump card which would put the goal at 17 and you would be over")
                                Print("[Middle Aged Man] We both draw a hidden card at the start of the round that only we know, making it harder to know the opponents score")
                                Print("[Middle Aged Man] If one of us goes over the target score and the other is under, the person under automatically wins and if we're both over the score it's whoever is closer")
                                Print("[Middle Aged Man] There is only 13 cards in the deck ranging from 1-13 with no duplicates, so if you have a 3 that means I cant have a 3")
                                Print("[Middle Aged Man] Now, are you ready to play?")
                                input("Press Enter to continue: ")
                                enemy_name = "Middle Aged Man"
                                difficulty = "Medium"
                                play_21(player_data, gold_bet, enemy_name, difficulty)

                            elif action == '2':
                                enemy_name = "Middle Aged Man"
                                difficulty = "Medium"
                                play_21(player_data, gold_bet, enemy_name, difficulty)

                            else:
                                Print("Please Enter a number between 1 and 2")

                            gold_bet += 1
                            if player_data['gold'] > gold_bet:
                                Print("[Middle Aged Man] Congratulations Knight... You win!")
                                Print(f"You win {gold_bet} Gold!!")
                                player_data['gold'] = int(player_data['gold'] * 1.5)
                            else:
                                Print("[Middle Aged Man] Aww, how about we play again sometime?")
                                player_data['gold'] = int(player_data['health'] * 0.5)
                                Print(f"You lost {gold_bet} Gold :(")

                            break
                        elif action == '2':
                            Print(f"[Knight] Nah, I'd rather keep my {gold_bet} Gold")
                            break
                        else:
                            Print("Please Enter a number between 1 and 2")

                elif random_event <= 0.15:
                    Print("You come across a tall metal cross above a tombstone and decide to enter")
                    time.sleep(1)
                    Print("\nYou come across an enemy!!")
                    battle(player_data)
                    Print("\nYou make it to the treasure!!")
                    Print("---Treasure---\n1x Health Potion\n+30 Max Health\n+45 Health\nSword Sharpener!\n+4 Damage")
                    player_data['max_health'] += 30
                    player_data['health'] += 45
                    player_data['health_potions'] += 1
                    for weapon in weapons_data:
                        if weapon['name'] == player_data['weapon_equipped']:
                            weapon['damage'] += 4
        
                
                elif random_event <= 0.20:
                    geniewish(player_data, weapons_data, armour_data)

                elif random_event <= 0.30:
                    if storm_power <= 0:
                        Print("A small snow storm starts to form weakening you a bit.\n-10 Health")
                        player_data['health'] -= 10
                    elif storm_power == 1:
                        Print("The storm starts to get stronger and you feel the cold wind biting at your skin and freezing your sword\n-20 Health\n-1 Damage")
                        player_data['health'] -= 20
                        for weapon in weapons_data:
                            if weapon['name'] == player_data['weapon_equipped']:
                                weapon['damage'] -= 1

                    elif storm_power == 2:
                        Print("The storm is getting stronger and you feel your body freezing up\n-30 Health\n-1 Damage\n-1 Defence")
                        player_data['health'] -= 30
                        for weapon in weapons_data:
                            if weapon['name'] == player_data['weapon_equipped']:
                                weapon['damage'] -= 1
                        for armour in armour_data:
                            if armour['name'] == player_data['armour_equipped']:
                                player_data['defence'] -= armour['defence']
                                armour['defence'] -= 1
                                player_data['defence'] -= 1

                    elif storm_power == 3:
                        Print("The storm's power increases\n-20 Health\n-10 Max Health\n-1 Damage")
                        player_data['health'] -= 20
                        player_data['max_health'] -= 10
                        for weapon in weapons_data:
                            if weapon['name'] == player_data['weapon_equipped']:
                                weapon['damage'] -= 1

                    elif storm_power == 4:
                        Print("You start feeling the cold through your armour and clothes onto your chest\n-10 Health\n-20 Max Health\n-2 Defence")
                        player_data['health'] -= 10
                        player_data['max_health'] -= 20
                        for armour in armour_data:
                            if armour['name'] == player_data['armour_equipped']:
                                player_data['defence'] -= armour['defence']
                                armour['defence'] -= 2
                                player_data['defence'] -= 2

                    elif storm_power == 5:
                        Print("The storm is getting more powerful and you feel your body freezing up\n-35 Health\n-2 Damage\n-2 Defence")
                        player_data['health'] -= 35
                        for weapon in weapons_data:
                            if weapon['name'] == player_data['weapon_equipped']:
                                weapon['damage'] -= 2
                        for armour in armour_data:
                            if armour['name'] == player_data['armour_equipped']:
                                player_data['defence'] -= armour['defence']
                                armour['defence'] -= 2
                                player_data['defence'] -= 2

                    elif storm_power == 6:
                        Print("The storm is getting too strong and you feel your body freezing up\n-40 Health\n-2 Damage\n-3 Defence")
                        player_data['health'] -= 40
                        for weapon in weapons_data:
                            if weapon['name'] == player_data['weapon_equipped']:
                                weapon['damage'] -= 2
                        for armour in armour_data:
                            if armour['name'] == player_data['armour_equipped']:
                                player_data['defence'] -= armour['defence']
                                armour['defence'] -= 3
                                player_data['defence'] -= 3

                    elif storm_power == 7:
                        Print("The storm is getting really strong almost making it impossible to see\n-30 Max Health\n-2 Strength")
                        player_data['max_health'] -= 30
                        player_data['strength'] -= 2

                    elif storm_power == 8:
                        Print("The storm gets too strong forcing you to take shelter by hiding in a divot on the otherside of a tree stump to the wind\n-25 Max Health\n-3 Strength\n-5 Defence")
                        player_data['max_health'] -= 25
                        player_data['strength'] -= 3
                        for armour in armour_data:
                            if armour['name'] == player_data['armour_equipped']:
                                player_data['defence'] -= armour['defence']
                                armour['defence'] -= 5
                                player_data['defence'] -= 5
                                
                        check_death(player_data)
                        time.sleep(1)
                        Print("After the storm weakens you force yourself through the storm encountering Bigfoot and are forced to fight him to live.")
                        Print("However, you can quickly access your inventory before he reaches you")
                        inventory_display(player_data, weapons_data, armour_data)
                        fight_boss = True
                        battle(player_data)
                        fight_boss = False
                        player_data['location'] = 'Swamplands'
                        healed_today = False
                        break

                    check_death(player_data)
                    storm_power += 1
                    
                elif random_event <= 0.40:
                    while True:
                        Print("You come across a small wooden shack with the lights on\n[1] Enter\n[2] Leave")
                        action = input("Enter: ")
                        if action == '1':
                            person_inside = random.randint(1, 3)
                            if person_inside == 1:
                                while True:
                                    Print("You walk up to the door and knock and the door blows open revealing a cozy place that seems abandoned\n[1] Rest\n[2] Loot\n[3] Pray to the shrine")
                                    action = input("Enter: ")
                                    if action == '1':
                                        Print("You decide to rest for a bit and regain your health\n+75 Health")
                                        player_data['health'] += 75
                                        if player_data['health'] > player_data['max_health']:
                                            player_data['health'] = player_data['max_health']
                                        break
                                    elif action == '2': 
                                        Print("You decide to loot the shack and find a small bag of gold\n+50 Gold")
                                        player_data['gold'] += 50
                                        break
                                    elif action == '3':
                                        if storm_power == 2 or 3:
                                            Print("You kneel down and pray to the shrine and it glows a bright blue and you feel a surge of power\n+1 Strength")
                                            player_data['strength'] += 1
                                            storm_power = 0
                                            
                                        elif storm_power >= 4 or 5:
                                            Print("You kneel down and pray to the shrine and it glows a bright blue and you feel a surge of power\n+2 Strength")
                                            player_data['strength'] += 2
                                            storm_power = 0
                                        
                                        elif storm_power >= 6 or 7:
                                            Print("You kneel down and pray to the shrine and it glows a bright blue and you feel a surge of power\n+3 Strength")
                                            player_data['strength'] += 3
                                            storm_power = 0
                                        
                                        else:
                                            Print("You kneel down and pray to the shrine but nothing happens")
                                        break
                                    else:
                                        Print("Please Enter a number between 1 and 3")

                            elif person_inside == 2:
                                Print("A small creature greets you at the door and invites you in for a meal\n+35 Health")
                                player_data['health'] += 35
                                storm_power -= 1
                                break
                            else:
                                Print("A small creature greets you at the door and invites you in for a meal\nHowever as they shut the door behind you they start swinging their knife!\n-25 Health")
                                player_data['health'] -= 25
                                break

                        elif action == '2':
                            Print("You decide to leave the shack and head back into the snow")
                            break
                        else:
                            Print("Please Enter a number between 1 and 2")

                elif random_event <= 0.45:
                    Print("As you stumble through the snow you across a circle in the middle of the snow where the storm stops and the sun shines allowing you to regain your strength and defrost your items!")
                    Print("+15 Max Health\n+35 Health\n+2 Damage\n+1 Armour Defence")
                    player_data['max_health'] += 15
                    player_data['health'] += 35
                    if player_data['health'] > player_data['max_health']:
                        player_data['health'] = player_data['max_health']
                    for weapon in weapons_data:
                        if weapon['name'] == player_data['weapon_equipped']:
                            weapon['damage'] += 2
                    for armour in armour_data:
                        if armour['name'] == player_data['armour_equipped']:
                            player_data['defence'] += 1
                            armour['defence'] += 1

                elif random_event <= 0.50:
                    while True:
                        Print("You come across a caravan with a bunch of people on the back\n[1] Fight\n[2] Ask for a ride\n[3] Leave them alone")
                        action = input("Enter: ")
                        if action == '1':
                            fight_caravan = True
                            battle(player_data)
                            battle(player_data)
                            fight_caravan = False
                            Print("You successfully defeat the caravan and take their items\n---Items---\n+50 Gold\n--Armour plating--\n+3 Armour Defence\nEnchanted Book!!")
                            player_data['gold'] += 50
                            for armour in armour_data:
                                if armour['name'] == player_data['armour_equipped']:
                                    player_data['defence'] += 3
                                    armour['defence'] += 3
                            random_enchant(player_data, weapons_data)
                            break
                        elif action == '2':
                            Print("You ask the caravan for a ride and they agree but only if you pay them 100 Gold!")
                            if player_data['gold'] >= 100:
                                player_data['gold'] -= 100
                                Print("-100 Gold\n\nWhile in the caravan the feeling of cold seems to disapear and you feel a bit warmer\n+50 Health")
                                storm_power -= 1
                                player_data['health'] += 50
                                if player_data['health'] > player_data['max_health']:
                                    player_data['health'] = player_data['max_health']
                                break
                            else:
                                Print("You don't have enough Gold")
                                
                        elif action == '3':
                            Print("You decide not to risk it and continue on in the freezing cold as they ride away")
                            break
                        else:
                            Print("Please Enter a number between 1 and 3")
            
                elif random_event <= 0.55:
                    while True:
                        Print("[Unknown] I have a proposition for you knight, I shall swap your defence with your strength and give you 100 Gold but increase the power of the storm.\n[1] Yes\n[2] No")
                        action = input("Enter: ")
                        if action == '1':
                            Print("\n[Unknown] Good choice")
                            time.sleep(0.5)
                            Print("\n+100 Gold")
                            player_data['gold'] += 100
                            for armour in armour_data:
                                if armour['name'] == player_data['armour_equipped']:
                                    temp_defence = (player_data['defence'] - armour['defence'])
                            player_data['defence'] = player_data['strength']
                            player_data['strength'] = temp_defence
                            storm_power += 1
                            break
                        elif action == '2':
                            Print("[Knight] How about no")
                            break
                        else:
                            Print("Please Enter 1 or 2")
                            
                elif random_event <= 0.60:
                    Print("As you sit down for a second you look up to the sky and see a beautiful aurora with moon shining down on you, allowing to feel truly calm for the next hour\n+25 Max Health\n+60 Health\n+1 Strength")
                    time.sleep(2)
                    player_data['max_health'] += 25
                    player_data['health'] += 60
                    player_data['strength'] += 1

                elif random_event <= 0.65:
                    Print("You find a small cave and decide to enter... When suddenly you hear a voice.\nIt's a girl who begs for food...\nYou start up a fire share some of your food helping her get to full strength\n+1 Companion")
                    player_data['companion'] += 1

                elif random_event <= 0.70:
                    Print("You come across a wizard type guy who offers to allow you to choose the events you encounter next for the remainder of the day\n[1] Yes\n[2] No")
                    while True:
                        action = input("Enter: ")
                        if action == '1':
                            Print("\n[Knight] Sure, I'd like to accept that offer... is there any catch?")
                            Print("\n[Wizard] No, knight, there is no catch, I just want to help you slay the dragon")
                            Print("\n[Knight] Alright then, what do I do?")
                            Print("\n[Wizard] You will know")
                            picked_events_left = exploration_time
                            break
                        elif action == '2':
                            Print("[Knight] Whatever you're selling, I aint buying yo")
                            break
                        else:
                            Print("Please Enter a number between 1 and 2")

                elif random_event <= 0.75:

                    escape_chance = 0  # Initial escape chance

                    Print("The storm grows stronger making it almost inpossible to see... Can you survive long enough to make it out?")
                    while True:
                        # Escape once escape chance hits 100
                        Print(f"\n---You are currently {escape_chance}% of the way through the storm---\n")
                        if escape_chance >= 100:
                            Print("\nYou survived long enough for the storm to calm down! Congratulations!\n+3 Strength")
                            storm_power = 0
                            player_data['strength'] += 3
                            break

                        # Random event
                        road_luck = random.random()
                        
                        if road_luck <= 0.15:  # Go left or right
                            Print("You accidentally took your eyes off the path and got lost")

                            while True:
                                action = input("Which way do you go to find the path again?\n\n[1] Left\n[2] Right\n[3] Straight\nEnter: ")
                                
                                if action == '1':   
                                    Print("You step on a weird ball that's really squishy.\n[Knight] Ew")
                                    escape_chance += 5
                                    break

                                elif action == '2':
                                    if viewed_map:
                                        Print("After following the directions on the map you find the path again")
                                        escape_chance = 100  
                                    Print("You encounter a small fur guy who offers some snow goggles and some food\n+25 Health")
                                    player_data['health'] += 25
                                    escape_chance += 15
                                    break

                                elif action == '3':
                                    random_event = random.random()
                                    
                                    if random_event <= 0.10:
                                        Print("You fall into a hole with a clock which takes you back to Day 1 with all your stats and past decisions with extra defence and strength\nDay = 1\n+5 Strength\n+5 Defence")
                                        time.sleep(2)
                                        player_data['day'] = 1
                                        exploration_time = 0
                                        player_data['defence'] += 5
                                        player_data['strength'] += 5
                                        player_data['location'] = 'Forest'
                                        break
                                    
                                    else:
                                        Print("You find nothing")
                                    break
                                else:
                                    Print("Please Enter a number between 1 and 3")

                        elif road_luck <= 0.25:  # Abandoned Camp
                            Print("You walk into an abandoned hut")
                            while True:
                                action = input("What do you do?\n\n[1] Search the camp\n[2] Move on\nEnter: ")
                                if action == '1':
                                    Print("You find some food in a pot")
                                    print("+25 Health")
                                    player_data['health'] += 25
                                    break
                                elif action == '2':
                                    Print("You leave")
                                    escape_chance += 15
                                    break

                        elif road_luck <= 0.35:  # Hermit Event
                            Print("You come across a Hermit sitting next to a tree.")
                            while True:
                                action = input("What do you do?\n\n[1] Talk to him\n[2] Ignore him\nEnter: ")
                                if action == '1':
                                    if seen_hermit == False:
                                        PRint("\n[Hermit] Another wanderer, lost in the endless road. Sit. Listen.")
                                        time.sleep(2)
                                        PRint("\n[Knight] But... I have to get out.")
                                        time.sleep(1)
                                        PRint("\n[Hermit] Sit, I shall only be a minute")
                                        time.sleep(2)
                                        PRint("\n[Hermit] The storm... it consumes even the best of us")
                                        PRint("\n[Knight] Yes, and its about to consume us if we don't get out of here")
                                        time.sleep(1)
                                        PRint("\n[Hermit] That's what I thought... No patience, knight. No wisdom. Just a blade and an angry heart.")
                                        time.sleep(3)
                                        PRint("[Hermit] How do you think I've survived here so long?")
                                        time.sleep(3)
                                        PRint("\n[Knight] I don't know, probably a camp or something")
                                        PRint("\n[Hermit] Hah, you knight... are blind to see it")
                                        PRint("\n[Knight] What does that even mean? I can't even see anywhere in the storm")
                                        PRint("\n[Hermit] The storm represents your anger, your rage. It clouds your vision, and it will consume you if you let it.")
                                        time.sleep(8)
                                        PRint("\nA gust of wind runs through your armour. You shiver...\n")
                                        time.sleep(3)
                                        PRint("[Knight] So what do I do?")
                                        PRint("\n[Hermit] Think of the storm as a person trying to soothe you after a fight. It wants to help you, but you must let it in.")
                                        time.sleep(2)
                                        PRint("\nThe Hermit grabs your shoulder\n")
                                        time.sleep(2)
                                        PRint("[Hermit] Think of the storm as a friend not an enemy")
                                        seen_hermit = True
                                        
                                    Print("+1 Strength\n+10 Max Health\n+20 Health")
                                    player_data['strength'] += 1
                                    player_data['max_health'] += 10
                                    player_data['health'] += 20
                                    escape_chance = 95
                                    break

                                elif action == '2':
                                    Print("The hermit slowly shakes his head as you walk back into the storm.")
                                    escape_chance += 10
                                    break

                                else:
                                    Print("Please Enter a number 1 or 2")

                        elif road_luck <= 0.45: # Storm
                            Print("A sudden storm rages around you, making it hard to see.")
                            while True:
                                action = input("What do you do?\n\n[1] Wait for the storm to calm down\n[2] Push on\nEnter: ")
                                if action == '1':
                                    Print("The storm passes...")
                                    escape_chance -= 5
                                    break
                                elif action == '2':
                                    Print("You brave the storm but emerge exhausted and injured.\n-10 Max Health\n-10 Health")
                                    player_data['max_health'] -= 10
                                    player_data['health'] -= 10
                                    escape_chance += 10
                                    check_death(player_data)
                                    break
                                else:
                                    Print("Please Enter a number between 1 and 2")
                                
                                
                        elif road_luck <= 0.60:  # River Event
                            Print("You hear a distant sound of rushing water.")
                            while True:
                                action = input("What do you do?\n\n[1] Investigate\n[2] Stay on the path\nEnter: ")
                                if action == '1':
                                    Print("You discover a river that seems to block your path.")
                                    river_event = random.randint(1, 4)
                                    if river_event == 1:
                                        Print("You find a bridge and cross safely.")
                                        escape_chance += 10
                                    elif river_event == 2 or 3:
                                        Print("You swim across, but the current is strong.\n-20 Health")
                                        player_data['health'] -= 20
                                        escape_chance += 10
                                    elif river_event == 4:
                                        Print("You slip and fall in! It takes time to get out so you continue on the path now cold.\n-15 Health")
                                        player_data['health'] -= 15
                                        escape_chance -= 10
                                    break
                                elif action == '2':
                                    Print("You stay on the path, avoiding danger.")
                                    escape_chance += 10
                                    break
                                else:
                                    Print("Please Enter a number between 1 and 2")
                                check_death(player_data)

                        elif road_luck >= 0.90:  # Lost Villager Event
                            Print("A strange shadow follows you silently.")
                            while True:
                                action = input("What do you do?\n\n[1] Confront it\n[2] Ignore it\nEnter: ")
                                if action == '1':
                                    villager_event = random.randint(1, 3)
                                    if villager_event <= 1:
                                        Print("The shadow reveals itself to be a lost villager who is grateful for your help.")
                                        Print("They hand you a bag of gold.\n+65 Gold")
                                        player_data['gold'] += 65
                                    elif villager_event == 2:
                                        Print("The person begs for food. You give them a piece of food you found, and they give you a map in return.")
                                        viewed_map = True
                                    elif villager_event == 3:
                                        Print("As you step closer, the shadow lunges at you! It's a Snow Bear!\n-30 Health")
                                        player_data['health'] -= 30
                                    check_death(player_data)
                                    break
                                elif action == '2':
                                    Print("The shadow fades into the snow")
                                    break
                                else:
                                    Print("Please Enter a number between 1 and 2")
                        else:
                            Print("The storm weakens a bit allowing you to see for a couple seconds")
                            escape_chance += 35
                            
                        escape_chance += 5

                elif random_event <= 0.80:
                    Print("As you are walking over some ice it suddenly cracks under you and you fall down an ice crevasse!\n-20 Health")
                    player_data['health'] -= 16
                    check_death(player_data)
                    time.sleep(1)
                    Print("\nAs you get up dazed you look around you to find a bunch of crystals, you walk up to one and touch it!\n+4 Health")
                    berries_left = random.randint(3, 7)
                    
                    # List of available berries
                    berries = [ 
                        "Red", 
                        "Black", 
                        "Lime", 
                        "Violet", 
                        "Baby Blue", 
                        "Dark Blue", 
                        "Yellow"
                    ]

                    # Infinite loop for berry hunting
                    while True:   
                        
                        # Randomly select a berry
                        berry = random.choice(berries)
                        
                        # Ask for the player's action
                        action = input(f"\nDo you to touch the {berry} crystal?\n\n[1] Yes\n[2] No\nEnter: ")
                        
                        if action == '1':
                            # Generate and apply a random effect
                            effect = random_berry_effect(player_data)
                            Print(f"You walk up to the {berry} crystal... It {effect}")
                            berries_left -= 1
                            
                            action = input("\nDo you want to continue looking?\n\n[1] Yes\n[2] No\nEnter: ")
                            
                            if berries_left == 0:
                                Print("You couldn't find anymore crystals")
                                break
                                
                            if action == '1':
                                Print("You continue looking and find another crystal")
                                
                            elif action == '2':
                                Print("You decide you are not addicted and start climbing out")
                                break
                            
                        elif action == '2':
                            Print(f"You decide not to  touch the {berry} crystal and continue looking")
                            berries_left -= 1
                        else:
                            Print("Invalid choice. Please choose [1] Yes or [2] No")

                elif random_event <= 0.85: # Quest up mountain for enchanted frost orb
                    Print("You found nothing!!!")
                    
                elif random_event <= 0.90:
                    upgraded_armour = False
                    frozen_peaks_blacksmith(player_data, armour_data, weapons_data)

                elif random_event <= 0.99:
                    frozen_peaks_merchant(player_data)
                else:
                    Print("You found nothing!!") # epic quest

            # Player gets the memory game
            elif exploration <= 0.55:
                os.system('cls')

                if colours_left == 6:
                    pattern = []
                    possible_colours = ["Red", "Blue", "Yellow", "Green"]

                if colours_left > 0:
                    pattern.append(random.choice(possible_colours))
                    Print("[Unknown] Hello, Knight...")
                    time.sleep(1)
                    Print("[Unknown] I need you to remember this pattern, it is imperative to your survival.")
                    print(pattern)  # Display the pattern
                    time.sleep(5)  # Give the player time to memorize it
                    colours_left -= 1
                    os.system('cls')
                else:
                    # After the pattern has been shown, ask the player to repeat it
                    Print("[Unknown] Now, repeat the pattern I showed you.")
                    player_input = input("Enter the pattern in the correct order (separate by spaces, e.g., 'Red Blue Yellow'): ").strip().split()

                    # Check if the player's input matches the pattern
                    if player_input == pattern:
                        # Player succeeded
                        Print("[Unknown] Well done, Knight... You've remembered the pattern!")
                        time.sleep(1)
                        Print("[Unknown] You've proven your memory and courage. As a reward, you gain strength for the trials ahead.")
                        time.sleep(2)

                        Print(f"[Unknown] You're reward is:\n+5 Strength\n+5 Defence\n+75 Max Health\n+150 Health\n+200 Gold")
                        player_data['strength'] += 5
                        player_data['defence'] += 5
                        player_data['max_health'] += 75
                        player_data['health'] += 150
                        player_data['gold'] += 200

                    else:
                        # Player failed, apply punishment
                        Print("[Unknown] You have failed to remember the pattern...")
                        time.sleep(1)
                        Print(f"[Unknown] As punishment, you shall lose your toenail!\n-1 Health")
                        player_data['health'] -= 1
                        check_death(player_data)
                        colours_left = 6

            # Player walks into a trap
            elif exploration <= 0.65:
                Print("\nUh Oh!")
                time.sleep(1)
                trap_luck = random.random()
                if trap_luck < 0.40:
                    Print("\nAs you were walking over some ice, it broke under your feet causing you to fall into the freezing cold water\n-20 Health")
                    player_data['health'] -= 20
                elif trap_luck < 0.80:
                    Print("\nWhile walking underneath a cliff a huge lump of snow falls onto you!\n-35 Health ")
                    player_data['health'] -= 35
                else:
                    Print("\nHaha just kidding there was no trap but you did find a icicle thats shaped like a sword")
                check_death(player_data)
                
            # Player finds an enemy
            elif exploration <= 0.93:
                battle(player_data)
            # Player encounters the merchant
            else:
                frozen_peaks_merchant(player_data)
            exploration_time -= 1                   
        else:
            player_data['day'] += 1
            break

# Frozen Merchant Encounter
def frozen_peaks_merchant(player_data):
    Print("\n[Snow Wanderer] Hello, Knight, What would you like to buy?")
    while True:
        
        if player_data['weapon_equipped'] not in player_data['owned_weapons']:
            player_data['owned_weapons'].append(player_data['weapon_equipped'])
        if player_data['armour_equipped'] not in player_data['owned_armour']:
            player_data['owned_armour'].append(player_data['armour_equipped'])
                
        Print(f"\nYou have {player_data['gold']} Gold")
        print("\n-----Swords-----\n\n[1] Flame Sword --750 Gold--\n[2] Frost Sword --1.3k Gold--\n\n-----Spears-----\n\n[3] Eagle Spear --1k Gold--\n\n-----Armour-----\n[4] Yeti Armour --900 Gold--\n[5] Titanium Armour --2.35k Gold--")
        action = input("\n-----Potions/Crystals-----\n\n[6] Health Potion --250 Gold--\n[7] Health Crystal --650 Gold--\n\n-----Items-----\n\nEnchant Book --2k Gold--\n\n[r] Exit ")
        if action == '1':
            if player_data['gold'] >= 750:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    if "Flame Sword" in player_data['owned_weapons']:
                        Print("\n[Snow Wanderer] You don't need another Flame Sword I see one on your back!")
                    else:
                        Print("\n[Knight] I would like a ☆ Flame Sword ☆  Please")
                        time.sleep(0.5)
                        Print("\n-750 Gold")
                        player_data['gold'] -= 750
                        player_data['owned_weapons'].append("Flame Sword")
                        time.sleep(0.5)
                        Print("\n[Snow Wanderer] Here you go young one")
                else:
                    pass    
        elif action == '2':
            if player_data['gold'] >= 1300:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    if "Frost Sword" in player_data['owned_weapons']:
                        Print("\n[Snow Wanderer] You don't need another Frost Sword I see one on your back!")
                    else:
                        Print("\n[Knight] I would like a ☆ Frost Sword ☆ to slay the Yeti!")
                        time.sleep(0.5)
                        Print("\n-1.3k Gold")
                        player_data['gold'] -= 1300
                        player_data['owned_weapons'].append("Frost Sword")
                else:
                    pass
        elif action == '3':
            if player_data['gold'] >= 1000:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    if "Eagle Spear" in player_data['owned_weapons']:
                        Print("You already own this")
                    else:
                        Print("\n[Knight] Can I have a ☆ Eagle Spear ☆ ??")
                        Print("\n-1k Gold")
                        time.sleep(0.5)
                        Print("\n[Snow Wanderer] Ooh, lucky you its my last one!")
                        player_data['gold'] -= 1000
                        player_data['weappon_equipped'] = "Eagle Spear"
                        time.sleep(0.5)
                        Print("[Snow Wanderer] Good luck")
            else:
                Print("[Snow Wanderer] Sorry but you can't afford this item")
            
        elif action == '4':
            if player_data['gold'] >= 900:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    if "Yeti Armour" in player_data['owned_armour']:
                        Print("You already own this")
                    else:
                        for armour in armour_data:
                            if armour['name'] == player_data['armour_equipped']:
                                player_data['defence'] -= armour['defence']
                                Print("\n[Knight] Can I have some ☆ Yeti Armour ☆ ?")
                                Print("\n-900 Gold")
                                time.sleep(0.5)
                                Print("\n[Snow Wanderer] I made this one myself! Using the skin of a dead Yeti of course")
                                player_data['defence'] += 19
                                player_data['gold'] -= 900
                                player_data['armour_equipped'] = "Yeti Armour"
                                time.sleep(0.5)
                                Print("[Snow Wanderer] Good luck")
                                break
                        
            else:            
                Print("[Snow Wanderer] Sorry but you can't afford this item")
            
        elif action == '5':
            if player_data['gold'] >= 2350:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    if "Titanium Armour" in player_data['owned_armour']:
                        Print("You already own this")
                    else:
                        for armour in armour_data:
                            if armour['name'] == player_data['armour_equipped']:
                                player_data['defence'] -= armour['defence']
                                Print("\n[Knight] Can I have some ☆ Titanium Armour ☆ ?")
                                time.sleep(0.5)
                                Print("\nThe merchant gives a slow and approving nod")
                                time.sleep(1)
                                Print("\n-2.35k Gold")
                                player_data['defence'] += 31
                                player_data['gold'] -= 2350
                                player_data['armour_equipped'] = "Titanium Armour"
                                time.sleep(0.5)
                                Print("\n[Snow Wanderer] Good luck in the Frozen Peaks knight 😉")
                                break                  
            else:            
                Print("[Snow Wanderer] Sorry but you can't afford this item")
            
        elif action == '6':
            if player_data['gold'] >= 250:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    Print("\n[Knight] One health potion Merchant!")
                    Print("\n-250 Gold")
                    Print("\n[Merchant] Here you go! Did you know that if you die but have a health potion in your inventory it will use the potion and keep you alive instead? All for 250 gold!")
                    Print("\n[Snow Wanderer] Is there anything else I can get for you?")
                    player_data['gold'] -= 250
                    player_data['health_potions'] += 1
                    use_health_potion(player_data)
            else:            
                Print("[Snow Wanderer] Sorry but you can't afford this item")  
                     
        elif action == '7':
            if player_data['gold'] >= 650:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    Print("\n[Knight] Can I have the Health Crystal Please?")
                    Print("\n-650 Gold")
                    Print("\n[Snow Wanderer] Sure thing, now you should be ready for anything!")
                    Print("\nYou stare into the crystal.\n+35 Max Health\n+40 Health")
                    player_data['gold'] -= 650
                    player_data['max_health'] += 35
                    player_data['health'] += 35   
                    
        elif action == '8':
            if player_data['gold'] >= 2000:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    Print("\n[Knight] Can I an enchant book please?")
                    Print("\n[Snow Wanderer] Sure, but I can't guarantee it will be good")
                    Print("\n-2k Gold")
                    random_enchant(player_data, weapons_data) 
                    player_data['gold'] -= 2000
                    Print("\n[Merchant] I hope you enjoy your new enchantment")
                    
            else:        
                Print("[Snow Wanderer] Sorry but you can't afford this item")
            
        elif action == 'r':
            Print("\n[Snow Wanderer] I shall see you soon")
            print("\n-------------------------------------------------------------------------")
            break
        else:
            Print("Please Enter a valid option") 
            
# Blacksmith Shop (Goblin Tinkerer)
def frozen_peaks_blacksmith(player_data, weapons_data, armour_data):
    global upgraded_armour

    Print("\n-----Goblin Tinkerer-----")
    Print("[Goblin Tinkerer] Hello Knight, what would ya like?")
    while True:
        Print(f"\nGold: {player_data['gold']}")
        action = input("\n[1] Shop\n[2] Sharpnen Sword\n[3] Upgrade Armour --200 Gold--\n[r] Leave\nEnter: ").lower()
        if action == '1':
            Print("\n[Knight] I would like to look at your shop please!")
            time.sleep(2)
            os.system('cls')
            Print("-----Goblin Tinkerer Shop-----")
            Print("\n[Goblin Tinkerer] Welcome")
            while True:
                
                if player_data['weapon_equipped'] not in player_data['owned_weapons']:
                    player_data['owned_weapons'].append(player_data['weapon_equipped'])
                if player_data['armour_equipped'] not in player_data['owned_armour']:
                    player_data['owned_armour'].append(player_data['armour_equipped'])
                
                Print("What do you want?")
                Print(f"\nYou have {player_data['gold']} Gold")
                action = input("\n-----Swords-----\n\n[1] Flame Sword --600 Gold--\n[2] Frost Sword --1.1k Gold--\n\n-----Armour-----\n\n[3] Yeti Armour --800 Gold--\n[4] Titanium Armour --2k Gold--\n[r] Leave\nEnter: ").lower()
                if action == '1':
                    if player_data['gold'] >= 600:
                        confirmation = input("Press Enter to confirm or ' r ' to Return ")
                        if confirmation == '':
                            if "Flame Sword" in player_data['owned_weapons']:
                                Print("\n[Goblin Tinkerer] Already have one")
                            else:
                                Print("\n[Knight] I would like an ☆ Flame Sword ☆ Please")
                                time.sleep(1)
                                Print("\n-600 Gold")
                                player_data['gold'] -= 600
                                player_data['weapon_equipped'] = "Flame Sword"
                                time.sleep(1)
                                Print("\n[Goblin Tinkerer] Here")
                                    
                    else:
                        Print("[Goblin Tinkerer] You are poor") 
                        
                elif action == '2':
                    if player_data['gold'] >= 1100:
                        confirmation = input("Press Enter to confirm or ' r ' to Return ")
                        if confirmation == '':
                            if "Frost Sword" in player_data['owned_weapons']:
                                Print("\n[Goblin Tinkerer] Only need 1")
                            else:
                                Print("\n[Knight] Can I have a ☆ Frost Sword ☆ Please")
                                Print("\n-1.1k Gold")
                                player_data['gold'] -= 1100
                                player_data['weapon_equipped'] = "Frost Sword"
                                time.sleep(0.5)
                                Print("\n[Goblin Tinkerer] Good")
                    else:
                        Print("[Goblin Tinkerer] Not enough gold") 

                elif action == '3':
                    if player_data['gold'] >= 800:
                        confirmation = input("Press Enter to confirm or ' r ' to Return ")
                        if confirmation == '':
                            if "Yeti Armour" in player_data['owned_armour']:
                                Print("You already own this")
                            else:
                                for armour in armour_data:
                                    if armour['name'] == player_data['armour_equipped']:
                                        player_data['defence'] -= armour['defence']
                                        Print("\n[Knight] Can I have some ☆ Yeti Armour ☆ ?")
                                        time.sleep(0.5)
                                        Print("\nHe heads to the back of the shop and grabs out the Yeti armour")
                                        time.sleep(1)
                                        Print("\n-800 Gold")
                                        player_data['defence'] += 19
                                        player_data['gold'] -= 800
                                        player_data['armour_equipped'] = "Yeti Armour"
                                        time.sleep(0.5)
                                        Print("\n[Goblin Tinkerer] Come soon")
                    else:
                        Print("[Goblin Tinkerer] Not enough") 

                elif action == '4':
                    if player_data['gold'] >= 2000:
                        confirmation = input("Press Enter to confirm or ' r ' to Return ")
                        if confirmation == '':
                            if "Titanium Armour" in player_data['owned_armour']:
                                Print("You already own this")
                            else:
                                for armour in armour_data:
                                    if armour['name'] == player_data['armour_equipped']:
                                        player_data['defence'] -= armour['defence']
                                        Print("\n[Knight] Can I have some ☆ Titanium Armour ☆ ?")
                                        time.sleep(0.5)
                                        Print("\nHe looks under the counter and grabs out the titanium armour")
                                        time.sleep(1)
                                        Print("\n-2k Gold")
                                        player_data['defence'] += 31
                                        player_data['gold'] -= 2000
                                        player_data['armour_equipped'] = "Titanium Armour"
                                        time.sleep(0.5)
                                        Print("\n[Goblin Tinkerer] Come soon")

                elif action == 'r':
                    Print("\n[Goblin Tinkerer] Out now\n\n[Knight] I am 😠\n\n[Goblin Tinkerer] Good")
                    print("\n-------------------------------------------------------------------------")
                    break
                else:
                    Print("Please Enter a valid option")
            
        elif action == '2':
            if player_data['weapon_equipped'] == "Iron Sword" or "Flame Sword":
                input("\n350 Gold for 4 Extra Damage\nPress Enter to confirm: ")
                if player_data['gold'] >= 350:
                    Print("\n-350 Gold\n+4 Damage")
                    player_data['gold'] -= 350
                    for weapon in weapons_data:
                        if weapon['name'] == player_data['weapon_equipped']:
                            weapon['damage'] += 4
                else:
                    Print("\n[Goblin Tinkerer] Not for free")
                    
            elif player_data['weapon_equipped'] == "Frost Sword":
                input("\n650 Gold for 3 Extra Damage\nPress Enter to confirm: ")
                if player_data['gold'] >= 650:
                    Print("\n-650 Gold\n+3 Damage")
                    player_data['gold'] -= 650
                    for weapon in weapons_data:
                        if weapon['name'] == player_data['weapon_equipped']:
                            weapon['damage'] += 3
                else:
                    Print("\n[Goblin Tinkerer] Too expensive for you")
                    
            else:
                Print("\n[Goblin Tinkerer] No")
                
        elif action == '3':
            if player_data['gold'] >= 200:
                if upgraded_armour == False:
                    if player_data['armour_equipped'] == "No Armour" or "Cloth Armour":
                        Print("\n[Goblin Tinkerer] What armour?")
                    else:
                        Print("\n[Knight] Can you upgrade my armour?")
                        time.sleep(1)
                        Print("\n[Goblin Tinkerer] Give")
                        time.sleep(2)
                        Print("\n[Knight] Sure\n-200 Gold")
                        time.sleep(2)
                        Print("\n*tink *tink")
                        time.sleep(0.6)
                        Print("*bink *bam")
                        Print("\n[Goblin Tinkerer] Here\n+2 Armour Defence\n")
                        player_data['gold'] -= 200
                        upgraded_armour = True
                        for armour in armour_data:
                            if armour['name'] == player_data['armour_equipped']:
                                armour['defence'] += 2
                                player_data['defence'] += 2             
                else:
                    Print("\n[Goblin Tinkerer] Not again")
            else:
                Print("[Goblin Tinkerer] Not free knight")
                
        elif action == 'r':
            Print("\n[Goblin Tinkerer] Bye Knight")
            break

# -- Swamplands -- #

# Swamplands Enemies list
def enemy_data_swamplands():
    leech = {"name": "Leech", "health": 60, "strength": 15, "gold": 15}
    cursed_lilypad = {"name": "Cursed Lillypad", "health": 135, "strength": 39, "gold": 50}
    witch = {"name": "Witch", "health": 130, "strength": 75, "gold": 70}
    arc = {"name": "ARC", "health": 165, "strength": 55, "gold": 80}
    rotwood = {"name": "Rotwood", "health": 250, "strength": 200, "gold": 100}
    zombie = {"name": "Zombie", "health": 300, "strength": 17, "gold": 90}
    skin_walker = {"name": "Skin Walker", "health": 133, "strength": 300, "gold": 150}
    devil = {"name": "Devil", "health": 1000, "strength": 100, "gold": 1000}
    
    random_enemy = random.random()
    if random_enemy < 0.20:
        current_enemy = leech # 20%
    elif random_enemy < 0.40:
        current_enemy = cursed_lilypad # 20%
    elif random_enemy < 0.60:
        current_enemy = witch # 20%
    elif random_enemy < 0.75:
        current_enemy = arc # 15%
    elif random_enemy < 0.86:
        current_enemy = rotwood # 11%
    elif random_enemy < 0.93:
        current_enemy = zombie # 7%
    elif random_enemy < 0.99:
        current_enemy = skin_walker # 6%
    else:
        current_enemy = devil # 1%
        
    return current_enemy

# Player Explores Swamplands
def explore_swamplands(player_data):
    exploration_time = random.randint(3, 6) # How many events the player in encounter
    while True:
        if exploration_time > 0:
            exploration = random.random() # What event the player will encounter
            # Player comes back with nothing
            if exploration < 0.35:
                Print("\nYou came back empty handed")
                exploration_time -= 1
            # Player finds a shrine
            elif exploration < 0.45:
                Print("\nYou uncover a mysterious shrine!")
                Print("[1] Investigate [2] Leave")
                action = input("Enter: ")
                if action == '1':
                    shrine_luck = random.random() # What happens when the player touches the shrine
                    if shrine_luck < 0.33:
                        Print("\nYou feel a warm sensation cover your body +35 Health +5 Max Health")
                        player_data['max_health'] += 5
                        player_data['health'] += 35
                        exploration_time -= 1
                    elif shrine_luck < 0.66:
                        Print("\nYou feel a figure touch your shoulder...")
                        time.sleep(3)
                        Print("\nBefore you can catch a glimpse, it disappears into the trees and you hope that nothing bad happened")
                        player_data['max_health'] -= 10
                        exploration_time -= 1
                    else:
                        Print("\nYou feel lucky +30 Gold")
                        player_data['gold'] += 30
                        exploration_time -= 1
                elif action == '2':
                    Print("\nYou leave the shrine and continue on")
                    exploration_time -= 1
            # Player walks into a trap
            elif exploration < 0.55:
                Print("\nYou walked into a trap!")
                trap_luck = random.random()
                if trap_luck < 0.40:
                    Print("\nYou fell into a hole and took 10 Damage")
                    player_data['health'] -= 10
                    exploration_time -= 1
                elif trap_luck < 0.80:
                    Print("\nYou got hit by a falling log and took 30 Damage")
                    player_data['health'] -= 30
                    exploration_time -= 1
                else:
                    Print("\nHaha just kidding there was no trap there but you did find an apple + 5 Health")
                    player_data['health'] += 5
                    exploration_time -= 1
            # Player finds an enemy
            elif exploration < 0.90:
                battle(player_data)
                exploration_time -= 1
            # Player encounters the merchant
            else:
                swamplands_merchant(player_data)
                exploration_time -= 1                   
        else:
            player_data['day'] += 1
            break

# Forest Merchant Encounter
def swamplands_merchant(player_data):
    while True:
        Print("\n[Merchant] Hello I am a merchant what would you like to buy?")
        Print(f"\nYou have {player_data['gold']} Gold")
        action = input("\n-----Swords-----\n\n[1] Steel Sword --300 Gold--\n[2] Flame Sword --650 Gold--\n\n-----Spears-----\n\n[3] Eagle Spear --650 Gold--\n\n-----Potions/Crystals-----\n\n[4] Health Potion --100 Gold--\n[5] Health Crystal --600 Gold--\n\n[r] Exit ")
        if action == '1':
            if player_data['gold'] >= 300:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    if "Steel Sword" in player_data['owned_weapons']:
                        Print("\n[Merchant] You don't need another Steel Sword I see one on your back!")
                    else:
                        Print("\n[Knight] I would like an ☆ Steel Sword ☆  Please")
                        time.sleep(0.5)
                        Print("\n-300 Gold")
                        player_data['gold'] -= 300
                        player_data['owned_weapons'].append("Steel Sword")
                        time.sleep(0.5)
                        Print("\n[Merchant] Here you go young one")
                else:
                    pass    
        elif action == '2':
            if player_data['gold'] >= 650:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    if "Flame Sword" in player_data['owned_weapons']:
                        Print("\n[Merchant] You don't need another Flame Sword I see one on your back!")
                    else:
                        Print("\n[Knight] I would like an ☆ Flame Sword ☆  Please")
                        player_data['gold'] -= 650
                        player_data['owned_weapons'].append("Flame Sword")
                else:
                    pass
        elif action == '3':
            if player_data['gold'] >= 650:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    if "Hunting Bow" in player_data['owned_weapons']:
                        Print("You already own this")
                    else:
                        player_data['gold'] -= 650
                        player_data['owned_weapons'].append("Hunting Bow ")
                else:
                    pass
        elif action == '4':
            if player_data['gold'] >= 150:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    possible_health = player_data['max_health'] - player_data['health']
                    if possible_health > 150:
                        use_health_potion(player_data)
                else:
                    pass
        elif action == '5':
            if player_data['gold'] >= 600:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    Print("You stared into the crystal and gained 35 MAX health")
                    player_data['max_health'] += 35
                    player_data['health'] += 35   
                else:
                    pass
        elif action == 'r':
            break
        else:
            Print("Please Enter a valid option") 

# -- Rest Of Game -- #

# Knight RPG intro
def intro():
    print("###########################################################################################################################################################")
    print("##   #####   ##      #######   ###         ####              #####    ########    ###             #######           #####          #####              #####")
    print("##   ####   ###   #   ######   ######   #####    #################    ########    #######    ############   ####   ######   #####   ###    ################")
    print("##   ###   ####   ##   #####   ######   #####    #################    ########    #######    ############   ####   ######   #####   ###    ################")
    print("##   ##   #####   ###   ####   ######   #####    #################    #######     #######    ############         #######   #####  ####    ################")
    print("##      #######   ####   ###   ######   #####    #####          ##                #######    ############   ###   #######         #####    ######        ##")
    print("##   #   ######   #####   ##   ######   #####    #########   #####    ########    #######    ############   ####   ######   ###########    ########    ####")
    print("##   ##   #####   ######   #   ######   #####    #########   #####    ########    #######    ############   #####   #####   ###########    ########    ####")
    print("##   ###   ####   #######      ######   #######    #####    ######    ########    #######    ############   ######   ####   ############    ######    #####")
    print("##   ####   ###   ########     ###         ######         ########    ########    #######    ############   #######   ###   #############            ######")
    print("###########################################################################################################################################################")

# Plays Queen and knight yapping
def start_prologue(settings):
    intro()

    print("\n-------------------------------------------------------------------------")
    Print("\nLoading data...")
    time.sleep(random.uniform(1, 1.8))
    Print("Loading Complete!")
    print("\n-------------------------------------------------------------------------")
        
    if settings["skip_intro"] == True:
        pass
    else:
        Print("\n-----Prologue-----")
        Print("[Queen] You have been tasked with slaying the dragon that dwells in the Caves of Hulpha. This will not be an easy quest, as you must journey through the Frozen Peaks, Swamplands, and the village of Klare.\n[Queen] Good luck, my brave knight. My kingdom and I will await your safe return.\n")
        Print("[Knight] I accept this quest, my queen. For your safety and for the honor of the kingdom, I shall see the beast slain. The Frozen Peaks, the Swamplands, and the villagers of Klare will not stop me. I will come back safely.\n")
        Print("[Queen] Brave words, good knight, but strength alone will not defeat the dragon. You must use intelligence, patience, and follow your heart.\n[Queen] Go brave knight and may the gods be on your side ❤️\n")
        settings['skip_intro'] = True
        with open('savedata.json', 'w') as save_file:
            json.dump(settings, save_file, indent=4)
    return settings

# Enemy Battle
def battle(player_data):
    # Determine the current enemy based on location
    if player_data['location'] == 'Forest':
        current_enemy = enemy_data_forest()
    elif player_data['location'] == 'Frozen Peaks':
        current_enemy = enemy_data_frozen_peaks()
    elif player_data['location'] == 'Swamplands':
        current_enemy = enemy_data_swamplands()
    else:
        Print("Unknown location!")
        return

    Print(f"\n-----Enemy Battle-----\nYou encounter a {current_enemy['name']}!")

    # Ensure player health does not exceed max health
    player_data['health'] = min(player_data['health'], player_data['max_health'])

    # Get equipped weapon data
    equipped_weapon = next((w for w in weapons_data if w['name'] == player_data['weapon_equipped']), None)
    if not equipped_weapon:
        Print("Error: Equipped weapon not found!")
        return

    true_damage = equipped_weapon['damage'] + player_data['strength']
    crit_bonus = 0
    lifesteal_value = 0

    # Handle weapon enchantments
    if equipped_weapon['special'] != "None":
        enchant = equipped_weapon['special']
        if enchant.startswith("Strength"):
            strength_level = int(enchant.split()[1])  # Extract the level (1, 2, or 3)
            strength_multiplier = {1: 0.35, 2: 0.75, 3: 1.50}[strength_level]  # Map levels to multipliers
            true_damage += int(true_damage * strength_multiplier)  # Add percentage-based bonus
        elif enchant.startswith("Precision"):
            crit_bonus += int(enchant.split()[1]) * 25
        elif enchant.startswith("Life Steal"):
            lifesteal_value = {1: 10, 2: 15, 3: 20}[int(enchant.split()[2])]
            
    base_enemy_damage = max(0, current_enemy['strength'] - player_data['defence'])  # Calculate base enemy damage minus player defence
    
    if base_enemy_damage <= 0:
        base_enemy_damage = -5

    if settings['skip_battles'] == True:
        
        # Fight loop without text
        while player_data['health'] > 0 and current_enemy['health'] > 0:
            
            # Player Attacks
            player_damage = random.randint(max(1, true_damage - 3), true_damage + 5)

            # Checks for companion
            if player_data['companion']:
                companion_damage = (random.randint(3, 5) * player_data['companion'])
            else:
                companion_damage = 0
                
            # Checks for critical hit
            crit_roll = random.randint(1, 100)
            if crit_roll <= player_data['crit_chance'] + crit_bonus:
                player_damage *= 2
                
            current_enemy['health'] -= player_damage
            current_enemy['health'] -= companion_damage
            
            if lifesteal_value > 0:
                drained = int(player_damage * (lifesteal_value / 100))
                player_data['health'] += drained
                      
            if current_enemy['health'] <= 0:
                Print(f"\nYou defeated the {current_enemy['name']}!")
                player_data['gold'] += current_enemy['gold']
                Print(f"You have {player_data['health']} health remaining, and received {current_enemy['gold']} gold")
                break
            
            # Enemy Attacks
            enemy_damage = max(0, random.randint(base_enemy_damage - 3, base_enemy_damage + 5))
            if enemy_damage >= 0:
                player_data['health'] -= enemy_damage
                check_death(player_data)

    else:

        # Fight loop with text
        while player_data['health'] > 0 and current_enemy['health'] > 0:
            
            # Player Attacks
            player_damage = random.randint(max(1, true_damage - 3), true_damage + 5)

            # Checks for companion
            if player_data['companion']:
                companion_damage = (random.randint(3, 5) * player_data['companion'])
            else:
                companion_damage = 0
                
            # Checks for critical hit
            crit_roll = random.randint(1, 100)
            if crit_roll <= player_data['crit_chance'] + crit_bonus:
                Print("\nCritical Hit!")
                player_damage *= 2
            
            
            current_enemy['health'] -= player_damage
              
            # Sets enemy health to 0 if defeated 
            if current_enemy['health'] <= 0:
                current_enemy['health'] = 0

            Print(f"\n[Knight] You attacked the {current_enemy['name']} and dealt {player_damage} damage! Health remaining: {current_enemy['health']}")
            if lifesteal_value > 0:
                drained = int(player_damage * (lifesteal_value / 100))
                player_data['health'] += drained
                Print(f"You gained {drained} health!")
              
            if companion_damage == 0:
                pass
            else:
                if current_enemy['health'] <= 0: # Skips companion attack if enemy is dead
                    pass
                else:
                    current_enemy['health'] -= companion_damage
                    Print(f"Your companion does {companion_damage} damage! Health remaining: {current_enemy['health']}\n")

            if current_enemy['health'] <= 0:
                Print(f"\nYou defeated the {current_enemy['name']}!")
                player_data['gold'] += current_enemy['gold']
                Print(f"You recieved {current_enemy['gold']} gold")
                break
            
            #Enemy Attacks
            enemy_damage = random.randint(max(0, base_enemy_damage - 3), max(0, base_enemy_damage + 5))

            player_data['health'] -= enemy_damage
            if player_data['health'] <= 0:
                player_data['health'] = 0
            Print(f"[Enemy] The {current_enemy['name']} did {enemy_damage} damage! Health remaining: {player_data['health']}")
            check_death(player_data)
            
            time.sleep(1.4) # Delay Between attacks
            
        if player_data['health'] > 0:
            Print("\n[Knight] Ha! No enemy shall stop me from slaying the dragon!")

# Main game loop
def start_story(player_data, settings):
    
    global healed_today, fight_boss, seen_hermit
    
    if settings['debugging'] == False:
        Print("\n-----Main Game-----")
        Print("You leave the castle and head out to the forest and setup a camp")
        time.sleep(2)
    else:
        player_data['max_health'] = 1000
        player_data['health'] = 1000
        player_data['gold'] = 100000
        
    
    while True:

        if player_data['health'] > player_data['max_health']:
            player_data['health'] = player_data['max_health']
            
        #Stops CMD from cleaning before the text is finished being read    
        input("\nPress Enter to continue: ")
          
        stat_display(player_data)
        print(f"\n{display_random_tip()}")
        print("\n-----Choices-----")
        print("[1] Explore\n[2] Rest\n[3] View Inventory\n[4] Settings\n[5] Help\n[6] Update log\n[7] Fight Zone Boss")
        
        if player_data['slime_kingdom'] == True:
            print("[8] Slime Kindom")
        if settings['debugging']:
            print("[10] Debugging")
        action = input("Enter: ")
        
        if action == '1':
            
            # If the player is in the forest
            if player_data['location'] == 'Forest':
                explore_forest(player_data, weapons_data)
                
            # If the player is in the frozen peaks        
            elif player_data['location'] == 'Frozen Peaks':
                explore_frozen_peaks(player_data)
                
            # If the player is in the swamplands
            elif player_data['location'] == 'Swamplands':
                explore_swamplands(player_data)
                
            healed_today = False
                
        elif action == '2':
            if healed_today == False:
                player_data['health'] = min(player_data['max_health'], player_data['health'] + 30)
                player_data['max_health'] += 5
                Print("\n[Knight] I shall sit down to regain my strength (+30 Health, +5 Max Health)")
                healed_today = True
            else:
                Print("\n[Knight] I have too much energy to sit down right now")
            time.sleep(1)
            
        elif action == '3':
            # Display inventory
            inventory_display(player_data, weapons_data, armour_data)
            
        elif action == '4':
            # Display settings
            settings_display(settings)
            
        elif action == '5':
            # Help menu
            os.system('cls') # Clear CMD
            Print("-----Help Menu-----")
            print("[1] How to win the game\n[2] Progressing through levels\n[3] What are enchants and how do they work?\n[4] List of enchants and their effects\n[5] How to spend gold and what to buy")
            print("[6] Understanding companions\n[7] How defence works\n[8] How critical hits work\n[r] Return to main menu")
            action = input("Enter: ")
            
            if action == '1':
                Print("\nTo win the game, you must journey through four zones: Forest, Frozen Peaks, Swamplands, and the Village of Klare. Each zone has a boss that you must defeat to progress. After completing all zones, you will face the final challenge: slaying the dragon.")
            elif action == '2':
                Print("\nTo progress through the game, explore each zone to gather resources, fight enemies, and prepare for the zone boss. Defeating the boss unlocks the next zone. Each zone has unique enemies, events, and challenges.")
            elif action == '3':
                Print("\nEnchants are special bonuses applied to your equipped weapon. They can increase damage, critical hit chance, or even provide life steal. Enchants are permanent for the weapon they are applied to and remain even when swapping weapons.")
            elif action == '4':
                Print("\n--- Enchant List ---")
                Print("Strength 1: +35% Damage")
                Print("Strength 2: +75% Damage")
                Print("Strength 3: +150% Damage")
                Print("Precision 1: +25% Critical Hit Chance")
                Print("Precision 2: +50% Critical Hit Chance")
                Print("Life Steal 1: +10% Life Steal")
                Print("Life Steal 2: +15% Life Steal")
                Print("Life Steal 3: +20% Life Steal")
            elif action == '5':
                Print("\nGold can be spent at merchants and blacksmiths to buy weapons, armour, potions, and crystals. Merchants appear randomly during exploration, while blacksmiths are found in specific events. Use gold wisely to improve your stats and gear.")
            elif action == '6':
                Print("\nCompanions are allies that assist you in battle by dealing additional damage to enemies. They are acquired through specific events and remain with you throughout your journey. Every time you aquire a new companion they will deal more damage")
            elif action == '7':
                Print("\nDefence reduces the damage you take from enemies. It is primarily determined by the armour you have equipped. Upgrading your armour at blacksmiths or through events increases your defence. The stats of armour can be viewed in the armour stat's in the inventory")
            elif action == '8':
                Print("\nCritical hits are powerful attacks that deal double damage. Your critical hit chance is determined by your weapon and any enchants applied to it. Higher critical hit chance increases the likelihood of landing a critical hit. This can be viewed in the weapon's stats in the inventory")
            elif action == 'r':
                Print("\nReturning to the main menu...")
            else:
                Print("\nPlease Enter a number between 1 and 9")
                
        elif action == '6':
            # Update log
            os.system('cls') # Clear CMD
            Print("\n-----Current Version: 4.1-----")
            print("-Enchants now work and can be found in more places")
            print("-Made Enchants buyable from merchants")
            print("-Health potions now store in your inventory and will be used to save you from death")
            print("-Added 2 new events to the Frozen Peaks")
            print("\n---Bugs/Changes---")
            print("-Buffed the Enchants to be more useful")
            print("-Removed 'Check Stats' and made it stay at the top")
            print("-Removed Recommended stats from help menu and added them to the boss fight menu")
            print("-Removed the owned weapons and armour from the stat display")
            print("-Changed the 'Critical Hit!' To be in the center of the attacks not at the top")
            print("-Changed the inventory to be easier to navigate")
            print("-Changed the possible rewards from Frozen Peaks crystal cave event from 5+ or -5 to +7 or -7")
            print("-Changed some events in Frozen Peaks have a higher chance to give health")
            print("-Changed slime kingdom exit from '3' to 'r'")
            print("-Changed the frozen peaks 'storm power' to be set to 0 when escaping the endless storm event")
            print("-Changed the 'Knight RPG' intro")
            print("-Changed the rewards of a potion in the Forest cave event")
            print("-Changed when fighting a boss it will now show your recommended defence alongside health and damage")
            print("-Changed the skip intro setting to be set to true after viewing the intro for the first time")
            print("-Changed so if the enemy is already dead, your companions won't attack")
            print("-Changed the game to load wayy faster")
            print("-Changed the Frozen Peaks merchant to be more common")
            print("-Fixed the enemy and player health going into the negatives")
            print("-Fixed blacksmiths being able to upgrade 'No Armour'")
            print("-Fixed viewing the endless storm map crashing the game")
            print("-Fixed a bug where the potion reward from the Old Lady wouldn't work")
            print("-Fixed not being able to buy armour from the Goblin Tinkerer")
            print("-Fixed health potions not working in Frozen Peaks")
            print("-Fixed not fighting the correct enemy in the cave")
            print("-Fixed auto exiting the blacksmith when buying extra damage")
            print("-Fixed robbing the villager saying +3 defence instead of +2 defence")
            print("-Fixed only being able to upgrade armour once in the entire game")
            print("-Fixed multiple incorrect formattings")
            print("-Fixed the Frozen Peaks wizard event from not working")
            print("\n-----Previous Version: V4-----")
            print("-ADDED THE FROZEN PEAKS!!! with about 20 new events, along with the frozen merchant")
            print("-ADDED WORKING and swapable armour from the merchants!!!")
            print("-Added the SLIME KINGDOM!!!")
            print("-Changed defence rewards to be mostly applied to the current armour instead of the player")
            print("-Added a setting to skip the opening dialogue upon opening the game")
            print("-Added tips above the main menu")
            print("-Your settings now save")
            print("-Reworked meeting Bob and the bounty hunters")
            print("-Reworked the endless road to be easier to escape")
            print("-Added more outcomes to the shrine (along with 2 super rare ones :O)")
            print("-Added a press Enter to continue setting")
            print("-Reworked the help menu to include new features and make it easier to understand")
            print("-The terminal now clears to make it easier to see whats happening")
            print("-Added an intro")
            print("-Nerfed the Elf rewards massively")
            print("-Removed Debug mode from settings")
            print("-The player now starts on day 1 instead of 0")
            print("-Removed strength from the berry event and decreased the odds of the berry being positive")
            print("-New Trap in the forest area")
            print("-Made the falling log trap weaker")
            print("-Tweaked flower event rewards")
            print("-Updated Rock Paper Scissors")
            print("-Updated 21 Game")
            print("-Renamed Coins to Gold in check stats")
            print("\n---Bugs---")
            print("-Fixed game crash when exploring haunted house")
            print("-Fixed one of the haunted house events not finishing")
            print("-Fixed multiple instances of the game not registering an invalid input")
            print("-Fixed Frost Orb from bandit outpost showing rewards incorrectly")
            print("-Fixed the map in the endless road not letting you escape")
            print("-Fixed variables not fully resetting when restarting the game")
            print("-Fixed an issue where the merchant would say you cant afford something after you buy it")
            print("-Fixed multiple instances of the game breaking when entering an invalid number")
            print("-Fixed an event that caused you to fight the same enemy over and over")
            print("-Fixed game not ending if player presses anything other than 1 when dead")
            print("-Fixed the berry event from never running out of berries")
            print("-Fixed the gotten lost event to not end when going left")
            print("-Fixed some spelling issues")
            print("\n-----Previous Version: V3.1-----")
            print("-Added a game of Rock Paper Scissors")
            print("\n-----Previous Version: V3-----")
            print("- Added the Frozen Peaks and Swamplands area")
            print("- Added a Forest, Frozen Peaks and Swamplands boss")
            print("- Added functionality to defence")
            print("- Added critical hits")
            print('- Added around 20 new events and removed the " You found nothing " (mostly) (for the forest area)')
            print("- Added a game of 21 that you can vs a villagers in for gold (easily accessible in debug menu)")
            print("- Added a simple game of higher or lower to bet gold on (easily accessible in debug menu)")
            print("- Added Enchants... without the effects!!")
            print("\n-------------------------------------------------------------------------")
            
        elif action == '7':
            
            os.system('cls') # Clear CMD

            true_damage = get_equipped_weapon_damage(player_data, weapons_data) + player_data['strength']
            Print(f"Your Health: {player_data['health']}, Your Damage: {true_damage}, Your Defence: {player_data['defence']}")
            Print("\nHowler Recommended: 150 Health, 35 Damage, 10 Defence")
            Print("Bigfoot Recommended: 500 Health, 80 Damage, 25 Defence")
            Print("Headwitch Recommended: 1200 Health, 180 Damage, 40 Defence")
            Print("Baron Recommended: 2500 Health, 250 Damage, 70 Defence")
            Print("Dragon Recommended: ???")

            action = input("\nAre you sure you want to fight the boss?\n\n[1] Yes\n[2] No\nEnter: ")
            if action == '1':
                if player_data['location'] == 'Forest':
                    fight_boss = True
                    battle(player_data)
                    fight_boss = False
                    player_data['location'] = 'Frozen Peaks'
                    healed_today = False
                    seen_hermit = False
                    time.sleep(3)
                    os.system('cls')
                    Print("As you go to leave towards the Frozen Peaks you take a look back at the Howler's body and feel proud.")
                    Print("\n------ FROZEN PEAKS ------")

                elif player_data['location'] == 'Frozen Peaks':
                    fight_boss = True
                    battle(player_data)
                    fight_boss = False
                    player_data['location'] = 'Swamplands'
                    healed_today = False
                    os.system('cls')
                    Print("As you leave the storm of Frozen Peaks you look at Bigfoot's body and feel a sense of accomplishment")

                elif player_data['location'] == "Swamplands":
                    fight_boss = True
                    battle(player_data)
                    fight_boss = False
                    player_data['location'] = 'Klare'
                    healed_today = False

        elif action == '8':
            if player_data['slime_kingdom']:
                slime_kingdom(player_data)

        elif action == '10':
            
            # Debugging Menu
            if settings['debugging'] == True:
                print("\n---Debugging Menu---")
                action = input("\n[1] Set Max Health\n[2] Set Health\n[3] Set Strength\n[4] Set Defence\n[5] Set Current Armour\n[6] Set Gold\n[7] Set Location\n[8] Set Current Weapon\n[9] Roll Weapon Enchant\nEnter: ")
                if action == '1':
                    player_data['max_health'] = int(input("Set Max Health: "))
                elif action == '2':
                    player_data['health'] = int(input("Set Health: "))
                elif action == '3':
                    player_data['strength'] = int(input("Set Strength: "))
                elif action == '4':
                    player_data['defence'] = int(input("Set Defence: "))
                elif action == '5':
                    new_armour = input("Set Current Armour: ")
                    player_data['armour_equipped'] = new_armour
                    player_data['owned_armour'].append(new_armour)
                elif action == '6':
                    player_data['gold'] = int(input("Set Gold: "))
                elif action == '7':
                    action = input("[1] Forest\n[2] Frozen Peaks\n[3] Swamplands\n[4] Village Of Klare\nEnter: ")
                    if action == '1':
                        player_data['location'] = 'Forest'
                    elif action == '2':
                        player_data['location'] = 'Frozen Peaks'
                        player_data['max_health'] = 300
                        player_data['health'] = 250
                        player_data['strength'] = 35
                        player_data['defence'] = 10
                    elif action == '3':
                        player_data['location'] = 'Swamplands'
                    elif action == '4':
                        player_data['location'] = 'Klare'
                elif action == '8':
                    new_weapon = input("Set Current Weapon: ")
                    player_data['weapon_equipped'] = new_weapon
                    player_data['owned_weapons'].append(new_weapon)
                elif action == '9':
                    random_enchant(player_data, weapons_data)

        elif action == 'debug enable':
            settings['debugging'] = True
            with open('savedata.json', 'w') as save_file:
                json.dump(settings, save_file, indent=4)
        elif action == 'debug disable':
            settings['debugging'] = False
            with open('savedata.json', 'w') as save_file:
                json.dump(settings, save_file, indent=4)
        else:
            print("That is not a valid input")

# Ending dialog      
def start_ending():
    Print("You made it back safely and won!")

# Checks if the player has died
def check_death(player_data):
    if player_data['health'] <= 0:
        if player_data['health_potions'] > 0:
            player_data['health_potions'] -= 1
            Print("\nYou used a health potion to save yourself from dying!\n+10 Health")
            player_data['health'] += 10
        else:
            game_over()
    else:
        pass

# If player dies
def game_over():

    Print("\nYou have unfortunately died, failing to slay the dragon and save the kingdom")
    action = input("Press 1 to Play Again or press Enter to exit\nEnter: ")
    if action == '1':
        global fight_boss, fight_caveman, fight_campfire_bandit, fight_bandit_outpost, fight_villager
        global fight_ghost, fight_merchant, fight_black_knight, fight_endless_road_skeleton, fight_bandit_leader
        global fight_elder_yeti, viewed_map, encounter_1, encounter_2, helped_bob, seen_bob, seen_bounty_hunter, seen_hermit
        global colours_left, healed_today, upgraded_armour, storm_power, picked_events_left
        # Reset globals
        fight_boss = False
        fight_caveman = False
        fight_campfire_bandit = False
        fight_bandit_outpost = False
        fight_ghost = False
        fight_merchant = False
        fight_black_knight = False
        fight_endless_road_skeleton = False
        fight_bandit_leader = False
        fight_elder_yeti = False
        viewed_map = False
        encounter_1 = True
        encounter_2 = False
        helped_bob = False
        seen_bob = False
        seen_bounty_hunter = False
        seen_hermit = False
        colours_left = 6
        healed_today = True
        upgraded_armour = False
        fight_villager = False
        storm_power = 0
        picked_events_left = 0
        os.system('cls')
        start_game()
        
    else:
        sys.exit()

start_game()