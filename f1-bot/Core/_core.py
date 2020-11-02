# -*- coding: utf-8 -*-
import sys
import os
import platform
import requests
from datetime import datetime
from colorama import init, Fore, Back, Style
from optparse import OptionParser

init(autoreset=True)


def is_architecture_64bit() -> bool:
    return sys.maxsize > 2**32


def architecture() -> str:
    return platform.uname().machine


def is_site_up(url='https://www.autosport.com/f1') -> bool:
    return requests.head(url).status_code == 200


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


class Start:
    'Checks whether it is the first time the program started by seeing if a file exists or not'

    def __init__(self, file_path):
        self.file_path = file_path

    def is_first(self) -> bool:
        return not os.path.isfile(self.file_path)

    @staticmethod
    def splash_screen():
        Console.printc("    ____  _                          __   _________   ____        __          ___    ___ \n" +
                       "   / __ \\(_)_____________  _________/ /  / ____<  /  / __ )____  / /_   _   _|__ \\  |__ \\\n" +
                       "  / / / / / ___/ ___/ __ \\/ ___/ __  /  / /_   / /  / __  / __ \\/ __/  | | / /_/ /  __/ /\n" +
                       " / /_/ / (__  ) /__/ /_/ / /  / /_/ /  / __/  / /  / /_/ / /_/ / /_    | |/ / __/_ / __/ \n" +
                       "/_____/_/____/\\___/\\____/_/   \\__,_/  /_/    /_/  /_____/\\____/\\__/    |___/____(_)____/ ", Fore.LIGHTCYAN_EX)

    @staticmethod
    def load_args(version):
        if len(sys.argv) == 1:
            return

        parser = OptionParser(version=version)

        parser.add_option("-t", "--token", dest="token", help="Discord bot token", metavar="TOKEN")
        parser.add_option("-p", "--prefix", dest="prefix", help="Discord chat prefix to access the bot (default: '--')", metavar="PREFIX")

        parser.add_option("-d", "--debug", dest="debug", action="store_true", help="Turn debug mode on/off (default: False)", metavar="True/False")
        parser.add_option("-T", "--timestamp", dest="timestamp", action="store_true", help="Turn timestamp on/off (default: False)", metavar="True/False")

        parser.add_option("-c", "--cache", dest="cache", help="Turn caching on/off (default: True)", metavar="True/False")
        parser.add_option("-C", "--cache_time_delta", dest="cache_time_delta", help="The time while the cached data is valid (default: 1800 sec)", metavar="CACHE_TIME_DELTA")

        options, args = parser.parse_args()
        return vars(options)
