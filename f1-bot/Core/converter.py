# -*- coding: utf-8 -*
import json
import pytz
from tzlocal import get_localzone
from datetime import datetime, timezone


def str2bool(string: str) -> bool:
    'Converts str to bool'
    return string.lower() in ("true", "t")

# Time


def to_local_timzone(dt):
    'Converts time to local time'
    return dt.astimezone(get_localzone())


def to_utc_timzone(dt):
    'Converts local time to utc time'
    return dt.astimezone(pytz.timezone('UTC'))

# JSON


def __convert_to_dict(obj):
    obj_dict = {"__class__": obj.__class__.__name__, "__module__": obj.__module__}
    obj_dict.update(obj.__dict__)

    return obj_dict


def obj2json(obj: object, filename: str):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(obj, f, default=__convert_to_dict, indent=4)


def __dict_to_obj(my_dict):
    if "__class__" in my_dict:
        class_name = my_dict.pop("__class__")
        module_name = my_dict.pop("__module__")

        module = __import__(module_name)
        class_ = getattr(module, class_name)
        obj = class_(**my_dict)
    else:
        obj = my_dict
    return obj


def json2obj(filename: str) -> object:
    with open(filename, 'r') as json_data:
        return json.load(json_data, object_hook=__dict_to_obj)
