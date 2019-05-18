# -*- coding: utf-8 -*-
import sys
from debug import Debug
from optparse import OptionParser

__not_optional_parameters = ["token"]
__optional_parameters = {"timezone":"CET", "prefix":"--", "debug":True}

def read():
    return {k:v.replace("\n", "").replace(" ", "").replace("\t", "") for k, v in (l.split(':') for l in open("usr.cfg"))}

def update_from_argv(d, version):
    if len(sys.argv) == 1:
        return

    parser = OptionParser(version = version)
    parser.add_option("--token", dest="token", help="Discord bot token", metavar="{token}"),
    parser.add_option("--timezone", dest="timezone", help="Your Current timezone (CET, UTC, GMT etc)", metavar="{timezone}")
    parser.add_option("--prefix", dest="prefix", help="Discord chat prefix to access the bot (default: --)", metavar="{prefix}")
    parser.add_option("--debug", dest="debug", help="Turn debug mode on/off", metavar="True/False")

    (options, args) = parser.parse_args()
    options = vars(options)
    
    for parameter in options:
        if options.get(parameter) != None:
            if parameter == "debug":
                d.update({parameter:  __str2bool(options.get(parameter))})
            else:
                d.update({parameter: options.get(parameter)})
    return

def test(d):
    for parameter in __not_optional_parameters:
        if d.get(parameter) == None:
            Debug.Error("SYS", f"'{parameter}' parameter must be defined!")
            Debug.Pause()
            Debug.Exit()

    for parameter in __optional_parameters:
        if d.get(parameter) == None:
            Debug.Warning("SYS", f"'{parameter}' parameter not found in usr.cfg! Default is '{__optional_parameters.get(parameter)}'")
            d.update({parameter: __optional_parameters.get(parameter)})
        elif parameter == "debug":
            d.update({parameter: __str2bool(d.get(parameter))})

    return

__str2bool = lambda v: str(v).lower() in ("yes", "true", "t", "y", "1")