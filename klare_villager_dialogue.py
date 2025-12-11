import random, time

from printdelay import Print

# Tracks which villager has been spoken to today
villagers_talked = {
    "terry": False,
    #"james": False,
    #"finn": False,
    "albert": False,
    "emily": False,
    #"lucy": False
    }


def talk_to_villagers(player_data):
    global villagers_talked

    day = player_data['day']

    # Get a list of villagers you haven't talked to yet
    available = [v for v, talked in villagers_talked.items() if not talked]
    if not available:
        Print("\nYou head out to chat but nobody seems to take notice of you.")
        return

    # Randomly pick a villager from those not yet talked to
    chosen = random.choice(available)

    if chosen == "terry":
        talk_to_terry(day, player_data)
    elif chosen == "james":
        talk_to_james(day)
    elif chosen == "finn":
        talk_to_finn(day)
    elif chosen == "albert":
        talk_to_albert(day)
    elif chosen == "emily":
        talk_to_emily(day, player_data)
    elif chosen == "lucy":
        talk_to_lucy(day)

    # Mark that villager as talked to for the day
    villagers_talked[chosen] = True

def reset_villagers_talked():
    global villagers_talked
    for v in villagers_talked:
        villagers_talked[v] = False

def talk_to_terry(day, player_data):

    # ---- DAY 30 - 35 ----
    if 30 <= day <= 35:

        Print("\n[Villager] Hello knight, hope you brought gold along from your adventures. That's the only thing left in Klare")
        time.sleep(1)
        Print("\n[Knight] Who are you?")
        time.sleep(1)
        Print("\n[Terry] I'm Terry")
    
        while True:
            print("\n[1] You sound bitter Terry")
            print("[2] What do you mean it's the only thing left?")
            print("[3] Can you spare some gold?")
            choice = input("Enter: ")

            # ---- 1. You sound bitter ----
            if choice == '1':
                Print("\n[Terry] Bitter? Maybe... But when you've sold everything worth anything, words come cheap")
                time.sleep(1)
                Print("\n[Knight] Maybe you just need a new start")
                time.sleep(1)
                Print("\n[Terry] Heh. New starts cost gold too")
                return
                
            # ---- 2. What do you mean? ----
            elif choice == '2':
                Print("\n[Terry] I mean nothing here has value anymore. That sword of yours? Worthless, since no one can afford it.")
                time.sleep(1)
                Print("\n[Knight] Then how's a merchant still in business?")
                time.sleep(1)
                Print("\n[Terry] He sells to the rich, and sells us our only food.")
                
                while True:
                    print("\n[1] Tell me more about the merchant")
                    print("[2] We should rob the merchant then")
                    print("[r] Leave")
                    mini_choice = input("Enter: ")

                    # Ask more about him
                    if mini_choice == '1':
                        Print("\n[Terry] He came here when Klare was still normal. Good thinking, bad timing.")
                        time.sleep(1)
                        Print("\n[Knight] Why doesn't he leave? He obviously has the money to do so")
                        time.sleep(1)
                        Print("\n[Terry] He has connections that even the Baron does not, and so he is kept around.")
                        return
                    
                    # Robbing comment
                    elif mini_choice == '2':
                        Print("\n[Terry] Rob him? With what? Our fists? Believe it or not, he has guards protecting him these days, you are not the first with this idea.")
                        return
                    
                    elif mini_choice == 'r':
                        return
                    
                    else:
                        Print("\nPlease Enter a valid input")

            # ---- 3. Spare some gold? ----
            elif choice == '3':
                Print("\n[Terry] Spare gold? Ha! I wouldn't give it away if I was the richest man here. Make sure you don't ever either")
                
                while True:
                    print("\n[1] Pleaaase?")
                    print("[2] Gold can’t be that hard to get?")
                    print("[3] I have plenty on me right now though")
                    print("[r] Leave")
                    mini_choice = input("Enter: ")

                    if mini_choice == '1':
                        Print("\n[Terry] No gold comes free. Not here, not anymore.")
                        return

                    elif mini_choice == '2':
                        Print("\n[Terry] Try earning some then. Come see me tomorrow when you have nothing.")
                        return
                    
                    elif mini_choice == '3':
                        Print("\n[Terry] Then best you use it wisely.")
                        return
                    
                    elif mini_choice == 'r':
                        return
                    
                    else:
                        Print("\nPlease Enter a valid input")

            else:
                Print("\nPlease Enter a valid input")

    # ---- DAYS 36 - 40 ----
    elif 36 <= day <= 40:

        Print("\n[Terry] Supprised to see you still sane. I didn't think you'd last this long.")
        time.sleep(1)
        Print("\n[Knight] I am a knight after all.")
        time.sleep(1.5)
        Print("[Knight] You make it sound difficult to live here.")
        time.sleep(1)
        Print("\n[Terry] It is. I'm sure you've talked to the others by now. Now, they were no knights, but still good people once, look at them now.")

        while True:
            print("\n[1] I'm literally winning so much gold right now it's crazy.")
            print("[2] Do you have any news from town?")
            print("[3] Why are you legit so negative Terry?")
            print("[4] How are you still sane if everybody else isn't?")
            choice = input("Enter: ")

            # ---- 1. Bragging about gold ----
            if choice == '1':
                Print("\n[Terry] Good. Enjoy it while the tables stay fair.")
                time.sleep(1)
                Print("\n[Knight] What do you mean?")
                time.sleep(1)
                Print("\n[Terry] Do you really think they'll let you walk away with money and not be mad?")
                return

            # ---- 2. News from town ----
            elif choice == '2':
                Print("\n[Terry] The merchant seems scared. There's more guards around him than usual.")
                time.sleep(1)
                Print("\n[Knight] Do you know why he would need MORE guards?")
                time.sleep(1)
                Print("\n[Terry] No clue. Something's definitely weird about it though.")

                while True:
                    print("\n[1] Do you think someone’s planning to rob him?")
                    print("[2] Maybe he's hiding something now?")
                    print("[r] Leave")
                    mini_choice = input("Enter: ")

                    if mini_choice == '1':
                        Print("\n[Terry] Wouldn’t surprise me.")
                        time.sleep(1)
                        Print("\n[Knight] You'd think guards would be the last thing to add if that was the case.")
                        time.sleep(1)
                        Print("\n[Terry] Maybe he knows something we don't.")
                        return

                    elif mini_choice == '2':
                        Print("\n[Terry] The merchant's always been strange.")
                        time.sleep(1)
                        Print("\n[Knight] Strange how?")
                        time.sleep(1)
                        Print("\n[Terry] A rich man shows up in Klare and has never lost a bet, yet only bets a couple days a year.")
                        time.sleep(1)
                        Print("\n[Knight] Would it not be because he owns the only store in town?")
                        time.sleep(1)
                        Print("\n[Terry] My point exactly, if he's greedy enough to stay in town, I'd guess he'd want to bet everyday.")
                        time.sleep(1)
                        Print("\n[Knight] Sounds sus.")
                        time.sleep(1)
                        Print("\n[Terry] Yeah... sure.")
                        return

                    elif mini_choice == 'r':
                        return

                    else:
                        Print("\nPlease Enter a valid input")

            # ---- 3. Calling out his negativity ----
            elif choice == '3':
                Print("\n[Terry] Negative? I've lost everything I've ever once owned here for Christ sake. Course I'd be negative")
                time.sleep(1)
                Print("\n[Knight] my bad broski.")
                time.sleep(1)
                return

            elif choice == '4':
                Print("[Terry] Because... I'd rather not go into it now.")
                return

            else:
                Print("\nPlease Enter a valid input")

            # ---- DAYS 41 - 45 ----
    elif 41 <= day <= 45:

        Print("\n[Terry] So I hear, you're really heading for the dragon, huh?")
        time.sleep(1)
        Print("\n[Knight] Someone has to.")
        time.sleep(1)
        Print("\n[Terry] Crazy… You are one tough guy, everybody sees Klare as a nightmare town and to you it was a 'pitstop' or something?")
        time.sleep(1)
        Print("\n[Knight] Pretty much. Maybe one day I'll teach you some tricks.")

        while True:
            print("\n[1] Do you have any last advice before I go?")
            print("[2] So… what ever happened with the merchant?")
            print("[r] Leave")
            choice = input("Enter: ")

            # ---- 1. Dragon sword ----
            if choice == '1':
                Print("\n[Terry] Not advice per se, more so an item")
                time.sleep(1)
                Print("\n[Knight] Ooh, what kind of item?")
                time.sleep(1)
                Print("\n[Terry] This item:")
                Print("\nTerry hands you a Mythical Blade!")
                time.sleep(1)
                Print("\n[Terry] It was my Great Grandfather's...")
                Print("[Terry] It was just a regular sword until my Great Grandmother enchanted it with something, I don't really know.")
                time.sleep(1)
                Print("[Terry] I never sold it...")
                time.sleep(1)
                Print("[Terry] Good luck killing the dragon knight... Maybe... Just maybe, I underestimated you.")
                player_data['owned_weapons'].append("Mythical Blade")
                return

            # ---- 2. Merchant status ----
            elif choice == '2':
                Print("\n[Terry] Oh yeah, nah we’re cool now.")
                time.sleep(1)
                Print("\n[Knight] …Cool?")
                time.sleep(1)
                Print("\n[Terry] Yeah. He had just heard a rumour that more people were coming to town and was taking a precaution")
                time.sleep(1)
                Print("\n[Knight] Do you know who spread that? Does it have anything to do with me coming to town?")
                time.sleep(1)
                Print("\n[Terry] Not at all, it was just a precaution... No, it was a 'just in case' type thing.")
                time.sleep(1)
                Print("\n[Knight] Right.")
                time.sleep(1)
                Print("\n[Terry] Good luck knight… Maybe I underestimated you.")
                return

            elif choice == 'r':
                Print("\n[Terry] Good luck knight… Maybe I underestimated you.")
                return

            else:
                Print("\nPlease Enter a valid input")

