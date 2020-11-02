# -*- coding: utf-8 -*
from __future__ import annotations
import json
from Core import Console
from Core import converter as Converter
from colorama import Fore
from typing import cast


class UserConfig:
    def __init__(self, token: str, prefix: str, debug: bool, timestamp: bool, cache: bool, cache_time_delta: int):
        self.version = "v2"
        self.token = token
        self.prefix = prefix
        self.debug = debug
        self.timestamp = timestamp
        self.cache = cache
        self.cache_time_delta = cache_time_delta

    def save(self):
        'Saves this user config'
        Converter.obj_to_json_file(self, "usr.cfg")

    def update(self, invar: dict):
        'Updates the user config with args'
        if invar is None:
            Exception("invar is None")

        self.__dict__.update((k, v) for k, v in invar.items() if v is not None)

    @staticmethod
    def load() -> UserConfig:
        'Loads user config and returns it as UserConfig class'
        try:
            return cast(UserConfig, Converter.json_file_to_obj("usr.cfg"))
        except Exception as e:
            Console.error("UserConfig (load)", f"Load Error: {e}")
            return UserConfig.creation_ui("corrupted")

    @staticmethod
    def creation_ui(txt="missing") -> UserConfig:
        'UI for creating a usr.cfg file. Returns the newly created UserConfig class.'

        Console.warning("UserConfig", f"'usr.cfg' file is {txt}!")

        if(not Console.yes_or_no("Do you wish to create it (Y/n)? ", Fore.LIGHTYELLOW_EX)):
            raise Exception("'usr.cfg' file is missing! The application cannot be started!")

        while True:
            Console.clear()
            Console.printc("Fields marked with '*' are essential!\n" +
                           "Other fields can be left empty.", Fore.LIGHTRED_EX)

            token = ""
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

            # var validation
            prefix = prefix if prefix != "" else "--"
            debug = Converter.str2bool(debug)
            timestamp = Converter.str2bool(timestamp)
            cache = Converter.str2bool(cache)
            cache_td = int(cache_td) if cache_td != "" else 1800

            print("-------------------------------------------------------------------\n" +
                  "Check if all values are correct!\n" +
                  f"token={token}\n" +
                  f"prefix={prefix}\n" +
                  f"debug={debug}\n" +
                  f"timestamp={timestamp}\n" +
                  f"caching={cache}\n" +
                  f"cache_time_delta={cache_td}\n" +
                  "-------------------------------------------------------------------\n")

            if Console.yes_or_no("Save and continue (Y/n)? "):
                usr_conf = UserConfig(token, prefix, debug, timestamp, cache, cache_td)
                usr_conf.save()
                print("DONE!")
                return usr_conf
