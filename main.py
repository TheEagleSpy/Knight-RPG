# Modules
import time
import random
import sys
import os
import traceback
from datetime import datetime

# Mechanics
from data_save_load import *
from inventory import *
from klare_villager_dialogue import talk_to_villagers, reset_villagers_talked
from updatelog import updatelog
from printdelay import Print, PRint
from tips import display_random_tip

# Minigames
from minigames.twentyone import play_21
from minigames.rps import play_rps
from minigames.higherlower import play_higherlower
from minigames.memory import play_memory
from minigames.liarsdice import play_liars_dice
from geniewish import geniewish

# Colours
RED = "\033[91m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
PURPLE = "\033[95m"
GOLD = "\033[33m"
SILVER = "\033[37m"
BLACK = "\033[30m"
RESET = "\033[0m"

LOG_FILE = "crash_log.txt"

current_slot = None

# Player Actions
healed_today = True
upgraded_armour = False

# Enemies

# -- Forest --
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

fight_boss = False
killed_baron = False
lost_to_baron = False

# -- Forest --
viewed_map = False
helped_bob = False
seen_bob = False
seen_bounty_hunter = False

# -- Frozen Peaks --
storm_power = 0
picked_events_left = 0
colours_left = 5
memory_sequence = []

# -- Village of Klare --
curent_hour = 0

# Makes the game run (dont touch)
def start_game():
    # Goes to next part of game one the previous is done
    start_prologue(settings)
    show_save_menu()
    start_story(player_data, settings, game_stats, klare_data)
    start_ending(player_data, game_stats)

# Player Stats
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
        "crit_chance": 9,
        "owned_weapons": ["Bronze Sword"],
        "owned_armour": ["No Armour"],
        "companions": 0,
        "slime_kingdom": False,
        "beaten_game": False,
        "debugging": False,
    }
    return player_data

# Sets up player data
player_data = main_player()

# Display player stats
def stat_display(player_data):
    os.system('cls') # Clear CMD
    if player_data['day'] == 14 and player_data['location'] == "Forest":
        Print("**At the end of this exploration is the Howler fight, use this day to heal, buy weapons and anything else**\n")
    if player_data['day'] == 29 and player_data['location'] == "Frozen Peaks":
        Print("**At the end of this exploration is the Bigfoot fight, use this day to heal, buy weapons and anything else**\n")
    elif player_data['day'] == 44 and player_data['location'] == "Village of Klare":
        Print("**When the bell rings at the end of this exploration you will fight the dragon, make sure to SPEND ALL YOUR GOLD on the merchant**\n")

    print("-----Character Stats-----")
    print(f"Health: {player_data['health']}/{player_data['max_health']}")
    print(f"Strength: {player_data['strength']}")
    print(f"Defence: {player_data['defence']}")
    print(f"Gold: {player_data['gold']}")
    print(f"Day: {player_data['day']}")
    print(f"Location: {player_data['location']}")
    print(f"Weapon: {player_data['weapon_equipped']}")
    print(f"Crit Chance: {player_data['crit_chance']}")
    print(f"Companions: {player_data['companions']}")
    print("\n-------------------------------------------------------------------------")

# Klare specific settings
def klare_data():
    klare_data = {
        "day_pass": False, # Single day pass
        "basic_pass": False, # Lifetime pass for basic area
        "premium_pass": False, # Lifetime pass for elite area

        "easy_beaten": [], # Name of each easy enemy beaten
        "medium_beaten": [], # Name of each medium enemy beaten
        "hard_beaten": [], # Name of each hard enemy beaten
    }
    return klare_data

klare_data = klare_data()

