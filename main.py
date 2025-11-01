# Modules
import time
import random
import sys

# Mechanics
from inventory import inventory_display
from inventory import get_equipped_weapon_damage

# Minigames
from twentyone import play_21
from higherlower import play_higherlower

# Player Actions
healed_today = True
upgraded_armour = False

# Enemies
fight_boss = False
fight_caveman = False
fight_campfire_bandit = False
fight_bandit_outpost = False
fight_ghost = False

# Game Actions
viewed_map = False
encounter_1 = True
encounter_2 = False
helped_bob = False
seen_bob = False

# Print text with delay
def Print(text, delay=0.02): #0.02
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

# Makes the game run (dont touch)
def start_game():
    # Sets up player data
    player_data = main_player()
    # Goes to next part of game one the previous is done
    start_prologue()
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
        "day": 0,
        "location": 'Forest',
        "weapon_equipped": 'Bronze Sword',
        "crit_chance": 2,
        "life_steal": 0,
        "owned_weapons": ["Bronze Sword"],
        "companion": False,
    }
    return player_data

# Display player stats
def stat_display(player_data):
    print("\n-----Character Stats-----")
    print(f"Max Health: {player_data['max_health']}")
    print(f"Health: {player_data['health']}")
    print(f"Strength: {player_data['strength']}")
    print(f"Defence: {player_data['defence']}")
    print(f"Coins: {player_data['gold']}")
    print(f"Day: {player_data['day']}")
    print(f"Location: {player_data['location']}")
    print(f"Weapon: {player_data['weapon_equipped']}")
    print(f"Owned Weapons: {player_data['owned_weapons']}")
    print("\n-------------------------------------------------------------------------")

# Weapons Data
def weapons():
    weapons_data = [
        # Swords
        {"name": "Bronze Sword", "damage": 8, "crit_chance": 2, "special": "None"},
        {"name": "Iron Sword", "damage": 16, "crit_chance": 5, "special": "None"},
        {"name": "Steel Sword", "damage": 35, "crit_chance": 7, "special": "None"},
        {"name": "Flame Sword", "damage": 70, "crit_chance": 10, "special": "None"},
        {"name": "Frost Sword", "damage": 85, "crit_chance": 35, "special": "None"},
        {"name": "Shadow Blade", "damage": 145, "crit_chance": 15, "special": "Life Steal 1"},
        {"name": "Dragon Blade", "damage": 450, "crit_chance": 0, "special": "None"},
        # Bows
        {"name": "Hunting Bow", "damage": 25, "crit_chance": 3, "special": "None"},
        {"name": "Elven Bow", "damage": 45, "crit_chance": 8, "special": "None"},
        {"name": "Dragon Bow", "damage": 130, "crit_chance": 0, "special": "None"},
        # Spears
        {"name": "Eagle Spear", "damage": 35, "crit_chance": 100, "special": "None"},
    ]
    return weapons_data

# Sets up weapon data
weapons_data = weapons()

# Gives the player's current sword an enchant
def enchant_equipped_weapon(weapon):
    enchantments = {
        "Strength 1": {"type": "damage", "value": 15, "rarity": 0.3},
        "Strength 2": {"type": "damage", "value": 45, "rarity": 0.2},
        "Strength 3": {"type": "damage", "value": 100, "rarity": 0.1},
        "Precision 1": {"type": "crit", "value": 10, "rarity": 0.3},
        "Precision 2": {"type": "crit", "value": 25, "rarity": 0.2},
        "Life Steal 1": {"type": "lifesteal", "value": 5, "rarity": 0.3},
        "Life Steal 2": {"type": "lifesteal", "value": 10, "rarity": 0.2},
        "Life Steal 3": {"type": "lifesteal", "value": 15, "rarity": 0.1}
    }

    if "Sword" in weapon['name']:
        enchantment_pool = []
        for enchant, data in enchantments.items():
            enchantment_pool.extend([enchant] * int(data['rarity'] * 100))
        chosen_enchant = random.choice(enchantment_pool)
        weapon['special'] = chosen_enchant
        print(f"{weapon['name']} has been enchanted with {chosen_enchant}!")
    else:
        print("This weapon cannot be enchanted.")

# Selects the random sword Enchant
def random_enchant(player_data, weapons_data):
    weapon = next((w for w in weapons_data if w['name'] == player_data['weapon_equipped']), None)
    if weapon:
        enchant_equipped_weapon(weapon)

# Displays Settings    
def settings_display():
    while True:
        print("\n-----Settings-----")    
        print(f"[1] Skip Battles: {'True' if settings['skip_battles'] else 'False'}")
        print(f"[2] Debugging Mode: {'True' if settings['debugging'] else 'False'}")
        print("[r] Exit")
        
        try:
            settings_choice = input("\nEnter: ").lower()
            if settings_choice == '1':
                skip_battles()
            elif settings_choice == '2':
                settings['debugging'] = 'True'
            elif settings_choice == 'r':
                print("\n-------------------------------------------------------------------------")
                break
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Invalid input! Please Enter a number.")

# Skip battle setting      
def skip_battles():
    settings["skip_battles"] = not settings["skip_battles"]
    skip_battles = "True" if settings["skip_battles"] else "False"

# List of settings        
settings = {
    "skip_battles": False,
    "debugging": False,
}

# Uses a health potion if allowed
def use_health_potion(player_data):
    possible_health = player_data['health'] - player_data['max_health']
    if player_data['location'] == 'Forest':
        health_potion = 50
        if possible_health >= health_potion:
            player_data['health'] += health_potion
            Print(f"You drank the potion and gained {health_potion}")
        else:
            print("error")
    elif player_data['location'] == 'Frozen_Peaks':
        health_potion = 75
        if possible_health >= health_potion:
            player_data['health'] += health_potion
            Print(f"You drank the potion and gained {health_potion}")
        else:
            print("error")
    elif player_data['location'] == "Swamplands":
        health_potion = 125
        if possible_health >= health_potion:
            player_data['health'] += health_potion
            Print(f"You drank the potion and gained {health_potion}")
        else:
            print("error")
    else:
        Print("You cannot use health potions here")

# Function to generate random effects
def random_berry_effect(player_data):
    effect_type = random.choice(["increase", "increase", "decrease"])  # Randomly decide if the effect is positive or negative
    stat = random.choice(["max_health", "health", "strength", "gold", "crit_chance"])  # Randomly choose a stat
    amount = random.randint(1, 3)  # Random effect amount
    
    # Apply effect
    if effect_type == "increase":
        player_data[stat] += amount
        return f"increases your {stat.replace('_', ' ')} by {amount}!"
    else:
        player_data[stat] = max(0, player_data[stat] - amount)  # Ensure stats don't go below 0
        return f"decreases your {stat.replace('_', ' ')} by {amount}."

# Change weapon damage
def edit_weapon_damage(player_data, new_damage):
    weapon_name = player_data["equipped_weapon"]
    for weapon in weapons_data:
        if weapon["name"] == weapon_name:
            weapon["damage"] = new_damage
            print(f"Updated {weapon_name} damage to {new_damage}.")
            break
            
# -- Forest -- #

