# -*- coding: utf-8 -*
import json
from Core import Console
from Core import converter as Conv
from colorama import Fore

class UserConfig:
    def __init__(self, token:str, prefix:str, debug:bool, browser_path:str):
        self.token = token
        self.prefix = prefix
        self.debug = debug if type(debug) == bool else Conv.strtbool(debug)
        self.browser_path = browser_path
    
    def save(self):
        'Saves this user config'
        Conv.obj_to_json(self, "usr.cfg")
    
    def update(self, invar:dict):
        'Updates the user config with args'
        if invar is None:
            return

        if type(invar) is tuple:
            invar = dict(invar)
        self.__dict__.update((k,v) for k,v in invar.iteritems() if v is not None)

    @staticmethod
    def load():
        'Loads user config and returns it as UserConfig class'
        return Conv.json_to_obj("usr.cfg") 

    @staticmethod
    def creation_ui():
        'UI for creating a usr.cfg file. Returns the newly created UserConfig class.'

        Console.warning("UserConfig", "'usr.cfg' file is missing!")

        if(not Console.yes_or_no("Do you wish to create it (Y/n)? ", Fore.LIGHTYELLOW_EX)):
            raise Exception("'usr.cfg' file is missing! The application cannot be started!")
            Console.Exit()

        done = False
        while not done:
            Console.clear()
            Console.printc("Fields marked with '*' are essential!\n"+
                    "Fields marked with '**' are essential for the f2 module only!\n"+
                    "Other fields can be left empty.", Fore.LIGHTRED_EX)
            
            while True:
                token = input("Token (*): ")
                if token != "":
                    break
                else:
                    Console.printc("Token is not optional! Please enter your token.", Fore.LIGHTYELLOW_EX)

            prefix = input("Prefix (default: '--'): ")
            debug = input("Debug (True/False, default: True): ")
            browser_path = input("Browser's path (**): ")

            # var validation
            prefix = prefix if prefix != "" else "--"
            debug = debug if debug != "" else True
            browser_path = browser_path if browser_path != "" else "undefined"

            print("-------------------------------------------------------------------\n"+
                  "Check if all the values are correct!\n"+
                  f"token={token}\n"+
                  f"prefix={prefix}\n"+
                  f"debug={debug}\n"+
                  f"browser_path={browser_path}\n"+
                  "-------------------------------------------------------------------")
            
            print("")
            done = Console.yes_or_no("Save and continue (Y/n)? ")        

        usr_c = UserConfig(token, prefix, debug, browser_path)
        usr_c.save()
        print("DONE!")
        return usr_c