# Weapons Data
def weapons():
    weapons_data = [

        # Swords
        {"name": "Bronze Sword", "damage": 8, "crit_chance": 9, "special": "None"},
        {"name": "Shiny Sword", "damage": 16, "crit_chance": 9, "special": "None"},
        {"name": "Iron Sword", "damage": 17, "crit_chance": 14, "special": "None"},
        {"name": "Steel Sword", "damage": 35, "crit_chance": 23, "special": "None"},
        
        {"name": "Flame Sword", "damage": 63, "crit_chance": 28, "special": "None"},
        {"name": "Frost Sword", "damage": 85, "crit_chance": 11, "special": "None"},
        
        {"name": "Mythical Blade", "damage": 39, "crit_chance": 0, "special": "Strength 3"},
        {"name": "Shadow Blade", "damage": 125, "crit_chance": 25, "special": "Life Steal 1"},
        
        {"name": "Dragon Blade", "damage": 450, "crit_chance": 0, "special": "None"},

        # Bows
        {"name": "Hunting Bow", "damage": 16, "crit_chance": 5, "special": "None"},
        {"name": "Elven Bow", "damage": 22, "crit_chance": 11, "special": "None"},
        
        {"name": "Compound Bow", "damage": 58, "crit_chance": 17, "special": "None"},

        {"name": "Composite Bow", "damage": 70, "crit_chance": 15, "special": "None"},
        
        {"name": "Dragon Bow", "damage": 130, "crit_chance": 0, "special": "None"},

        # Spears    
        {"name": "Wooden Spear", "damage": 12, "crit_chance": 80, "special": "None"},

        {"name": "Eagle Spear", "damage": 45, "crit_chance": 80, "special": "None"},

        {"name": "Rock Spear", "damage": 70, "crit_chance": 80, "special": "None"},
        {"name": "Baron's Spear", "damage": 90, "crit_chance": 80, "special": "None"},
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
        {"name": "Titanium Armour", "defence": 26},

        {"name": "Adamantium Armour", "defence": 40},
        {"name": "Ash Armour", "defence": 44},
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
        "Life Steal 3": {"type": "lifesteal", "value": 25, "rarity": 0.1}
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
        print("\nThis weapon cannot be enchanted :(")

# Selects the random sword Enchant
def random_enchant(player_data, weapons_data):
    weapon = next((i for i in weapons_data if i['name'] == player_data['weapon_equipped']), None)
    if weapon:
        enchant_equipped_weapon(weapon)

# Variable containing all the game stats
game_stats = {
    "games_opened": 0,
    "times_rested": 0,
    "bosses_killed": 0,
    "enemies_killed": 0,
    "total_damage_dealt": 0,
    "gold_earned": 0,
    "critical_hits": 0,
    "battles_lost": 0,
    "days_survived": 0,
    "items_bought": 0,
    "times_dodged": 0,
    "health_potions_used": 0,
    "minigames_played": 0,
    "gambles_won": 0,
    "gambles_lost": 0,
    "good_events": 0,
    "bad_events": 0,
    }

# Variable containing all the achievements
achievements = {

    # Non cool achievements
    "Monster Slayer I": 0/50,
    "Monster Slayer II": 0/100,
    "Monster Slayer III": 0/200, # kill 200 enemies
    "Survivor I": 0/25,
    "Survivor II": 0/99, # survive 99 events
    "Health Hoarder": 0/300, # have 300 max health

    # do something cool for the achievement
    "Early Exit I": False, # leaving the forest early (before day 15)
    "Early Exit II": False, # leaving the frozen peaks early (before day 30)
    "Early Exit III": False, # leaving the village of klare early (before day 45)
    "Merchant Rock Paper Scissors": False, # typing rps into the merchant
    "Hey I found the castle": False, # bob coming back with reward from robbing the castle
    "I am #1": 0/20, # beating every enemy in Klare
    "Dragon Slayer": False, # killing the dragon
    "Bug Mode": False, # activate debug mode
    "You and what army?": 0/5, # have 5 companions at once in a single run
    "Hermit Listener": 0/2, # listen to both hermits entire story (forest and snow)
    "Sword Collector": 0/7, # Own every type of sword
    "Bow Collector": 0/4, # Own every type of bow
    "Spear Collector": 0/2, # Own every type of Spear
    "Ultimate Collecter": 0/13, # Own every weapon in the game at once
    "Money Saver": False, # Purchase from the blacksmith
    "Memory Master": False, # Win the memory game
    "Enchanted": False, # Enchanting a weapon for the first time
    "Dodged": False, # Dodge an attack
    "Light work": False, # Beat an enemy without taking damage
    "Free Health": False, # Health to full health from lifesteal
    "Villager Returned": False, # Return the villager to klare

    }

# Displays Settings    
def settings_display(settings):
    while True:
        os.system('cls')  # Clear CMD
        print("-----Settings-----")    
        print(f"[1] Skip Battles: {'True' if settings['skip_battles'] else 'False'}")
        print(f"[2] Skip Intro: {'True' if settings['skip_intro'] else 'False'}")
        print(f"[3] Press Enter After Events: {'True' if settings['enter_to_continue'] else 'False'}")
        print(f"[4] View Lifetime Stats")
        print("[r] Exit")

        try:
            settings_choice = input("\nEnter: ").lower()
            if settings_choice == '1':
                settings["skip_battles"] = not settings["skip_battles"]
            elif settings_choice == '2':
                settings["skip_intro"] = not settings["skip_intro"]
            elif settings_choice == '3':
                settings["enter_to_continue"] = not settings["enter_to_continue"]
            elif settings_choice == '4':
                view_game_stats(game_stats)
            elif settings_choice == 'r':
                print("\n-------------------------------------------------------------------------")
                break
            else:
                print("Please Enter a valid input")

            # Write updated global settings to main file only
            save_global_data(settings, game_stats)

        except ValueError:
            print("Please Enter a valid input")

# List of settings        
settings = {
    "skip_battles": False,
    "skip_intro": False,
    "enter_to_continue": True,
    }

# -- Save data stuff -- #

# Sets the game settings as the saved settings
settings, game_stats = load_global_data()
player_data, klare_data, world_state = {}, {}, {}

# Apply all world_state keys back into globals
apply_world_state_to_globals(world_state, globals())

# Pick and load slot
def show_save_menu():
    while True:
        os.system('cls')  # Clear CMD
        slots = list_save_slots()
        print("---- SAVE SLOTS ----")
        for s in slots:
            if s["exists"]:
                meta = s["meta"]
                print(f"[{s['slot']}] Day {meta.get('day', '?')} | "
                      f"Location: {meta.get('location', 'Forest')} | "
                      f"Last Load: {meta.get('last_played', 'N/A')}")
            else:
                print(f"[{s['slot']}] Empty Slot")
                
        print("[r] Exit Game")
        print("--------------------")


        choice = input("\nSelect slot (1–3) or 'r' to quit: ").strip().lower()

        if choice == "r":
            sys.exit()

        # enter debug slot
        if choice == "debug":
            return load_debug_slot_and_apply()

        try:
            slot_num = int(choice)
            if not (1 <= slot_num <= 3):
                print("Please enter 1-3")
                continue
        except ValueError:
            print("Please enter a valid input")
            continue

        if slot_actions_menu(slot_num):
            break

# Slot options
def slot_actions_menu(slot_num):
    os.system('cls')  # Clear CMD
    slots = list_save_slots()
    slot_info = next((s for s in slots if s["slot"] == slot_num), None)

    if not slot_info:
        print("Invalid slot.")
        return False

    exists = slot_info["exists"]
    print("---- SLOT MENU ----")
    if exists:
        meta = slot_info["meta"]
        print(f"Slot {slot_num}: Day {meta.get('day', '?')} | "
              f"{meta.get('location', 'Forest')} | "
              f"Last Played: {meta.get('last_played', 'N/A')}")
        print("--------------------")
        print("[1] Load Game")
        print("[2] Delete Save")
        print("[3] Back")
    else:
        print(f"Slot {slot_num}: Empty")
        print("--------------------")
        print("[1] New Game")
        print("[2] Back")

    action = input("Enter: ").strip().lower()

    if exists:
        if action == "1":
            return load_slot_and_apply(slot_num)  # Return True if loaded successfully
        elif action == "2":
            delete_game(slot_num)
        elif action == "3":
            return False
        else:
            print("Invalid option.")
    else:
        if action == "1":
            new_game(slot_num)
            return load_slot_and_apply(slot_num)
        elif action == "2":
            return False
        else:
            print("Invalid option.")
    return False

# Creates a new save
def new_game(slot_num):
    global current_slot, player_data, klare_data, world_state
    current_slot = slot_num

    # Load fresh default values for a new save
    defaults = get_default_values()
    player_data = defaults["player_data"].copy()
    klare_data = defaults["klare_data"].copy()
    world_state = defaults["world_state"].copy()

    # Save both global and slot data
    save_slot(current_slot, player_data, klare_data, weapons_data, armour_data, world_state)
    save_global_data(settings, game_stats)

    print(f"\nNew game created in slot {current_slot}.")

# Loads save and starts game
def load_slot_and_apply(slot_num):
    global current_slot, player_data, klare_data, world_state, weapons_data, armour_data
    current_slot = slot_num

    data = load_slot(slot_num)
    if not data:
        print("No save found or save file is corrupted.")
        return False

    player_data = data["player_data"]
    klare_data = data["klare_data"]
    weapons_data = data["weapons_data"]
    armour_data = data["armour_data"]
    world_state = data["world_state"]

    apply_world_state_to_globals(world_state, globals())
    return True

# Loads debug save and starts game
def load_debug_slot_and_apply():
    global current_slot, player_data, klare_data, world_state, weapons_data, armour_data
    current_slot = "debug"

    defaults = get_default_values()
    path = get_slot_path("debug")

    if not os.path.exists(path):
        player_data = defaults["player_data"].copy()
        klare_data = defaults["klare_data"].copy()
        weapons_data = defaults["weapons_data"].copy()
        armour_data = defaults["armour_data"].copy()
        world_state = defaults["world_state"].copy()

        player_data["debugging"] = True
        player_data["slime_kingdom"] = True

        save_slot("debug", player_data, klare_data, weapons_data, armour_data, world_state)
        print("\nNew debug slot created.")
    else:
        data = load_slot("debug")
        if not data:
            print("Debug save corrupted, recreating.")
            return load_debug_slot_and_apply()

        player_data = data["player_data"]
        klare_data = data["klare_data"]
        weapons_data = data["weapons_data"]
        armour_data = data["armour_data"]
        world_state = data["world_state"]
        player_data["debugging"] = True

        print("\nLoaded existing debug slot.")

    apply_world_state_to_globals(world_state, globals())
    return True

# Deletes selected save
def delete_game(slot_num):
    os.system('cls')  # Clear CMD
    confirm = input(f"Confirm delete slot {slot_num}? \n[1] Yes\n[2] No\nEnter: ").lower()
    if confirm == "1":
        delete_slot(slot_num)
        print(f"Slot {slot_num} deleted.")
    else:
        print("Delete cancelled.")

# -- Helper Functions -- #

# Uses a health potion if allowed
def use_health_potion(player_data, game_stats):
    possible_health = player_data['max_health'] - player_data['health'] 
    if player_data['location'] == 'Forest':
        health_potion = 50
        if player_data['health'] < player_data['max_health']:
            healed = min(health_potion, possible_health)
            player_data['health'] += healed
            Print(f"You drank the potion and gained {healed} Health")

            game_stats['health_potions_used'] += 1

        else:
            Print("You're already at full health.")

    elif player_data['location'] == 'Frozen Peaks':
        health_potion = 75
        if player_data['health'] < player_data['max_health']:
            healed = min(health_potion, possible_health)
            player_data['health'] += healed
            Print(f"You drank the potion and gained {healed} Health")

            game_stats['health_potions_used'] += 1

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
    effect_type = random.choice(["increase", "decrease"])  # Randomly decide if the effect is positive or negative
    if player_data['location'] == "Forest":
        stat = random.choice(["max_health", "health", "gold"])  # Randomly choose a stat
        amount = random.randint(1, 3)  # Random effect amount
    else:
        stat = random.choice(["max_health", "health", "gold", "crit_chance", "defence"])  # Randomly choose a stat
        if stat == "defence":
            amount = 1
        else:
            amount = random.randint(2, 7)  # Random effect amount for other locations and effects
    
    # Apply effect
    if effect_type == "increase":
        player_data[stat] += amount
        return f"increases your {stat.replace('_', ' ')} by {amount}!"
    else:
        player_data[stat] -= amount
        check_death(player_data, game_stats)
        return f"decreases your {stat.replace('_', ' ')} by {amount}."

# Function to get weapon by name
def get_weapon_by_name(name):
    for weapon in weapons_data:
        if weapon['name'] == name:
            return weapon
    return None

# Function to get armour by name
def get_armour_by_name(name):
    for armour in armour_data:
        if armour['name'] == name:
            return armour
    return None

# Slime Kingdom with blacksmith and shop
def slime_kingdom(player_data):
    os.system('cls')
    Print("You head towards the slime kingdom")
    while True:
        action = input("\n---Slime Kingdom---\n[1] Merchant\n[2] Forest Blacksmith\n[r] Leave\nEnter: ")
        if action == '1':
            if player_data['location'] == 'Forest':
                forest_merchant(player_data, game_stats, weapons_data, armour_data)
            elif player_data['location'] == 'Frozen Peaks':
                frozen_peaks_merchant(player_data, game_stats, weapons_data, armour_data)
        elif action == '2':
            forest_blacksmith(player_data, weapons_data, armour_data, game_stats)
        elif action == 'r':
            break
        else:
            Print("Please Enter a valid input")

# For the gold earned stat
def track_gold_earned(player_data, before_gold, game_stats):
    after_gold = player_data['gold']
    delta = after_gold - before_gold

    # Only track positive gains
    if delta > 0:
        game_stats['gold_earned'] += delta

# idk
def advance_time(current_hour, current_minute, minutes):
    current_minute += minutes
    while current_minute >= 60:
        current_minute -= 60
        current_hour += 1
    return current_hour, current_minute

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
    giant_orc = {"name": "Giant Orc", "health": 65, "strength": 15, "gold": 50}
    metal_skeleton = {"name": "Metal Skeleton", "health": 60, "strength": 15, "gold": 60}
    strong_bandit = {"name": "Strong Bandit", "health": 100, "strength": 13, "gold": 85}
    distorted_figure = {"name": "Distorted Figure", "health": 40, "strength": 30, "gold": 65}
    # Boss
    howler = {"name": "Howler", "health": 300, "strength": 25, "gold": 300}
    # Exploration enemies
    caveman = {"name": "Cave Man", "health": 30, "strength": 8, "gold": 40}
    campfire_bandit = {"name": "Bandit", "health": 40, "strength": 7, "gold": 30}
    ghost = {"name": "Ghost", "health": 50, "strength": 8, "gold": 0}
    merchant = {"name": "Merchant", "health": 100, "strength": 3, "gold": 125}
    black_knight = {"name": "Black Knight", "health": 120, "strength": 11, "gold": 0}
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
def explore_forest(player_data, weapons_data, game_stats):
    global viewed_map,fight_boss, fight_caveman, fight_campfire_bandit, fight_ghost, helped_bob, seen_bob, seen_bounty_hunter, upgraded_armour, fight_merchant, fight_black_knight, fight_endless_road_skeleton, fight_bandit_leader, fight_villager
    exploration_time = random.randint(3, 6) # How many events the player will encounter
    
    while True:
        if exploration_time > 0:

            before_gold = player_data['gold']

            if player_data['debugging'] == False:
                exploration = random.random()

            else:
                try:
                    exploration = float(input("0 Exploration, 0.6 Shrine, 0.7 Trap, 0.95 Enemy, 1 Merchant\nExploration value: "))
                except ValueError:
                    exploration = random.random()
                    
            if player_data['day'] == 5 and exploration_time == 3:
                exploration = 1

            elif player_data['day'] == 11 and exploration_time == 3:
                exploration = 1

            elif player_data['day'] == 14 and exploration_time == 1:
                exploration = 1

            # Main Exploration
            if exploration <= 0.50:
                
                Print(f"\n{GREEN}-----Wilderness Exploration-----{RESET}")
                if player_data['debugging'] == False:
                    random_event = random.random()
                    
                else: # if player enables debug they can change the event
                    try:
                        print("0.05 Cave, 0.10 House, 0.15 Sunny Field, 0.20 Elf, 0.25 Campsite, 0.30 Animal Attack, 0.35 Strength Plant, 0.40 Lost Villager, 0.45 Endless Road, 0.50 Bandit Outpost")
                        print("0.55 Catapiller Queen, 0.60 Encounter Bob, 0.65 Bounty Hunters, 0.70 Dark Witch, 0.75 Friendly Enemy, 0.80 Gotten Lost, 0.85 Berries, 0.90 Slime Kingdom, 0.95 Blacksmith, 1 Stuck Sword")
                        random_event = float(input("Exploration value: "))
                    except ValueError:
                        random_event = random.random()
                        
                if random_event <= 0.05: # Cave event
                    Print("You find a cave that looks lived in...\n\n[Knight] I hope they aren't nearby")
                    time.sleep(1)
                    cave_event = random.random()
                    
                    if cave_event <= 0.25:
                        Print("[Knight] Eww it stinks in here, wait, is that?")
                        time.sleep(2)
                        Print("\nYou see a half eaten human corspe and leave immediately")
                        
                    elif cave_event <= 0.50:
                        while True:
                            action = input("\nYou find a potion on the table\n\n[1] Drink\n[2] Leave\nEnter: ")
                            
                            if action == '1':
                                Print("\n[Knight] Ooh a weird potion, I shall drink it!")
                                time.sleep(2)
                                potion_effect = random.random()
                                
                                if potion_effect <= 0.15:
                                    Print("[Knight] I don feel so goo-")
                                    Print("\nYou pass out...")
                                    time.sleep(2)
                                    Print("\n[Goblin] Haha your gold is now mine")
                                    Print(f"-{player_data['gold']} Gold")
                                    player_data['gold'] = 0

                                    # Increase stat of bad events by 1
                                    game_stats['bad_events'] += 1 
                                    
                                elif potion_effect <= 0.50:
                                    Print("[Knight] This tastes interesting")
                                    Print("\nYou suddenly feel warm...")
                                    time.sleep(2)
                                    Print("+30 Health")
                                    player_data['health'] += 30

                                    # Increase stat of good events by 1
                                    game_stats['good_events'] += 1
                                    
                                elif potion_effect <= 0.75:
                                    Print("[Knight] Give me another! This is tastes awesome!\n+20 Max Health\n+50 Health")
                                    player_data['max_health'] += 20
                                    player_data['health'] += 50
                                    
                                    # Increase stat of good events by 1
                                    game_stats['good_events'] += 1

                                else:
                                    Print("[Knight] I sure do love me some water")
                                    Print("\n+10 Health")
                                    player_data['health'] += 10

                                    # Increase stat of good events by 1
                                    game_stats['good_events'] += 1

                                break           
                            elif action == '2':
                                Print("You break the potion on the floor and leave the house before anything weird happens")
                                break
                            else:
                                Print("Please Enter a valid input")
                                
                    elif cave_event <= 0.75:
                        Print("\nYou checked every corner and found nothing")
                        Print("\n[Knight] Well that was a waste of time")
                        
                    else:
                        Print("\nYou checked every corner and found nothing")
                        Print("You leave...")
                        time.sleep(2)
                        Print("\n[Knight] Gah! Who are you?")
                        fight_caveman = True
                        battle(player_data, game_stats)
                        fight_caveman = False

                        # Increase stat of bad events by 1
                        game_stats['bad_events'] += 1 
                        
                elif random_event <= 0.10: # House Event
                    Print("You stumble into a run down wooden house among the trees")
                    
                    while True:
                        action = input("\n[Knight] This doesn't look dangerous at all\n\n[1] Investigate\n[2] Leave\nEnter: ")
                        if action == '1':
                            
                            house_event = random.random()
                            
                            if house_event <= 0.25:
                                Print("\nYou see a ghost and it starts swinging at you")
                                fight_ghost = True
                                battle(player_data, game_stats)
                                fight_ghost = False

                                # Increase stat of bad events by 1
                                game_stats['bad_events'] += 1 
                                
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
                                        check_death(player_data, game_stats)
                                        Print(f"+{chest_reward} Gold!")
                                        player_data['gold'] += chest_reward

                                        # Increase stat of good events by 1
                                        game_stats['good_events'] += 1

                                    elif action == '2':
                                        Print("You continue looking and find nothing so you leave")
                                    else:
                                        Print("\nPlease Enter a valid input")
                                    break
                                elif house_luck <= 0.66:
                                    Print(f"\nAfter checking the downstairs you head into the attic finding a mysterious book. You open it and in a sudden flash of light it takes the {player_data['weapon_equipped']} out of your hand and enchants it:") # NOT FINISHED
                                    random_enchant(player_data, weapons_data)

                                    # Increase stat of good events by 1
                                    game_stats['good_events'] += 1

                                else:
                                    Print("Suddenly you fall into the floor getting your foot stuck\n-5 Health")
                                    player_data['health'] -= 5
                                    check_death(player_data, game_stats)

                                    # Increase stat of bad events by 1
                                    game_stats['bad_events'] += 1
                            
                            else:
                                Print("\nYou find armour plating\n+2 Armour Defence")
                                for armour in armour_data:
                                    if armour['name'] == player_data['armour_equipped']:
                                        armour['defence'] += 2
                                        player_data['defence'] += 2
                                
                                # Increase stat of good events by 1
                                game_stats['good_events'] += 1

                            break
                        
                        elif action == '2':
                            Print("You leave the house safely")
                            break
                    
                elif random_event <= 0.15: # Plant Event
                    Print("You come across a flower field and the sun starts shining\n+5 Max Health\n+10 Health\n+1 Strength\n+1 Weapon Damage\n+1 Armour Defence\n+20 Gold")
                    player_data['max_health'] += 5
                    player_data['health'] += 10
                    player_data['gold'] += 20
                    Print("\n[Knight] It's a good day today")
                    if player_data['health'] > 0:
                        for armour in armour_data:
                            if armour['name'] == player_data['armour_equipped']:
                                armour['defence'] += 1
                                player_data['defence'] += 1
                    
                    elif player_data['health'] > 0:
                        for weapon in weapons_data:
                            if weapon['name'] == player_data['weapon_equipped']:
                                weapon['damage'] += 1
                    
                    # Increase stat of good events by 1
                    game_stats['good_events'] += 1

                
                elif random_event <= 0.20: # Elf Event
                    Print("You walk into a mystical clearing filled with crystals and tall flowers surrounding it")
                    Print("\n[Kind Elf] Welcome...")
                    time.sleep(1.5)
                    Print("[Kind Elf] I see you struggling and I wish to grant you something of your choosing\n")
                    time.sleep(1.5)
                    elf_luck = random.random()
                    if elf_luck <= 0.33:
                        while True:
                            action = input(f"[1] Double your current Gold, Current Gold: {player_data['gold']}\n[2] Free Elven Bow\n[3] +50 Max Health\nEnter: ")
                            if action == '1':
                                player_data['gold'] *= 2
                                Print(f"\n[Kind Elf] Your wish has been granted you now have: {player_data['gold']} Gold!")
                                break
                            elif action == '2':
                                player_data['owned_weapons'].append("Elven Bow")
                                Print("\n[Kind Elf] May it serve you well")
                                break

                            elif action == '3':
                                player_data['max_health'] += 50
                                player_data['health'] += 50
                                Print("\n[Kind Elf] You are now stronger than ever, go complete your quest\n+50 Max Health")
                                break

                            else:
                                Print("\nPlease Enter a valid input")
                            
                    elif elf_luck <= 0.66:

                        while True:
                            action = input("[1] Random Enchantment\n[2] Free Steel Sword\n[3] 60% Crit rate with current weapon\nEnter: ")
                            if action == '1':
                                random_enchant(player_data, weapons_data)
                                break

                            elif action == '2':
                                player_data['owned_weapons'].append("Steel Sword")
                                Print("\n[Kind Elf] Well, here is your new ☆ Steel Sword ☆... Enjoy")
                                break

                            elif action == '3':
                                Print("\n[Kind Elf] Now you can deal more damage more often!")

                                # Find equipped weapon
                                equipped_weapon = None
                                for w in weapons_data:
                                    if w["name"] == player_data["weapon_equipped"]:
                                        equipped_weapon = w
                                        break

                                if equipped_weapon:
                                    # Apply crit buff to the weapon itself
                                    equipped_weapon["crit_chance"] = 60

                                    # Re-equip to recalc crit correctly via your existing function
                                    view_weapon_stats(player_data, equipped_weapon, weapons_data)

                                break


                    else:
                        while True:
                            action = input(f"[1] +3 Weapon Damage\n[2] +125 Gold\n[3] Set Max Health between 75 and 165\nEnter: ")
                            if action == '1':
                                Print("\nYour Sword's blade shines against the sun\n+3 Weapon Damage")
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
                                Print("\nPlease Enter a valid input")   

                    # Increase stat of good events by 1
                    game_stats['good_events'] += 1         

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

                                # Increase stat of good events by 1
                                game_stats['good_events'] += 1
                                
                            elif campsite_event < 0.7:
                                for armour in armour_data:
                                    if armour['name'] == player_data['armour_equipped']:
                                        Print("You found an old piece of wood that you stick to your armour for extra defence\n+1 Armour Defence")
                                        armour['defence'] += 1
                                        player_data['defence'] += 1
                                        break

                                # Increase stat of good events by 1
                                game_stats['good_events'] += 1
                                
                            else:
                                old_health = player_data['health']
                                player_data['health'] -= random.randint(5, 15)
                                new_health = old_health - player_data['health']
                                Print(f"While searching, you disturbed a snake and got bitten!\n-{new_health} Health")
                                check_death(player_data, game_stats)

                                # Increase stat of bad events by 1
                                game_stats['bad_events'] += 1 

                            break   

                        elif action == "2":
                            Print("\nYou decide to rest at the campsite.\n")
                            campsite_event = random.random()

                            if campsite_event < 0.5:
                                Print("After a long rest your health is restored to max")
                                player_data['health'] = player_data['max_health']

                                # Increase stat of good events by 1
                                game_stats['good_events'] += 1
                                
                            else:
                                fight_campfire_bandit = True
                                Print("You were attacked by bandits during your rest.")
                                battle(player_data, game_stats)
                                fight_campfire_bandit = False

                                # Increase stat of bad events by 1
                                game_stats['bad_events'] += 1 

                            break
                        
                        elif action == "3":
                            Print("\nYou decide to leave the campsite alone. Better safe than sorry.")
                            
                            break
                        else:
                            Print("Please Enter a valid input")
                elif random_event <= 0.30: # Animal Attack
                    Print("A wild animal attacks you unexpectedly!")

                    if player_data['defence'] >= 4:
                        Print("Luckily your armour blocks the attack and you kill it")

                    else:
                        Print("It does 15 Damage!")
                        player_data['health'] -= 15
                        check_death(player_data, game_stats)
                        Print("\nHowever you manage to kill it before it does anything else")

                        # Increase stat of bad events by 1
                        game_stats['bad_events'] += 1 

                elif random_event <= 0.35: # Edible Plants Event
                    Print("You found a rare edible plant and decide to eat it")
                    Print("+2 Strength")
                    player_data['strength'] += 2

                    # Increase stat of good events by 1
                    game_stats['good_events'] += 1
                    

                elif random_event <= 0.40: # Lost Villager
                    Print("You encounter a lost looking villager on the side of the path")

                    while True:
                        action = input("\n[Knight] Should I go and investigate?\n\n[1] Walk up to him\n[2] Turn and walk the other way\nEnter: ")

                        if action == "1":
                            Print("\nYou cautiously approach the villager, who notices you and looks relieved.")
                            Print("\n[Villager] Oh, thank the heavens! I’ve been wandering for hours...")
                            choice = input("\n[1] Help out\n[2] Rob\nEnter: ")

                            if choice == "1":
                                Print("\n[Knight] What happened to you?")
                                Print("\n[Villager] My village was raided by bandits, and I got separated from my family...")
                                time.sleep(1.5)
                                outcome = random.random()

                                if outcome < 0.3:
                                    Print("\nThe villager bursts into tears and hands you a family heirloom, insisting you keep it for protection.\n+2 Defence")
                                    player_data['defence'] += 2
                                elif outcome < 0.6:
                                    Print("\nThe villager gives you some money and says to meet him back here if you ever find his family.\n+45 Gold")
                                    player_data['gold'] += 45
                                else:
                                    Print("[Villager] May I please come with you on your adventure as word is that you are going to travel through the village or Klare.")
                                    Print("\n[Knight] Yes, you may... as long as you help me")
                                    Print("\n[Villager] I promise to, good knight")
                                    player_data['companions'] += 1
                                
                                # Increase stat of good events by 1
                                game_stats['good_events'] += 1

                                break
                            elif choice == '2':
                                Print("\n[Knight] Give me all your money!")
                                Print("\n[Villager] No please, I have just lost my family as my village was raided by bandits")
                                Print("\n[Knight] Well that sounds unfortunate")
                                Print("[Knight] I'll just take this and be on my way\n+25 Gold\n\nYou found a defence charm\n+2 Defence")
                                player_data['defence'] += 2
                                player_data['gold'] += 25
                                Print("\n[Villager] No you wont! 😭")
                                fight_villager = True
                                battle(player_data, game_stats)
                                fight_villager = False

                                # Increase stat of bad events by 1
                                game_stats['bad_events'] += 1 

                                break
                            else:
                                Print("\nPlease Enter a valid input")

                        elif action == '2':
                            Print("\nYou head the other way as he aimlessly stumbles around")
                            break

                        else:
                            Print("\nPlease Enter a valid input")
                        
                elif random_event <= 0.45: # Endless Road Event
                    
                    escape_chance = 0  # Initial escape chance percentage
                    

                    Print("Welcome to the Endless Road! Can you find your way out?")
                    while True:

                        # Set escape chance to 100 if its over 100
                        if escape_chance > 100:
                            escape_chance = 100

                        # Escape once escape chance hits 100
                        Print(f"\n---You are currently {escape_chance}% of the way escaped from the road---")
                        print(f"--You have {player_data['health']} Health Left--\n")
                        if escape_chance >= 100:
                            Print("You found the way out! Congratulations!\n+125 Gold")
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
                                        Print("\nAfter following the directions on the map you make your way off the road!")
                                        escape_chance = 100     
                                    Print("\nYou encounter a strange glowing crystal. It hums with energy.\n+1 Strength\n-1 Armour Defence")
                                    player_data['strength'] += 1
                                    for armour in armour_data:
                                        if armour['name'] == player_data['armour_equipped']:
                                            armour['defence'] -= 1
                                            player_data['defence'] -= 1
                                    escape_chance += 5
                                    break

                                elif action == '2':
                                    Print("\nA dense fog surrounds you, and you hear whispers from all around.\n-5 Health")
                                    player_data['health'] -= 5
                                    check_death(player_data, game_stats)
                                    break

                                elif action == '3':
                                    random_event = random.random()
                                    
                                    if random_event <= 0.10:
                                        Print("\nYou fall into a hole with a clock which takes you back to Day 1 with all your stats and past decisions with extra defence and strength\nDay = 1\n+3 Strength\n+3 Defence")
                                        time.sleep(2)
                                        player_data['day'] = 1
                                        exploration_time = 0
                                        player_data['defence'] += 3
                                        player_data['strength'] += 3
                                        escape_chance = 100
                                        player_data['health'] += 10
                                    
                                    elif random_event <= 0.35:
                                        Print("\nYou Brush past the bushes and find...")
                                        time.sleep(2)
                                        Print("Absolutely nothing")
                                        
                                    elif random_event:
                                        Print("\nYou Brush past the bushes and find...")
                                        time.sleep(2)
                                        Print("A skeleton that gets up and attacks you!")
                                        fight_endless_road_skeleton = True
                                        battle(player_data, game_stats) 
                                        fight_endless_road_skeleton = False
                                        check_death(player_data, game_stats)
                                    break
                                else:
                                    Print("\nYou are unsure, so you spin in a circle and walk forward")
                                    action = random.randint(1,3)

                        elif road_luck <= 0.25:  # Abandoned Camp
                            Print("You stumble across an abandoned campsite.")
                            while True:
                                action = input("What do you do?\n\n[1] Search the camp\n[2] Move on\nEnter: ")
                                if action == '1':
                                    Print("\nYou find some food on the campfire, but the air feels ominous.")
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
                                action = input("What do you do?\n\n[1] Hear his story (1~ minute)\n[2] Skip the story\n[3] Ignore him\nEnter: ")
                                if action == '1':
                                    PRint("\n[Hermit] Another wanderer, lost in the endless road. Sit. Listen.")
                                    time.sleep(2)
                                    PRint("\n[Knight] What is it you want, hermit?")
                                    time.sleep(2)
                                    PRint("\n[Hermit] I once walked as you do, blade in hand, fire in my heart. Until... I hunted the Howler.")
                                    PRint("\n[Knight] The Howler? That's just a myth.")
                                    time.sleep(1)
                                    PRint("\n[Hermit] That's what I thought... until I heard it's cry in the dead of night. A sound that tears through you, a wail that breaks the mind. And then I saw it.")
                                    time.sleep(7)
                                    PRint("\nThe Hermit's voice breaks, his eyes hollow as if reliving the moment.\n")
                                    time.sleep(3)
                                    PRint("[Hermit] A beast born from nightmares. Eyes like burning coals. A mouth that stretched too wide, too many teeth. Its flesh swallowed my arrows, its skin turned my sword to dust.")
                                    PRint("\n[Knight] And how are you here talking to me?")
                                    PRint("\n[Hermit] I learned it's secret. It fears itself. The reflection turns it's power inward, shattering its form like brittle glass.")
                                    time.sleep(8)
                                    PRint("\nA gust of wind runs through the ruins around you. The fire crackles, and shadows quickly move along the hermit's face.\n")
                                    time.sleep(3)
                                    PRint("[Knight] So you defeated it?")
                                    PRint("\n[Hermit] No such victory is ever so easy. I lured it to the stillest pool I could find. It peered into the water, and for the first time, it saw itself. The scream it unleashed—")
                                    time.sleep(2)
                                    PRint("\nThe Hermit grips his sword, knuckles white. His breath turns shallow.\n")
                                    time.sleep(2)
                                    PRint("[Hermit] It was not pain. It was recognition. It saw what it was. What it had become. And for a single, trembling second, it hesitated.")
                                    PRint("\n[Knight] And you struck.")
                                    PRint("\n[Hermit] I plunged the remaining of my blade into it's heart... I felt it die by my hands. And yet…")
                                    time.sleep(4)
                                    PRint("\nThe fire dims.\n")
                                    time.sleep(2)
                                    PRint("[Knight] Yet what?")
                                    PRint("\n[Hermit] I'm here... I have tried to leave, countless times. But the Howler was no ordinary beast. When I killed it, something took it's place.")
                                    time.sleep(4)
                                    PRint("\n[Knight] What do you mean?")
                                    PRint("\n[Hermit] The Howler is not a creature. It is a curse. A hunter must always remain. It watches, waits, and when the path is dark… it returns.")
                                    time.sleep(3)
                                    PRint("\n[Knight] Are you saying—")
                                    PRint("\n[Hermit] One day, you too may hear it's cry. When you do, pray you are ready.")
                                    time.sleep(4)
                                    PRint("\nThe Hermit's eyes fill with something unspoken. A weight settles in your chest, but also a fire.")
                            
                                    Print("\n+1 Strength\n+10 Max Health\n+20 Health")
                                    player_data['strength'] += 1
                                    player_data['max_health'] += 10
                                    player_data['health'] += 20
                                    escape_chance += 5
                                    break

                                elif action == '2':
                                    Print("\nThe hermit starts yapping and you zone out to think about your quest.")
                                    Print("After you zone back in, you thank the hermit for the story and leave, fired up for the journey ahead.")

                                    Print("\n+1 Strength\n+10 Max Health\n+20 Health")
                                    player_data['strength'] += 1
                                    player_data['max_health'] += 10
                                    player_data['health'] += 20
                                    escape_chance += 5
                                    break

                                elif action == '3':
                                    Print("The hermit slowly shakes his head as you walk away.")
                                    escape_chance += 10
                                    break

                                else:
                                    Print("Please Enter a valid input")

                        elif road_luck <= 0.45: # Storm
                            Print("A sudden storm rages around you, making it hard to see.")
                            while True:
                                action = input("What do you do?\n\n[1] Wait for the storm to pass\n[2] Push on\nEnter: ")
                                if action == '1':
                                    Print("\nThe storm passes, but you feel like you lost precious time.")
                                    escape_chance -= 5
                                    break
                                elif action == '2':
                                    Print("\nYou brave the storm but emerge exhausted and injured.\n-5 Max Health\n-5 Health")
                                    player_data['max_health'] -= 5
                                    player_data['health'] -= 5
                                    escape_chance += 10
                                    check_death(player_data, game_stats)
                                    break
                                else:
                                    Print("Please Enter a valid input")
                                
                                
                        elif road_luck <= 0.60:  # River Event
                            Print("You hear a distant sound of rushing water.")
                            while True:
                                action = input("What do you do?\n\n[1] Investigate\n[2] Stay on the path\nEnter: ")
                                if action == '1':
                                    Print("\nYou discover a river that seems to block your path.")
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
                                    Print("Please Enter a valid input")
                                check_death(player_data, game_stats)

                        elif road_luck <= 0.75: # Find map
                            Print("You find an old map on the ground.")
                            while True:
                                action = input("What do you do?\n\n[1] Study the map\n[2] Leave it\nEnter: ")
                                if action == '1':
                                    Print("\nYou stare at the blank paper for a while, after turning it over it says 'Right is for the weak, Left is for the Strong and if you go straight you might run into a bomb'")
                                    viewed_map = True
                                    break
                                elif action == '2':
                                    Print("\nYou ignore the map and continue on.")
                                    escape_chance += 15
                                    break
                                else:
                                    Print("Please Enter a valid input")
                        elif road_luck >= 0.90:  # Lost Villager Event
                            Print("A strange shadow follows you silently.")
                            while True:
                                action = input("What do you do?\n\n[1] Confront it\n[2] Ignore it\nEnter: ")
                                if action == '1':
                                    villager_event = random.randint(1, 3)
                                    if villager_event == 1:
                                        Print("\nThe shadow reveals itself to be a lost villager who is grateful for your help.")
                                        Print("They hand you a small bag of gold.\n+50 Gold")
                                        player_data['gold'] += 50
                                    elif villager_event == 2:
                                        Print("\nThe person begs for food. You give them a berry you found, and they give you a map in return. That tells you to go left")
                                        viewed_map = True
                                    elif villager_event == 3:
                                        Print("\nAs you step closer, the shadow lunges at you! It's a bandit!\n-10 Health")
                                        player_data['health'] -= 10
                                    check_death(player_data, game_stats)
                                    break
                                elif action == '2':
                                    Print("The shadow fades into the darkness.")
                                    break
                                else:
                                    Print("Please Enter a valid input")
                        else:
                            Print("You come across a tower and decide to climb it allowing you to see most of the way to the exit")
                            escape_chance += 35
                            
                        escape_chance += 5

                        if escape_chance < 100:
                            player_data['health'] -= 10
                            Print("\nYou lose 10 Health due to starvation")
                            check_death(player_data, game_stats)

                    # Increase stat of bad events by 1
                    game_stats['bad_events'] += 1 

                elif random_event <= 0.50: # Bandit camp with 4 enemies
                    while True:
                        action = input("You come across a bandit outpost with a bunch of enemies! (VERY HARD) Do you wish to enter?\n\n[1] Enter\n[2] Walk around it and continue on\nEnter: ")
                        if action == '1':
                            global fight_bandit_outpost
                            fight_bandit_outpost = True
                            battle(player_data, game_stats)
                            battle(player_data, game_stats)
                            battle(player_data, game_stats)
                            battle(player_data, game_stats)
                            fight_bandit_outpost = False
                            
                            Print("\nYou make your way to their treasure...")
                            time.sleep(2)
                            treasure = random.random()

                            # Increase stat of good events by 1
                            game_stats['good_events'] += 1
                            
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
                                PRint("You open the chest to find a bunch of junk...\n\n-----Items-----\nJunk\nJunk\nJunk\nYou found a health potion!\n+1 Health Potion\nJunk\nYou found a Forest Orb!\n+100 Gold")
                                Print("\n[Knight] Ooh a Forest Orb")
                                Print("The Forest Orb merges with your armour and sword\n+4 Armour Defence\n-1 Sword Damage")
                                player_data['gold'] += 100
                                for armour in armour_data:
                                    if armour['name'] == player_data['armour_equipped']:
                                        armour['defence'] += 4
                                        player_data['defence'] += 4

                                for weapon in weapons_data:
                                    if weapon['name'] == player_data['weapon_equipped']:
                                        weapon['damage'] -= 1
                                        break
                          
                            else:
                                Print(f"As you get closer to the treasure, your {player_data['weapon_equipped']} begins to glow\n\n-----Items-----\nEnchanted book!!!")
                                random_enchant(player_data, weapons_data)

                            break

                        elif action == '2':
                            Print("\nYou walk around the bandit outpost and continue on")
                            break

                        else:
                            Print("Please Enter a valid input")
                        
                elif random_event <= 0.55: # Encounter caterpillar princess
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
                        "[Knight] It is an honour to meet you, Princess. Your forest is truly enchanting.",
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
                        {"item": "Armour Plate", "description": "Gives armour Defence."},
                        {"item": "Potion of Strength", "description": "A potion that will make you bigger and stronger"},
                        {"item": "Caterpillar Charm", "description": "A charm said to allow you to hit critical hits more often."},
                        {"item": "Forest Jewel", "description": "A gem that massively increases Max Health"}
                    ]
                    
                    # Randomly select discovery dialogue
                    Print(random.choice(discovery_dialogues))
                    time.sleep(2)
                    # Randomly select greeting
                    Print("\n" + random.choice(greetings))
                    time.sleep(2)
                    # Randomly select knight's response
                    Print("\n" + random.choice(knight_responses))
                    time.sleep(2)
                    # Randomly select second dialogue
                    Print("\n" + random.choice(second_dialogues))
                    time.sleep(2)
                    Print("[Caterpillar Princess] I know of your journey to fight the dragon, I also know that you arent currently strong enough to beat him yet, so take this:")
                    reward = random.choice(rewards)
                    Print(f"\nThe Caterpillar Princess hands you a {reward['item']}.")
                    Print(f"Description: {reward['description']}")
                    if reward['item'] == "Armour Plate":
                        Print("You use the armour plates\n+3 Armour Defence")
                        for armour in armour_data:
                                if armour['name'] == player_data['armour_equipped']:
                                    armour['defence'] += 3
                                    player_data['defence'] += 3
                        
                    elif reward['item'] == "Potion of Strength":
                        Print("\n--You drink the potion--\n\n+15 Max Health\n+20 Health\n+3 Strength")
                        player_data['max_health'] += 15
                        player_data['health'] += 20
                        player_data['strength'] += 3
                    
                    elif reward['item'] == "Caterpillar Charm":
                        Print("\n--You wear the charm around your wrist--\n\n+30% Critical Hit Chance")

                        # Find equipped weapon
                        equipped_weapon = None
                        for w in weapons_data:
                            if w["name"] == player_data["weapon_equipped"]:
                                equipped_weapon = w
                                break

                        if equipped_weapon:
                            # Apply crit buff to the weapon itself
                            equipped_weapon["crit_chance"] += 30

                            # Re-equip to recalc crit correctly via your existing function
                            view_weapon_stats(player_data, equipped_weapon, weapons_data)

                        break

                        
                    elif reward['item'] == "Forest Jewel":
                        Print("\n--You use the Jewel--\n\n+65 Max Health")
                        player_data['max_health'] += 65
                        
                    Print("\nYou thank the Caterpillar Princess and continue on your journey, feeling enpowered by the encounter.")

                    # Increase stat of good events by 1
                    game_stats['good_events'] += 1
                    
                    
                elif random_event <= 0.60:  # Encounter Bob // Bob Reward // Meet an Old Lady

                    if not seen_bob:  # First time meeting Bob
                        while True:
                            Print("[Bob] Hello stranger, I am heading to the castle to steal from their vault. If you tell me the way to the castle, I will give you a cut.")
                            action = input("\n[1] Tell Him\n[2] Start Capping\nEnter: ")

                            seen_bob = True  # Marks Bob as encountered

                            if action == '1':  # Helping Bob
                                Print("\n[Knight] I don't exactly remember the way, but if you head to the clearing that way, you should be able to see the castle.")
                                Print("\n[Bob] Thanks man, I shall give you the rewards if I am to see you again.")
                                helped_bob = True
                                seen_bounty_hunter = False
                                break

                            elif action == '2':  # Rejecting Bob
                                Print("\n[Knight] I have got no idea, I'm from the town in that direction.")
                                Print("\n[Bob] Okay, well, I shall continue on my adventure then.")
                                helped_bob = False
                                break

                            else:
                                Print("Please Enter a valid input")

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
                                action = input("\nDo you want to use the potion now?\n\n[1] Yes\n[2] No\nEnter: ")
                                if action == '1':
                                    use_health_potion(player_data, game_stats)
                                elif action == '2':
                                    Print("\nYou decide to save it for later in case of an emergency")
                                    player_data['health_potions'] += 1
                                else:
                                    Print("Please Enter a valid input")
                                    continue
                                break
                            elif action == '2':
                                Print("\n[Old Lady] May fortune still find you, even if kindness does not...")
                                break
                            else:
                                Print("Please Enter a valid input")

                    # Increase stat of good events by 1
                    game_stats['good_events'] += 1


                elif random_event <= 0.65:  # Bounty hunter event
                    while True:
                        if not seen_bounty_hunter:
                            Print("[Bounty Hunters] Have you seen this little guy called Bob wandering around robbing places and 'giving you a cut' of what he steals?")
                            seen_bounty_hunter = True
                            action = input("\n[1] Yes, I know where he is\n[2] I have never seen him before\nEnter: ")

                            # Told the hunters yes
                            if action == '1':
                                if helped_bob:  # You helped Bob earlier
                                    Print("\n[Knight] He is heading towards my castle to rob it!")
                                    time.sleep(1.5)
                                    Print("\n[Bounty Hunters] Well, I hate to tell you this, but he was asking where the castle was and it appears you have told him.")
                                    time.sleep(3)
                                    Print("-----Castle-----")
                                    time.sleep(0.5)
                                    Print("\n[Queen] Why, Knight, did you betray me like this?")
                                    time.sleep(1)
                                    Print("\n[Knight] I'm sorry, my queen.")
                                    Print("\n[Queen] It's okay, Knight. I shall just require you to pay a small amount of the vault back...")

                                    while True:
                                        sub_action = input("\n[1] Pay\n[2] Refuse to pay\nEnter: ")

                                        if sub_action == '1':
                                            Print("\n[Queen] 2000 GOLD! Guards, empty his pockets.")

                                            if player_data['gold'] >= 2000:
                                                Print("\n-2000 Gold")
                                                player_data['gold'] -= 2000
                                                Print("\n[Queen] The debt is settled.")
                                                break

                                            else:
                                                Print("\n[Knight] But my Queen, I do not have 2000 gold.")
                                                Print("\n[Queen] Then you will wager your life instead.")

                                                Print("\n[Queen] Face the elite gambler of Klare.")
                                                Print("[Queen] Win, and you live. Lose... and you die.")

                                                difficulty = "elite"
                                                enemy_name = "Rich guy"
                                                gold_bet = 2000

                                                play_21(player_data, klare_data, difficulty, gold_bet, enemy_name, game_stats)

                                                if enemy_name not in klare_data['elite_beaten']:
                                                    Print("\n[Queen] You have failed.")
                                                    Print("[Queen] You are no longer needed knight, goodbye")

                                                    Print("\n[Knight] ...So this is how it ends.")

                                                    player_data['health'] = 0
                                                    Print("\nYou were executed for defying the queen.\n")
                                                    check_death()

                                                else:
                                                    Print("\n[Queen] Hmph. Your skill has spared you this time.")
                                                    Print("[Queen] The stolen gold is reclaimed.")

                                                break

                                        elif sub_action == '2':
                                            Print("\n[Knight] I refuse to pay.")

                                            Print("\n[Queen] Then you leave me no choice.")
                                            Print("[Queen] You will face the elite gambler of Klare.")
                                            Print("[Queen] Win, and you live. Lose... and you die.")

                                            difficulty = "elite"
                                            enemy_name = "Rich guy"
                                            gold_bet = 2000

                                            play_21(player_data, klare_data, difficulty, gold_bet, enemy_name, game_stats)

                                            if enemy_name not in klare_data['elite_beaten']:
                                                Print("\n[Queen] You have lost. Guards... end this.")

                                                Print("\n[Knight] ...So this is how it ends.")

                                                player_data['health'] = 0
                                                Print("\nYou were executed for defying the Queen.")
                                                return

                                            else:
                                                Print("\n[Queen] Very well. You have proven your worth.")
                                                Print("[Queen] The stolen gold is reclaimed.")

                                            break

                                        else:
                                            Print("Please Enter a valid input.")

                                    game_stats['bad_events'] += 1
                                    break

                                elif seen_bob and not helped_bob:  # You rejected Bob before
                                    Print("[Bounty Hunters] Ah, so you helped this little guy rob the castle did you?")
                                    Print("\n[Knight] Well... when I said I know where he is... I mean I sent him off in that direction.")
                                    Print("\n[Bounty Hunters] Thanks! We will be on our way. Just so you know, he was never going to give back that gold. Here's a thanks :) \n+250 Gold")
                                    player_data['gold'] += 250
                                    game_stats['good_events'] += 1
                                    break

                                else:  # You never met Bob
                                    Print("\n[Bounty Hunters] You do know that having helped him will result in the dungeon penalty?")
                                    time.sleep(1)
                                    Print("\n[Knight] Haha 🫥 just kidding. I have no idea who or where this guy is.")
                                    break

                            elif action == '2':  # Lied to protect Bob or if you havent seen him
                                if helped_bob:
                                    Print("\n[Bounty Hunters] Haha, well you see, Bob... is this the guy who gave you directions?")
                                    Print("\n[Bob] Never *winks*")
                                    Print("\nHe gestures you with his head over to the trees... once the bounty hunters leave with bob you scurry over to the trees and find a chest filled with gold\n+1000 Gold!!!")
                                    player_data['gold'] += 1000
                                    game_stats['good_events'] += 1
                                    break
                                else:
                                    Print("\n[Bounty Hunters] Well, if you ever see him, let us know, and we will pay you highly.")
                                    break

                            else:
                                Print("Please Enter a valid input")
                                continue

                        else:
                            Print("[Bounty Hunters] I assume you still haven't seen him...\n\n[Knight] No I have not")
                            break
                            
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
                            player_data['crit_chance'] = 9 # bronze sword crit chance
                            weapons()

                            Print(f"\n[Dark Witch] I have reset your Max Health, Health, Gold and taken all your Weapons but doubled your {changed_stat}.")
                            Print(f"[Dark Witch] Old: {changed_stat} {starting_stat}, New: {changed_stat} {new_stat}.")
                            
                            if player_data['companions'] == 0:
                                Print("[Dark Witch] I have also summoned a companion for your adventures.")
                                player_data['companions'] += 1
                            break

                        elif action == '2':
                            Print("\n[Knight] No thanks,")
                            break

                        else:
                            Print("\nPlease Enter a valid input")
                        
                elif random_event <= 0.75: # Meet a friendly orc, rock or albert
                    friendly_enemy = [
                        "Orc",
                        "Rock",
                        "Albert"
                    ]

                    friendly_dialogue = {
                        "Orc": "\nThe Orc grunts as if asking a question",
                        "Rock": ["\nThe Rock just sits silently... but somehow you feel stronger from it's presence."],
                        "Albert": "\nAlbert adjusts his hole filled shirt.\n\n[Albert] Sit down with me young man, let me tell you about my glory days"
                    }
                    
                    friendly_enemy = random.choice(friendly_enemy)
                    Print(f"[Knight] Hello there... {friendly_enemy}")
                    Print(friendly_dialogue[friendly_enemy])
                    if friendly_enemy == 'Orc':
                        Print("\n[Knight] I am on a quest to defeat the dragon, and I wish for you to join me")
                        Print("\n[Orc] *Grunts in agreement*\n+1 Companion")
                        player_data['companions'] += 1
                    else:
                        Print("\n+1 Strength")
                        player_data['strength'] += 1
                    
                    # Increase stat of good events by 1
                    game_stats['good_events'] += 1

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
                            Print("Please Enter a valid input")
              
                elif random_event <= 0.85: # berry event

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
                        
                        action = input(f"\nDo you want to eat the {berry} berry?\n\n[1] Yes\n[2] No\nEnter: ")
                        
                        if action == '1':
                            # Apply a random effect
                            effect = random_berry_effect(player_data)
                            Print(f"\nYou eat the {berry} berry! It {effect}")
                            berries_left -= 1
                            
                            action = input("\nDo you want to continue looking?\n\n[1] Yes\n[2] No\nEnter: ")
                            
                            if berries_left == 0:
                                Print("\nYou couldnt find anymore berries to eat")
                                break
                            
                            if action == '1':
                                Print("\nYou continue looking and find another berry!")
                                
                            elif action == '2':
                                Print("\nYou decide you are full and stop looking")
                                break
                            
                        elif action == '2':
                            Print(f"You decide not to eat the {berry} berry and continue looking.")
                            berries_left -= 1
                        else:
                            Print("Please Enter a valid input")
                        
                elif random_event <= 0.90: # save slime king and lets you visit his kingdom anytime during your forest and frozen peak adventure
                    if player_data['slime_kingdom'] == True:
                        Print("You found nothing")
                    else:
                        Print("You hear a faint cry for help and decide to investigate\nA small slime soldier runs up to you and asks that you defend their kingdom.")
                        while True:
                            action = input("\n[1] Help (HARD)\n[2] Ignore\nEnter: ")
                            if action == '1':
                                Print("\nYou follow the slime soldier to the kingdom and see a massive slime king being attacked by a group of bandits")
                                fight_campfire_bandit = True
                                battle(player_data, game_stats)
                                battle(player_data, game_stats)
                                battle(player_data, game_stats)
                                fight_campfire_bandit = False
                                fight_bandit_leader = True
                                battle(player_data, game_stats)
                                fight_bandit_leader = False
                                Print("\nAfter you slay the final bandit, the slime king thanks you and offers you a home in his kingdom anytime you wish")
                                player_data['slime_kingdom'] = True

                                # Increase stat of good events by 1
                                game_stats['good_events'] += 1
                                
                                break
                            elif action == '2':
                                Print("\n[Knight] Sorry little guys, I'm just not strong enough to save you right now.")
                                break
                            else:
                                Print("Please Enter a valid input")

                elif random_event <= 0.95: # meet blacksmith to sharpen sword, and improve armour for gold
                    Print("You spot a blacksmith store and decide to enter")
                    upgraded_armour = False

                    # Increase stat of good events by 1
                    game_stats['good_events'] += 1

                    forest_blacksmith(player_data, weapons_data, armour_data, game_stats)

                else:
                    if "Shiny Sword" not in player_data['owned_weapons']:
                        Print("You walk up to a sword stuck in some stone, how will you try to get it out?")

                        game_stats['good_events'] += 1
                        while True:
                            action = input("\n[1] Use Max Health\n[2] Use Strength\n[3] Use your sword\n[4] Ask your companions to help\nEnter: ")

                            if action == '1':
                                if player_data['max_health'] >= 200:
                                    Print("\nUsing your massive body, you force the sword out of the stone")
                                    Print("---You found a Shiny Sword!!---")
                                    player_data['owned_weapons'].append("Shiny Sword")
                                else:
                                    Print("You try to lift it out of the stone but aren't strong enough yet")
                                break

                            elif action == '2':
                                if player_data['strength'] >= 5:
                                    Print("\nUsing pure strenth, you smash the stone to pieces and grab the sword")
                                    Print("---You found a Shiny Sword!!---")
                                    player_data['owned_weapons'].append("Shiny Sword")
                                else:
                                    Print("You punch the rocks as hard as you can but nothing happens")
                                break

                            elif action == '3':
                                Print("\nYou swing your sword into the stone, blunting it in the proccess. What did you think would happen? 💀\n-1 Damage")
                                for weapon in weapons_data:
                                    if weapon['name'] == player_data['weapon_equipped']:
                                        weapon['damage'] -= 1
                                break

                            elif action == '4':
                                if player_data['companions'] >= 2:
                                    Print("\nYou and your companions gather around and all lift at once. The sword comes loose!!")
                                    Print("---You found a Shiny Sword!!---")
                                    player_data['owned_weapons'].append("Shiny Sword")
                                else:
                                    Print("[Companion] I am nawt even gonna try.")

                                break

                            else:
                                print("\nPlease enter a valid input")
                    else:
                        Print("You found nothing")


                            
            # Player finds a shrine
            elif exploration <= 0.60:
                Print(f"\n{YELLOW}-----Hidden Shrine-----{RESET}")
                Print("You uncover what looks to be a mysterious shrine!")
                
                while True:
                    action = input("\n[1] Investigate\n[2] Leave\nEnter: ")

                    if action == '1':
                        shrine_luck = random.random()  # What happens when the player touches the shrine

                        if shrine_luck <= 0.20:  # Positive Shrine Effect 20%
                            Print("\nYou feel a warm sensation cover your body +35 Health +5 Max Health")
                            player_data['max_health'] += 5
                            player_data['health'] += 35

                            # Increase stat of good events by 1
                            game_stats['good_events'] += 1 

                        elif shrine_luck <= 0.40:  # Negative Shrine Effect 20%
                            Print("\nYou feel a figure touch your shoulder...")
                            time.sleep(2)
                            Print("\nBefore you can catch a glimpse, it disappears into the trees, and you hope that nothing bad happened")
                            player_data['max_health'] -= 10

                            # Increase stat of bad events by 1
                            game_stats['bad_events'] += 1 

                        elif shrine_luck <= 0.55:  # Ancient Well 15%
                            Print("\nYou stumble upon an old, moss-covered well.")
                            well_luck = random.random()
                            if well_luck <= 0.33:
                                Print("\nYou find a small pouch at the bottom\n+50 Gold")
                                player_data['gold'] += 50

                                # Increase stat of good events by 1
                                game_stats['good_events'] += 1 

                            elif well_luck <= 0.66:
                                Print("\nThe well seems to whisper to you, filling you with confidence and Strength\n+1 Strength")
                                player_data['strength'] += 1

                                # Increase stat of good events by 1
                                game_stats['good_events'] += 1 

                            else:
                                Print("\nYou slip and fall!\n-20 Health")
                                player_data['health'] -= 20
                                check_death(player_data, game_stats)

                                # Increase stat of bad events by 1
                                game_stats['bad_events'] += 1 

                        elif shrine_luck <= 0.75:  # Lost Merchant 20%
                            Print("\nA Merchant sits by the shrine with a broken cart, looking distressed.")
                            while True:
                                action = input("\n[1] Help him fix his cart\n[2] Rob him\n[3] Ignore\nEnter: ")

                                if action == '1':
                                    Print("\nYou lend a hand and repair the cart draining your energy. The Merchant thanks you.\n+50 Gold\n-10 Health")
                                    player_data['gold'] += 50
                                    player_data['health'] -= 10
                                    check_death(player_data, game_stats)
                                    break

                                elif action == '2':
                                    Print("\nYou threaten the merchant and take his gold, but not without a fight.")
                                    fight_merchant = True
                                    battle(player_data, game_stats)
                                    fight_merchant = False
                                    break
                                elif action == '3':
                                    Print("\n[Knight] I don't feel like dealing with that right now")
                                    break
                                else:
                                    Print("\nPlease Enter a valid input")
                        

                        elif shrine_luck <= 0.90:  # Sleeping Bear 15%

                            # Increase stat of bad events by 1
                            game_stats['bad_events'] += 1 
                            
                            while True:
                                Print("\nYou spot a massive bear sleeping on the path.")
                                action = input("\n[1] Sneak past\n[2] Attack\nEnter: ")

                                if action == '1':
                                    if random.random() <= 0.50:
                                        Print("\nYou successfully sneak past!")

                                        # Increase stat of good events by 1
                                        game_stats['good_events'] += 1 

                                    else:
                                        Print("\nThe bear wakes up and swipes at you! -25 Health")
                                        player_data['health'] -= 25
                                        check_death(player_data, game_stats)

                                        # Increase stat of bad events by 1
                                        game_stats['bad_events'] += 1 
                                        break

                                elif action == '2':
                                    Print("\nYou battle the bear fiercely, and as you slash through it's bones it somehow sharpens your sword\n+1 Damage\n-30 Health")
                                    for weapon in weapons_data:
                                        if weapon['name'] == player_data['weapon_equipped']:
                                            weapon['damage'] += 1
                                    player_data['health'] -= 30
                                    check_death(player_data, game_stats)
                                    break
                                
                                else:
                                    Print("\nPlease Enter a valid input")

                        elif shrine_luck <= 0.95:  # Cursed Knight 5%
                            Print("\nA knight in black armor approaches, appearing to want to protect the shrine.")
                            fight_black_knight = True
                            battle(player_data, game_stats)
                            fight_black_knight = False

                            # Increase stat of bad events by 1
                            game_stats['bad_events'] += 1 

                        else:  # Golden Deer 5%
                            Print("\nA golden deer appears in the clearing, it's fur shimmering.")
                            time.sleep(2)
                            Print("You follow the deer mesmerised...")
                            time.sleep(1)
                            Print("\nIt slowly walks up to a chest and rubs it's nose against it")
                            time.sleep(1)
                            Print("\nYou walk up to the chest to find it full of coins!\n+150 Gold")
                            player_data['gold'] += 150  

                            # Increase stat of good events by 1
                            game_stats['good_events'] += 1 
                        break
                    
                    elif action == '2':
                        Print("\nYou leave the shrine alone")
                        break
                    else:
                        Print("\nPlease Enter a valid input")
                        
            # Player walks into a trap
            elif exploration <= 0.70:
                print(f"\n{RED}-----Trap-----{RESET}")
                time.sleep(1)
                trap_luck = random.random()
                if trap_luck <= 0.25:
                    Print("You fall into a hole and take 10 Damage")
                    player_data['health'] -= 10
                    
                elif trap_luck <= 0.60:
                    Print("You get hit by a falling log and take 20 Damage")
                    player_data['health'] -= 20

                elif trap_luck <= 0.80:
                    Print("You step on a tree branch and roll your ankle taking 15 Damage")
                    player_data['health'] -= 15
                else:
                    Print("Haha just kidding there was no trap there but you did find an apple +5 Health")
                    player_data['health'] += 5
                
                check_death(player_data, game_stats)

                # Increase stat of bad events by 1
                game_stats['bad_events'] += 1 
                    
            # Player finds an enemy
            elif exploration <= 0.95:

                # Increase stat of bad events by 1
                game_stats['bad_events'] += 1 

                battle(player_data, game_stats)
                
            # Player encounters the merchant
            else:

                # Increase stat of good events by 1
                game_stats['good_events'] += 1 

                forest_merchant(player_data, game_stats, weapons_data, armour_data)

            exploration_time -= 1

            # Adds earned gold to stat
            track_gold_earned(player_data, before_gold, game_stats)
            
            if settings['enter_to_continue']:
                if exploration_time == 0:
                    pass
                else:
                    input("\nPress Enter to continue: ")                   
        else:
            player_data['day'] += 1
            if player_data['day'] == 15:
                Print("\n[Knight] There is nothing left here... I think it's time I continue onto the Frozen Peaks, MIGHTY DRAGON HERE I COME")
                Print("\nYou hike through most of the forest and before you exit you are stopped by the HOWLER")
                fight_boss = True
                battle(player_data, game_stats)
                fight_boss = False
                player_data['location'] = 'Frozen Peaks'

                # Increase game stat of bosses killed by 1
                game_stats['bosses_killed'] += 1

            # Increase game stat of days survived by 1
            game_stats['days_survived'] += 1

            break