# Forest Enemies list
def enemy_data_forest(player_data):
    # Easy
    rock = {"name": "Pet Rock", "health": 5, "strength": -5, "gold": 5}
    weak_goblin = {"name": "Weak Goblin", "health": 7, "strength": 3, "gold": 25}
    strong_goblin = {"name": "Strong Goblin", "health": 19, "strength": 7,  "gold": 40}
    orc = {"name": "Orc", "health": 30, "strength": 8, "gold": 20}
    weak_bandit = {"name": "Weak Bandit", "health": 50, "strength": 5, "gold": 35}
    skeleton = {"name": "Skeleton", "health": 20, "strength": 6, "gold": 5}
    wild_dog = {"name": "Wild Dog", "health": 35, "strength": 9, "gold": 5}
    strong_orc = {"name": "Strong Orc", "health": 35, "strength": 13, "gold": 30}
    treasure_chest = {"name": "Treasure Chest", "health": 5, "strength": -5, "gold": 150}
    # Medium
    fly = {"name": "Fly", "health": 10, "strength": 90, "gold": 30}
    albert = {"name": "Albert (homeless)", "health": 50, "strength": 6, "gold": 5}
    defensive_bird = {"name": "Defensive Bird", "health": 20, "strength": 10, "gold": 10}
    wolf = {"name": "Wolf", "health": 40, "strength": 6, "gold": 15}
    cursed_spirit = {"name": "Cursed Spirit", "health": 35, "strength": 15, "gold": 30}
    tree_ent = {"name": "Tree Ent", "health": 65, "strength": 8, "gold": 120}
    sword_skeleton = {"name": "Sword Skeleton", "health": 20, "strength": 20, "gold": 50}
    # Hard
    giant_orc = {"name": "Giant Orc", "health": 75, "strength": 13, "gold": 50}
    metal_skeleton = {"name": "Metal Skeleton", "health": 60, "strength": 8, "gold": 60}
    strong_bandit = {"name": "Strong Bandit", "health": 100, "strength": 9, "gold": 85}
    distorted_figure = {"name": "Distorted Figure", "health": 20, "strength": 45, "gold": 65}
    # Boss
    howler = {"name": "Howler", "health": 300, "strength": 25, "gold": 300}
    # Random encounter enenmies
    caveman = {"name": "Cave Man", "health": 30, "strength": 8, "gold": 40}
    campfire_bandit = {"name": "Bandit", "health": 35, "strength": 8, "gold": 30}
    ghost = {"name": "Ghost", "health": 70, "strength": 10, "gold": 50}

    global fight_boss, fight_caveman, fight_campfire_bandit, fight_bandit_outpost, fight_ghost

    if fight_boss == True:
        current_enemy = howler
        player_data['location'] = 'Frozen Peaks'
    elif fight_caveman == True:
        current_enemy = caveman
    elif fight_campfire_bandit == True:
        current_enemy = campfire_bandit
    elif fight_bandit_outpost == True:
        enemy_type = random.random()
        if enemy_type <= 0.80: # 80%
            current_enemy = weak_bandit
        else: # 20%
            current_enemy = strong_bandit
    elif fight_ghost == True:
        current_enemy = ghost
                
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
            elif random_enemy < 0.60: # 30%
                current_enemy = metal_skeleton
            elif random_enemy < 0.85: # 25%
                current_enemy = strong_bandit
            else: # 15%
                current_enemy = distorted_figure

    return current_enemy

