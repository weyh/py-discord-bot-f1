# -*- coding: utf-8 -*-
import sys, os, platform
from colorama import init, Fore, Back, Style
from optparse import OptionParser

init(autoreset=True)

def IsArchitecture64bit():
    return sys.maxsize > 2**32

def Architecture():
    return platform.uname().machine

class Console:
    debug = False

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
    def log(src:str, msg, force_debug = False):
        if force_debug or Console.debug:
            print(Fore.LIGHTWHITE_EX + "> " + src + ": " + str(msg))

    @staticmethod
    def warning(src:str, msg):
        print(Fore.LIGHTYELLOW_EX + "> " + src + ": " + str(msg))

    @staticmethod
    def error(src:str, msg):
        print(Fore.LIGHTRED_EX + "> " + src + ": " + str(msg))

    @staticmethod
    def printc(text, color = ""):
        'Colored Print'
        if isinstance(text, list):
            for _t in text:
                print(color + str(_t))
        else:
            print(color + str(text))


    @staticmethod
    def yes_or_no(question = "", c_color = ""):
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

class Start:
    'Checks whether it is the first time the program started by seeing if a file exists or not'

    def __init__(self, file_path):
        self.file_path = file_path

    def is_first(self) -> bool:
        return not os.path.isfile(self.file_path)

    @staticmethod
    def splash_screen():
        Console.printc(" _                       __       _             __ \n"+
                       "| \ o  _  _  _  __ _|   |_ /|    |_) _ _|_       _)\n"+
                       "|_/ | _> (_ (_) | (_|   |   |    |_)(_) |_   \_//__", Fore.LIGHTCYAN_EX)
    
    @staticmethod
    def load_args(version):
        if len(sys.argv) == 1:
            return

        parser = OptionParser(version = version)
        parser.add_option("--token", dest="token", help="Discord bot token", metavar="{token}"),
        parser.add_option("--prefix", dest="prefix", help="Discord chat prefix to access the bot (default: --)", metavar="{prefix}")
        parser.add_option("--debug", dest="debug", help="Turn debug mode on/off", metavar="True/False")
        parser.add_option("--browser_path", dest="browser_path", help="browser path", metavar="{browser_path}")

        (options, args) = parser.parse_args()
        
        return vars(options)