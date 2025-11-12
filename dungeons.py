import time

def Print(text, delay=0.02): #0.02
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def dungeons(player_data, dungeons_reason):
    Print("[Knight] Well... What do I do now???")
    time.sleep(1)
    if dungeons_reason == 'queen':
        escape_cost = 2000
    else:
        escape_cost = 1000
        
    while True:
        Print("")