# Player explores forest
def explore_forest(player_data):
    global viewed_map, fight_caveman, fight_campfire_bandit, fight_ghost, helped_bob, seen_bob, upgraded_armour
    exploration_time = random.randint(3, 6) # How many events the player in encounter
    
    while True:
        if exploration_time > 0:
            exploration = random.random() # What event the player will encounter
            
            input("Press Enter to continue\nEnter: ")
            
            # Random Events
            # Main Exploration
            if exploration <= 0.45:
                
                Print("\n-----Wilderness Exploration-----")
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
                            action = input("You find a potion on the table\n[1] Drink\n[2] Leave\nEnter: ")
                            
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
                                    Print("[Knight] Give me another! This is tastes awesome\n+30 Max Health\n+30 Health")
                                    player_data['max_health'] += 30
                                    player_data['health'] += 30
                                    
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
                        fight_caveman == True
                        battle(player_data)
                        
                elif random_event <= 0.10: # House Event
                    Print("You stumble into a run down wooden house amoung the trees")
                    action = input("\n[Knight] This doesnt look dangerous at all\n\n[1] Investigate\n[2] Leave\nEnter: ")
                    
                    if action == '1':
                        
                        house_event = random.random()
                        
                        if house_event <= 0.25:
                            Print("You see a ghost and it starts swinging at you")
                            fight_ghost = True
                            battle(player_data)
                            fight_ghost = False
                            
                        elif house_event <= 0.50:
                            Print("\n[Knight] The door wont open... guess ill continue on")
                            
                        elif house_event <= 0.75:
                            Print("You walk up to the door and it opens. You look around for danger then head inside")
                            house_luck = random.random()
                            if house_luck <= 0.33:
                                chest_reward = random.randint(35, 300)
                                Print(f"After exploring around the house for while you find a chest with {chest_reward} Gold.\n[Knight] It has an ominous glow...")
                                time.sleep(1, 2)
                                action = input("[1] Take Chest\n[2] Leave House\nEnter: ")
                                if action == '1':
                                    player_data['health'] -= 10
                                    Print("You take the chest and lose 10 Health")
                                    check_death(player_data)
                                elif action == '2':
                                    Print("You continue looking and find nothing so you leave")
                                else:
                                    Print("\nPlease Enter a number between 1 and 2")
                                break
                            elif house_luck <= 0.66:
                                Print(f"\nAfter checking the downstairs you head into the attic finding a mysterious book. You open it and in a sudden flash of light it takes the {player_data['weapon_equipped']} out your hand and enchants it with") # NOT FINISHED
                                random_enchant(player_data, weapons_data)
                            else:
                                Print("You fall through the floor and")
                        
                        else:
                            Print("\nYou find armour plating\n+3 Defence")
                            player_data['defence'] += 3
                        break
                    
                    elif action == '2':
                        Print("You leave the house safely")
                        break                  
                    
                elif random_event <= 0.15: # Plant Event
                    Print("You come across a flower field and the sun starts shining\n+5 Max Health\n+10 Health\n+2 Strength\n+1 Defence\n+20 Gold")
                    player_data['max_health'] += 5
                    player_data['health'] += 10
                    player_data['strength'] += 2
                    player_data['defence'] += 1
                    player_data['gold'] += 20
                    Print("\n[Knight] Its a good day today")

                elif random_event <= 0.20: # Elf Event
                    Print("You walk into a mystical clearing filled with crystals and tall flowers surrounding it")
                    Print("\n[Kind Elf] Welcome...")
                    time.sleep(1.5)
                    Print("[Kind Elf] I see you struggling and I wish to grant you something of your choosing\n")
                    time.sleep(1.5)
                    elf_luck = random.random()
                    if elf_luck <= 0.33:
                        while True:
                            action = input(f"[1] Double your current Gold, Current Gold: {player_data['gold']}\n[2] +10 Strength\n[3] +50 Max Health\nEnter: ")
                            if action == '1':
                                player_data['gold'] *= 2
                                Print(f"\n[Kind Elf] Your wish has been granted you now have: {player_data['gold']} Gold!")
                                break
                            elif action == '2':
                                player_data['strength'] += 10
                                Print(f"\n[Kind Elf] I believe this will do you well:\n+10 Strength!")
                                break
                            elif action == '3':
                                player_data['max_health'] += 50
                                Print("\n[Kind Elf] You are now stronger than ever, go complete your quest\n+50 Max Health")
                                break
                            else:
                                Print("\nPlease Enter a number between 1 and 3")
                            
                    elif elf_luck <= 0.66:
                        action = input("[1] Random Enchantment\n[2] Flame Sword (Weapon From Next Area)\n[3] 100% Crit rate with current weapon\nEnter: ")
                        while True:
                            if action == '1':
                                random_enchant(player_data, weapons_data)
                                break
                            elif action == '2':
                                player_data['owned_weapons'].append("Flame Sword")
                                player_data['weapon_equipped'] = "Flame Sword"
                                Print("\n[Kind Elf] Well here is your new ☆ Flame Sword ☆... Enjoy")
                                break
                            elif action == '3':
                                Print("\n[Kind Elf] Now you will do double damage to every enemy with this sword!")
                                player_data['crit_chance'] = 100
                                break
                            else:
                                Print("\nPlease Enter a number between 1 and 3")

                    else:
                        action = input(f"[1] +15 Strength\n[2] +200 Gold\n[3] Set Max Health between 80 and 160\nEnter: ")
                        while True:
                            if action == '1':
                                Print("\nYour armour creaks as you grow in size\n+15 Strength")
                                player_data['strength'] += 15
                                break
                            elif action == '2':
                                Print("\nYour money bag starts to overflow as 200 gold coins are placed into it")
                                player_data['gold'] += 200
                                break
                            elif action == '3':
                                player_data['max_health'] = random.randint(80, 160)
                                Print(f"\n[Kind Elf] your new max health is {player_data['max_health']}!")
                                break
                            else:
                                Print("\nPlease Enter a number between 1 and 3")            

                elif random_event <= 0.25: # Campsite Event
                    Print("You stumbled upon an abandoned campsite.")
                    Print("The campsite seems deserted, but it might hold valuable resources.")
                    
                    action = input("\n[1] Loot Campsite\n[2] Rest without looting\n[3] Continue on your journey\nEnter: ")
    
                    while True:
                        if action == "1":
                            Print("\nYou carefully search the campsite for anything useful.\n")
                            campsite_event = random.random()

                            if campsite_event < 0.4:
                                Print("You found some gold coins hidden under a pile of ashes.")
                                player_data['gold'] += random.randint(10, 50)
                            elif campsite_event < 0.7:
                                Print("You found a sturdy piece of equipment that boosts your defence.")
                                player_data['defence'] += random.randint(1, 3)
                            else:
                                Print("While searching, you disturbed a snake and got bitten! You lose some health.")
                                player_data['health'] -= random.randint(5, 15)

                        elif action == "2":
                            Print("\nYou decide to rest at the campsite.\n")
                            campsite_event = random.random()

                            if campsite_event < 0.5:
                                Print("After a long rest your health is restored to max")
                                player_data['health'] = player_data['max_health']
                            else:
                                fight_campfire_bandit = True
                                Print("You were attacked by bandits during your rest. You fought them off but lost some health.")
                                battle(player_data)

                        elif action == "3":
                            Print("You decide to leave the campsite alone. Better safe than sorry.")
                        else:
                            Print("Invalid choice. You hesitate for too long and move on without doing anything.")
                        break

                elif random_event <= 0.30: # Animal Attack
                    Print("A wild animal attacks you unexpectedly!")
                    Print("It does 15 Damage!")
                    player_data['health'] -= 15
                    check_death(player_data)
                    Print("However you manage to kill it before it does anything else")

                elif random_event <= 0.35: # Edible Plants Event
                    Print("You found a rare edible plant and decide to eat it")
                    Print("+3 Strength")
                    player_data['strength'] += 3

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
                                Print("The villager bursts into tears and hands you a family heirloom, insisting you keep it for protection.\n+3 Defence")
                                player_data['defence'] += 3
                            elif outcome < 0.6:
                                Print("The villager gives you some money and says to meet him back here if you ever find his family.\n+25 Gold")
                                player_data['gold'] += 25
                            else:
                                Print("[Villager] May I please come with you along your adventure as word is that you are going to travel through the village or Klare.")
                                Print("\n[Knight] Yes, you may... as long as you help me")
                                Print("\n[Villager] I promise to, good knight")
                                player_data['companion'] = "True"
                        elif choice == '2':
                            Print("\n[Knight] Give me all your money!")
                            Print("\n[Villager] No please, I have just lost my family as my village was raided by bandits")
                            Print("\n[Knight] Well that sounds unfortnate")
                            Print("[Knight] I'll just take this and be on my way\n+25 Gold\n\nYou found a defence charm\n+3 Defence")
                            player_data['defence'] += 3
                            player_data['gold'] += 25
                        else:
                            Print("Please Enter a number between 1 and 2")
                    else:
                        Print("Please Enter a number between 1 and 2")
                        
                elif random_event <= 0.45: # Endless Road Event
                    
                    escape_chance = 0  # Initial escape chance percentage

                    Print(f"Welcome to the Endless Road! Can you find your way out?")
                    while True:
                        # Escape once escape chance hits 100
                        Print(f"\n---You are currently {escape_chance}% of the way escaped from the road---\n")
                        if escape_chance >= 100:
                            print("\nYou found the way out! Congratulations!\n+150 Gold")
                            player_data['gold'] += 150
                            break

                        # Random event
                        road_luck = random.random()
                        
                        if road_luck <= 0.15: # Go left or right
                            Print("You find a fork in the road.")
                            action = input("Which way do you go?\n[1] Left\n[2] Right\nEnter: ")
                            if action == '1':
                                Print("You encounter a strange glowing crystal. It hums with energy.\n+2 Strength\n-1 Defence")
                                player_data['strength'] += 2
                                player_data['defence'] -= 1
                                if viewed_map == True:
                                    escape_chance += 100
                                
                            elif action == '2':
                                Print("A dense fog surrounds you, and you hear whispers from all around.\n-10 Health")
                                player_data['health'] -= 10
                                escape_chance -= 5
                                check_death(player_data)

                        elif road_luck <= 0.25: # Abandond Camp
                            Print("You stumble across an abandoned campsite.")
                            action = input("What do you do?\n\n[1] Search the camp\n[2] Move on\nEnter: ")
                            if action == '1':
                                Print("You find some useful supplies, but the air feels ominous.")
                                Print("\n[Knight] I better get out of here before something bad happens")
                                # Gain items, but maybe trigger a future trap
                            elif action == '2':
                                Print("You leave the camp behind and continue on your journey.")
                                escape_chance + 5

                        elif road_luck <= 0.35: # Hermit 
                            Print("You come across a Hermit sitting by the path.")
                            action = input("What do you do?\n\n[1] Talk to him\n[2] Ignore him\nEnter: ")
                            if action == '1':
                                Print("The Hermit shares his story about how he killed a howler, the fiercest monster in the forest.\n+1 Strength\n+10 Max Health\n+20 Health")
                                player_data['strength'] += 1
                                player_data['max_health'] += 10
                                player_data['health'] += 20
                                escape_chance += 5
                            elif action == '2':
                                Print("The hermit shakes his head as you walk away.")
                                escape_chance += 10

                        elif road_luck <= 0.45: # Storm
                            Print("A sudden storm rages around you, making it hard to see.")
                            action = input("What do you do?\n\n[1] Wait for the storm to pass\n[2] Push on\nEnter: ")
                            if action == '1':
                                Print("The storm passes, but you feel like you lost precious time.")
                                escape_chance -= 10
                            elif action == '2':
                                Print("You brave the storm but emerge exhausted and injured.\n-5 Max Health\n-5 Health")
                                player_data['max_health'] -= 5
                                player_data['health'] -= 5
                                escape_chance += 20

                        elif road_luck <= 0.60: # Find map
                            Print("You find an old, tattered map on the ground.")
                            action = input("What do you do?\n\n[1] Study the map\n[2] Leave it\nEnter: ")
                            if action == '1':
                                Print("\nYou stare at the blank paper for a while, after turning it over it says 'go left if you want to get out'")
                                viewed_map == True
                            elif action == '2':
                                Print("You ignore the map and continue on.")
                                escape_chance + 5

                        elif road_luck <= 0.75: # River
                            Print("You hear a distant sound of rushing water.")
                            action = input("What do you do?\n\n[1] Investigate\n[2] Stay on the path\nEnter: ")
                            if action == '1':
                                Print("You discover a river that seems to block your path.")
                                # Potential detour or obstacle
                            elif action == '2':
                                Print("You stay on the path, avoiding potential danger.")
                                escape_chance += 10
                                
                        elif road_luck >= 0.90: # Find Lost villager
                            Print("A strange shadow follows you silently.")
                            action = input("What do you do?\n\n[1] Confront it\n[2] Ignore it\nEnter: ")
                            if action == '1':
                                Print("The shadow reveals itself to be a harmless traveler seeking guidance.")
                                # Gain an ally or information
                            elif action == '2':
                                Print("The shadow fades into the darkness.")
                        else:
                            Print("You come across a tower and decide to climb it allowing you to see a way to the exit")
                            escape_chance += 35

                        # Increment escape chance after every event
                        escape_chance += 5
                        player_data['health'] -= 10
                        Print("\nYou lose 10 Health due to starvation")
                        check_death(player_data)

                elif random_event <= 0.50: # Bandit camp with 3 enenmies
                    action = input("You come across a bandit outpost with a bunch of enenmies! (VERY DIFFICULT) Do you wish to enter?\n\n[1] Enter\n[2] Walk around it and continue on\nEnter: ")
                    
                    if action == '1':
                        global fight_bandit_outpost
                        fight_bandit_outpost = True
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
                            Print("The chest pops open and you see a glowing item sitting in the corner!\n\n-----Items-----\nYou found an enchanted Frost Orb!!!")
                            Print("\n[Knight] I thought those were from the Frozen Peaks...")
                            Print(f"+{player_data['max_health']} Max Health and {player_data['health']}Health x2")
                            player_data['max_health'] *= 2
                            player_data['health'] *= 2
                        elif treasure <= 0.75:
                            Print("You open the chest to find a bunch of junk...\n\n-----Items-----\nJunk\nJunk\nJunk\nYou found a health potion!\n+1 Health Potion\nJunk\nYou found a Forest Orb!\n+100 Gold\n+5 Defence\n-3 Strength")
                            Print("\n[Knight] Ooh a forest orb")
                            player_data['gold'] += 100
                            player_data['defence'] += 5
                            player_data['strength'] -= 3
                        else:
                            Print(f"As you get closer to the treasure, your {player_data['equipped_weapon']} begins to glow\n\n-----Items-----\nEnchanted book!!!")
                            random_enchant(player_data, weapons_data)
                            
                    elif action == '2':
                        Print("You walk around the bandit outpost and continue on")
                        
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
                        player_data['defence'] += 5
                        
                    elif reward['item'] == "Potion of Strength":
                        Print("You drink the potion\n+15 Max Health\n+20 Health\n+3 Strength")
                        player_data['max_health'] += 15
                        player_data['health'] += 20
                        player_data['strength'] += 3
                    
                    elif reward['item'] == "Caterpillar Charm":
                        Print("You wear the charm around your wrist\n+10% Critical Hit Chance")
                        player_data['crit_chance'] += 10
                        
                    else:
                        Print("You use the Jewel\n+65 Max Health")
                        player_data['max_health'] += 65
                        
                    Print("\nYou thank the Caterpillar Princess and continue on your journey, feeling enriched by the encounter.")
                    
                elif random_event <= 0.60: # Encounter bob
                    
                    action = input("[Bob] Hello stranger, I am heading to the castle to steal from their vault, if you tell me the way to the castle I will give you a cut.\n\n[1] Tell Him\n[2] Start Capping\nEnter: ")
                    
                    seen_bob = True
                    
                    if action == '1':
                        Print("\n[Knight] I dont exactly remember the way but if you head to the clearing that way you should be able to see the castle")
                        Print("\n[Bob] Thank you, I shall give you the rewards if I am to see you again")
                        helped_bob = True
                        
                    elif action == '2':
                        Print("\n[Knight] I have got no idea, im from the town in that direction.")
                        Print("\n[Bob] Okay well I shall continue on my adventure then")
                        helped_bob = False
                        
                elif random_event <= 0.65: # Ask if you have seen bob
                    Print("[Bounty Hunter] Have you seen this little guy called Bob wandering around robbing places and 'giving you a cut' of what he steals?")
                    
                    action = input("\n[1] Yes I know where he is\n[2] I have never seen him before\nEnter: ")
                    
                    if action == '1':
                        if helped_bob == True:
                            Print("\n[Knight] He is heading towards my castle to open the vault in that direction")
                            time.sleep(1.5)
                            Print("\n[Bounty Hunter] Well, he obviously didnt know where the castle was so therefore you told him and so we will take you back to the queen of the castle")
                            time.sleep(3)
                            Print("\n[Queen] Why, Knight did you betray me like this?")
                            time.sleep(1)
                            Print("\n[Knight] I'm sorry my queen")
                            Print("\n[Queen] Its okay Knight, I shall just require you to pay a small amount of the vault back...")
                            while True:
                                action = input("\n[1] Pay\n[2] Go to the dungeons\nEnter: ")
                                if action == '1':
                                    Print("\n[Queen] 2000 GOLD! Guards, empty his pockets")
                                    Print("\n-2000 Gold")
                                    player_data['gold'] -= 2000
                                    break
                                elif action == '2':
                                    Print("\n[Knight] I would rather go to the dungeons then pay that!")
                                    Print("\n[Queen] Well too bad")
                                    # enter_dungeons() # Remove the Queen: well too bad
                                    break
                        elif seen_bob == True:
                            if helped_bob == False:
                                Print("\n[Knight] Well, when I saw I know where he is... I mean I sent him off in that direction")
                                Print("\n[Bounty Hunter] Thanks, we will be on our way and just so you know he was never going to give back that gold so we will give you a smaller amount instead!\n+750 Gold")
                                player_data['gold'] += 750
                                
                        elif seen_bob == False:
                            Print("\n[Knight] Haha just kidding I have no idea who or where this guy is")
                            
                    elif action == '2':
                        if helped_bob == True:
                            Print("[Bounty Hunter] Haha, well you see, Bob... Is this the guy who gave you directions?") # No, wink leaves
                        elif helped_bob == False:
                            Print("[Bounty Hunter] Well, if you ever see him let us know and we will pay you highly")
                            
                elif random_event <= 0.70: # witch that sets player stats to original but doubles a random stat
                    Print("You stumble into a mysterious forest")
                    Print("\n[Unknown] Hello Knight,")
                    time.sleep(1)
                    Print("\n[Knight] Uhm, Hello mysterious voice...")
                    time.sleep(1)
                    Print("\n[Unknown] Do you wish to gain ultimate power?")
                    time.sleep(1)

                    action = input("\n[1] Yes\n[2] No\nEnter: ")

                    if action == '1':
                        Print("\n[Knight] Yes, I do")
                        starting_stat = None
                        changed_stat = None
                        random_stat = random.randint(1, 4)
                        
                        if random_stat == 1:  # Max Health
                            changed_stat = "Max Health"
                            starting_stat = player_data['max_health']
                        elif random_stat == 2:  # Health
                            changed_stat = "Health"
                            starting_stat = player_data['health']
                        elif random_stat == 3:  # Strength
                            changed_stat = "Strength"
                            starting_stat = player_data['strength']
                        elif random_stat == 4:  # Defence
                            changed_stat = "Defence"
                            starting_stat = player_data['defence']
                        
                        if changed_stat == "Max Health":
                            new_stat = starting_stat * 2
                            player_data['max_health'] = new_stat
                            player_data['health'] = 100
                            player_data['strength'] = 0
                            player_data['defence'] = 0
                        elif changed_stat == "Health":
                            new_stat = starting_stat * 2
                            player_data['max_health'] = new_stat
                            player_data['health'] = new_stat
                            player_data['strength'] = 0
                            player_data['defence'] = 0
                        elif changed_stat == "Strength":
                            new_stat = starting_stat * 2
                            player_data['max_health'] = 100
                            player_data['health'] = 100
                            player_data['strength'] = new_stat
                            player_data['defence'] = 0
                        elif changed_stat == "Defence":
                            new_stat = starting_stat * 2
                            player_data['max_health'] = 100
                            player_data['health'] = 100
                            player_data['strength'] = 0
                            player_data['defence'] = new_stat
                        
                        Print("Note: You will need to re-equip armor to restore your defense or change armor (will be fixed in v4).")
                        Print(f"\n[Dark Witch] I have reset all your stats but doubled your {changed_stat}.")
                        Print(f"[Dark Witch] Old: {changed_stat} {starting_stat}, New: {changed_stat} {new_stat}.")
                        
                        if not player_data['companion']:
                            Print("[Dark Witch] I have also summoned a companion for your adventures.")
                            player_data['companion'] = True

                    elif action == '2':
                        Print("\n[Knight] No thanks,")
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

                elif random_event <= 0.80: # makes exploration 2-3 events longer
                    Print("You seem to have gotten lost, which way do you go to get back?")
                    correct_way = random.randint(1, 2)

                    while True:
                        action = input("\n[1] Left\n[2] Right\nEnter: ")
                        
                        if action == '1' and correct_way == 1:
                            Print("\nYou safely got back on track and continued on")
                            break
                        
                        elif action == '1' and correct_way == 2:
                            Print("\nYou go to the left but now the path looks even more unfamiliar")
                            exploration_time += 1
                        
                        elif action == '2' and correct_way == 2:
                            Print("\nYou safely got back on track and continued on")
                            break
                        
                        elif action == '2' and correct_way == 1:
                            Print("\nYou go to the right but now the path looks even more unfamiliar")
                            exploration_time += 1
                        
                        else:
                            Print("Please enter a number between 1 and 2")
                            
                elif random_event <= 0.85: # go and forage for food 5 good, 2 bad, 1 really bad

                    Print("Since you are running low on food you decide to go and hunt for some berries")
                    
                    berries_left = 10
                    
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
                        if berries_left > 0:
                            # Randomly select a berry
                            berry = random.choice(berries)
                            
                            # Ask for the player's action
                            action = input(f"\nDo you want to eat the {berry} berry?\n\n[1] Yes\n[2] No\nEnter: ")
                            
                            if action == '1':
                                # Generate and apply a random effect
                                effect = random_berry_effect(player_data)
                                Print(f"You eat the {berry} berry! It {effect}")
                                berries_left - 1
                                
                                action = input("\nDo you want to continue looking?\n\n[1] Yes\n[2] No\nEnter: ")
                                
                                if action == '1':
                                    Print("You continue looking and find another berry!")
                                    
                                elif action == '2':
                                    Print("You decide you are full and stop looking")
                                    break
                                
                            elif action == '2':
                                Print(f"You decide not to eat the {berry} berry and continue looking.")
                                berries_left - 1
                            else:
                                Print("Invalid choice. Please choose [1] Yes or [2] No.")
                                
                            
                            
                        else:
                            Print("You couldnt find anymore berries to eat")
                            break
                        
                elif random_event <= 0.90: # save slime king and lets you visit his kingdom anytime during your forest and frozen peak adventure
                    print("You found nothing")

                elif random_event <= 0.95: # meet blacksmith to sharpen sword, and improve armour for gold
                    Print("You spot a blacksmith and decide to enter")
                    Print("\n-----Blacksmith-----")
                    while True:
                        Print("[Blacksmith] Hello Knight, what would ya like?")
                        Print(f"\nGold: {player_data['gold']}")
                        action = input("\n[1] Shop\n[2] Sharpnen Sword\n[3] Upgrade Armour (free)\n[r] Leave\nEnter: ").lower()
                        if action == '1':
                            Print("\n[Knight] I would like to look at your shop please")
                            forest_blacksmith(player_data)
                            
                        elif action == '2':
                            if player_data['weapon_equipped'] == "Bronze Sword" or "Iron Sword":
                                input("\n150 Gold for 10 Extra Damage\nPress Enter to confirm: ")
                                if player_data['gold'] >= 150:
                                    Print("-150 Gold")
                                    player_data['gold'] -= 150
                                    player_data['strength'] += 10
                                    # edit_weapon_damage(player_data, )
                                else:
                                    Print("\n[Blacksmith] That is unfortunately not enough to upgrade your sword")
                                    
                            elif player_data['weapon_equipped'] == "Flame Sword":
                                input("\n200 Gold for 5 Extra Damage\nPress Enter to confirm: ")
                                if player_data['gold'] >= 200:
                                    Print("-200 Gold")
                                    player_data['gold'] -= 200
                                    player_data['strength'] += 5
                                else:
                                    Print("\n[Blacksmith] That is unfortunately not enough to upgrade your sword")
                                    
                            else:
                                Print("\n[Blacksmith] Sorry, I dont know how to enchant that sword")
                                
                        elif action == '3':
                            if upgraded_armour == False:
                                Print("\n[Knight] Can you upgrade my armour?")
                                time.sleep(1)
                                Print("\n[Blacksmith] Hand it over and I'll be back to you in a minute")
                                time.sleep(2)
                                Print("\n[Knight] Sure")
                                time.sleep(2)
                                Print("\n*tink *tink")
                                time.sleep(0.6)
                                Print("*bink *bam")
                                Print("\n[Blacksmith] Here ya go\n+5 Defence\n")
                                player_data['defence'] += 5
                                upgraded_armour = True
                                
                            else:
                                Print("\n[Blacksmith] Sorry, I cant upgrade it any further")
                                
                        elif action == 'r':
                            Print("\n[Blacksmith] See you next time!")
                            break
                else:
                    print("You found nothing")
                            
            # Player finds a shrine
            elif exploration <= 0.60:
                Print("\n-----Hidden Shrine-----")
                Print("You uncover a mysterious shrine!")
                action = input("\n[1] Investigate\n[2] Leave\nEnter: ")

                if action == '1':
                    shrine_luck = random.random() # What happens when the player touches the shrine
                    if shrine_luck <= 0.33:
                        Print("\nYou feel a warm sensation cover your body +35 Health +5 Max Health")
                        player_data['max_health'] += 5
                        player_data['health'] += 35

                    elif shrine_luck <= 0.66:
                        Print("\nYou feel a figure touch your shoulder...")
                        time.sleep(2)
                        Print("\nBefore you can catch a glimpse, it disapears into the trees and you hope that nothing bad happend")
                        player_data['max_health'] -= 10

                    else:
                        Print("\nYou feel lucky +30 Gold")
                        player_data['gold'] += 30

                elif action == '2':
                    Print("\nYou leave the shrine and continue on")
                    
            # Player walks into a trap
            elif exploration <= 0.70:
                Print("\nYou walked into a trap!")
                trap_luck = random.random()
                if trap_luck <= 0.40:
                    Print("You fell into a hole and took 10 Damage")
                    player_data['health'] -= 10
                    
                elif trap_luck <= 0.80:
                    Print("You got hit by a falling log and took 30 Damage")
                    player_data['health'] -= 30
                    
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
                              
        else:
            player_data['day'] += 1
            break