def talk_to_james(day):
    if day == 30:
        while True:
            Print("\n[James] Why are you here knight? You should leave this place before it corrupts you.")
            print("\n[1] I just got here though.")
            print("[2] Haha, I'm a knight, I can handle it.")
            print("[3] I need to get better gear before I fight the dragon.")
            choice = input("Enter: ")
            if choice == '1':
                Print("[James] And you better leave just as quick. This village has a way of changing people. Ask Albert if you see him today.")
                Print("[Knight] I will keep that in mind. Goodbye.")
                break
            elif choice == '2':
                Print("[James] Just because you're a knight doesnt mean you can bluff somebody out of their money.")
                Print("[Knight] But im the main character sooo...")
                Print("[James] We'll see then player")
                break
            elif choice == '3':
                Print("[James] If you stay here for longer you will be fighting the dragon with your fists.")
                Print("[Knight] If Klare is a gambling village why would they take my sword?")
                Print("[James] I guarantee you in a couple days you will be trading in your sword for 30 gold coins and another spin.")
                break

def talk_to_finn(day):
    if day == 30:
        while True:
            Print("\n[Finn] I'd get back inside if I were you. The streets aren't safe for outsiders. Especially after the lockdown.")
            print("\n[1] Why's that?")
            print("[2] What was the lockdown for?")
            choice = input("Enter: ")

