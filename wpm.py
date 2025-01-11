import atexit
import os
import threading
import time
import random
import pyfiglet
import cursor
from termcolor import colored
import keyboard

RED = "\033[0;31m"
GREEN = "\033[0;32m"
CYAN = "\033[0;36m"
YELLOW = "\033[1;33m"
ORANGE = "\033[38;2;255;165;0m"
LIGHT_GREEN = "\033[1;32m"
RESET = "\033[0m"


class WPM:
    def __init__(self):
        self.phrases = {
            "easy":
            ["The quick brown fox jumps over the lazy dog.",
             "Python programming is fun and powerful.",
             "The rain in Spain falls mainly on the plain.",
             "She sells seashells by the seashore.",
             "Practice makes perfect.",
             "The early bird catches the worm.",
             "Actions speak louder than words."
            ],

            "medium": 
            ["Typing is an essential skill in the modern world.",
            "Practice makes perfect in typing and coding.",
            "Pack my box with five dozen liquor jugs.",
            "How much wood would a woodchuck chuck if a woodchuck could chuck wood?",
            "It's a beautiful day in the neighborhood",
            "To be or not to be, that is the question.",
            ],

            "hard": 
            ["How razorback-jumping frogs can level six piqued gymnasts!",
             "Sphinx of black quartz, judge my vow.",
            "Mr Jock, TV quiz PhD, bags few lynx.",
            "The six sleek swans swam swiftly southward while the jagged rocks jutted sharply from the sea."
            ]
            }
        

        self.done = False
        self.count = 0
        self.current_phrase = ""
        self.wpm = 0
    def start(self):
        while True:
            self.done = False
            self.count = 0
            self.intro()
            self.give_phrase()

            counter_thread = threading.Thread(target=self.start_counter)
            counter_thread.daemon = True
            counter_thread.start()

            while not self.done:
                cursor.show()
                self.attempt = input("\n> ").strip()
                if self.attempt == self.current_phrase:
                    cursor.hide()
                    self.done = True
                else:
                    os.system("cls" if os.name == "nt" else "clear")
                    self.incorrect_phrase()
                    print(self.current_phrase)
            
            self.calculate_wpm()
            print(f"\n{GREEN}CORRECT!{RESET}\n{CYAN}Time:{RESET} {self.count:.2f} seconds\n{CYAN}WPM:{RESET} {round(self.wpm)}")
            input("\nPress Enter to continue")

    def start_counter(self):
        while not self.done:
            time.sleep(.001)
            self.count += .001

    def give_phrase(self):
        self.current_phrase = random.choice(self.phrases[self.difficulty])
        print(self.current_phrase)

    def calculate_wpm(self):
        words = len(self.current_phrase.split())
        self.wpm = (words / self.count) * 60
        
    def incorrect_phrase(self):
        try:
            right_phrase = [i for i in enumerate(self.current_phrase)]
            wrong_phrase = [i for i in enumerate(self.attempt)]
            compare = zip(right_phrase, wrong_phrase)
            wrong_chars = [char[1] for char in compare if char[0] != char[1]]
            wrong_chars = list(zip(*wrong_chars))
            wrong_chars = wrong_chars[0]
            show_errors = f""
            for i, char in enumerate(self.current_phrase):
                if i in wrong_chars:
                    show_errors += f"{RED}{char}{RESET}"
                else:
                    show_errors += char
            
            print(f"{RED}Incorrect{RESET}: {show_errors}\n")
        except IndexError:
            print(f"{RED}Incorrect: {self.current_phrase}{RESET}\n")

    def intro(self):
        cursor.hide()

        while True:
            os.system("cls")
            print(colored(pyfiglet.figlet_format("WPM Typing Test\n\n", font="small"), "yellow"))
            self.difficulty = input(f"{YELLOW}Enter Difficulty\n1. Easy\n2. Medium\n3. Hard{RESET}\n\n> ")
            if self.difficulty[0] == "1":
                self.difficulty = "easy"
                break
            elif self.difficulty[0] == "2":
                self.difficulty = "medium"
                break
            elif self.difficulty[0] == "3":
                self.difficulty = "hard"
                break
            else:
                print("Invalid input. please enter number")
                input("Press enter to continue")
        
        if self.difficulty == "easy":
            input(f"{YELLOW}Difficulty{RESET} {LIGHT_GREEN}{self.difficulty.upper()}{RESET} - {YELLOW}Press Enter to start{RESET}".center(80))

        elif self.difficulty == "medium":
            input(f"{YELLOW}Difficulty{RESET} {ORANGE}{self.difficulty.upper()}{RESET} - {YELLOW}Press Enter to start{RESET}".center(80))

        if self.difficulty == "hard":
            input(f"{YELLOW}Difficulty{RESET} {RED}{self.difficulty.upper()}{RESET} - {YELLOW}Press Enter to start{RESET}".center(80))


        os.system("cls")
        for i in range(3, 0, -1):
            print(colored(pyfiglet.figlet_format(str(i)), "yellow"))
            time.sleep(1)
            os.system("cls")
        print(colored(pyfiglet.figlet_format("GO"), "green"))
        time.sleep(1)
        os.system("cls")



def main():
    try:
        keyboard.block_key("up")
        wpm = WPM()
        wpm.start()
    except KeyboardInterrupt:
        cursor.show()
        print("Closing due to 'ctrl + C'...")



if __name__ == "__main__":
    atexit.register(keyboard.unhook_all)
    main()