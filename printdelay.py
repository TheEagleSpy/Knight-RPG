import time
import os

PRINT_SPEED = 0.02

# Print text with delay fast
def set_print_speed(speed):
    global PRINT_SPEED
    PRINT_SPEED = speed

def Print(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(PRINT_SPEED)
    print()
    
# Print text with slow delay
def PRint(text, delay=0.03): #0.03 = 3ms
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")