# Forest Merchant Encounter
def forest_merchant(player_data, game_stats, weapons_data, armour_data):
    Print(f"\n-----Merchant-----")
    Print("[Merchant] Hello I am a merchant! What would you like to buy?")

    while True:
        if player_data['weapon_equipped'] not in player_data['owned_weapons']:
            player_data['owned_weapons'].append(player_data['weapon_equipped'])
        if player_data['armour_equipped'] not in player_data['owned_armour']:
            player_data['owned_armour'].append(player_data['armour_equipped'])

        Print(f"\nYou have {player_data['gold']} Gold")

        print("\n-----Swords-----\n\n[1] Iron Sword --200 Gold--\n[2] Steel Sword --450 Gold--")
        print("\n-----Bows-----\n\n[3] Hunting Bow --180 Gold--")
        print("\n-----Spears-----\n\n[4] Wooden Spear --220 Gold--")
        print("\n-----Armour-----\n\n[5] Cloth Armour --225 Gold--\n[6] Iron Armour --500 Gold--")
        print("\n-----Potions/Crystals-----\n\n[7] Health Potion --100 Gold--\n[8] Health Crystal --350 Gold--")
        print("\n-----Items-----\n\n[9] Enchant Book --750 Gold--")
        print("\n-----Other-----\n\n[i] View Inventory\n[r] Exit")

        action = input("\nEnter: ").lower()


        # ----------------- Inventory -----------------
        if action == 'i':
            inventory_display(player_data, weapons_data, armour_data)
            continue


        # ----------------- Weapons -----------------
        if action in ['1','2','3','4']:

            weapon_map = {
                '1': ('Iron Sword', 200),
                '2': ('Steel Sword', 450),
                '3': ('Hunting Bow', 180),
                '4': ('Wooden Spear', 220)
            }

            weapon_name, cost = weapon_map[action]
            new_weapon = get_weapon_by_name(weapon_name)

            if player_data['gold'] < cost:
                Print("\n[Merchant] Sorry but you can't afford this item.")
                continue

            if weapon_name in player_data['owned_weapons']:
                Print(f"\n[Merchant] You already have the {weapon_name}.")
                continue

            stat_comparison(get_weapon_by_name(player_data['weapon_equipped']), new_weapon, "weapon")
            
            if input("\nPress Enter to confirm or 'r' to cancel: ") == "":
                Print(f"\n-{cost} Gold")
                player_data['gold'] -= cost
                player_data['owned_weapons'].append(weapon_name)

                Print("\n[Merchant] Excellent choice, knight.")
                game_stats['items_bought'] += 1

        # ----------------- Armour -----------------
        elif action in ['5','6']:

            armour_map = {
                '5': ('Cloth Armour', 225),
                '6': ('Iron Armour', 500)
            }

            armour_name, cost = armour_map[action]
            selected_armour = get_armour_by_name(armour_name)

            if player_data['gold'] < cost:
                Print("\n[Merchant] Sorry but you can't afford this item.")
                continue

            if armour_name in player_data['owned_armour']:
                Print(f"\n[Merchant] You already own {armour_name}.")
                continue

            stat_comparison(get_armour_by_name(player_data['armour_equipped']), selected_armour, "armour")

            if input("\nPress Enter to confirm or 'r' to cancel: ") == "":
                Print(f"\n-{cost} Gold")
                player_data['gold'] -= cost
                player_data['owned_armour'].append(armour_name)

                # add new armour defence
                old_def = get_equipped_armour_defence(player_data, armour_data)
                player_data['defence'] -= old_def

                player_data['armour_equipped'] = armour_name

                player_data['defence'] += selected_armour['defence']

                Print("\n[Merchant] May it protect you in every battle ahead.")
                game_stats['items_bought'] += 1


        # ----------------- Items -----------------
        elif action == '7':
            if player_data['gold'] < 100:
                Print("\n[Merchant] Sorry but you can't afford this item.")
                continue

            Print("\n-----Health Potion-----")
            if input("\nPress Enter to confirm or 'r' to cancel: ") == "":
                player_data['gold'] -= 100
                player_data['health_potions'] += 1
                Print("\n[Merchant] Stay alive out there.")
                game_stats['items_bought'] += 1


        elif action == '8':
            if player_data['gold'] < 250:
                Print("\n[Merchant] Sorry but you can't afford this item.")
                continue

            Print("\n-----Health Crystal-----")
            if input("\nPress Enter to confirm or 'r' to cancel: ") == "":
                player_data['gold'] -= 250
                player_data['max_health'] += 35
                player_data['health'] += 50
                Print("\n[Merchant] A strong choice.")
                game_stats['items_bought'] += 1


        elif action == '9':
            if player_data['gold'] < 750:
                Print("\n[Merchant] Sorry but you can't afford this.")
                continue

            if input("\nPress Enter to confirm or 'r' to cancel: ") == "":
                player_data['gold'] -= 750
                random_enchant(player_data, weapons_data)
                Print("\n[Merchant] Your weapon glows with power.")
                game_stats['items_bought'] += 1


        elif action == 'r':
            Print("\n[Merchant] Farewell, knight.")
            break

        else:
            Print("Please enter a valid input.")