# Forest Merchant Encounter
def forest_merchant(player_data):
    print("\n-------------------------------------------------------------------------")
    while True:
        Print("\n[Merchant] Hello I am a merchant what would you like to buy?")
        Print(f"\nYou have {player_data['gold']} Gold")
        action = input("\n-----Swords-----\n\n[1] Iron Sword --100 Gold--\n[2] Steel Sword --225 Gold--\n\n-----Bows-----\n\n[3] Hunting bow --200 Gold--\n\n-----Potions/Crystals-----\n\n[4] Health Potion --50 Gold--\n[5] Health Crystal --300 Gold--\n\n[r] Exit\nEnter: ").lower()
        if action == '1':
            if player_data['gold'] >= 100:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    if "Iron Sword" in player_data['owned_weapons']:
                        Print("\n[Merchant] You dont need another Iron Sword I see one on your back")
                    else:
                        Print("\n[Knight] I would like an ☆ Iron Sword ☆ Please")
                        time.sleep(1)
                        Print("\n-100 Gold")
                        player_data['gold'] -= 100
                        player_data['weapon_equipped'] = "Iron Sword"
                        time.sleep(1)
                        Print("\n[Merchant] Here you go young one")
                        
            Print("[Merchant] Sorry but you can't afford this item")
            
        elif action == '2':
            if player_data['gold'] >= 225:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    if "Steel Sword" in player_data['owned_weapons']:
                        Print("\n[Merchant] You dont need another Steel Sword I see one on your back")
                    else:
                        Print("\n[Knight] Can I have a ☆ Steel Sword ☆ Please")
                        Print("\n-225 Gold")
                        player_data['gold'] -= 225
                        player_data['weapon_equipped'] = "Steel Sword"
                        time.sleep(0.5)
                        Print("\n[Merchant] I believe you can kill anything with this!")
            
            Print("[Merchant] Sorry but you can't afford this item")

        elif action == '3':
            if player_data['gold'] >= 200:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    if "Hunting Bow" in player_data['owned_weapons']:
                        Print("You already own this")
                    else:
                        Print("\n[Knight] Can I have a ☆ Hunting Bow ☆ Please")
                        time.sleep(0.5)
                        Print("\n[Merchant] Thats a good choice! Hope it does you well")
                        player_data['gold'] -= 200
                        player_data['weappon_equipped'] = "Hunting Bow"
                        time.sleep(0.5)
                        Print("[Merchant] Good luck")
                        
            Print("[Merchant] Sorry but you can't afford this item")
            
        elif action == '4':
            if player_data['gold'] >= 50:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    Print("\n[Knight] One health potion Merchant!")
                    # Print("\n[Merchant] Here you go! Did you know that if you die but have a health potion in your inventory it will use the potion and keep you alive instead? All for 50 gold")
                    Print("[Merchant] Is there anything else I can get for you?")
                    possible_health = player_data['max_health'] - player_data['health']
                    player_data['gold'] -= 50
                    
                    if possible_health > 50:
                        use_health_potion(player_data)
                    else:
                        player_data['health'] = player_data['max_health']
                        
            Print("[Merchant] Sorry but you can't afford this item")  
                     
        elif action == '5':
            if player_data['gold'] >= 300:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    Print("\n[Knight] Can I have the Health Crystal Please?")
                    Print("\n-300 Gold")
                    Print("\n[Merchant] Sure thing, now you should be ready for anything!")
                    Print("\nYou stared into the crystal.\n+20 Max Health\n+30 Health")
                    player_data['gold'] -= 300
                    player_data['max_health'] += 20
                    player_data['health'] += 20   
                    
            Print("[Merchant] Sorry but you can't afford this item")
            
        elif action == 'r':
            Print("\n[Merchant] I shall see you soon")
            print("\n-------------------------------------------------------------------------")
            player_data['owned_weapons'].append(player_data['weapon_equipped'])
            break
        else:
            Print("Please Enter a valid option") 

