# -*- coding: utf-8 -*
from __future__ import annotations
from Core import Console
from Core import converter as conv
from colorama import Fore
import configparser as cfgpar

UCFG_VERSION = "v3"


class UserConfig:
    def __init__(self, version: str, token: str, prefix: str, debug: bool, timestamp: bool, temp_dir: str):
        self.version = version
        self.token = token
        self.prefix = prefix
        self.debug = debug
        self.timestamp = timestamp
        self.temp_dir = temp_dir

    def save(self):
        'Saves this user config'

        cfg = cfgpar.ConfigParser()
        cfg["UserConfig"] = self.__dict__
        with open("usr.cfg", "w") as f:
            cfg.write(f)

    def update(self, invar: dict):
        'Updates the user config with args'
        if invar is None:
            Exception("invar is None")

        invar["version"] = None
        self.__dict__.update((k, v) for k, v in invar.items() if v is not None)

    @staticmethod
    def __from_cfg(file: str) -> UserConfig | None:
        cfg = cfgpar.ConfigParser()
        cfg.read(file)

        if not cfg.has_section("UserConfig"):
            return None
        if not cfg.has_option("UserConfig", "token"):
            return None

        v = UCFG_VERSION
        if cfg.has_option("UserConfig", "version"):
            v = cfg.get("UserConfig", "version")

        ucfg = UserConfig(v, cfg["UserConfig"]["token"], "--", False, False, "./temp")

        if cfg.has_option("UserConfig", "prefix"):
            ucfg.prefix = cfg["UserConfig"]["prefix"]
        if cfg.has_option("UserConfig", "debug"):
            ucfg.debug = conv.str2bool(cfg["UserConfig"]["debug"])
        if cfg.has_option("UserConfig", "timestamp"):
            ucfg.timestamp = conv.str2bool(cfg["UserConfig"]["timestamp"])
        if cfg.has_option("UserConfig", "temp_dir"):
            ucfg.temp_dir = cfg["UserConfig"]["temp_dir"]

        return ucfg

    @ staticmethod
    def load() -> UserConfig:
        'Loads user config and returns it as UserConfig class'

        ucfg: UserConfig | None
        ucfg = UserConfig.__from_cfg("usr.cfg")

        if ucfg is None:
            Console.error("UserConfig (load)", f"Load Error: UserConfig cannot be parsed")
            ucfg = UserConfig.creation_ui("corrupted")

        return ucfg

    @ staticmethod
    def creation_ui(txt="missing") -> UserConfig:
        'UI for creating a usr.cfg file. Returns the newly created UserConfig class.'

        Console.warning("UserConfig", f"'usr.cfg' file is {txt}!")

        if(not Console.yes_or_no("Do you wish to create it (Y/n)? ", Fore.LIGHTYELLOW_EX)):
            raise Exception("'usr.cfg' file is missing! The application cannot be started!")

        while True:
            # Console.clear()
            Console.printc("Fields marked with '*' are essential!\n" +
                           "Other fields can be left empty.", Fore.LIGHTRED_EX)

            token = ""
            while True:
                token = input("Token (*): ")

                if token == "":
                    Console.printc("Token is not optional! Please enter your token.", Fore.LIGHTRED_EX)
                else:
                    break

            i_prefix = input("Prefix (default: '--'): ")
            i_debug = input("Debug (True/False, default: False): ")
            i_timestamp = input("Timestamp for console logs (True/False, default: False): ")
            temp_dir = input("Full path to temp directory (default: './tmp'): ")

            # var validation
            prefix = i_prefix if i_prefix != "" else "--"
            debug = conv.str2bool(i_debug)
            timestamp = conv.str2bool(i_timestamp)
            temp_dir = temp_dir if temp_dir != "" else "./tmp"

            print("-------------------------------------------------------------------\n" +
                  "Check if all values are correct!\n" +
                  f"token={token}\n" +
                  f"prefix={prefix}\n" +
                  f"debug={debug}\n" +
                  f"timestamp={timestamp}\n"
                  f"temp_dir={temp_dir}\n" +
                  "-------------------------------------------------------------------\n")

            if Console.yes_or_no("Save and continue (Y/n)? "):
                usr_conf = UserConfig(UCFG_VERSION, token, prefix, debug, timestamp, temp_dir)
                usr_conf.save()
                print("DONE!")
                return usr_conf
