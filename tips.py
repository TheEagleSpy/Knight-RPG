import random

def display_random_tip():
    tips = [
        "Tip: Whenever you gain/lose defence or weapon damage while exploring it is also reflected in the item's description in your inventory.",
        "Tip: If battles ever feel too long, you can toggle 'Skip Battles' in the settings menu.",
        "Tip: You can rest after every exploration",
        "Tip: The slime kindom is really powerful as it allows you to acess the merchant and the blacksmith whenever you wish.", 
        "Tip: If you ever aren't sure about a feature try looking inside the help menu.",
        "Fact: There is just under 4000 lines of code in this game.",
        "Tip: Your settings save even after closing the game.",
        "Tip: You have about a 20% chance of getting a merchant each time you explore.",
        "Tip: You will be forced to fight the Howler on day 15.",
        "Tip: The blacksmith is a great way to upgrade your weapon and armor as it is cheaper than the merchant.",
        "Tip: You will lose connection with the slime kingdom after you go to the Swamplands.",
        "Tip: Dont forget to check the help menu if you are ever confused.",
        "Fact: V1 Had 250 lines of code, V2 Had 950, V3 Had 2500, and V4 has just under 4000.",
        "Fact: 70% of the code in this game is in the main file.",
        "Fact: There is 8 different files in this game.",
        "Tip: You can play a game of rock paper scissors with the forest merchant by typing 'rps' while talking to him.",
        "Fact: Every event in the forest exploration has a 5% chance of happening.",
        "Tip: Pretty much all events have multiple outcomes. Meaning just because an event is bad once doesn't mean it will be bad again.",
        "Tip: You can rest after each exploration.",
        "Tip: The slime kingdom is really important for the Frozen Peaks as it's way cheaper and you will need to heal a lot"
    ]
    return random.choice(tips)