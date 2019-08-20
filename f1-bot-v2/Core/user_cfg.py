# -*- coding: utf-8 -*
import json
from Core import Console
from Core import converter as Conv
from colorama import Fore

class UserConfig:
    def __init__(self, token:str, prefix:str, debug:bool, timestamp:bool, cache:bool, cache_time_delta:float, browser_path:str):
        self.token = token
        self.prefix = prefix
        self.debug = debug if type(debug) == bool else Conv.strtbool(debug)
        self.timestamp = timestamp if type(timestamp) == bool else Conv.strtbool(timestamp)
        self.cache = cache if type(cache) == bool else Conv.strtbool(cache)
        self.cache_time_delta = float(cache_time_delta)
        self.browser_path = browser_path
    
    def save(self):
        'Saves this user config'
        Conv.obj_to_json(self, "usr.cfg")
    
    def update(self, invar:dict):
        'Updates the user config with args'
        if invar is None:
            return

        self.__dict__.update((k,v) for k,v in invar.items() if v is not None)

    @staticmethod
    def load():
        'Loads user config and returns it as UserConfig class'
        try:
            return Conv.json_to_obj("usr.cfg")
        except Exception as e:
            Console.error("UserConfig (load)", f"Load Error: {e}")
            return UserConfig.creation_ui("corrupted")


    @staticmethod
    def creation_ui(txt="missing"):
        'UI for creating a usr.cfg file. Returns the newly created UserConfig class.'

        Console.warning("UserConfig", f"'usr.cfg' file is {txt}!")

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
            debug = input("Debug (True/False, default: False): ")
            timestamp = input("Timestamp for console logs (True/False, default: False): ")
            cache = input("Caching (True/False, default: True): ")
            cache_td = input("Caching time delta (default: 1800 sec): ")
            browser_path = input("Browser's path (**): ")

            # var validation
            prefix = prefix if prefix != "" else "--"
            debug = debug if debug != "" else False
            timestamp = timestamp if timestamp != "" else False
            cache = cache if cache != "" else True
            cache_td = cache_td if cache_td != "" else 1800
            browser_path = browser_path if browser_path != "" else "undefined"

            print("-------------------------------------------------------------------\n"+
                  "Check if all the values are correct!\n"+
                  f"token={token}\n"+
                  f"prefix={prefix}\n"+
                  f"debug={debug}\n"+
                  f"timestamp={timestamp}\n"+
                  f"caching={cache}\n"+
                  f"cache_time_delta={cache_td}\n"+
                  f"browser_path={browser_path}\n"+
                  "-------------------------------------------------------------------")
            
            print("")
            done = Console.yes_or_no("Save and continue (Y/n)? ")        

        usr_c = UserConfig(token, prefix, debug, timestamp, cache, cache_td, browser_path)
        usr_c.save()
        print("DONE!")
        return usr_c