# Blacksmith Shop
def forest_blacksmith(player_data, weapons_data, armour_data, game_stats):
    global upgraded_armour

    Print(f"\n{BLACK}-----Blacksmith-----{RESET}")
    Print("[Blacksmith] Hello Knight, what would ya like?")

    while True:
        Print(f"\nGold: {player_data['gold']}")
        action = input(
            "\n[1] Shop\n[2] Sharpen Sword --250 Gold--\n[3] Upgrade Armour (free)"
            "\n\n[i] Inventory\n[r] Leave\nEnter: "
        ).lower()


        if action == 'i':
            inventory_display(player_data, weapons_data, armour_data)
            continue


        if action == '1':
            Print("\n[Knight] What have you got blacksmith?")
            time.sleep(1)
            os.system('cls')

            weapon_map = {
                '1': ('Iron Sword', 75),
                '2': ('Steel Sword', 200)
            }

            armour_map = {
                '3': ('Iron Armour', 425)
            }

            while True:
                Print(f"\nGold: {player_data['gold']}")
                action = input(
                    "\n-----Swords-----"
                    "\n[1] Iron Sword --75 Gold--"
                    "\n[2] Steel Sword --200 Gold--"
                    "\n\n-----Armour-----"
                    "\n[3] Iron Armour --425 Gold--"
                    "\n\n[r] Leave\nEnter: "
                ).lower()


                if action in weapon_map:

                    name, cost = weapon_map[action]
                    new_weapon = get_weapon_by_name(name)

                    if player_data['gold'] < cost:
                        Print("[Blacksmith] You don't have the gold")
                        continue

                    stat_comparison(
                        get_weapon_by_name(player_data['weapon_equipped']),
                        new_weapon,
                        "weapon"
                    )

                    if input("\nPress Enter to confirm or 'r' to cancel: ") == "":
                        Print(f"\n- {cost} Gold")
                        player_data['gold'] -= cost
                        player_data['owned_weapons'].append(name)

                        Print("\n[Blacksmith] Solid choice")
                        game_stats['items_bought'] += 1


                elif action in armour_map:

                    name, cost = armour_map[action]
                    new_armour = get_armour_by_name(name)

                    if player_data['gold'] < cost:
                        Print("[Blacksmith] Not enough gold")
                        continue

                    stat_comparison(
                        get_armour_by_name(player_data['armour_equipped']),
                        new_armour,
                        "armour"
                    )

                    if input("\nPress Enter to confirm or 'r' to cancel: ") == "":

                        Print(f"\n- {cost} Gold")
                        player_data['gold'] -= cost
                        player_data['owned_armour'].append(name)

                        Print("\n[Blacksmith] You're welcome knight, this is the best armour in the forest")
                        game_stats['items_bought'] += 1

                elif action == 'r':
                    Print("\n[Blacksmith] Come back soon knight!")
                    break

                else:
                    Print("Please Enter a input")

        elif action == '2':

            if player_data['gold'] < 250:
                Print("\n[Blacksmith] Not enough gold")
                continue

            if input("\n250 Gold for +3 Damage\nPress Enter to confirm or 'r' to cancel: ") == "":
                player_data['gold'] -= 250
                Print("\n+3 Weapon Damage")

                for weapon in weapons_data:
                    if weapon['name'] == player_data['weapon_equipped']:
                        weapon['damage'] += 3
                        break

        elif action == '3':

            if upgraded_armour:
                Print("\n[Blacksmith] Can't upgrade further.")
                continue

            if player_data['armour_equipped'] in ["No Armour", "Cloth Armour"]:
                Print("\n[Blacksmith] You've got no armour to upgrade")
                continue
                
            upgraded_armour = True

            for armour in armour_data:
                if armour['name'] == player_data['armour_equipped']:
                    armour['defence'] += 2
                    player_data['defence'] += 2
                    print("\n+2 Armour Defence")
                    break



        elif action == 'r':
            Print("\n[Blacksmith] See you next time!")
            break

        else:
            Print("Please enter a valid input.")

# -- Frozen Peaks -- #