# Blacksmith Shop
def forest_blacksmith(player_data):
    Print("-----Blacksmith Shop-----")
    Print("\n[Blacksmith] Welcome to me shop")
    while True:
        Print("What can I get ya?")
        Print(f"\nYou have {player_data['gold']} Gold")
        action = input("\n-----Swords-----\n\n[1] Iron Sword --75 Gold--\n[2] Steel Sword --200 Gold--\n[r] Leave\nEnter: ").lower()
        if action == '1':
            if player_data['gold'] >= 75:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    if "Iron Sword" in player_data['owned_weapons']:
                        Print("\n[Blacksmith] You dont need another Iron Sword I see one on your back")
                    else:
                        Print("\n[Knight] I would like an ☆ Iron Sword ☆ Please")
                        time.sleep(1)
                        Print("\n-75 Gold")
                        player_data['gold'] -= 75
                        player_data['weapon_equipped'] = "Iron Sword"
                        time.sleep(1)
                        Print("\n[Blacksmith] I always got the best rates just for you")
                else:
                    pass    
        elif action == '2':
            if player_data['gold'] >= 200:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    if "Steel Sword" in player_data['owned_weapons']:
                        Print("\n[Blacksmith] You dont need another Steel Sword I see one on your back")
                    else:
                        Print("\n[Knight] Can I have a ☆ Steel Sword ☆ Please")
                        Print("\n-200 Gold")
                        player_data['gold'] -= 200
                        player_data['weapon_equipped'] = "Steel Sword"
                        time.sleep(0.5)
                        Print("\n[Blacksmith] I believe you can kill anything with this!")
        elif action == 'r':
            Print("\n[Blacksmith] Come back soon for another armour upgrade!")
            print("\n-------------------------------------------------------------------------")
            player_data['owned_weapons'].append(player_data['weapon_equipped'])
            break
        else:
            Print("Please Enter a valid option")
             
