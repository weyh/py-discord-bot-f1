# -*- coding: utf-8 -*
from colorama import Fore
from Core.debug import Debug

class UserConfig:
    def __init__(self, token, prefix, timezone, debug, browser_path):
        self.data = []

        self.data.append("token=" + token)

        if prefix != "":
            self.data.append(f"prefix={prefix}")

        if timezone != "":
            self.data.append(f"timezone={timezone}")

        if debug != "":
            self.data.append(f"debug={debug.capitalize()}")

        if browser_path != "":
            self.data.append(f"browser_path={browser_path}")

    def create(self):
        with open("usr.cfg", 'w', encoding="utf-8") as out:
            out.writelines("%s\n" % data for data in self.data)
    
    @staticmethod
    def Setup_UI():
        Debug.Warning("UserConfig", "'usr.cfg' file is missing!")

        if(not Debug.YesOrNoQuestion("Do you wish to create it (Y/n)? ", Fore.LIGHTYELLOW_EX)):
            raise Exception("'usr.cfg' file is missing! The application cannot be started!")
            Debug.Exit()

        done = False
        while not done:
            Debug.Clear()
            Debug.Print("Fields marked with '*' are essential!\n"+
                    "Fields marked with '**' are essential for the f2 module only!\n"+
                    "Other fields can be left empty.", Fore.LIGHTRED_EX)

            token = input("Token (*): ")
            prefix = input("Prefix (default: '--'): ")
            timezone = input("Timezone (CET, UTC, GMT etc, default: CET): ")
            debug = input("Debug (True/False, default: True): ")
            browser_path = input("Browser's path (**): ")

            print("-------------------------------------------------------------------\n"+
                  "Check if all the values are correct!\n"+
                  f"token={token}\n"+
                  f"prefix={prefix if prefix != '' else '--'}\n"+
                  f"timezone={timezone if timezone != '' else 'CET'}\n"+
                  f"debug={debug if debug != '' else 'True'}\n"+
                  f"browser_path={browser_path if browser_path != '' else 'undefined'}\n"+
                  "-------------------------------------------------------------------")
            
            print("")

            done = Debug.YesOrNoQuestion("Save and continue (Y/n)? ")

        UserConfig(token, prefix, timezone, debug, browser_path).create()
        print("DONE!")
    