# Frozen Peaks Enemies list
def enemy_data_frozen_peaks():
    # Easy   
    frost_orc = {"name": "Frost Orc", "health": 110, "strength": 22, "gold": 25}
    ice_wraith = {"name": "Ice Wraith", "health": 65, "strength": 32, "gold": 30}
    snow_hunter = {"name": "Snow Hunter", "health": 85, "strength": 37, "gold": 40}
    shade = {"name": "Shade", "health": 55, "strength": 35, "gold": 75}
    golem = {"name": "Golem", "health": 225, "strength": 30, "gold": 80}
    frost_wraith = {"name": "Frost Wraith", "health": 50, "strength": 40, "gold": 45}
    ice_elemental = {"name": "Ice Elemental", "health": 70, "strength": 30, "gold": 50}
    wolf_pack = {"name": "Wolf Pack", "health": 90, "strength": 35, "gold": 35}
    # Medium
    frozen_knight = {"name": "Frozen Knight", "health": 120, "strength": 30, "gold": 70}
    cursed_shade = {"name": "Cursed Shade", "health": 100, "strength": 50, "gold": 90}
    snow_titan = {"name": "Snow Titan", "health": 150, "strength": 32, "gold": 100}
    yeti = {"name": "Yeti", "health": 260, "strength": 35, "gold": 120}
    frost_yeti = {"name": "Frost Yeti", "health": 200, "strength": 40, "gold": 150}
    ice_ghost = {"name": "Ice Ghost", "health": 170, "strength": 45, "gold": 130}
    frost_giant = {"name": "Frost Giant", "health": 220, "strength": 40, "gold": 200}
    wendigo = {"name": "Wendigo", "health": 230, "strength": 60, "gold": 250}
    # Hard
    blizzard_golem = {"name": "Blizzard Golem", "health": 425, "strength": 35, "gold": 300}
    ancient_wraith = {"name": "Ancient Wraith", "health": 270, "strength": 50, "gold": 275}
    snow_serpant = {"name": "Snow Serpent", "health": 255, "strength": 55, "gold": 320}
    baby_bigfoot = {"name": "Baby Bigfoot", "health": 285, "strength": 70, "gold": 350}
    snow_beast = {"name": "Snow Beast", "health": 280, "strength": 65, "gold": 400}
    # Boss
    bigfoot = {"name": "Bigfoot", "health": 650, "strength": 90, "gold": 700}
    # Exploration Enemies
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
def explore_frozen_peaks(player_data, weapons_data, game_stats):
    global fight_elder_yeti, storm_power, fight_boss, healed_today, fight_caravan, picked_events_left, upgraded_armour, viewed_map
    exploration_time = random.randint(4, 7) # How many events the player will encounter

    while True:
        if exploration_time > 0:
            
            before_gold = player_data['gold']

            if picked_events_left > 0:
                action = input("\n---Encounter Menu---\n[1] Exploration\n[2] Memory Game\n[3] Enemy Encounter\n[4] Merchant\nEnter: ")
                if action == '1':
                    exploration = 0.45
                elif action == '2':
                    exploration = 0.60
                elif action == '3':
                    exploration = 0.93
                elif action == '4':
                    exploration = 1

            else:   
                exploration = random.random()

            if player_data['day'] == 13 and exploration_time == 4:
                exploration = 1
            elif player_data['day'] == 19 and exploration_time == 1:
                exploration = 1
            elif player_data['day'] == 25 and exploration_time == 3:
                exploration = 1
            elif player_data['day'] == 29 and exploration_time == 1:
                exploration = 1

            if player_data['debugging']: # if player enables debug they can change the event
                try:
                    exploration = float(input("0 Exploration, 0.60 Memory, 0.70 Trap, 0.93 Enemy, 1 Merchant\nExploration value: "))
                except ValueError:
                    exploration = random.random()
                    
            # Main Exploration
            if exploration <= 0.45:
                Print(f"\n{BLUE}-----Snow Exploration-----{RESET}")

                # Wizard chooses first
                if picked_events_left > 0:
                    picked_events_left -= 1
                    try:
                        print("\n---Exploration Menu---\n[1] Find Elder Yeti\n[2] Tombstone Dungeon\n[3] Storm Power Increase\n[4] Abandoned Wooden Shack\n[5] Snow Safe Circle\n[6] Caravan Escort\n[7] Defence and Strength Swap")
                        print("[8] Aurora In The Sky\n[9] Find a Companion\n[10] Endless Storm\n[11] Ice Cave\n[12] Blacksmith\n[13] Merchant")
                        action = input("Enter: ")

                        if action == '1':
                            random_event = 0.05
                        elif action == '2':
                            random_event = 0.15
                        elif action == '3':
                            random_event = 0.30
                        elif action == '4':
                            random_event = 0.40
                        elif action == '5':
                            random_event = 0.45
                        elif action == '6':
                            random_event = 0.50
                        elif action == '7':
                            random_event = 0.55
                        elif action == '8':
                            random_event = 0.60
                        elif action == '9':
                            random_event = 0.65
                        elif action == '10':
                            random_event = 0.75
                        elif action == '11':
                            random_event = 0.80
                        elif action == '12':
                            random_event = 0.90
                        elif action == '13':
                            random_event = 0.99
                        else:
                            Print("Please Enter a valid input")
                    except ValueError:
                        random_event = 0.60

                # Normal random exploration
                elif player_data['debugging'] == False:
                    random_event = random.random()

                # Debug manual input
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
                            battle(player_data, game_stats)
                            fight_elder_yeti = False
                            Print("\nYou have defeated the Elder Yeti!!\n3 Random Enchantments!")
                            random_enchant(player_data, weapons_data)
                            random_enchant(player_data, weapons_data)
                            random_enchant(player_data, weapons_data)
                            break
                        elif action == '2':
                            Print("\nYou decide its not even close to worth it and quietly sneak around an ice spike and head the other way")
                            break
                        else:
                            Print("\nPlease Enter a valid input")

                elif random_event <= 0.10:
                    Print("You find a small cave and decide to enter... When suddenly you hear a voice.")
                    time.sleep(1)
                    gold_bet = int(player_data['gold'] / 2)
                    while True:
                        action = input(f"\n[Middle Aged Man] Hello, Knight... Want to play a game of 21 worth {gold_bet} Gold?\n[1] Yes\n[2] No\nEnter: ")
                        if action == '1':
                            Print("\n[Knight] Sure, I could use some extra Gold")
                            action = input("\n[Middle Aged Man] Do you wish to know the rules?\n\n[1] Yes\n[2] No\nEnter: ")
                            if action == '1':
                                Print("\n[Middle Aged Man] The rules aren't as simple as you have to get as close to 21 as possible without going over") 
                                Print("[Middle Aged Man] There are trump cards, which are cards that can allow you to change the target goal to another number such as 24")
                                Print("[Middle Aged Man] Now however I could then use a 17 trump card which would put the goal at 17 and you would be over")
                                Print("[Middle Aged Man] We both draw a hidden card at the start of the round that only we know, making it harder to know the opponents score")
                                Print("[Middle Aged Man] If one of us goes over the target score and the other is under, the person under automatically wins and if we're both over the score it's whoever is closer")
                                Print("[Middle Aged Man] There is only 13 cards in the deck ranging from 1-13 with no duplicates, so if you have a 3 that means I cant have a 3")
                                Print("[Middle Aged Man] Now, are you ready to play?")
                                input("Press Enter to continue: ")

                            Print("\n[Middle Aged Man] Alright, let's start")
                            enemy_name = "Middle Aged Man"
                            difficulty = "Medium"

                            play_21(player_data, klare_data, difficulty, gold_bet, enemy_name, game_stats)

                            game_stats['minigames_played'] += 1
                            break

                        elif action == '2':
                            Print(f"\n[Knight] Nah, I'd rather keep my {gold_bet} Gold")
                            break
                        else:
                            Print("\nPlease Enter a valid input")

                elif random_event <= 0.15:
                    Print("You come across a tall metal cross above a tombstone and decide to enter")
                    time.sleep(1)
                    Print("\nYou come across an enemy!!")
                    battle(player_data, game_stats)
                    Print("\nYou make it to the treasure!!")
                    Print("\n---Treasure---\n1x Health Potion\n+30 Max Health\n+45 Health\n\nSword Sharpener!\n+4 Damage")
                    player_data['max_health'] += 30
                    player_data['health'] += 45
                    player_data['health_potions'] += 1
                    for weapon in weapons_data:
                        if weapon['name'] == player_data['weapon_equipped']:
                            weapon['damage'] += 4
        
                
                elif random_event <= 0.20:
                    geniewish(player_data, weapons_data, armour_data)

                elif random_event <= 0.35:
                    if storm_power <= 0:
                        Print("A small snow storm starts to form weakening you a bit.\n\n-10 Health")
                        player_data['health'] -= 10
                    elif storm_power == 1:
                        Print("The storm starts to get stronger and you feel the cold wind biting at your skin and freezing your sword\n\n-20 Health\n-1 Damage")
                        player_data['health'] -= 20
                        for weapon in weapons_data:
                            if weapon['name'] == player_data['weapon_equipped']:
                                weapon['damage'] -= 1

                    elif storm_power == 2:
                        Print("The storm is getting stronger and you feel your body freezing up\n\n-30 Health\n-1 Weapon Damage\n-1 Armour Defence")
                        player_data['health'] -= 30
                        for weapon in weapons_data:
                            if weapon['name'] == player_data['weapon_equipped']:
                                weapon['damage'] -= 1
                        for armour in armour_data:
                            if armour['name'] == player_data['armour_equipped']:
                                armour['defence'] -= 1
                                player_data['defence'] -= 1

                    elif storm_power == 3:
                        Print("The storm's power increases\n\n-20 Health\n-10 Max Health\n-1 Weapon Damage")
                        player_data['health'] -= 20
                        player_data['max_health'] -= 10
                        for weapon in weapons_data:
                            if weapon['name'] == player_data['weapon_equipped']:
                                weapon['damage'] -= 1

                    elif storm_power == 4:
                        Print("You start feeling the cold through your armour and clothes onto your chest\n\n-10 Health\n-20 Max Health\n-2 Armour Defence")
                        player_data['health'] -= 10
                        player_data['max_health'] -= 20
                        for armour in armour_data:
                            if armour['name'] == player_data['armour_equipped']:
                                armour['defence'] -= 2
                                player_data['defence'] -= 2

                    elif storm_power == 5:
                        Print("The storm is getting more powerful and you feel your body freezing up\n\n-35 Health\n-2 Weapon Damage\n-2 Armour Defence")
                        player_data['health'] -= 35
                        for weapon in weapons_data:
                            if weapon['name'] == player_data['weapon_equipped']:
                                weapon['damage'] -= 2
                        for armour in armour_data:
                            if armour['name'] == player_data['armour_equipped']:
                                armour['defence'] -= 2
                                player_data['defence'] -= 2

                    elif storm_power == 6:
                        Print("The storm is getting too strong and you feel your body freezing up\n\n-40 Health\n-2 Weapon Damage\n-3 Armour Defence")
                        player_data['health'] -= 40
                        for weapon in weapons_data:
                            if weapon['name'] == player_data['weapon_equipped']:
                                weapon['damage'] -= 2
                        for armour in armour_data:
                            if armour['name'] == player_data['armour_equipped']:
                                armour['defence'] -= 3
                                player_data['defence'] -= 3

                    elif storm_power == 7:
                        Print("The storm is getting really strong almost making it impossible to see. You don't know how much harsher of a storm you can take but it's not much\n\n-30 Max Health\n-2 Strength")
                        player_data['max_health'] -= 30
                        player_data['strength'] -= 2

                    elif storm_power == 8:
                        Print("The storm gets too strong forcing you to take shelter by hiding in a divot on the otherside of a tree stump to the wind\n\n-25 Max Health\n-3 Strength\n-5 Armour Defence")
                        player_data['max_health'] -= 25
                        player_data['strength'] -= 3
                        for armour in armour_data:
                            if armour['name'] == player_data['armour_equipped']:
                                armour['defence'] -= 5
                                player_data['defence'] -= 5
                                
                        check_death(player_data, game_stats)
                        time.sleep(1)
                        Print("After the storm weakens you force yourself through the storm encountering Bigfoot and are forced to fight him.")
                        Print("However, you can quickly access your inventory before he reaches you")
                        inventory_display(player_data, weapons_data, armour_data)
                        fight_boss = True
                        battle(player_data, game_stats)
                        fight_boss = False
                        game_stats['bosses_killed'] += 1
                        player_data['location'] = 'Village of Klare'
                        healed_today = False
                        os.system('cls')
                        Print("As you leave the storm of the Frozen Peaks you look at Bigfoot's body and feel a sense of accomplishment")
                        if player_data['day'] < 30:

                            time.sleep(1)
                            Print("\nYou wander into Klare and are immedietly caught by a guard and taken to a hotel")
                            time.sleep(1.5)
                            Print("\n[Guard] The town is current on lockdown due to recent events, you will have to stay here for a while")
                            time.sleep(1)
                            Print("\n[Knight] What happend??")
                            time.sleep(1.5)
                            Print("\n[Guard] Accomodation is on us, but you will have to stay here until further notice, Goodbye")
                            time.sleep(1)
                            Print("\nYou stay in the hotel, eating and resting until the lockdown is lifted")

                            days_passed = 30 - player_data['day']
                            player_data['day'] = 30

                            print(f"\n{days_passed} days later...")
                            time.sleep(1)
                            Print("\n--ANNOUNCEMENT--\n[Unknown] The lockdown has been lifted, I want everybody back to work.")

                        Print("\n------ VILLAGE OF KLARE -----")

                    check_death(player_data, game_stats)
                    storm_power += 1
                    
                elif random_event <= 0.40:
                    while True:
                        Print("You come across a small wooden shack with the lights on\n\n[1] Enter\n[2] Leave")
                        action = input("Enter: ")
                        if action == '1':
                            person_inside = random.randint(1, 3)
                            if person_inside == 1:
                                while True:
                                    Print("\nYou walk up to the door and knock and the door blows open revealing a cozy place that seems abandoned\n\n[1] Rest\n[2] Loot\n[3] Pray to the shrine")
                                    action = input("Enter: ")
                                    if action == '1':
                                        Print("\nYou decide to rest for a bit and regain your health\n+75 Health")
                                        player_data['health'] += 75
                                        if player_data['health'] > player_data['max_health']:
                                            player_data['health'] = player_data['max_health']
                                        break
                                    elif action == '2': 
                                        Print("\nYou decide to loot the shack and find a small bag of gold\n+50 Gold")
                                        player_data['gold'] += 50
                                        break
                                    elif action == '3':
                                        if storm_power in [2,3]:
                                            Print("\nYou kneel down and pray to the shrine and it glows a bright blue and you feel a surge of power\n+1 Strength")
                                            player_data['strength'] += 1
                                            storm_power = 0
                                            
                                        elif storm_power in [4,5]:
                                            Print("\nYou kneel down and pray to the shrine and it glows a bright blue and you feel a surge of power\n+2 Strength")
                                            player_data['strength'] += 2
                                            storm_power = 0
                                        
                                        elif storm_power in [6,7]:
                                            Print("\nYou kneel down and pray to the shrine and it glows a bright blue and you feel a surge of power\n+3 Strength")
                                            player_data['strength'] += 3
                                            storm_power = 0
                                        
                                        else:
                                            Print("\nYou kneel down and pray to the shrine but nothing happens")
                                        break
                                    else:
                                        Print("Please Enter a valid input")

                            elif person_inside == 2:
                                Print("\nA small creature greets you at the door and invites you in for a meal\n\n+35 Health")
                                player_data['health'] += 35
                                storm_power -= 1
                                break
                            else:
                                Print("\nA small creature greets you at the door and invites you in for a meal\nHowever as they shut the door behind you they start swinging their knife!\n\n-25 Health")
                                player_data['health'] -= 25
                                check_death(player_data, game_stats)
                                break

                        elif action == '2':
                            Print("\nYou decide to leave the shack and head back into the snow")
                            break
                        else:
                            Print("Please Enter a valid input")

                elif random_event <= 0.45:
                    Print("As you push forward you come across a circle in a seemingly random spot in the snow where the storm completely stops. As you enter the circle the sun shines down on you, allowing you to regain your strength and defrost your items!")
                    Print("\n+15 Max Health\n+35 Health\n+2 Weapon Damage\n+1 Armour Defence")
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
                        Print("You come across a caravan with a bunch of people on the back\n\n[1] Fight\n[2] Ask for a ride\n[3] Leave them alone")
                        action = input("Enter: ")
                        if action == '1':
                            fight_caravan = True
                            battle(player_data, game_stats)
                            battle(player_data, game_stats)
                            fight_caravan = False
                            Print("\nYou successfully defeat the caravan and take their items\n\n---Items---\n+75 Gold\n\n--Armour plating--\n+3 Armour Defence\n\nEnchanted Book!!")
                            player_data['gold'] += 75
                            for armour in armour_data:
                                if armour['name'] == player_data['armour_equipped']:
                                    player_data['defence'] += 3
                                    armour['defence'] += 3
                            random_enchant(player_data, weapons_data)
                            break
                        elif action == '2':
                            Print("\nYou ask the caravan for a ride and they agree but only if you pay them 100 Gold!")
                            if player_data['gold'] >= 100:
                                player_data['gold'] -= 100
                                Print("\n-100 Gold\n\nWhile in the caravan the feeling of cold seems to disapear and you feel warmer\n+90 Health")
                                storm_power -= 1
                                player_data['health'] += 90
                                if player_data['health'] > player_data['max_health']:
                                    player_data['health'] = player_data['max_health']
                                break
                            else:
                                Print("\nYou don't have enough Gold so they leave you in the cold :(")
                                
                        elif action == '3':
                            Print("\nYou decide not to risk it and continue on in the freezing cold as they ride away")
                            break
                        else:
                            Print("\nPlease Enter a valid input")
            
                elif random_event <= 0.55:
                    while True:
                        Print("[Unknown] I have a proposition for you knight, I shall swap your defence with your strength and give you 100 Gold but increase the power of the storm.\n\n[1] Yes\n[2] No")
                        action = input("Enter: ")

                        if action == '1':
                            Print("\n[Unknown] Good choice")
                            time.sleep(0.5)

                            Print("\n+100 Gold")
                            player_data['gold'] += 100

                            armour_defence = 0
                            for armour in armour_data:
                                if armour['name'] == player_data['armour_equipped']:
                                    armour_defence = armour['defence']
                                    break

                            # Remove armour first to get base defence
                            base_defence = player_data['defence'] - armour_defence

                            # Swap base stats
                            temp = base_defence
                            base_defence = player_data['strength']
                            player_data['strength'] = temp

                            # Reapply armour
                            player_data['defence'] = base_defence + armour_defence

                            storm_power += 1
                            break

                        elif action == '2':
                            Print("\n[Knight] How about no")
                            break

                        else:
                            Print("\nPlease Enter a valid input")
                            
                elif random_event <= 0.60:
                    Print("As you sit down for a second you look up to the sky and see a beautiful aurora with moon shining down on you, allowing to feel truly calm for the next hour\n+25 Max Health\n+60 Health\n+1 Strength")
                    time.sleep(2)
                    player_data['max_health'] += 25
                    player_data['health'] += 60
                    player_data['strength'] += 1

                elif random_event <= 0.65:
                    Print("You find a small cave and decide to enter... When suddenly you hear a voice.\nIt's a hooded figure who begs for food...\nYou start up a fire, share some of your food and have a chat, helping her get to full strength\n+1 Companion")
                    player_data['companions'] += 1

                elif random_event <= 0.70:
                    Print("You come across a wizardy looking guy who offers to allow you to choose the events you encounter next for the remainder of the day\n[1] Yes\n[2] No")
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
                            Print("\n[Knight] Whatever you're selling, I aint buying yo")
                            break
                        else:
                            Print("\nPlease Enter a valid input")

                elif random_event <= 0.75:

                    escape_chance = 0  # Initial escape chance

                    Print("The storm grows stronger making it almost inpossible to see... Can you survive long enough to make it out?")
                    while True:

                        # Set escape chance to 100 if its over 100
                        if escape_chance > 100:
                            escape_chance = 100

                        # Escape once escape chance hits 100
                        Print(f"\n---You are currently {escape_chance}% of the way through the storm---")
                        print(f"-You have {player_data['health']} Health Left\n")

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
                                    Print("You step on a weird ball that's really squishy.\n\n[Knight] Ew")
                                    escape_chance += 5
                                    break

                                elif action == '2':
                                    if viewed_map:
                                        Print("After following the directions on the map you find the path again")
                                        escape_chance = 100  
                                    Print("You encounter a small furball who offers some snow goggles and some food\n+25 Health")
                                    player_data['health'] += 25
                                    escape_chance += 15
                                    break

                                elif action == '3':
                                    random_event = random.random()
                                    
                                    if random_event <= 0.05:
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
                                    Print("Please Enter a valid input")

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
                                action = input("What do you do?\n\n[1] Hear his story (30~ seconds)\n[2] Skip the story\nEnter: ")
                                if action == '1':
                                    PRint("\n[Hermit] Another wanderer, lost in the endless road. Sit. Listen.")
                                    time.sleep(2)
                                    PRint("\n[Knight] But... I have to get out.")
                                    time.sleep(1)
                                    PRint("\n[Hermit] Sit, I shall only be a minute")
                                    time.sleep(2)
                                    PRint("\n[Hermit] The storm... it consumes even the best of us")
                                    PRint("\n[Knight] Yes, and it's about to consume us if we don't get out of here")
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
                                    PRint("\n[Hermit] Think of the storm as a person trying to calm you after a fight. It wants to help you, but you must let it.")
                                    time.sleep(2)
                                    PRint("\nThe Hermit grabs your shoulder\n")
                                    time.sleep(2)
                                    PRint("[Hermit] Think of the storm as a friend not an enemy")
                                        
                                    Print("+1 Strength\n+15 Max Health\n+30 Health")
                                    player_data['strength'] += 1
                                    player_data['max_health'] += 10
                                    player_data['health'] += 20
                                    escape_chance = 100
                                    break

                                elif action == '2':
                                    Print("\nThe hermit starts yapping and you zone out to think about your quest.")
                                    Print("After you zone back in, you thank the hermit for the story and leave, fired up for the journey ahead.")

                                    Print("+1 Strength\n+15 Max Health\n+30 Health")
                                    player_data['strength'] += 1
                                    player_data['max_health'] += 10
                                    player_data['health'] += 20
                                    escape_chance += 30
                                    break

                                else:
                                    Print("Please Enter a valid input")

                        elif road_luck <= 0.45: # Storm
                            Print("An animal suddenly blocks your path.")
                            while True:
                                action = input("What do you do?\n\n[1] Wait for the animal to pass\n[2] Fight it\nEnter: ")
                                if action == '1':
                                    Print("The animal passes...")
                                    escape_chance -= 5
                                    break
                                elif action == '2':
                                    Print("You fight the animal and manage to kill it\n-20 Health")
                                    player_data['health'] -= 10
                                    escape_chance += 10
                                    check_death(player_data, game_stats)
                                    break
                                else:
                                    Print("Please Enter a valid input")
                                
                                
                        elif road_luck <= 0.60:  # River Event
                            Print("You hear a distant sound of rushing water.")
                            while True:
                                action = input("What do you do?\n\n[1] Investigate\n[2] Stay on the path\nEnter: ")
                                if action == '1':
                                    Print("\nYou discover a river that seems to block your path.")
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
                                    Print("Please Enter a valid input")
                                check_death(player_data, game_stats)

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
                                    check_death(player_data, game_stats)
                                    break
                                elif action == '2':
                                    Print("The shadow fades into the snow")
                                    break
                                else:
                                    Print("Please Enter a valid input")
                        else:
                            Print("The storm weakens a bit allowing you to see for a couple seconds")
                            escape_chance += 35
                            
                        escape_chance += 5

                elif random_event <= 0.80:
                    Print("As you are walking over some ice it suddenly cracks under you and you fall down an ice crevasse!\n-20 Health")
                    player_data['health'] -= 16
                    check_death(player_data, game_stats)
                    time.sleep(1)
                    Print("\nAs you get up dazed you look around you to find a bunch of crystals, you walk up to one and touch it!\n+4 Health")
                    crystals_left = random.randint(3, 7)
                    
                    # List of available berries
                    crystals = [ 
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
                        crystal = random.choice(crystals)
                        
                        # Ask for the player's action
                        action = input(f"\nDo you to investigate the {crystal} crystal?\n\n[1] Yes\n[2] No\nEnter: ")
                        
                        if action == '1':
                            # Generate and apply a random effect
                            effect = random_berry_effect(player_data)
                            Print(f"\nYou walk up to the {crystal} crystal... It {effect}")
                            crystals_left -= 1
                            
                            action = input("\nDo you want to continue looking?\n\n[1] Yes\n[2] No\nEnter: ")
                            
                            if crystals_left == 0:
                                Print("\nYou couldn't find anymore crystals")
                                break
                                
                            if action == '1':
                                Print("\nYou continue looking and find another crystal")
                                
                            elif action == '2':
                                Print("\nYou decide you are not addicted and start climbing out")
                                break
                            
                        elif action == '2':
                            Print(f"\nYou decide not to investigate the {crystal} crystal and continue looking")
                            crystals_left -= 1
                        else:
                            Print("\nPlease Enter a valid input")

                elif random_event <= 0.85: # Quest up mountain for frost orb
                    Print("You found nothing!!!")
                    
                elif random_event <= 0.90:  
                    upgraded_armour = False
                    frozen_peaks_blacksmith(player_data, armour_data, weapons_data, game_stats)

                elif random_event <= 0.99:
                    frozen_peaks_merchant(player_data, game_stats, weapons_data, armour_data)
                else:
                    Print("You found nothing!!") # epic quest

            # Player gets the memory game
            elif exploration <= 0.60:
                play_memory(player_data, game_stats, colours_left, memory_sequence)

            # Player walks into a trap
            elif exploration <= 0.70:
                Print(f"\n{RED}-----Trap-----{RESET}")
                time.sleep(1)
                trap_luck = random.random()
                if trap_luck < 0.40:
                    Print("As you were walking over some ice, it broke under your feet causing you to fall into the freezing cold water\n-20 Health")
                    player_data['health'] -= 20
                elif trap_luck < 0.80:
                    Print("While walking underneath a cliff a huge lump of snow falls onto you!\n-35 Health ")
                    player_data['health'] -= 35
                else:
                    Print("Haha just kidding there was no trap but you did find a icicle thats shaped like a sword")
                check_death(player_data, game_stats)
                
            # Player finds an enemy
            elif exploration <= 0.93:
                battle(player_data, game_stats)

            # Player encounters the merchant
            else:
                frozen_peaks_merchant(player_data, game_stats, weapons_data, armour_data)

            # Adds earned gold to stat
            track_gold_earned(player_data, before_gold, game_stats)

            exploration_time -= 1                   
        else:
            player_data['day'] += 1

            # Increase game stat of days survived by 1
            game_stats['days_survived'] += 1

            # theres a bug where it doesnt end. This is the fix I guess
            picked_events_left = 0
            break

# Frozen Merchant Encounter
def frozen_peaks_merchant(player_data, game_stats, weapons_data, armour_data):
    Print("\n-----Snow Merchant-----")
    Print("[Snow Wanderer] Hello, Knight, What would you like to buy?")
    
    while True:
        if player_data['weapon_equipped'] not in player_data['owned_weapons']:
            player_data['owned_weapons'].append(player_data['weapon_equipped'])
        if player_data['armour_equipped'] not in player_data['owned_armour']:
            player_data['owned_armour'].append(player_data['armour_equipped'])

        print(f"\nYou have {player_data['gold']} Gold")
        print("\n-----Swords-----\n\n[1] Flame Sword --750 Gold--\n[2] Frost Sword --1.15k Gold--")
        print("\n-----Bows-----\n\n[3] Compound Bow --850 Gold--")
        print("\n-----Spears-----\n\n[4] Eagle Spear --1k Gold--")
        print("\n-----Armour-----\n\n[5] Yeti Armour --900 Gold--\n[6] Titanium Armour --2k Gold--")
        print("\n-----Potions/Crystals-----\n\n[7] Health Potion --250 Gold--\n[8] Health Crystal --600 Gold--")
        print("\n-----Items-----\n\n[9] Enchant Book --1.6k Gold--")
        print("\n[i] View Inventory\n[r] Exit")
        
        action = input("\nEnter: ").lower()

        if action == 'i':
            inventory_display(player_data, weapons_data, armour_data)
            continue

        # -------------------- WEAPONS --------------------
        if action in ['1', '2', '3', '4']:

            weapon_map = {
                '1': ('Flame Sword', 750),
                '2': ('Frost Sword', 1150),
                '3': ('Compound Bow', 850),
                '4': ('Eagle Spear', 1000)
            }

            weapon_name, cost = weapon_map[action]
            new_weapon = get_weapon_by_name(weapon_name)

            if player_data['gold'] < cost:
                Print("\n[Snow Wanderer] Sorry, you can't afford that.")
                continue

            if weapon_name in player_data['owned_weapons']:
                Print(f"\n[Snow Wanderer] You already carry a {weapon_name}.")
                continue

            Print(f"\n[Knight] I'd like to see the {weapon_name}.")
            time.sleep(0.5)

            stat_comparison(get_weapon_by_name(player_data['weapon_equipped']), new_weapon, "weapon")

            if input("\nPress Enter to confirm or 'r' to cancel: ") == "":
                Print(f"\n-{cost} Gold")
                player_data['gold'] -= cost
                player_data['owned_weapons'].append(weapon_name)

                Print("\n[Snow Wanderer] Use it well.")
                game_stats['items_bought'] += 1


        # -------------------- ARMOUR --------------------
        elif action in ['5', '6']:

            armour_map = {
                '5': ('Yeti Armour', 900),
                '6': ('Titanium Armour', 2000)
            }

            armour_name, cost = armour_map[action]
            selected_armour = get_armour_by_name(armour_name)

            if player_data['gold'] < cost:
                Print("\n[Snow Wanderer] That's too expensive for you.")
                continue

            if armour_name in player_data['owned_armour']:
                Print(f"\n[Snow Wanderer] You already own {armour_name}.")
                continue

            Print(f"\n[Knight] Could I inspect the {armour_name}?")
            time.sleep(0.5)

            stat_comparison(get_armour_by_name(player_data['armour_equipped']), selected_armour, "armour")

            if input("\nPress Enter to confirm or 'r' to cancel: ") == "":
                Print(f"\n-{cost} Gold")
                player_data['gold'] -= cost
                player_data['owned_armour'].append(armour_name)

                old_def = get_equipped_armour_defence(player_data, armour_data)
                player_data['defence'] -= old_def

                player_data['armour_equipped'] = armour_name
                player_data['defence'] += selected_armour['defence']

                Print("\n[Snow Wanderer] Stay protected.")
                game_stats['items_bought'] += 1


        # -------------------- ITEMS --------------------
        elif action == '7':
            if player_data['gold'] < 250:
                Print("\n[Snow Wanderer] Not enough gold.")
                continue

            Print("\n-----Health Potion Stats-----\n+50 Health")
            if input("\nPress Enter to confirm or 'r' to cancel: ") == "":
                player_data['gold'] -= 250
                player_data['health_potions'] += 1
                Print("\n[Snow Wanderer] Stay alive.")
                game_stats['items_bought'] += 1


        elif action == '8':
            if player_data['gold'] < 600:
                Print("\n[Snow Wanderer] You can't afford that.")
                continue

            Print("\n-----Health Crystal Stats-----\n+50 Max Health\n+65 Health")
            if input("\nPress Enter to confirm or 'r' to cancel: ") == "":
                player_data['gold'] -= 600
                player_data['max_health'] += 50
                player_data['health'] += 65
                Print("\n[Snow Wanderer] Powerful item.")
                game_stats['items_bought'] += 1


        elif action == '9':
            if player_data['gold'] < 1600:
                Print("\n[Snow Wanderer] It's too pricey for you.")
                continue

            if input("\nPress Enter to confirm or 'r' to cancel: ") == "":
                player_data['gold'] -= 1600
                random_enchant(player_data, weapons_data)
                Print("\n[Snow Wanderer] May the enchant serve you.")
                game_stats['items_bought'] += 1


        elif action == 'r':
            Print("\n[Snow Wanderer] Safe travels.")
            break

        else:
            Print("Invalid option.")

# Blacksmith Shop (Goblin Tinkerer)
def frozen_peaks_blacksmith(player_data, weapons_data, armour_data, game_stats):
    global upgraded_armour

    Print("\n-----Goblin Tinkerer-----")
    Print("[Goblin Tinkerer] Hello Knight, what would ya like?")

    while True:
        Print(f"\nGold: {player_data['gold']}")
        action = input("\n[1] Shop\n[2] Sharpen Sword --350 Gold--\n[3] Upgrade Armour --200 Gold--\n\n[i] Inventory\n[r] Leave\nEnter: ").lower()

        if action == 'i':
            inventory_display(player_data, weapons_data, armour_data)
            continue

        if action == '1':
            Print("\n[Knight] I want to browse your stock.")
            time.sleep(1)
            os.system('cls')

            weapon_map = {
                '1': ('Flame Sword', 600),
                '2': ('Frost Sword', 1100)
            }

            armour_map = {
                '3': ('Yeti Armour', 800),
                '4': ('Titanium Armour', 1700)
            }

            while True:
                Print(f"\nGold: {player_data['gold']}")

                action = input(
                    "\n-----Swords-----\n"
                    "[1] Flame Sword --600 Gold--\n"
                    "[2] Frost Sword --1.1k Gold--\n"
                    "\n-----Armour-----\n"
                    "[3] Yeti Armour --800 Gold--\n"
                    "[4] Titanium Armour --1.7k Gold--\n"
                    "\n[r] Leave\nEnter: "
                ).lower()

                if action in weapon_map:
                    name, cost = weapon_map[action]
                    new_weapon = get_weapon_by_name(name)

                    if player_data['gold'] < cost:
                        Print("\n[Goblin Tinkerer] Too poor.")
                        continue

                    Print("\n[Goblin Tinkerer] Look.")
                    stat_comparison(
                        get_weapon_by_name(player_data['weapon_equipped']),
                        new_weapon,
                        "weapon"
                    )

                    if input("\nPress Enter to buy or 'r' to cancel: ").lower() == "":
                        Print(f"\n-{cost} Gold")
                        player_data['gold'] -= cost
                        player_data['owned_weapons'].append(name)

                        game_stats['items_bought'] += 1


                elif action in armour_map:
                    name, cost = armour_map[action]
                    new_armour = get_armour_by_name(name)

                    if player_data['gold'] < cost:
                        Print("\n[Goblin Tinkerer] Not enough.")
                        continue

                    stat_comparison(
                        get_armour_by_name(player_data['armour_equipped']),
                        new_armour,
                        "armour"
                    )

                    if input("\nPress Enter to buy or 'r' to cancel: ").lower() == "":
                        Print(f"\n-{cost} Gold")
                        player_data['gold'] -= cost
                        player_data['owned_armour'].append(name)

                        old_def = get_equipped_armour_defence(player_data, armour_data)
                        player_data['defence'] -= old_def

                        player_data['armour_equipped'] = name
                        player_data['defence'] += new_armour['defence']

                        game_stats['items_bought'] += 1


                elif action == 'r':
                    break

                else:
                    Print("Invalid option.")


        elif action == '2':

            if player_data['gold'] < 350:
                Print("\n[Goblin Tinkerer] No freebies.")
                continue

            if input("\n350 Gold for +4 Damage\nPress Enter to confirm or 'r' to cancel: ") == "":
                player_data['gold'] -= 350

                for weapon in weapons_data:
                    if weapon['name'] == player_data['weapon_equipped']:
                        weapon['damage'] += 4
                        break

                Print("\n[Goblin Tinkerer] Sharpened.")


        elif action == '3':

            if player_data['gold'] < 200:
                Print("\n[Goblin Tinkerer] Bring more gold.")
                continue

            if upgraded_armour:
                Print("\n[Goblin Tinkerer] Already done.")
                continue

            if player_data['armour_equipped'] in ["No Armour", "Cloth Armour"]:
                Print("\n[Goblin Tinkerer] No armour to upgrade.")
                continue

            player_data['gold'] -= 200
            upgraded_armour = True

            for armour in armour_data:
                if armour['name'] == player_data['armour_equipped']:
                    armour['defence'] += 2
                    player_data['defence'] += 2
                    break

            Print("\n[Goblin Tinkerer] Armour improved.")


        elif action == 'r':
            Print("\n[Goblin Tinkerer] Bye Knight.")
            break

        else:
            Print("Invalid option.")

# -- Village of Klare -- #

# Gamble Hall villager data
def klare_villager_data():
    villagers = [

        # Easy
        {"name": "Joe", "gold": 20, "difficulty": "Easy"},
        {"name": "Bob", "gold": 25, "difficulty": "Easy"},
        {"name": "Frank", "gold": 35, "difficulty": "Easy"},
        {"name": "Sue", "gold": 25, "difficulty": "Easy"},
        {"name": "Tom", "gold": 30, "difficulty": "Easy"},
        {"name": "Lily", "gold": 40, "difficulty": "Easy"},
        {"name": "Max", "gold": 33, "difficulty": "Easy"},
        {"name": "Emma", "gold": 50, "difficulty": "Easy"},

        # Medium
        {"name": "Oliver", "gold": 60, "difficulty": "Medium"},
        {"name": "Mia", "gold": 75, "difficulty": "Medium"},
        {"name": "Liam", "gold": 65, "difficulty": "Medium"},
        {"name": "Ava", "gold": 80, "difficulty": "Medium"},
        {"name": "Sophia", "gold": 70, "difficulty": "Medium"},
        {"name": "Noah", "gold": 55, "difficulty": "Medium"},
        {"name": "Albert", "gold": 85, "difficulty": "Medium"},
        {"name": "Ethan", "gold": 100, "difficulty": "Medium"},

        # Hard
        {"name": "Charlotte", "gold": 150, "difficulty": "Hard"},
        {"name": "Jack", "gold": 280, "difficulty": "Hard"},
        {"name": "Amelia", "gold": 230, "difficulty": "Hard"},
        {"name": "Henry", "gold": 250, "difficulty": "Hard"},
        {"name": "Isabella", "gold": 330, "difficulty": "Hard"},
        
    ]


    return villagers

# Klare main menu
def explore_klare(player_data, weapons_data, armour_data, klare_data):
    global current_hour

    Print("\n----- Village of Klare -----")

    intro_dialogue = [
        "You leave your cozy house and walk out into the sun, ready for a great day",
        "As you close the door, you look out to the rainy weather",
        "You look out the window and can barely see 10 meters infront of you, its going to be foggy today"
    ]

    current_hour = 9
    current_minute = 0

    Print(random.choice(intro_dialogue))
    time.sleep(2)

    klare_data['day_pass'] = False

    banked_gold = player_data['gold']

    while current_hour < 17:

        print(f"\nCurrent Time: {current_hour}:{current_minute:02d}")
        print("\n----- Choices -----")
        print("🗣️ [1] Talk to Villagers")
        print("💵 [2] Visit the Minigame Hall")
        print("🎪 [3] Go to the Town Merchant")
        print("❓ [4] How to play each minigame")
        print("🚪 [r] Return Home (End day early)")
        action = input("Enter: ")

        if action == '1':
            talk_to_villagers(player_data)
            current_hour, current_minute = advance_time(current_hour, current_minute, 10)

        elif action == '2':
            minigame_hall(player_data, klare_data)
            

        elif action == '3':
            klare_merchant(player_data, weapons_data, armour_data)

        elif action == '4':
            os.system('cls')
            print("\n----- Minigame Instructions -----")
            print("\n---Rock Paper Scissors---")
            print("-You can type 'Rock', 'Paper' or 'Scissors'.")
            print("-OR you can type 'r', 'p', 's'. Capital or not, doesnt matter")
            print("\n---Twenty One---")
            print("-The rules are not to reach 21 without exceeding it.")
            print("-Trump cards can modify the target score, for example changing it to 24.")
            print("-A trump card may also lower the target score, such as reducing it to 17, which can immediately place an opponent over the limit target score.")
            print("-Each player draws a hidden card at the start of the round.")
            print("-If one player exceeds the target score while the other remains below it, the player under the target wins automatically. If both players exceed the target, the winner is the one closest to it.")
            print("-The deck contains 13 cards numbered 1 through 13 with no duplicates, so if one card is in a player's hand it cannot appear in the opponent's hand.")
            print("\n---Higher or Lower---")
            print(r"-Guess if the next number is going to be below the 'Current Number: ' or higher than it. Thats bout it ¯\_(ツ)_/¯")
            print("\n---Liar's Dice---")
            print("-Enter bids as two numbers: quantity then face (e.g., 3 5). Meaning you claim there is atleast 3 dice with the face of 5 across all board")
            print("-You cannot lower a bid’s quantity or face value.")
            print("-You can always call bluff instead of raising.")
            print("-The active player is highlighted in green at the top of the screen.")
            print("-Eliminated players are permanently out, no respawns, no spare dice.")

        elif action == 'r':
            day_income = player_data['gold'] - banked_gold

            time.sleep(2)
            os.system('cls')
            
            if day_income > 0:
                tax = int(day_income * 0.12)
                player_data['gold'] -= tax
                Print(f"**The Baron takes his cut of your earnings. -{tax} Gold**")
            else:
                Print("**You earned nothing today. The baron doesn't take any tax.**")

            player_data['day'] += 1
            return

        else:
            Print("\nPlease enter a valid input.")

        while current_minute >= 60:
            current_minute -= 60
            current_hour += 1

        if current_hour >= 17:
            break

        if current_hour >= 17:

            day_income = player_data['gold'] - banked_gold

            time.sleep(2)
            os.system('cls')
            
            if day_income > 0:
                tax = int(day_income * 0.12)
                player_data['gold'] -= tax
                Print(f"**The Baron takes his cut of your earnings. -{tax} Gold**")
            else:
                Print("**You earned nothing today. The baron doesn't take any tax.**")

            Print(f"\nThe village bell rings, it’s {current_hour}:00 PM. You head home")
            player_data['day'] += 1

            time.sleep(2)

# Function to play minigames against villagers
def minigame_hall(player_data, klare_data):

    global current_hour
    # Checks if the player wants to buy a pass or if they already have a lifetime pass
    if klare_data['basic_pass'] == False and klare_data['day_pass'] == False:

        while True:

            Print("\n[Guard] 35 gold to enter or 500 gold for a lifetime pass")
            Print("\n[1] Pay Entry Fee\n[2] Purchase a lifetime pass\n[r] Exit")
            action = input("Enter: ")
            
            if action == '1':
                Print("\n[Knight] Yes, here is 35 gold")
                if player_data['gold'] >= 35:
                    Print("-35 Gold")
                    Print("\n[Guard] You may enter")
                    player_data['gold'] -= 35
                    klare_data['day_pass'] = True
                    break
                
                else:
                    Print("\n[Guard] Thats not enough, best you get out of here")
            
            elif action == '2':
                Print("\n[Knight] Can I get a lifetime pass?")
                if klare_data['basic_pass'] == False:
                    if player_data['gold'] >= 500:
                        Print("-500 Gold")
                        Print("\n[Guard] Yeah sure, heres a lifetime pass man")
                        klare_data['basic_pass'] = True
                        klare_data['day_pass'] = True
                        player_data['gold'] -= 500
                        break

                    else:
                        Print("\n[Guard] Thats not enough, best you get a single pass")
                else:
                    Print("[Guard] You already have one...? I mean, if you want to buy another, go for it...")

            elif action == 'r':
                Print("[Knight] Actually maybe not")
                break

            else:
                Print("\nPlease Enter a valid input")
                
            
    elif klare_data['basic_pass'] == True:
        Print("\n[Guard] Alright, head in")
        klare_data['day_pass'] = True
        time.sleep(1.5)
        os.system('cls')

    print("\n-------------------------------------------------")

    while klare_data['day_pass'] == True:

        if current_hour >= 17:
            break
        
        print(f"\nGold: {player_data['gold']}")
        print("\n-----Minigame Hall-----")
        print(f"🟩 [1] Easy ({GREEN}unlocked{RESET})")

        # Medium unlocks when all easy villagers beaten
        easy_unlocked = len(klare_data['easy_beaten']) == 8
        print(f"🟨 [2] Medium {f'({RED}locked{RESET})' if not easy_unlocked else f'({GREEN}unlocked{RESET})'}")

        # Hard unlocks when all medium villagers beaten
        medium_unlocked = len(klare_data['medium_beaten']) == 8
        print(f"🟥 [3] Hard {f'({RED}locked{RESET})' if not medium_unlocked else f'({GREEN}unlocked{RESET})'}")

        print("🔎 [4] View Opponents Beaten")
        print("🚪 [r] Exit Minigame Hall")
        action = input("Enter: ")

        if player_data['gold'] < 20:
            minimum_bet = 1
        else:
            minimum_bet = 20

        # Easy difficulty
        if action == '1':

            # check whether player has over 50 gold to play liarsdice and select a random game
            if player_data['gold'] >= 50:
                random_game = random.choice(["rps", "21", "higherlower", "liarsdice"])
            else:
                random_game = random.choice(["rps", "21", "higherlower"])

            # setup difficulty and enemy names
            difficulty = "easy"
            enemy_name = random.choice(["Joe", "Bob", "Frank", "Sue", "Tom", "Lily", "Max", "Emma"])
            
            # Setup max bets on minigames and reducing it if the player has under the gold amount
            if player_data['gold'] >= 100:
                rps_max = 75
            else:
                rps_max = player_data['gold']

            if player_data['gold'] >= 115:
                twentyone_max = 115
            else:
                twentyone_max = player_data['gold']

            if player_data['gold'] >= 35:
                higherlower_max = 35
            else:
                higherlower_max = player_data['gold']

            # Allow debug mode to select the game
            if player_data['debugging'] == True:
                random_game = input("Which game? (rps/21/higherlower/liarsdice): ").lower()

            # play a random minigame
            if random_game == "rps":

                gold_bet = random.randint(minimum_bet, rps_max)
                
                Print(f"\nYou will play Rock Paper Scissors against {enemy_name} for {gold_bet} gold")

                play_rps(player_data, klare_data, difficulty, gold_bet, enemy_name, game_stats)

            elif random_game == "21":

                gold_bet = random.randint(minimum_bet, twentyone_max)

                Print(f"\nYou will play a game of 21 against {enemy_name} for {gold_bet} gold")

                play_21(player_data, klare_data, difficulty, gold_bet, enemy_name, game_stats)

            elif random_game == "higherlower":

                while True:
                
                    gold_bet = random.randint(minimum_bet, higherlower_max)

                    Print(f"\nYou will play Higher or Lower starting with {gold_bet} gold")
                    play_higherlower(player_data, klare_data, difficulty, gold_bet, game_stats)
                    break

            elif random_game == "liarsdice":

                gold_bet = 50
                enemy_count = 5 # only pick 5 of the 8 names
                possible_names = ["Joe", "Bob", "Frank", "Sue", "Tom", "Lily", "Max", "Emma"]
                enemy_names = random.sample(possible_names, 5)


                Print(f"\nYou will play Liars Dice against {enemy_count} others for {gold_bet * enemy_count} gold")

                play_liars_dice(player_data, klare_data, enemy_count, difficulty, game_stats, gold_bet, enemy_names)
            
            current_hour += random.randint(1, 3)

        # Medium difficulty
        elif action == '2':
            if len(klare_data['easy_beaten']) == 8:

                if player_data['gold'] < 40:
                    minimum_bet = 1
                else:
                    minimum_bet = 40

                # check whether player has over 75 gold to play liarsdice and select a random game
                if player_data['gold'] >= 75:
                    random_game = random.choice(["rps", "21", "higherlower", "liarsdice"])
                else:
                    random_game = random.choice(["rps", "21", "higherlower"])

                # setup difficulty and enemy names
                difficulty = "medium"
                enemy_name = random.choice(["Oliver", "Mia", "Liam", "Sophia", "Noah", "Ava", "Albert", "Ethan"])
                
                # Setup max bets on minigames and reducing it if the player has under the gold amount
                if player_data['gold'] >= 125:
                    rps_max = 125
                else:
                    rps_max = player_data['gold']

                if player_data['gold'] >= 250:
                    twentyone_max = 250
                else:
                    twentyone_max = player_data['gold']

                if player_data['gold'] >= 70:
                    higherlower_max = 70
                else:
                    higherlower_max = player_data['gold']

                # Allow debug mode to select the game
                if player_data['debugging'] == True:
                    random_game = input("Which game? (rps/21/higherlower/liarsdice): ").lower()

                # Pick a game
                if random_game == "rps":

                    gold_bet = random.randint(minimum_bet, rps_max)
                    
                    Print(f"\nYou will play Rock Paper Scissors against {enemy_name} for {gold_bet} gold")

                    play_rps(player_data, klare_data, difficulty, gold_bet, enemy_name, game_stats)

                elif random_game == "21":

                    gold_bet = random.randint(minimum_bet, twentyone_max)

                    Print(f"\nYou will play a game of 21 against {enemy_name} for {gold_bet} gold")

                    play_21(player_data, klare_data, difficulty, gold_bet, enemy_name, game_stats)

                elif random_game == "higherlower":
                    
                    gold_bet = random.randint(minimum_bet, higherlower_max)

                    Print(f"\nYou will play Higher or Lower starting with {gold_bet} gold")
                    play_higherlower(player_data, klare_data, difficulty, gold_bet, game_stats)

                elif random_game == "liarsdice":

                    gold_bet = 90
                    enemy_count = 5
                    possible_names = ["Oliver", "Mia", "Liam", "Sophia", "Noah", "Ava", "Ethan", "Albert"]
                    enemy_names = random.sample(possible_names, 5)

                    Print(f"\nYou will play Liars Dice against {enemy_count} others for {gold_bet * enemy_count} gold")

                    play_liars_dice(player_data, klare_data, enemy_count, difficulty, game_stats, gold_bet, enemy_names)
                
                current_hour += random.randint(1, 3)

            else:
                Print("\nYou need to beat all of the 'Easy Tier' villagers first")

        elif action == '3':
            if len(klare_data['medium_beaten']) == 8:
                if player_data['gold'] < 60:
                    minimum_bet = 1
                else:
                    minimum_bet = 60

                # check whether player has over 150 gold to play liarsdice and select a random game
                if player_data['gold'] >= 150:
                    random_game = random.choice(["rps", "21", "higherlower", "liarsdice"])
                else:
                    random_game = random.choice(["rps", "21", "higherlower"])

                # setup difficulty and enemy names
                difficulty = "hard"
                enemy_name = random.choice(["Charlotte", "Jack", "Amelia", "Henry", "Isabella"])
                
                # Setup max bets on minigames and reducing it if the player has under the gold amount
                if player_data['gold'] >= 150:
                    rps_max = 150
                else:
                    rps_max = player_data['gold']

                if player_data['gold'] >= 300:
                    twentyone_max = 300
                else:
                    twentyone_max = player_data['gold']

                if player_data['gold'] >= 150:
                    higherlower_max = 150
                else:
                    higherlower_max = player_data['gold']

                # Allow debug mode to select the game
                if player_data['debugging'] == True:
                    random_game = input("Which game? (rps/21/higherlower/liarsdice): ").lower()

                # Pick a game
                if random_game == "rps":

                    gold_bet = random.randint(minimum_bet, rps_max)
                    
                    Print(f"\nYou will play Rock Paper Scissors against {enemy_name} for {gold_bet} gold")

                    play_rps(player_data, klare_data, difficulty, gold_bet, enemy_name, game_stats)

                elif random_game == "21":

                    gold_bet = random.randint(minimum_bet, twentyone_max)

                    Print(f"\nYou will play a game of 21 against {enemy_name} for {gold_bet} gold")

                    play_21(player_data, klare_data, difficulty, gold_bet, enemy_name, game_stats)

                elif random_game == "higherlower":
                    
                    gold_bet = random.randint(minimum_bet, higherlower_max)

                    Print(f"\nYou will play Higher or Lower starting with {gold_bet} gold")

                    play_higherlower(player_data, klare_data, difficulty, gold_bet, game_stats)

                elif random_game == "liarsdice":

                    gold_bet = 150
                    enemy_count = 5
                    enemy_names = ["Charlotte", "Jack", "Amelia", "Henry", "Isabella"]

                    Print(f"\nYou will play Liars Dice against {enemy_count} others for {gold_bet * enemy_count} gold")

                    play_liars_dice(player_data, klare_data, enemy_count, difficulty, game_stats, gold_bet, enemy_names)
                
                current_hour += random.randint(1, 3)

            else:
                Print("\nYou need to beat all of the 'Medium Tier' villagers first")

        elif action == '4':
            os.system('cls')
            print("-----Villagers Beaten-----")

            print("\nEasy Tier:")
            for name in ["Joe", "Bob", "Frank", "Sue", "Tom", "Lily", "Max", "Emma"]:
                status = f"({GREEN}BEATEN{RESET})" if name in klare_data['easy_beaten'] else f"({RED}UNBEATEN{RESET})"
                print(f"{name}: {status}")

            print("\nMedium Tier:")
            for name in ["Oliver", "Mia", "Liam", "Sophia", "Noah", "Ava", "Albert", "Ethan"]:
                status = f"({GREEN}BEATEN{RESET})" if name in klare_data['medium_beaten'] else f"({RED}UNBEATEN{RESET})"
                print(f"{name}: {status}")

            print("\nHard Tier:")
            for name in ["Charlotte", "Jack", "Amelia", "Henry", "Isabella"]:
                status = f"({GREEN}BEATEN{RESET})" if name in klare_data['hard_beaten'] else f"({RED}UNBEATEN{RESET})"
                print(f"{name}: {status}")

            input("\nPress Enter to return: ")
            os.system('cls')

        elif action == 'r':
            break

        else:
            Print("\nPlease Enter a valid input")

# Klare Merchant
def klare_merchant(player_data, weapons_data, armour_data):
    Print("\n-----Klare Merchant-----")
    Print("[Old Merchant] Hello, Knight, What would you like to buy?")
    
    while True:
        if player_data['weapon_equipped'] not in player_data['owned_weapons']:
            player_data['owned_weapons'].append(player_data['weapon_equipped'])
        if player_data['armour_equipped'] not in player_data['owned_armour']:
            player_data['owned_armour'].append(player_data['armour_equipped'])

        print(f"\nYou have {player_data['gold']} Gold")

        print("\n-----Swords-----\n\n[1] Shadow Blade --3.3k Gold--")
        print("\n-----Bows-----\n\n[2] Composite Bow --4k Gold--")
        print("\n-----Spears-----\n\n[3] Rock Spear --3.5k Gold--\n[4] Baron's Spear --4.5k Gold--")
        print("\n-----Armour-----\n\n[5] Ash Armour --4.2k Gold--\n[6] Dragonite Armour --5.2k Gold--")
        print("\n-----Potions/Crystals-----\n\n[7] Health Potion --1k Gold--\n[8] Max Health Potion --1.7k Gold--")
        print("\n-----Items-----\n\n[9] Enchant Book --3.7k Gold--")
        print("\n[i] View Inventory\n[r] Exit")
        
        action = input("\nEnter: ").lower()


        # ----------------- Inventory -----------------
        if action == 'i':
            inventory_display(player_data, weapons_data, armour_data)
            continue


        # ----------------- Weapons -----------------
        if action in ['1','2','3','4']:
            weapon_map = {
                '1': ('Shadow Blade', 4100),
                '2': ('Composite Bow', 3100),
                '3': ('Rock Spear', 3500),
                '4': ("Baron's Spear", 4200)
            }

            weapon_name, cost = weapon_map[action]
            new_weapon = get_weapon_by_name(weapon_name)

            if player_data['gold'] < cost:
                Print("\n[Old Merchant] Sorry but you can't afford this item.")
                continue

            if weapon_name in player_data['owned_weapons']:
                Print(f"\n[Old Merchant] You already own the {weapon_name}.")
                continue

            Print(f"\n[Knight] I would like to see your {weapon_name}, please.")
            time.sleep(0.4)

            stat_comparison(
                get_weapon_by_name(player_data['weapon_equipped']),
                new_weapon,
                "weapon"
            )

            if input("\nPress Enter to confirm or 'r' to cancel: ").lower() == "r":
                Print("\n[Old Merchant] No worries, perhaps another time.")
                continue

            Print(f"\n-{cost} Gold")
            player_data['gold'] -= cost
            player_data['owned_weapons'].append(weapon_name)

            Print("\n[Old Merchant] Here you go, young one.")
            game_stats['items_bought'] += 1


        # ----------------- Armour -----------------
        elif action in ['5','6']:
            armour_map = {
                '5': ("Ash Armour", 4200),
                '6': ('Dragonite Armour', 5200)
            }

            armour_name, cost = armour_map[action]
            new_armour = get_armour_by_name(armour_name)

            if player_data['gold'] < cost:
                Print("\n[Old Merchant] Sorry but you can't afford this item.")
                continue

            if armour_name in player_data['owned_armour']:
                Print(f"\n[Old Merchant] You already own {armour_name}.")
                continue

            Print(f"\n[Knight] May I try on your {armour_name}?")
            time.sleep(0.4)

            stat_comparison(
                get_armour_by_name(player_data['armour_equipped']),
                new_armour,
                "armour"
            )

            if input("\nPress Enter to confirm or 'r' to cancel: ").lower() == "r":
                Print("\n[Old Merchant] Very well, knight.")
                continue

            Print(f"\n-{cost} Gold")
            player_data['gold'] -= cost
            player_data['owned_armour'].append(armour_name)

            old_def = get_equipped_armour_defence(player_data, armour_data)
            player_data['defence'] -= old_def

            player_data['armour_equipped'] = armour_name
            player_data['defence'] += new_armour['defence']

            Print("\n[Old Merchant] May it protect you in every battle ahead!")
            game_stats['items_bought'] += 1


        # ----------------- Items -----------------
        elif action == '7':
            if player_data['gold'] < 1000:
                Print("\n[Old Merchant] Sorry but you can't afford this item.")
                continue

            Print("\n-----Health Potion Stats-----\n+100 Health")
            if input("\nPress Enter to confirm or 'r' to cancel: ") == "":
                player_data['gold'] -= 1000
                player_data['health_potions'] += 1
                Print("\n[Old Merchant] Stay alive out there.")
                game_stats['items_bought'] += 1


        elif action == '8':
            if player_data['gold'] < 1700:
                Print("\n[Old Merchant] Sorry but you can't afford this item.")
                continue

            Print("\n-----Max Health Potion Stats-----\n+80 Max Health")
            if input("\nPress Enter to confirm or 'r' to cancel: ") == "":
                player_data['gold'] -= 1700
                player_data['max_health'] += 80
                Print("\n[Old Merchant] Your strength grows.")
                game_stats['items_bought'] += 1


        elif action == '9':
            if player_data['gold'] < 3700:
                Print("\n[Old Merchant] Sorry but you can't afford this item.")
                continue

            if input("\nPress Enter to confirm or 'r' to cancel: ") == "":
                player_data['gold'] -= 3700
                random_enchant(player_data, weapons_data)
                Print("\n[Old Merchant] I hope you enjoy your enchantment.")
                game_stats['items_bought'] += 1


        elif action == 'r':
            Print("\n[Old Merchant] I shall see you soon.")
            print("\n-------------------------------------------------------------------------")
            break

        else:
            Print("Please Enter a valid input.")

# -- Rest Of Game -- #

# Knight RPG intro
def intro():
    print("##########################################################################################################################################################")
    print("##   #####   ##      #######   ###         ####              #####    ########    ###             ######           #####          #####              #####")
    print("##   ####   ###   #   ######   ######   #####    #################    ########    #######    ###########   ####   ######   #####   ###    ################")
    print("##   ###   ####   ##   #####   ######   #####    #################    ########    #######    ###########   ####   ######   #####   ###    ################")
    print("##   ##   #####   ###   ####   ######   #####    #################    #######     #######    ###########         #######   #####  ####    ################")
    print("##      #######   ####   ###   ######   #####    #####          ##                #######    ###########   ###   #######         #####    #####          #")
    print("##   #   ######   #####   ##   ######   #####    #########   #####    ########    #######    ###########   ####   ######   ###########    ########    ####")
    print("##   ##   #####   ######   #   ######   #####    #########   #####    ########    #######    ###########   #####   #####   ###########    ########    ####")
    print("##   ###   ####   #######      ######   #######    #####    ######    ########    #######    ###########   ######   ####   ############    ######    #####")
    print("##   ####   ###   ########     ###         ######         ########    ########    #######    ###########   #######   ###   #############            ######")
    print("##########################################################################################################################################################")

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
        Print("[Queen] You have been tasked with slaying the dragon that dwells in the Caves of Hulpha. This will not be an easy quest, as you must journey through the dense Forest, Frozen Peaks, and the devilish corrupted village that is Klare.\n[Queen] Good luck, my brave knight. My kingdom and I will await your safe return.\n")
        time.sleep(1)
        Print("[Knight] I accept this quest, my queen. For your safety and for the honour of the kingdom, I shall slay the beast. The Frozen Peaks and the gambling of Klare will not stop me. I will come back safely.\n")
        time.sleep(1)
        Print("[Queen] Brave words knight, but strength alone will not defeat the dragon. You must use intelligence, patience, and follow your heart.\n[Queen] Go brave knight and may the gods be on your side ❤️")
        settings['skip_intro'] = True

    save_global_data(settings, game_stats)

    return settings

# Enemy Battle
def battle(player_data, game_stats):

    # Determine the current enemy based on location
    if player_data['location'] == 'Forest':
        current_enemy = enemy_data_forest()
        current_enemy['health'] += player_data['day']
        if player_data['day'] >= 10:
            current_enemy['strength'] += 1
    elif player_data['location'] == 'Frozen Peaks':
        current_enemy = enemy_data_frozen_peaks()
        # Scale HP
        current_enemy['health'] = max(1, current_enemy['health'] - 45 + int(3 * player_data['day']))
        # Scale damage
        scaling = max(0.5, player_data['day'] / 15)  
        current_enemy['strength'] = int(current_enemy['strength'] * scaling)

    elif player_data['location'] == 'Village of Klare':
        current_enemy = {"name": "Baron", "health": 1000, "strength": 145, "gold": 0}

    Print(f"\n{RED}-----Enemy Battle-----{RESET}\nYou encounter a {current_enemy['name']}!")

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
            if player_data['companions']:
                companion_damage = (random.randint(3, 5) * player_data['companions'])
            else:
                companion_damage = 0
                
            # Checks for critical hit
            crit_roll = random.randint(1, 100)
            if crit_roll <= player_data['crit_chance'] + crit_bonus:
                player_damage *= 2

                # Increase stat of critical hits by 1
                game_stats['critical_hits'] += 1

            # Increase stat of total damage dealt by player damage
            game_stats['total_damage_dealt'] += player_damage
                
            current_enemy['health'] -= player_damage
            current_enemy['health'] -= companion_damage
            
            if lifesteal_value > 0:
                drained = int(player_damage * (lifesteal_value / 100))
                player_data['health'] += drained
                      
            if current_enemy['health'] <= 0:
                Print(f"\nYou defeated the {current_enemy['name']}!")
                player_data['gold'] += current_enemy['gold']
                Print(f"You have {player_data['health']} health remaining, and received {current_enemy['gold']} gold")

                # Increase stat of enemies killed by 1
                game_stats['enemies_killed'] += 1

                break
            
            # Enemy Attacks
            enemy_damage = max(0, random.randint(base_enemy_damage - 3, base_enemy_damage + 5))

            if "Bow" in player_data['weapon_equipped']:
                dodge_roll = random.randint(1, 100)
                if dodge_roll <= 30:
                    game_stats['times_dodged'] += 1
                else:
                    player_data['health'] -= enemy_damage
                    if check_death(player_data, game_stats, current_enemy['name']):
                        return
            else:
                player_data['health'] -= enemy_damage
                if check_death(player_data, game_stats, current_enemy['name']):
                    return


    else:

        # Fight loop with text
        while player_data['health'] > 0 and current_enemy['health'] > 0:
            
            # Player Attacks
            player_damage = random.randint(max(1, true_damage - 3), true_damage + 5)

            # Checks for companion
            if player_data['companions']:
                companion_damage = (random.randint(3, 5) * player_data['companions'])
            else:
                companion_damage = 0
                
            # Checks for critical hit
            crit_roll = random.randint(1, 100)
            if crit_roll <= player_data['crit_chance'] + crit_bonus:
                Print("\nCritical Hit!")
                player_damage *= 2

                # Increase stat of critical hits by 1
                game_stats['critical_hits'] += 1
            
            # Increase stat of total damage dealt by player damage
            game_stats['total_damage_dealt'] += player_damage

            current_enemy['health'] -= player_damage
              
            # Sets enemy health to 0 if defeated by player
            if current_enemy['health'] <= 0:
                current_enemy['health'] = 0

            Print(f"\n[Knight] You attack the {current_enemy['name']} and deal {player_damage} damage! Health remaining: {current_enemy['health']}")
            if lifesteal_value > 0:
                drained = int(player_damage * (lifesteal_value / 100))
                player_data['health'] += drained
                Print(f"You gained {drained} health!\n")
              
            if companion_damage == 0:
                pass
            else:
                if current_enemy['health'] <= 0: # Skips companion attack if enemy is dead
                    pass
                else:
                    current_enemy['health'] -= companion_damage

                    # Sets enemy health to 0 if defeated by companion
                    if current_enemy['health'] <= 0:
                        current_enemy['health'] = 0

                    if player_data['companions'] == 1:
                        Print(f"Your companion does {companion_damage} damage! Health remaining: {current_enemy['health']}\n")
                    else:
                        Print(f"Your {player_data['companions']} companions do {companion_damage} damage! Health remaining: {current_enemy['health']}\n")

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
                
            if "Bow" in player_data['weapon_equipped']:
                dodge_roll = random.randint(1, 100)
                
                if dodge_roll <= 30:  # 30% chance to dodge
                    Print(f"[Enemy] You dodged the attack from the {current_enemy['name']}!")

                    # Increase game stat of times dodged by 1
                    game_stats['times_dodged'] += 1
                else:
                    Print(f"[Enemy] The {current_enemy['name']} does {enemy_damage} damage! Health remaining: {player_data['health']}")
                    if check_death(player_data, game_stats, current_enemy['name']):
                        return
                    
            else:
                Print(f"[Enemy] The {current_enemy['name']} does {enemy_damage} damage! Health remaining: {player_data['health']}")
                if check_death(player_data, game_stats, current_enemy['name']):
                    return
            
            time.sleep(1.4) # Delay Between attacks
            
        if player_data['health'] > 0:

            # Increase stat of enemies killed by 1
            game_stats['enemies_killed'] += 1

            # Play win message
            win_message = random.randint(1, 3)
            if win_message == 1:
                Print("\n[Knight] Ha! No enemy shall stop me from slaying the dragon!")
            elif win_message == 2:
                Print("\n[Knight] No beast shall stop my quest!")
            else:
                Print("\n[Knight] One enemy less between me and the dragon!")

# Main game loop
def start_story(player_data, settings, game_stats, klare_data):
    
    global healed_today, fight_boss, killed_baron, lost_to_baron
    
    if player_data['debugging'] == False:
        Print("\n-----Main Game-----")
        if player_data['day'] == 0:
            Print("You leave the castle and head out to the forest and setup a camp")
        time.sleep(2)
    else:
        player_data['max_health'] = 1000
        player_data['health'] = 1000
        player_data['gold'] = 100000
        player_data['health_potions'] = 999
        player_data['slime_kingdom'] = True

        owned_weapon_names = set(player_data['owned_weapons'])
        owned_armour_names = set(player_data['owned_armour'])

        added_weapons = []
        added_armour = []

        # Add missing weapon names
        for w in weapons():
            if w['name'] not in owned_weapon_names:
                player_data['owned_weapons'].append(w['name'])
                added_weapons.append(w['name'])

        # Add missing armour names
        for a in armour():
            if a['name'] not in owned_armour_names:
                player_data['owned_armour'].append(a['name'])
                added_armour.append(a['name'])
            
    # Increase stat of games played by 1
    game_stats['games_opened'] += 1

    while True:
        
        save_global_data(settings, game_stats)
        save_slot(current_slot, player_data, klare_data, weapons_data, armour_data, world_state)

        # Makes sure player health isnt above max health
        if player_data['health'] > player_data['max_health']:
            player_data['health'] = player_data['max_health']

        # Makes sure crit chance isnt above 100
        if player_data['crit_chance'] > 100:
            player_data['crit_chance'] = 100
            equipped_weapon = None
            for w in weapons_data:
                if w["name"] == player_data["weapon_equipped"]:
                    equipped_weapon = w
                    break
            equipped_weapon['crit_chance'] = 100

        
        # Starts the dragon fight on day 45
        if player_data['day'] == 45:
            break
            
        #Stops CMD from cleaning via stat_display before the text is finished being read    
        input("\nPress Enter to continue: ")
          
        stat_display(player_data)

        print(f"\n{display_random_tip()}")

        print("\n-----Choices-----")
        print("🗺️ [1] Explore\n🛏️ [2] Rest\n📦 [3] View Inventory\n⚙️ [4] Settings\n❓ [5] Help\n📝 [6] Update log\n👹 [7] Fight Zone Boss")
        
        if player_data['slime_kingdom']:
            print("👑 [8] Slime Kindom")
        if player_data['debugging']:
            print("🐒 [10] Debugging")
        action = input("Enter: ")
        
        if action == '1':
            
            # If the player is in the forest
            if player_data['location'] == 'Forest':
                explore_forest(player_data, weapons_data, game_stats)
                
            # If the player is in the frozen peaks        
            elif player_data['location'] == 'Frozen Peaks':
                explore_frozen_peaks(player_data, weapons_data, game_stats)
                
            # If the player is in Klare
            elif player_data['location'] == 'Village of Klare':
                explore_klare(player_data, weapons_data, armour_data, klare_data)
                
            healed_today = False
                
        elif action == '2':
            if healed_today == False:
                if player_data['location'] == "Forest":
                    player_data['max_health'] += 5
                    player_data['health'] = min(player_data['max_health'], player_data['health'] + 30)
                    Print("\n[Knight] I shall sit down to regain my strength (+30 Health, +5 Max Health)")
                    healed_today = True

                    # increase stat of times rested by 1
                    game_stats['times_rested'] += 1
                
                elif player_data['location'] == "Frozen Peaks":
                    player_data['max_health'] += 5
                    player_data['health'] = min(player_data['max_health'], player_data['health'] + 40)
                    Print("\n[Knight] I shall sit down to regain my strength (+40 Health, +5 Max Health)")
                    healed_today = True

                    # increase stat of times rested by 1
                    game_stats['times_rested'] += 1

                else:
                    Print("\nYou can't rest in Klare")

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
            while True:
                input("\nPress Enter to continue: ")
                os.system('cls') # Clear CMD
                Print("-----Help Menu-----")
                print("[1] How to win the game\n[2] Progressing through levels\n[3] What are enchants and how do they work?\n[4] List of enchants and their effects\n[5] How to spend gold and what to buy")
                print("[6] Understanding companions\n[7] How defence works\n[8] How critical hits work\n[9] Weapon Features\n[r] Return to main menu")
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
                    Print("Life Steal 3: +25% Life Steal")
                elif action == '5':
                    Print("\nGold can be spent at merchants and blacksmiths to buy weapons, armour, potions, and crystals. Merchants appear randomly during exploration, while blacksmiths are found in specific events. Use gold wisely to improve your stats and gear")
                elif action == '6':
                    Print("\nCompanions are allies that assist you in battle by dealing additional damage to enemies. They are found through exploration events and remain with you throughout your journey. Every time you get a new companion they will deal more damage")
                elif action == '7':
                    Print("\nDefence reduces the damage you take from enemies. It is primarily determined by the armour you have equipped. Upgrading your armour at blacksmiths or through events increases your defence. The stats of armour can be viewed in the armour stat's in the inventory")
                elif action == '8':
                    Print("\nCritical hits are powerful attacks that deal double damage. Your critical hit chance is determined by your weapon and any enchants applied to it. Higher critical hit chance increases the likelihood of landing a critical hit. This can be viewed in the weapon's stats in the inventory")
                elif action == '9':
                    Print("\nSwords work as you would expect, attack, get attacked, repeat. When using a bow you have a 30% chance to dodge an incoming attack, bows can also not be enchanted. Spears, have lower damage but an 80% critical hit rate, like bows they cannot be enchanted")
                elif action == 'r':
                    break
                else:
                    Print("\nPlease Enter a valid input")
                
        elif action == '6':
            updatelog()
            
        elif action == '7':

            global killed_baron
            
            os.system('cls') # Clear CMD

            # find the average damage of the player with enchants and crits
            weapon = get_weapon_by_name(player_data['weapon_equipped'])
            base_damage = get_equipped_weapon_damage(player_data, weapons_data)
            dmg_bonus, crit_bonus = get_enchant_bonus(weapon)
            # Apply enchant damage multiplier
            enchanted_damage = base_damage + int(base_damage * dmg_bonus)
            # Apply strength
            enchanted_damage += player_data['strength']
            # Total crit chance including Precision enchants
            total_crit = weapon['crit_chance'] + crit_bonus
            # Average damage over time factoring crits
            avg_damage = enchanted_damage * (1 + (total_crit / 100))
            Print(
                f"Your Health: {player_data['health']}, "
                f"Your Damage: {int(avg_damage)} (avg with crits and enchants), "
                f"Your Defence: {player_data['defence']}"
            )

            Print("\nHowler Recommended: 150 Health, 35 Damage, 10 Defence (Forest)")
            Print("Bigfoot Recommended: 500 Health, 80 Damage, 25 Defence (Frozen Peaks)")
            Print("Baron Recommended: 500 Health, 150 Damage, 40 Defence (Klare)")
            Print("Dragon Recommended: ???")

            if player_data['location'] == "Village of Klare":
                Print("\n**Note that you do not need to kill the Baron to fight the dragon**")
                action = input("\nAre you sure you want to fight a boss?\n\n[1] Baron\n[2] Dragon\n[3] No\nEnter: ")
            else:
                action = input("\nAre you sure you want to fight the boss?\n\n[1] Yes\n[2] No\nEnter: ")

            if action == '1':
                if player_data['location'] == 'Forest': # Fight Howler
                    fight_boss = True
                    battle(player_data, game_stats)
                    fight_boss = False
                    game_stats['bosses_killed'] += 1
                    player_data['location'] = 'Frozen Peaks'
                    healed_today = False
                    time.sleep(3)
                    os.system('cls')
                    Print("As you go to leave towards the Frozen Peaks you take a look back at the Howler's body and feel proud\n\nYou heal to full health")
                    player_data['health'] = player_data['max_health']
                    Print("\n------ FROZEN PEAKS ------")

                elif player_data['location'] == 'Frozen Peaks': # Fight Bigfoot
                    fight_boss = True
                    battle(player_data, game_stats)
                    fight_boss = False
                    game_stats['bosses_killed'] += 1
                    player_data['location'] = 'Village of Klare'
                    player_data['slime_kingdom'] = False
                    player_data['companions'] = 0
                    
                    healed_today = False
                    os.system('cls')
                    Print("As you leave the storm of the Frozen Peaks you look at Bigfoot's body and feel a sense of accomplishment")
                    if player_data['day'] < 30:

                        Print("\nYou wander into Klare and are immedietly caught by a guard and taken to a hotel.")
                        time.sleep(1.5)
                        Print("\n[Guard] The town is current on lockdown due to recent events, you will have to stay here for a while.")
                        time.sleep(1)
                        Print("\n[Knight] What happend??")
                        time.sleep(1.5)
                        Print("\n[Guard] Accomodation is on us, but you will have to stay here until further notice, here's 150 gold for your troubles.")
                        time.sleep(1)
                        Print("\nYou stay in the hotel, eating and resting until the lockdown is lifted.")

                        days_passed = 30 - player_data['day']
                        player_data['day'] = 30
                        player_data['health'] = player_data['max_health']
                        player_data['gold'] += 150

                        print(f"\n{days_passed} days later...")
                        time.sleep(1)
                        Print("\n--ANNOUNCEMENT--\n[Unknown] The lockdown has been lifted, I want everybody back to work.")

                    Print("\n------ VILLAGE OF KLARE -----")

                elif player_data['location'] == 'Village of Klare' and killed_baron == False: # Fight baron
                    Print("\n[Knight] Baron, for too long have you ruled this village unfairly.")
                    Print("[Knight] All you do is take take take, and today I'm taking your life. 1v1 me lil bro")
                    Print("\n[Baron] Hahaha, you cannot defeat me knight, not even close.")
                    battle(player_data, game_stats)
                    if lost_to_baron == False:
                        Print("\n[Baron] How did a... a weak, old, fat, pathetic, broke, useless, miserable fool of a knight defeat ME?")
                        Print("\n[Knight] Nobody asked nerd.")
                        game_stats['bosses_killed'] += 1         
                        world_state["killed_baron"] = True
                        killed_baron = True
                        apply_world_state_to_globals(world_state, globals())
                    else:
                        Print("\n\n[Baron] Haha, not even close knight, best you keep gambling and earning me money instead.")
                
                else:
                    Print("\nHe's already dead bro, calm down.")
            
            elif action == '2' and player_data['location'] == "Village of Klare": # Fight dragon
                os.system('cls')
                Print("[Knight] I shall challenge the dragon...")
                time.sleep(1)
                if killed_baron == True:
                    Print("\n[Literally the entire village] ...")
                else:
                    Print("\n[Literally the entire village and the baron] ...")
                time.sleep(2)
                Print("\n[Knight] FOR THE QUEEN AND THE KINGDOM!!!")
                time.sleep(2)
                break
                

        elif action == '8':
            if player_data['slime_kingdom']:
                slime_kingdom(player_data)

        elif action == '10':
            
            # Debugging Menu
            if player_data['debugging'] == True:
                print("\n---Debugging Menu---")
                action = input("\n[1] Set Max Health\n[2] Set Health\n[3] Set Strength\n[4] Set Defence\n[5] Set Current Armour\n[6] Set Gold\n[7] Set Location\n[8] Set Current Weapon\n[9] Roll Weapon Enchant\n[10] Set Current day\n[11] Set Crit chance\nEnter: ")
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
                    action = input("[1] Forest\n[2] Frozen Peaks\n[3] Village Of Klare\nEnter: ")
                    if action == '1':
                        player_data['location'] = 'Forest'
                    elif action == '2':
                        player_data['location'] = 'Frozen Peaks'
                        player_data['max_health'] = 300
                        player_data['health'] = 250
                        player_data['strength'] = 35
                        player_data['defence'] = 10
                        player_data['day'] = 15
                    elif action == '3':
                        player_data['location'] = 'Village of Klare'
                        player_data['gold'] = 300
                elif action == '8':
                    new_weapon = input("Set Current Weapon: ")
                    player_data['weapon_equipped'] = new_weapon
                    player_data['owned_weapons'].append(new_weapon)
                elif action == '9':
                    random_enchant(player_data, weapons_data)
                elif action == '10':
                    player_data['day'] = int(input("Set Current Day: "))
                elif action == '11':
                    player_data['crit_chance'] = int(input("Set Crit Chance: "))

        elif action == 'debug enable':
            player_data['debugging'] = True

        elif action == 'debug disable':
            player_data['debugging'] = False

        else:
            print("That is not a valid input")
        
        save_global_data(settings, game_stats)

# Display different dragon based on health
def display_dragon_health(current_enemy):
    if current_enemy['health'] >= 1000:
        print(r"####### ################ #######")
        print(r"######   ##############   ######")
        print(r"#####                      #####")
        print(r"###     \              /     ###")
        print(r"###      \            /      ###")
        print(r"###       /\        /\       ###")
        print(r"###      |  |      |  |      ###")
        print(r"####      \/   | |  \/      ####")
        print(r"#####                      #####")
        print(r"#####                      #####")
        print(r"######   \/\/\/\/\/\/\/   ######")
        print(r"########                ########")
        print(r"##########            ##########")
        print(r"################################")
    
    elif current_enemy['health'] >= 750:
        print(r"####### ################ #######")
        print(r"######   ##############   ######")
        print(r"#####                      #####")
        print(r"###     \              /     ###")
        print(r"###      \            /      ###")
        print(r"###       /\        /\       ###")
        print(r"###      |  |      |  |      ###")
        print(r"####      \/   | |  \/      ####")
        print(r"#####                 ##   #####")
        print(r"#####                 ##   #####")
        print(r"######   \/\/\/\/\  \/\/  ######")
        print(r"########                ########")
        print(r"##########            ##########")
        print(r"################################")

    elif current_enemy['health'] >= 500:
        print(r"####### ################ #######")
        print(r"######   ##############   ######")
        print(r"#####                      #####")
        print(r"###     \              /     ###")
        print(r"###      \            /      ###")
        print(r"###       /\                 ###")
        print(r"###      |  |      ====      ###")
        print(r"####      \/   | |          ####")
        print(r"#####                 ##   #####")
        print(r"#####                 ##   #####")
        print(r"######   \/\/\/\/\  \/\/  ######")
        print(r"########                ########")
        print(r"##########            ##########")
        print(r"################################")

    elif current_enemy['health'] >= 250:
        print(r"####### ################ #######")
        print(r"######   ##############   ######")
        print(r"#####                      #####")
        print(r"###     \     ##       /     ###")
        print(r"###           ##      /      ###")
        print(r"###       /\                 ###")
        print(r"###      |  |      ====      ###")
        print(r"####      \/   |\           ####")
        print(r"#####   ##              ## #####")
        print(r"#####   ##              ## #####")
        print(r"######   \/   /\/\  \/\/  ######")
        print(r"########                ########")
        print(r"##########            ##########")
        print(r"################################")

# Ending fight
def start_ending(player_data, game_stats):

    current_enemy = {"name": "Dragon", "health": 1500, "strength": 190, "gold": 10000}

    Print(f"\n{RED}-----FINAL BATTLE-----{RESET}")
    Print(f"You walk up to the enterance of the Dragon's Lair and draw your weapon.")

    # Clamp player HP to max
    player_data['health'] = min(player_data['health'], player_data['max_health'])

    # Get equipped weapon data
    equipped_weapon = next((w for w in weapons_data if w['name'] == player_data['weapon_equipped']), None)
    if not equipped_weapon:
        Print("Error: Equipped weapon not found!")
        return

    # Base player damage
    true_damage = equipped_weapon['damage'] + player_data['strength']

    # Enchant / Crit / Lifesteal data
    crit_bonus = 0
    lifesteal_value = 0

    if equipped_weapon['special'] != "None":
        enchant = equipped_weapon['special']

        if enchant.startswith("Strength"):
            strength_level = int(enchant.split()[1])
            strength_multiplier = {1: 0.35, 2: 0.75, 3: 1.50}[strength_level]
            true_damage += int(true_damage * strength_multiplier)

        elif enchant.startswith("Precision"):
            crit_bonus += int(enchant.split()[1]) * 25

        elif enchant.startswith("Life Steal"):
            lifesteal_value = {1: 10, 2: 15, 3: 20}[int(enchant.split()[2])]

    # Dragon damage
    base_enemy_damage = max(0, current_enemy['strength'] - player_data['defence'])

    # ========= DRAGON BATTLE LOOP =========
    while player_data['health'] > 0 and current_enemy['health'] > 0:

        display_dragon_health(current_enemy)

        # ---- Player attacks ----
        player_damage = random.randint(max(1, true_damage - 5), true_damage + 7)

        # Critical hit
        crit_roll = random.randint(1, 100)
        if crit_roll <= player_data['crit_chance'] + crit_bonus:
            Print("\nCritical Hit!")
            player_damage *= 2
            game_stats['critical_hits'] += 1

        # Track damage dealt
        game_stats['total_damage_dealt'] += player_damage

        # Apply damage to dragon
        current_enemy['health'] -= player_damage
        if current_enemy['health'] < 0:
            current_enemy['health'] = 0

        Print(f"\n[Knight] You attack the Dragon for {player_damage} damage! Dragon HP: {current_enemy['health']}")

        # Lifesteal
        if lifesteal_value > 0:
            drained = int(player_damage * (lifesteal_value / 100))
            player_data['health'] += drained
            Print(f"You gained {drained} health!\n")

        # Dragon defeated
        if current_enemy['health'] <= 0:
            Print("\nTHE DRAGON FALLS!")
            player_data['gold'] += 10000
            Print(f"\nYou gain 10000 gold!")
            break

        # ---- Dragon attacks ---- #
        enemy_damage = random.randint(max(0, base_enemy_damage - 5), max(0, base_enemy_damage + 7))

        # Dodge if bow equipped
        if "Bow" in player_data['weapon_equipped']:
            dodge_roll = random.randint(1, 100)
            if dodge_roll <= 30:
                Print("[Dragon] You dodged the attack!")
                game_stats['times_dodged'] += 1
                time.sleep(2)
                continue

        # Apply dragon damage
        player_data['health'] -= enemy_damage
        if player_data['health'] < 0:
            player_data['health'] = 0

        Print(f"[Dragon] The dragon hits you for {enemy_damage} damage! Health remaining: {player_data['health']}")

        check_death(player_data, game_stats)

        time.sleep(2)

    # ---- Victory ---- #
    if player_data['health'] > 0:
        game_stats['enemies_killed'] += 1
        game_stats['bosses_killed'] += 1
        player_data['dragon_defeated'] = True
        player_data['owned_weapons'].append("Dragon Sword")
        player_data['owned_armour'].append("Dragon Armour")

        Print("\n[Knight] At last... the kingdom is safe")

        time.sleep(2)
        Print("\nYou travel back to the castle, and the people watch you as you make your way into the throne room.")
        
        time.sleep(3)
        Print("\n[Knight] Queen... the dragon is dead.")

        time.sleep(3)
        Print("\n[Queen] Well done knight, you have done what only one person ever could, and what many said was impossible.")
        Print("[Queen] The dragon of Hulpha is no more, and the road through the Forest, Frozen Peaks, and Klare is safe once again.")
        time.sleep(2)

        Print("\n[Knight] I thank you, my queen. There were many dangers, but the thought of this kingdom kept me going")
        time.sleep(2)

        Print("\n[Queen] You faced more than danger knight.")
        Print("[Queen] You faced the entire world and everything it threw at you.")
        time.sleep(2)

        Print("\n[Knight] Every battle was worth it, knowing it will help our people sleep in peace.")
        time.sleep(3)

        Print("\n[Queen] The kingdom owes you a debt that cannot be repaid in gold or praise alone.")
        Print("[Queen] You will forever be remembered as the Knight of Hulpha, the one who ended the dragon’s reign.")
        time.sleep(3)

        Print("\n[Knight] Thank you, Queen. But I ask for no legacy or no legend. I just ask that the kingdom be built without fear.")
        time.sleep(2)

        Print("\n[Queen] And so it shall. Rest now, knight.\n[Queen] Your quest is complete 💖.")

        input("\n\nAnd good work player, I hope you enjoyed the game and thank you so much for playing c:\n\nPress Enter to exit: ")

# Checks if the player has died
def check_death(player_data, game_stats, enemy_name=None):
    if player_data['health'] <= 0:

        if player_data['health_potions'] > 0:
            player_data['health_potions'] -= 1
            Print("\nYou used a health potion to save yourself from dying!\n+10 Health")
            player_data['health'] = 10
            game_stats['health_potions_used'] += 1
            return False
        
        if enemy_name == "Baron":
            global lost_to_baron
            if player_data['health'] <= 0:
                player_data['health'] = player_data['max_health']
                player_data['gold'] = 50
                lost_to_baron = True
                return True
            else:
                return False

        else:
            game_stats['battles_lost'] += 1
            game_over()

    return False

# If player dies
def game_over():

    Print("\nYou have unfortunately died, failing to slay the dragon and save the kingdom")

    reset_world_state(globals())

    player_data = main_player()

    world_state = get_world_state_from_globals(globals())

    save_slot(current_slot, player_data, klare_data, weapons_data, armour_data, world_state)

    action = input("Press 1 to Play Again or press Enter to exit\nEnter: ")
    if action == '1':
        os.system('cls')
        start_game()
        
    else:
        sys.exit()

try:
    start_game()

except Exception:
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("\n====================\n")
        f.write(f"Crash Time: {datetime.now()}\n\n")
        f.write(traceback.format_exc())

    print("\nAn error occurred 😊")
    print("Crash details were written to crash_log.txt.")
    input("\nPress Enter to exit...")

# V6

# make crit chance update correctly in merchants and make them equip swords when you buy them.

# uknown bug where after some exploration events bronze sword stat comparison shows up and ends day early...?
# I just viewed bronze sword stats in inventory before exploring

# idea of showing enemy stats before battle and showing the enemy scaling on its stats like "You encounter a bandit (100 health | 10 strength +2 from enemy scaling)"

# add a bug event in frozen peaks (1% chance) where you 1v1 a bug enemy and if you lose it crashes the game.

# add arena to slime kingdom or even just for free where you can fight enemies for gold. (like 3 max each day) MAYBE tiers so its like a boss fight
# where you can see the enemy HP and attack plus the gold reward.

# Make slime kingdom event like 10% chance (or force it to happen atleast once) and move a forest event to the frozen peaks.

# make changes to if you say youve seen bob to hunters without having seen him (like they have bob and he says you helped him or sum)

# EXPAND THE TALL METAL CROSS to feel like a maze before enemy and reward

# achievements

# fix frozen peakjs endless road reused stuff (lazy guy over here)
# update endless storm frozen peaks, try and not sound like a copy and paste

# make a "Elite" difficulty above hard for each minigame where the enemy gets a hint like what ALL your cards are in 21
# or 1 option you DIDNT pick in RPS.
# or what 3 of the peoples dice are in liars dice instead of 2

# add a gambling game where its like the impossible quiz but 10 gold per attempt.

# V5.1

#add confirmation to upgrading armour dawg (snow wanderer)
#make items auto equip and stuff.
#fix slime kingdom navigation feeling like poo
#add a cap of like 200 gold to the middle aged man
#snow wanderer says +50 health for potion when its actually 75
#------ VILLAGE OF KLARE ----- <-- theres one less dash on the right side
#-The rules are not to reach 21 without exceeding it. <-- Bad wording
#killing baron removes guard from the minigame hall