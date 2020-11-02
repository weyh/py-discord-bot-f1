# -*- coding: utf-8 -*-
import os
import shutil
from datetime import datetime, timedelta
from Core import Console
from Core import converter as Converter
from dataclasses import dataclass
from typing import cast


@dataclass
class Cache:
    def __init__(self, date: str, type: str, data: str):
        self.date = date
        self.type = type
        self.data = data


class CacheManager:
    cache_enabled = True
    time_delta = 1800  # sec

    @staticmethod
    def load(type: str) -> Cache:
        'Loads json as Cache obj'
        return cast(Cache, Converter.json_file_to_obj(f"./cache/{type}.json"))

    @staticmethod
    def valid_cache_exists(type: str) -> bool:
        'Checks whether the json file exists'
        if os.path.exists(f"./cache/{type}.json"):
            if datetime.strptime(CacheManager.load(type).date, "%Y-%m-%d %H:%M:%S.%f") + timedelta(seconds=CacheManager.time_delta) > datetime.now():
                return True

        return False

    @staticmethod
    def save(cache_obj: Cache):
        'Saves self'
        if not os.path.exists('./cache'):
            os.mkdir("cache")
        Converter.obj_to_json_file(cache_obj, f"./cache/{cache_obj.type}.json")

    @staticmethod
    def clear():
        shutil.rmtree('./cache')