def talk_to_albert(day):

    if 30 <= day <= 35:

        Print("\n[Albert] Hey knight! Care to bring some luck with you and accompany me to the gambling hall?")
        time.sleep(1)
        Print("\n[Knight] Luck?")
        time.sleep(1)
        Print("\n[Albert] Yeah, you look like a lucky guy and maybe we could win big.")

        while True:
            print("\n[1] You really think luck works like that?")
            print("[2] Are you winning much?")
            print("[3] You’ve been here a long time?")
            print("[r] Leave")
            choice = input("Enter: ")

            if choice == '1':
                Print("\n[Albert] Confidence summons fortune.")
                time.sleep(1)
                Print("\n[Knight] Sounds like crap.")
                time.sleep(1)
                Print("\n[Albert] That's what losers say.")
                time.sleep(1)
                Print("\n[Knight] No offence... buuuuut you kind of look like a loser.")
                time.sleep(1)
                Print("\n[Albert] HEY, come face me in the hall then big guy. I'm in the second division (medium difficulty)")
                time.sleep(1)
                Print("\n[Knight] Why not first?")
                time.sleep(1)
                Print("\n[Albert] BECAUSE, I WAS VERY UNLUCKY AND THEY DEMOTED ME, THAT'S ALL.")
                return

            elif choice == '2':
                Print("\n[Albert] Close every time.")
                time.sleep(1)
                Print("\n[Knight] Really?")
                time.sleep(1)
                Print("\n[Albert] *Almost* is basically winning... just without the reward...")
                return

            elif choice == '3':
                Print("\n[Albert] Years... No... Decades.")
                time.sleep(1)
                Print("\n[Knight] Why stay?")
                time.sleep(1)
                Print("\n[Albert] Winners don't walk away and if I wasn't a winner I wouldn't be here now would I?")
                return

            elif choice == 'r':
                return

            else:
                Print("\nPlease Enter a valid input")

    elif 36 <= day <= 40:

        Print("\n[Albert] Hey… knight, right?")
        time.sleep(1)
        Print("\n[Knight] Still chasing a big win?")
        time.sleep(1)
        Print("\n[Albert] Course I am.")

        while True:
            print("\n[1] You sound kinda tired.")
            print("[2] Any closer to winning?")
            print("[3] Have you ever thought about stopping?")
            print("[r] Leave")
            choice = input("Enter: ")

            if choice == '1':
                Print("\n[Albert] Tired of LOSING A 1000 POT IN LIARS DICE YEAH.")
                time.sleep(1)
                Print("\n[Knight] That doesn’t sound like much fun. I actually won a-")
                time.sleep(1)
                Print("\n[Albert] NO IT DOESN'T, GOOD FOR YOU.")
                return

            elif choice == '2':
                Print("\n[Albert] Just a bad streak.")
                time.sleep(1)
                Print("\n[Knight] Sounds like it's been quite a long streak...?")
                time.sleep(1)
                Print("\n[Albert] Bad luck runs out eventually. I have a feeling that end is soon.")
                return

            elif choice == '3':
                Print("\n[Albert] Quit while I'm ahead?")
                Print("[Albert] That doesn't make any sense.")
                time.sleep(1)
                Print("\n[Knight] You don't sound ahead.")
                time.sleep(1)
                Print("[Albert] I can assure you I am.")
                return

            elif choice == 'r':
                return

            else:
                Print("\nPlease Enter a valid input")

    elif 41 <= day <= 45:

        Print("\n[Albert] Hey...")
        time.sleep(1)
        Print("\n[Knight] Still here?")
        time.sleep(1)
        Print("\n[Albert] Where else would I be? Not like I have a choice anymore.")

        while True:
            print("\n[1] You okay? What happened to your good spirit?")
            print("[2] You ever win at all?")
            print("[3] Need help?")
            print("[r] Leave")
            choice = input("Enter: ")

            if choice == '1':
                Print("\n[Albert] I've never been better. In fact, my luck has been so good that I'm down 1500 gold now.")
                time.sleep(1)
                Print("\n[Knight] That's out of... how much did you start with?")
                time.sleep(1)
                Print("\n[Albert] 1000...")
                time.sleep(2)
                Print("\n[Knight] oh...")
                return

            elif choice == '2':
                Print("\n[Albert] Of course knight. I win all the time")
                time.sleep(1)
                Print("\n[Albert] Join me in a game in the hall and you can watch me win")
                return
            
            elif choice == '3':
                Print("\n[Albert] Of course.")
                time.sleep(1)
                Print("\n[Knight] When?")
                time.sleep(1)
                Print("\n[Albert] Now preferably, we can start with a 300 gold loan.")
                Print("[Albert] I'll make like 500 back, you can have 380, they'll promote me then-")
                time.sleep(1)
                Print("\n[Knight] Uhm, Albert? I meant like... emotional help.")
                time.sleep(1)
                return

            elif choice == 'r':
                return

            else:
                Print("\nPlease Enter a valid input")

