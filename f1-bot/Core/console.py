# -*- coding: utf-8 -*-
import sys
import os
import platform
from datetime import datetime
from colorama import init, Fore, Back, Style

init(autoreset=True)


class Console:
    debug = False
    timestamp = False

    @staticmethod
    def clear():
        if platform.system() == 'Windows':
            os.system("cls")
        else:
            os.system("clear")

    @staticmethod
    def pause():
        print(Style.RESET_ALL)
        input("Press <Enter> key to continue...")

    @staticmethod
    def exit():
        sys.exit()

    @staticmethod
    def log(src: str, msg, force_debug=False):
        if force_debug or Console.debug:
            _tmstamp = f"({datetime.now().strftime('%y/%m/%d %H:%M:%S.%f')})" if Console.timestamp else ""
            print(str(Fore.LIGHTWHITE_EX) + "> " + src + f"{_tmstamp}: " + str(msg))

    @staticmethod
    def warning(src: str, msg):
        _tmstamp = f"({datetime.now().strftime('%y/%m/%d %H:%M:%S.%f')})" if Console.timestamp else ""
        print(str(Fore.LIGHTYELLOW_EX) + "> " + src + f"{_tmstamp}: " + str(msg))

    @staticmethod
    def error(src: str, msg):
        _tmstamp = f"({datetime.now().strftime('%y/%m/%d %H:%M:%S.%f')})" if Console.timestamp else ""
        print(str(Fore.LIGHTRED_EX) + "> " + src + f"{_tmstamp}: " + str(msg))

    @staticmethod
    def printc(text, color=""):
        'Colored Print'
        if isinstance(text, list):
            for _t in text:
                print(color + str(_t))
        else:
            print(color + str(text))

    @staticmethod
    def yes_or_no(question="", c_color=""):
        'Yes or no question'
        valid = {"yes": True, "y": True, "ye": True,
                 "no": False, "n": False, 'default': True}

        while True:
            print(c_color + question, end="")
            choice = input().lower()

            if choice == '':
                return valid['default']
            elif choice in valid:
                return valid[choice]
            else:
                Console.printc("Please respond with 'yes' or 'no' (or 'y' or 'n').\n", Fore.LIGHTYELLOW_EX)
