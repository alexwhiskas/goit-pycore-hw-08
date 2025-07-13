# src/bot_helper/exit.py

from main import aliases

@aliases("close", "quit")
def exit():
    print("Good bye!")
    return False