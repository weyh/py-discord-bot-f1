# -*- coding: utf-8 -*-
import sys, os, platform
from colorama import init, Fore, Back, Style

init(autoreset=True)

class Debug(object):
    debug = False

    @staticmethod
    def IsArchitecture64bit():
        return sys.maxsize > 2**32

    @staticmethod
    def Architecture():
        return platform.uname().machine

    @staticmethod
    def Clear():
        if platform.system() == 'Windows':
            os.system("cls")
        else:
            os.system("clear")

    @staticmethod
    def Pause():
        print(Style.RESET_ALL)
        input("Press <Enter> key to continue...")

    @staticmethod
    def Exit():
        sys.exit()

    @staticmethod
    def Log(src:str, msg, force_debug = False):
        if force_debug or Debug.debug:
            print(Fore.LIGHTWHITE_EX + "> " + src + ": " + str(msg))

    @staticmethod
    def Warning(src:str, msg):
        print(Fore.LIGHTYELLOW_EX + "> " + src + ": " + str(msg))

    @staticmethod
    def Error(src:str, msg):
        print(Fore.LIGHTRED_EX + "> " + src + ": " + str(msg))

    @staticmethod
    def Print(msg, color = Fore.WHITE):
        if isinstance(msg, list):
            for m in msg:
                print(color + str(m))
        else:
            print(color + str(msg))


    @staticmethod
    def YesOrNoQuestion(question = "", c_color = ""):
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
                Debug.Print("Please respond with 'yes' or 'no' (or 'y' or 'n').\n", Fore.LIGHTYELLOW_EX)