# -- Frozen Peaks -- #

# Frozen Peaks Enemies list
def enemy_data_frozen_peaks(player_data):
    # Easy
    frost_orc = {"name": "Frost Orc", "health": 45, "strength": 13, "gold": 20}
    ice_wraith = {"name": "Ice Wraith", "health": 30, "strength": 25, "gold": 25}
    snow_hunter = {"name": "Snow Hunter", "health": 75, "strength": 20, "gold": 35}
    shade = {"name": "Shade", "health": 45, "strength": 90, "gold": 100}
    golem = {"name": "Golem", "health": 300, "strength": 8, "gold": 75}
    frost_wraith = {"name": "Frost Wraith", "health": 50, "strength": 30, "gold": 40}
    # Medium
    # Hard
    # Boss
    bigfoot = {"name": "Bigfoot", "health": 750, "strength": 40, "gold": 500}
    
    
    
    global fight_boss
    if fight_boss == True:
        current_enemy = bigfoot
        player_data['location'] = 'Swamplands'
        
    else:
            
        random_enemy = random.random()
        if random_enemy <= 0.35:
            current_enemy = frost_orc # 35%
        elif random_enemy <= 0.6:
            current_enemy = ice_wraith # 25%
        elif random_enemy <= 0.75:
            current_enemy = snow_hunter # 15%
        elif random_enemy <= 0.85:
            current_enemy = shade # 10%
        elif random_enemy <= 0.95:
            current_enemy = golem # 10%
        else:
            current_enemy = frost_wraith # 5%
            
    return current_enemy

