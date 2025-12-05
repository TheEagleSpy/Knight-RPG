import time

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