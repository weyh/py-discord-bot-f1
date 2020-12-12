# -*- coding: utf-8 -*-
import sys
from os import path
from colorama import Fore
from optparse import OptionParser
from Core import Console


class Start:
    'Checks whether it is the first time the program started by seeing if a file exists or not'

    def __init__(self, file_path):
        self.file_path = file_path

    def is_first(self) -> bool:
        return not path.isfile(self.file_path)

    @staticmethod
    def splash_screen():
        Console.printc(" ___  _                   _   ___ _   ___      _         ___   ___ \n" +
                       "|   \\(_)___ __ ___ _ _ __| | | __/ | | _ ) ___| |_  __ _|_  ) |_  )\n" +
                       "| |) | (_-</ _/ _ \\ '_/ _` | | _|| | | _ \\/ _ \\  _| \\ V // / _ / / \n" +
                       "|___/|_/__/\\__\\___/_| \\__,_| |_| |_| |___/\\___/\\__|  \\_//___(_)___|", Fore.LIGHTCYAN_EX)

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
