# -*- coding: utf-8 -*-
import os, shutil
from datetime import datetime, timedelta
from Core import Console
from Core import converter as Conv

class Cache:
    def __init__(self, date:str, type:str, data:str):
        self.date = date
        self.type = type
        self.data = data

    def save(self):
        if not os.path.exists('./cache'):
            os.mkdir("cache")
        Conv.obj_to_json(self, f"./cache/{self.type}.json")

class CacheManager:
    cache_enabled = True
    time_delta = 1800#sec

    @staticmethod
    def load(type:str) -> Cache:
        return Conv.json_to_obj(f"./cache/{type}.json")

    @staticmethod
    def valid_cache_exists(type:str) -> bool:
        if os.path.exists(f"./cache/{type}.json"):
            if datetime.strptime(CacheManager.load(type).date, "%Y-%m-%d %H:%M:%S.%f") + timedelta(seconds=CacheManager.time_delta) > datetime.now():
                return True

        return False

    @staticmethod
    def clear():
        shutil.rmtree('./cache')