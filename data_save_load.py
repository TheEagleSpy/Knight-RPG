import os
import json

# View game stats
def view_game_stats(game_stats):
    os.system('cls') # Clear CMD
    print("-----Game Stats-----")
    print(f"Games Played: {game_stats['games_played']}")
    print(f"Bosses Killed: {game_stats['bosses_killed']}")
    print(f"Enemies Killed: {game_stats['enemies_killed']}")
    print(f"Battles Won: {game_stats['battles_won']}")
    print(f"Battles Lost: {game_stats['battles_lost']}")
    print(f"Total Damage Dealt: {game_stats['total_damage_dealt']}")
    print(f"Critical Hits: {game_stats['critical_hits']}")
    print(f"Times Dodged: {game_stats['times_dodged']}")
    print(f"Health Potions Used: {game_stats['health_potions_used']}")
    print(f"Days Survived: {game_stats['days_survived']}")
    print(f"Items Bought: {game_stats['items_bought']}")
    print(f"Minigames Played: {game_stats['minigames_played']}")
    print(f"Gambles Won: {game_stats['gambles_won']}")
    print(f"Gambles Lost: {game_stats['gambles_lost']}")
    print(f"Times Rested: {game_stats['times_rested']}")
    print(f"Good Events: {game_stats['good_events']}")
    print(f"Bad Events: {game_stats['bad_events']}")
    print("\n-------------------------------------------------------------------------")
    input("\nPress Enter to return to Settings: ")

# Function to save all data to a JSON file
def save_all(file_name, settings, game_stats):
    combined_data = {
        "settings": settings,
        "game_stats": game_stats
    }
    with open(file_name, 'w') as save_file:
        json.dump(combined_data, save_file, indent=4)

# Function to load all data from a JSON file
def load_all(file_name):
    default_settings = {
        "skip_battles": False,
        "debugging": False,
        "skip_intro": False,
        "enter_to_continue": True,
    }

    default_stats = {
        "games_played": 0,
        "bosses_killed": 0,
        "enemies_killed": 0,
        "battles_won": 0,
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

    if not os.path.exists(file_name) or os.path.getsize(file_name) == 0:
        save_all(file_name, default_settings, default_stats)
        return default_settings, default_stats

    try:
        with open(file_name, 'r') as save_file:
            data = json.load(save_file)
        settings = data.get("settings", default_settings)
        stats = data.get("game_stats", default_stats)
        return settings, stats
    except (json.JSONDecodeError, FileNotFoundError):
        print("Save file corrupted. Resetting to defaults.")
        save_all(file_name, default_settings, default_stats)
        return default_settings, default_stats