# Player explores frozen peaks
def explore_frozen_peaks(player_data):
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
                        Print("\nBefore you can catch a glimpse, it disapears into the trees and you hope that nothing bad happend")
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
                frozen_peaks_merchant(player_data)
                exploration_time -= 1                   
        else:
            player_data['day'] += 1
            break

# Forest Merchant Encounter
def frozen_peaks_merchant(player_data):
    while True:
        Print("\n[Merchant] Hello I am a merchant what would you like to buy?")
        Print(f"\nYou have {player_data['gold']} Gold")
        action = input("\n-----Swords-----\n\n[1] Flame Sword --300 Gold--\n[2] Frost Sword --650 Gold--\n\n-----Spears-----\n\n[3] Eagle Spear --650 Gold--\n\n-----Potions/Crystals-----\n\n[4] Health Potion --100 Gold--\n[5] Health Crystal --600 Gold--\n\n[r] Exit ")
        if action == '1':
            if player_data['gold'] >= 300:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    if "Flame Sword" in player_data['owned_weapons']:
                        Print("\n[Merchant] You dont need another Flame Sword I see one on your back!")
                    else:
                        Print("\n[Knight] I would like an ☆ Flame Sword ☆  Please")
                        time.sleep(0.5)
                        Print("\n-300 Gold")
                        player_data['gold'] -= 300
                        player_data['owned_weapons'].append("Flame Sword")
                        time.sleep(0.5)
                        Print("\n[Merchant] Here you go young one")
                else:
                    pass    
        elif action == '2':
            if player_data['gold'] >= 650:
                confirmation = input("Press Enter to confirm or ' r ' to Return ")
                if confirmation == '':
                    if "Frost Sword" in player_data['owned_weapons']:
                        Print("\n[Merchant] You dont need another Frost Sword I see one on your back!")
                    else:
                        Print("\n[Knight] I would like an ☆ Frost Sword ☆  Please")
                        player_data['gold'] -= 650
                        player_data['owned_weapons'].append("Frost Sword")
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
            
# -- Swamplands -- #

# Swamplands Enemies list
def enemy_data_swamplands(player_data):
    leech = {"name": "Leech", "health": 60, "strength": 15, "gold": 15}
    cursed_lilypad = {"name": "Cursed Lillypad", "health": 135, "strength": 39, "gold": 50}
    witch = {"name": "Witch", "health": 130, "strength": 75, "gold": 70}
    arc = {"name": "ARC", "health": 165, "strength": 55, "gold": 80}
    rotwood = {"name": "Rotwood", "health": 250, "strength": 200, "gold": 100}
    zombie = {"name": "Zombie", "health": 300, "strength": 17, "gold": 90}
    skin_walker = {"name": "Skin Walker", "health": 133, "strength": 300, "gold": 150}
    devil = {"name": "Devil", "health": 10000, "strength": 10, "gold": 1000}
    
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
                        Print("\nBefore you can catch a glimpse, it disapears into the trees and you hope that nothing bad happend")
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
                        Print("\n[Merchant] You dont need another Steel Sword I see one on your back!")
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
                        Print("\n[Merchant] You dont need another Flame Sword I see one on your back!")
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
      
# Plays Queen and knight yapping and fake loading
def start_prologue():
    Print("-----Prologue-----")
    Print("[Queen] You have been tasked with slaying the dragon that dwells in the Caves of Hulpha. This will not be an easy quest, as you must journey through the Frozen Peaks, Swamplands, and the village of Klare.\n[Queen] Good luck, my brave knight. My kingdom and I will await your safe return.\n")
    Print("[Knight] I accept this quest, my queen. For your safety and for the honor of the kingdom, I shall see the beast slain. The Frozen Peaks, the Swamplands, and the villagers of Klare will not stop me. I will come back safely.\n")
    Print("[Queen] Brave words, good knight, but strength alone will not defeat the dragon. You must use intelligence, patience, and follow your heart.\n[Queen] Go brave knight and may the gods be on your side ❤️\n")
    start_game = input("Press Enter to begin ")
    
    if start_game == '':
        print("\n-------------------------------------------------------------------------")
        Print("\nLoading enemy_data (enemy_stats)...")
        time.sleep(random.uniform(0.2, 1.9))
        Print("Loading player_data (player_stats)...")
        time.sleep(random.uniform(1.3, 3.5))
        Print("Loading random variables...")
        time.sleep(random.uniform(0.2, 0.5))
        Print("Loading random events...")
        time.sleep(random.uniform(1.1, 2.3))
        Print("Finishing up...")
        time.sleep(random.uniform(0.3, 0.7))
        Print("Loading Complete!")
        print("\n-------------------------------------------------------------------------")
    elif start_game == 'egg':
        pass
    else:
        print("\n-------------------------------------------------------------------------")
        Print("\nLoading enemy_data (enemy_stats)...")
        time.sleep(random.uniform(0.5, 1.7))
        Print("Loading player_data (player_stats)...")
        time.sleep(random.uniform(1.0, 2.1))
        Print("Loading random variables...")
        time.sleep(random.uniform(1.5, 2.5))
        Print("Loading random events...")
        time.sleep(random.uniform(1.5, 2))
        Print("Finishing up...")
        time.sleep(random.uniform(1.1, 3.0))
        Print("Loading Complete")
        print("\n-------------------------------------------------------------------------")

# Enemy Battle
def battle(player_data):
    if player_data['location'] == 'Forest':
        current_enemy = enemy_data_forest(player_data)
    elif player_data['location'] == 'Frozen Peaks':
        current_enemy = enemy_data_frozen_peaks(player_data)
    elif player_data['location'] == 'Swamplands':
        current_enemy = enemy_data_swamplands(player_data)
    else:
        pass

    Print("\n-----Enemy Battle-----")
    Print(f"While exploring around the trees you encountered a {current_enemy['name']}")

    if player_data['health'] > player_data['max_health']:
        player_data['health'] = player_data['max_health']
    true_damage = get_equipped_weapon_damage(player_data, weapons_data) + player_data['strength'] # Calculate player damage including their strength
    base_enemy_damage = max(0, current_enemy['strength'] - player_data['defence'])  # Calculate base enemy damage
    
    if settings['skip_battles'] == True:
        
        # Fight loop without text
        while player_data['health'] > 0 and current_enemy['health'] > 0:
            
            # Player Attacks
            player_damage = random.randint(max(1, true_damage - 3), true_damage + 5)
            crit_roll= random.randint(1, 100)
            # Checks for critical hit
            if crit_roll <= player_data['crit_chance']:
                player_damage = random.randint(max(1, true_damage - 3), true_damage + 5)
                player_damage *= 2
                
            current_enemy['health'] -= player_damage
            
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
            player_damage = random.randint(max(1, true_damage -3), true_damage + 5)
            crit_roll= random.randint(1, 100)
            # Checks for critical hit
            if crit_roll <= player_data['crit_chance']:
                player_damage *= 2
                Print("\nCritical Hit!")
                
            current_enemy['health'] -= player_damage
            Print(f"\nYou attacked the {current_enemy['name']} and dealt {player_damage} damage! Health remaining: {current_enemy['health']}")
            
            if current_enemy['health'] <= 0:
                Print(f"\nYou defeated the {current_enemy['name']}!")
                player_data['gold'] += current_enemy['gold']
                Print(f"You recieved {current_enemy['gold']} gold")
                break
            
            #Enemy Attacks
            enemy_damage = random.randint(max(1, current_enemy['strength'] - 3), current_enemy['strength'] + 5)

            player_data['health'] -= enemy_damage
            Print(f"The {current_enemy['name']} did {enemy_damage} damage! Health remaining: {player_data['health']}")
            check_death(player_data)
            
            time.sleep(1.4) # Delay Between attacks
            
        if player_data['health'] > 0:
            Print("\n[Knight] Ha! No enemy shall stop me from slaying the dragon!")

