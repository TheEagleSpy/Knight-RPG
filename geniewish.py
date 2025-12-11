from functools import partial

def reward_strength(player_data):
    player_data['strength'] += 2
    print("Your strength has increased by 2!")

def reward_max_health(player_data):
    player_data['max_health'] += 15
    print("Your max health has increased by 15!")

def reward_health(player_data):
    player_data['health'] += 35
    print("Your health has increased by 35!")

def reward_gold(player_data):
    player_data['gold'] += 75
    print("You received an extra 75 gold!")

def reward_defence(player_data):
    player_data['defence'] += 2
    print("Your defence has increased by 2!")
    
def reward_crit(player_data):
    player_data['crit'] += 7
    print("Your critical chance has increased by 7%!")

def reward_armour(player_data, armour_data):
    for armour in armour_data:
        if armour['name'] == player_data['armour_equipped']:
            armour['defence'] += 3
            player_data['defence'] += 3
            print(f"Your {armour['name']} has been upgraded!\n+3 Armour Toughness")
        
def reward_weapon(player_data, weapons_data):
    for weapon in weapons_data:
        if weapon['name'] == player_data['weapon_equipped']:
            weapon['damage'] += 2
            print(f"Your {weapon['name']} has been upgraded!\n+2 Damage")

def geniewish(player_data, weapons_data, armour_data):
    wish_rewards = {
        "strength": reward_strength,
        "stronger": reward_strength,
        "power": partial(reward_weapon, weapons_data=weapons_data),
        "max health": reward_max_health,
        "vitality": reward_max_health,
        "endurance": reward_max_health,
        "health": reward_health,
        "restore": reward_health,
        "heal": reward_health,
        "gold": reward_gold,
        "wealth": reward_gold,
        "riches": reward_gold,
        "defence": reward_defence,
        "protection": reward_defence,
        "shield": reward_defence,
        "armour": partial(reward_armour, armour_data=armour_data),
        "equipment": partial(reward_armour, armour_data=armour_data),
        "fortification": partial(reward_armour, armour_data=armour_data),
        "an upgrade": reward_defence,
        "toughness": reward_defence,
        "upgrades": reward_defence,
        "weapon": partial(reward_weapon, weapons_data=weapons_data),
        "sword": partial(reward_weapon, weapons_data=weapons_data),
        "blade": partial(reward_weapon, weapons_data=weapons_data),
        "damage": partial(reward_weapon, weapons_data=weapons_data),
        "attack": partial(reward_weapon, weapons_data=weapons_data),
        "critical": reward_crit,
        "intelligence": reward_crit,
        "luck": reward_crit,
        "wisdom": reward_crit,
        "skill": reward_crit,
    }

    print("[Genie] Welcome, I shall grant you 3 wishes! However you must say the right word otherwise I will not grant them!")

    for wish_num in range(3):
        wish = input("\nI wish for: ").strip().lower()
        
        # Check if any keyword is contained in the wish
        matched_reward = None
        for keyword, reward_function in wish_rewards.items():
            if keyword in wish:  # Check if the keyword is in the input string
                matched_reward = reward_function
                break  # Stop searching after finding the first match
        
        if matched_reward:
            matched_reward(player_data)  # Grant the reward
            print(f"\n[Genie] Your wish for '{wish}' has been granted!")
        else:
            print(f"\n[Genie] Your wish for '{wish}' is unrecognized, Sorry")