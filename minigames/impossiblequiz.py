def play_impossiblequiz():
    print("\n--- Minigame: The Impossible Quiz ---")
    print("Answer all 10 questions correctly to win! (One mistake and you lose.)")
    print("Type the letter (A, B, C, or D) for your answer.\n")

    questions = [
        {
            "q": "What color is an orange?",
            "options": ["A) Orange", "B) Blue", "C) Purple", "D) Depends on the lighting"],
            "answer": "A"
        },
        {
            "q": "How many months have 28 days?",
            "options": ["A) 1", "B) 12", "C) 2", "D) Depends on leap years"],
            "answer": "B"
        },
        {
            "q": "Can you put a toaster in the oven?",
            "options": ["A) Yes, if it's unplugged", "B) No, it toasts itself", "C) Only on Fridays", "D) Please don’t"],
            "answer": "D"
        },
        {
            "q": "What is heavier: a kilogram of feathers or a kilogram of steel?",
            "options": ["A) Feathers", "B) Steel", "C) Neither", "D) Both"],
            "answer": "C"
        },
        {
            "q": "What number comes after 10?",
            "options": ["A) 11", "B) 10.1", "C) Depends", "D) J"],
            "answer": "A"
        },
        {
            "q": "If you mix red and white, what color do you get?",
            "options": ["A) Pink", "B) Salmon", "C) Gray", "D) Blood of your enemies"],
            "answer": "A"
        },
        {
            "q": "Which is correct: ‘Egg yolks is white’ or ‘Egg yolks are white’?",
            "options": ["A) First one", "B) Second one", "C) Neither", "D) Depends on the chicken"],
            "answer": "C"
        },
        {
            "q": "How many holes are in a polo shirt?",
            "options": ["A) 2", "B) 3", "C) 4", "D) 5"],
            "answer": "C"
        },
        {
            "q": "You have a single match and enter a dark room with a lamp, a fireplace, and a candle. What do you light first?",
            "options": ["A) Candle", "B) Lamp", "C) Fireplace", "D) The match"],
            "answer": "D"
        },
        {
            "q": "Can a man marry his widow’s sister?",
            "options": ["A) Yes", "B) No", "C) Only if he’s rich", "D) Only on Tuesdays"],
            "answer": "B"
        },
    ]

    for i, q in enumerate(questions, start=1):
        print(f"\nQuestion {i}: {q['q']}")
        for opt in q["options"]:
            print(opt)
        answer = input("Your answer: ").strip().upper()

        if answer != q["answer"]:
            print("\nWRONG! That’s the impossible quiz for you...")
            return False
        else:
            print("Correct!")

    print("\nCongratulations! You beat the Impossible Quiz!")
    return True

play_impossiblequiz()