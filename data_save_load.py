import os, json
from datetime import datetime

SAVE_FOLDER = "saves"
MAIN_FILE = "globalsavedata.json"
MAX_SLOTS = 3
DEBUG_SLOT = "save_debug.json"

if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

def view_game_stats(game_stats):
    os.system('cls')
    print("----- Game Stats -----")
    for key, value in game_stats.items():
        formatted_key = key.replace('_', ' ').title()
        print(f"{formatted_key}: {value}")
    print("\n-------------------------------------------------------------------------")
    input("\nPress Enter to return to Settings: ")

def get_slot_path(slot):
    if slot == "debug":
        return os.path.join(SAVE_FOLDER, DEBUG_SLOT)
    return os.path.join(SAVE_FOLDER, f"save_slot_{slot}.json")

def slot_exists(slot):
    return os.path.exists(get_slot_path(slot))

def list_save_slots():
    slots = []
    for i in range(1, MAX_SLOTS + 1):
        path = get_slot_path(i)
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                    meta = data.get("metadata", {})
            except json.JSONDecodeError:
                meta = {}
            slots.append({"slot": i, "exists": True, "meta": meta})
        else:
            slots.append({"slot": i, "exists": False, "meta": {}})
    return slots

def get_world_state_from_globals(global_dict):
    return {
        k: v for k, v in global_dict.items()
        if not k.startswith("__")
        and not callable(v)
        and isinstance(v, (bool, int, float, str))
    }

def apply_world_state_to_globals(world_state, global_dict):
    for k, v in world_state.items():
        global_dict[k] = v

def save_global_data(settings, game_stats):
    with open(MAIN_FILE, "w") as f:
        json.dump({
            "settings": settings,
            "game_stats": game_stats
        }, f, indent=4)

def load_global_data():
    defaults = get_default_values()
    if not os.path.exists(MAIN_FILE):
        save_global_data(defaults["settings"], defaults["game_stats"])
        return defaults["settings"], defaults["game_stats"]

    try:
        with open(MAIN_FILE, "r") as f:
            data = json.load(f)
        settings = data.get("settings", defaults["settings"])
        stats = data.get("game_stats", defaults["game_stats"])
        return settings, stats
    except (json.JSONDecodeError, FileNotFoundError):
        save_global_data(defaults["settings"], defaults["game_stats"])
        return defaults["settings"], defaults["game_stats"]

def save_slot(slot, player_data, klare_data, weapons_data, armour_data, world_state):
    metadata = {
        "slot_number": slot,
        "last_played": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "day": player_data.get("day", 1),
        "location": player_data.get("location", "Forest"),
    }

    path = get_slot_path(slot)
    with open(path, "w") as save_file:
        json.dump({
            "metadata": metadata,
            "player_data": player_data,
            "klare_data": klare_data,
            "weapons_data": weapons_data,
            "armour_data": armour_data,
            "world_state": world_state
        }, save_file, indent=4)

def load_slot(slot):
    from data_save_load import get_default_values
    path = get_slot_path(slot)
    if not os.path.exists(path):
        return None

    with open(path, "r") as f:
        data = json.load(f)

    defaults = get_default_values()
    # Merge missing keys into loaded data
    player = {**defaults["player_data"], **data.get("player_data", {})}
    klare = {**defaults["klare_data"], **data.get("klare_data", {})}
    weapons = data.get("weapons_data", defaults["weapons_data"])
    armour  = data.get("armour_data",  defaults["armour_data"])
    world = {**defaults["world_state"], **data.get("world_state", {})}

    data["player_data"] = player
    data["klare_data"] = klare
    data["weapons_data"] = weapons
    data["armour_data"] = armour
    data["world_state"] = world
    return data

def delete_slot(slot):
    path = get_slot_path(slot)
    if os.path.exists(path):
        os.remove(path)

def get_default_values():
    default_settings = {
        "skip_battles": False,
        "skip_intro": False,
        "enter_to_continue": True,
    }

    default_stats = {
        "games_played": 0,
        "bosses_killed": 0,
        "enemies_killed": 0,
        "gold_earned": 0,
        "battles_lost": 0,
        "total_damage_dealt": 0,
        "critical_hits": 0,
        "times_dodged": 0,
        "health_potions_used": 0,
        "days_survived": 0,
        "items_bought": 0,
        "minigames_played": 0,
        "gambles_won": 0,
        "gambles_lost": 0,
        "times_rested": 0,
        "good_events": 0,
        "bad_events": 0,
    }

    default_player_data = {
        "max_health": 100,
        "health": 100,
        "strength": 0,
        "defence": 0,
        "gold": 0,
        "day": 1,
        "location": "Forest",
        "health_potions": 0,
        "armour_equipped": "No Armour",
        "weapon_equipped": "Bronze Sword",
        "crit_chance": 9,
        "owned_weapons": ["Bronze Sword"],
        "owned_armour": ["No Armour"],
        "companions": 0,
        "slime_kingdom": False,
        "beaten_game": False,
        "debugging": False,
    }

    default_klare_data = {
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

    default_weapons_data = [

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

    default_world_state = {
        "healed_today": True,
        "upgraded_armour": False,
        "helped_bob": False,
        "seen_bob": False,
        "seen_bounty_hunter": False,
        "killed_baron": False,
        "storm_power": 0,
        "picked_events_left": 0,
        "colours_left": 5,
        "memory_sequence": [],
    }

    return {
        "settings": default_settings,
        "game_stats": default_stats,
        "player_data": default_player_data,
        "klare_data": default_klare_data,
        "weapons_data": default_weapons_data,
        "armour_data": armour_data,
        "world_state": default_world_state,
    }

def reset_world_state(global_dict):
    apply_world_state_to_globals(get_default_values()["world_state"], global_dict)