# Main game loop
def start_story(player_data, settings):
    Print("\n-----Main Game-----")
    Print("You leave the castle and head out to the forest and setup a camp")
    stat_display(player_data)
    global healed_today, fight_boss
    
    while True:
        if player_data['health'] > player_data['max_health']:
            player_data['health'] = player_data['max_health']
        print("\n[1] Explore\n[2] Rest\n[3] Check Stats\n[4] View Inventory\n[5] Settings\n[6] Help\n[7] Update log\n[8] Fight Zone Boss")
        action = input("Enter: ")
        
        if action == '1':
            # If the player is in the forest
            if player_data['location'] == 'Forest':
                explore_forest(player_data) 
                healed_today = False
            # If the player is in the frozen peaks        
            elif player_data['location'] == 'Frozen Peaks':
                explore_frozen_peaks(player_data)
                healed_today = False
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
                
        elif action == '3':
            # Display stats
            stat_display(player_data)
            
        elif action == '4':
            # Display inventory
            inventory_display(player_data, weapons_data)
            
        elif action == '5':
            # Display settings
            settings_display()
            
        elif action == '6':
            # Help menu
            Print("\n-----Help Menu-----")
            Print("\n[1] How to win\n[2] Progessing through levels\n[3] What are enchants?\n[4] Enchant list\n[5] How do I spend my gold?\n[6] Recommended stats for bosses")
            action = input("Enter: ")
            if action == '1':
                Print("\nTo win you must go through the 4 zones (forest, frozen peaks, swamplands and the town) then defeat the dragon")
            elif action == '2':
                Print("\nTo progress to the next area you must defeat the boss of the current area you are in")
            elif action == '3':
                Print("\nEnchants are applied to the current weapon you have equipped and are saved when swapping weapons")
            elif action == '4':
                Print("Strength 1 +15% Damage\nStrength 2 +45% Damage\nStrength 3 +100% Damage\nPrecision 1 +10% Crit Chance\nPrecision 2 +25% Crit Chance\nLife Steal 1 +5% Life Stolen\nLife Steal 2 +10% Life Stolen\nLife Steal 3 +15% Life Stolen")
            elif action == '5':
                Print("\nYou can spend gold at the merchant which has about a 20% chance of appearing each day")
            elif action == '6':
                true_damage = get_equipped_weapon_damage(player_data, weapons_data) + player_data['strength']
                Print(f"Your Health: {player_data['health']}, Your Damage: {true_damage}")
                Print("Howler: 180 Health 40 Damage\nBigfoot: 500 Health 80 Damage\nHeadwitch: 1200 Health 180 Damage\nBaron: 2000 Health 250 Damage\nDragon: ???")
                
        elif action == '7':
            # Update log
            Print("\n-----Previous Version: V3-----")
            Print("\n- Added the Frozen Peaks and Swamplands area")
            Print("- Added a Forest, Frozen Peaks and Swamplands boss")
            Print("- Added functionality to defence")
            Print("- Added critical hits")
            Print('- Added around 20 new events and removed the " You found nothing " (mostly) (for the forest area)')
            Print("- Added a game of 21 that you can vs a villagers in for gold (easily accessible in debug menu)")
            Print("- Added a simple game of higher or lower to bet gold on (easily accessible in debug menu)")
            Print("- Added Enchants... without the effects!!")
            print("\n-----Previous Version: V2-----")
            print("\n- Added a debugging menu")
            print("- Added a help menu")
            print("- Removed Levels")
            print("- Added wayyy more Forest enemies")
            print("- Balance changes")
            print("- More dialogue")
            print("- Changed starting prologue")
            print("- Added some more dividers between parts of the game")
            print("\n-------------------------------------------------------------------------")
            
        elif action == '8':
            
            fight_boss = True
            battle(player_data)
            fight_boss = False
            healed_today = False
            
        elif action == '9':
            
            # Debugging Menu
            if settings['debugging'] == 'True':
                print("\n---Debugging Menu---")
                action = input("[1] Change Player Stats\n[2] Minigames (WIP)\nEnter:")
                if action == '1':
                    action = input("\n[1] Set Max Health\n[2] Set Health\n[3] Set Strength\n[4] Set Defence\n[5] Set Gold\n[6] Set Location\n[7] Set Current Weapon\n[8] Roll Weapon Enchant\nEnter: ")
                    if action == '1':
                        player_data['max_health'] = int(input("Set Max Health: "))
                    elif action == '2':
                        player_data['health'] = int(input("Set Health: "))
                    elif action == '3':
                        player_data['strength'] = int(input("Set Strength: "))
                    elif action == '4':
                        player_data['defence'] = int(input("Set Defence: "))
                    elif action == '5':
                        player_data['gold'] = int(input("Set Gold: "))
                    elif action == '6':
                        player_data['location'] = input("Set Current Location: ")
                    elif action == '7':
                        new_weapon = input("Set Current Weapon: ")
                        player_data['weapon_equipped'] = new_weapon
                        player_data['owned_weapons'].append(new_weapon)
                    elif action == '8':
                        random_enchant(player_data, weapons_data)
                        
                elif action == '2':
                    action = input("\n[1] Play 21\n[2] Play Higher Or Lower\nEnter:")
                    if action == '1':
                        play_21()
                    elif action == '2':
                        play_higherlower(player_data)
            else:
              print("That is not a valid input")  
        else:
            print("That is not a valid input")

# Ending dialog      
def start_ending():
    Print("You made it back safely and won!")

# Checks if the player has died
def check_death(player_data):
    if player_data['health'] <= 0:
        game_over()
    else:
        pass

# If player dies
def game_over():
    Print("\nYou have unfortunately died, failing to slay the dragon and save the kingdom")
    action = input("Press 1 to Play Again (Possibly Broken idk) or press Enter to exit\nEnter: ")
    if action == '1':
        
        global fight_boss, fight_caveman, fight_campfire_bandit, fight_bandit_outpost, healed_today, viewed_map
        
        healed_today = True
        fight_boss = False
        fight_caveman = False
        fight_campfire_bandit = False
        fight_bandit_outpost = False
        viewed_map = False
        
        start_game()
        
    elif action == '':
        sys.exit()

start_game()