# -*- coding: utf-8 -*-
from debug import Debug

__not_optional_paramaters = ["token"]
__optional_paramaters = {"timezone":"CET", "prefix":"--"}

def dictionary_test(d):
    for paramater in __not_optional_paramaters:
        if d.get(paramater) == None:
            Debug.Error("SYS", f"'{paramater}' paramater not found in usr.cfg!")
            Debug.Pause()
            Debug.Exit()

    for paramater in __optional_paramaters:
        if d.get(paramater) == None:
            Debug.Warning("SYS", f"'{paramater}' paramater not found in usr.cfg! Default is '{__optional_paramaters.get(paramater)}'")
            d.update({paramater: __optional_paramaters.get(paramater)})
    return ""