def talk_to_emily(day, player_data):
    if 30 <= day <= 35:

        Print("\n[Emily] Oh... hi! You're the knight everyone is talking about, right?")
        time.sleep(1)
        Print("\n[Knight] That's me.")
        time.sleep(1)
        Print("\n[Emily] Wow… I didn’t think you'd actually come to Klare.")
        time.sleep(1)
        Print("\n[Knight] Why's that?")
        time.sleep(1)
        Print("\n[Emily] People with any sense stay away from here…")
        Print("[Emily] And then I heard you were really planning on fighting the dragon.")
        Print("[Emily] That's really brave.")

        while True:
            print("\n[1] I heard Klare’s a gambling town?")
            print("[2] The hotel room here is actually really nice.")
            print("[3] What was the lockdown all about?")
            print("[r] Leave")
            choice = input("Enter: ")

            if choice == '1':
                Print("\n[Emily] Yeah… that's true.")
                Print("[Emily] It kind of gets a hold on people once they start.")
                time.sleep(1)
                Print("\n[Knight] Sounds rough.")
                time.sleep(1)
                Print("\n[Emily] It is… I hope you won’t get stuck here too.")
                return

            elif choice == '2':
                Print("\n[Emily] Hey, I’m glad you like it.")
                time.sleep(1)
                Print("\n[Emily] It’s one of the only cozy spots left in town.")
                time.sleep(1)
                Print("\n[Knight] I might actually sleep properly tonight.")
                time.sleep(1)
                Print("\n[Emily] Hopefully, I bet it was a tough journey getting here.")
                return

            elif choice == '3':
                Print("\n[Emily] They said it was for safety…")
                time.sleep(1)
                Print("\n[Emily] But no one ever explained what the danger actually was.")
                time.sleep(1)
                Print("\n[Knight] That doesn’t really help.")
                time.sleep(1)
                Print("\n[Emily] Sorry, that's all I have for you about that.")
                return

            elif choice == 'r':
                return

            else:
                Print("\nPlease Enter a valid input")
        
    # ---- DAYS 36 - 40 ----
    elif 36 <= day <= 40:

        Print("\n[Emily] Oh, hey knight!")
        Print("[Emily] I was hoping I’d see you again.")
        Print("[Emily] Everyone keeps talking about you... the dragon... the winnings, all of it.")
        time.sleep(1)
        Print("\n[Knight] Sounds like I’m getting famous.")
        time.sleep(1)
        Print("\n[Emily] Yeah, just be careful of the jealous people.")

        while True:
            print("\n[1] Got any tips for the gambling games?")
            print("[2] Do you honestly think I can beat the dragon?")
            print("[3] What do you mean 'the jealous people'? Are they gonna attack me or something?")
            print("[r] Leave")
            choice = input("Enter: ")

            if choice == '1':
                Print("\n[Emily] I’m not amazing at them… but I’ve watched enough to notice patterns.")
                time.sleep(1)
                Print("\n[Emily] I can explain some tips if it helps.")
                time.sleep(1)
                Print("\n[Knight] Yeah if you could pls.")
                time.sleep(1)
                Print("\n[Emily] Not anything particularly good but...")
                Print("[Emily] In liars dice, if you have a high amount of 5s or 6s, I'd personally bet the total of dice you know +1")
                Print("[Emily] This basically guarentees that by the time it's your turn again, the bid will be a bluff.")
                time.sleep(1)
                Print("\n[Knight] Sick, thanks.")
                Print("\n[Emily] Here… take this too, one of the games is on me. 😊")
                Print("\nEmily gives you 69 gold!\n\n+69 gold 😉")
                player_data['gold'] += 69

                return

            elif choice == '2':
                Print("\n[Emily] Yeah. I really do.")
                time.sleep(1)
                Print("\n[Knight] Even knowing its the strongest beast in the land?")
                time.sleep(1)
                Print("\n[Emily] Especially because of that.")
                Print("[Emily] Someone needs to believe in you.")
                return

            elif choice == '3':
                Print("\n[Emily] I don’t think anyone’s going to attack you…")
                Print("[Emily] Just… people here don’t like seeing someone win when they haven’t.")
                time.sleep(1)
                Print("\n[Knight] So they're probably going to rob me?.")
                time.sleep(1)
                Print("\n[Emily] Probably, but try not to let it distract you.")
                time.sleep(1)
                Print("\n[Knight] Thanks Emily. You stay safe too.")
                return

            elif choice == 'r':
                return

            else:
                Print("\nPlease Enter a valid input")

    # ---- DAYS 41 - 45 ----
    elif 41 <= day <= 45:

        # qucik math for the chats
        day_till_dragon = 45 - day
        hour_till_dragon = random.randint(2, 11)

        Print("\n[Emily] So it’s really happening… you’re going for the dragon.")
        time.sleep(1)
        Print("\n[Knight] Yeah. I'm getting close to all the gear and upgrades I need.")
        time.sleep(1)
        Print(f"\n[Emily] Best you be quick. I hear that the dragon is specifically coming in {day_till_dragon} days and {hour_till_dragon} hours.")
        Print("[Emily] I just wanted to say I’m glad that you are going to fight this dragon.")
        time.sleep(1)
        Print("[Emily] If you succeed, maybe this town can go back to the way it was... and... maybe you could come back for me?")
        time.sleep(1)

        while True:
            print("\n[1] hell nah.")
            print("[2] Of course I will.")
            print("[r] Leave")
            choice = input("Enter: ")

            if choice == '1':
                Print("\n[Emily] Oh... yeah... I figured you'd say something like that.")
                time.sleep(1)
                Print("\n[Knight] I just don’t want to lie to you.")
                time.sleep(1)
                Print("\n[Emily] I get it. This isn’t exactly a normal trip.")
                Print("[Emily] You really are crazy knight.")
                time.sleep(1)
                Print("[Emily] Well... either way, here's a little bit more gold for the merchant.\n\n+200 Gold")
                player_data['gold'] += 200
                return

            elif choice == '2':
                Print("\n[Emily] R-really?")
                time.sleep(1)
                Print("\n[Knight] Yeah. I'll come back for you.")
                time.sleep(1)
                Print("\n[Emily] …Then I’ll be waiting. I'll see you soon 💖")
                Print("[Emily] Oh, and before you go... here's some extra gold for the merchant :)\n\n+100 Gold")
                player_data['gold'] += 100
                return

            else:
                Print("\nPlease Enter a valid input")

def talk_to_lucy(day):
    pass

if __name__ == "__main__":
    # Example player data
    player_data = {'day': 30}

    while True:
        
        # Talk to villagers
        day = int(input("What day is it: "))

        for i in range(6):
            talk_to_villagers(player_data)
        reset_villagers_talked()
        player_data['day'] += 1

# MAKE ONE OF THE CHARACTERS "INVESTIGATE" THE MERCHANT AND THEN DISSAPEAR ON DAY 41-45