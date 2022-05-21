# -*- coding: utf-8 -*-

import shutil
import requests
import os
import json
from tabulate import tabulate
from datetime import datetime
import fastf1
import pandas as pd
from Core.converter import to_local_time

from Core.console import Console


def json2obj(json_file):
    return json.loads(json.dumps(json_file))


def get_event_schedule(year: int):
    return fastf1.get_event_schedule(year, include_testing=False)


def get_time(event, event_name: str) -> pd.Timestamp:
    if event['Session1'] == event_name:
        return event['Session1Date']
    elif event['Session2'] == event_name:
        return event['Session2Date']
    elif event['Session3'] == event_name:
        return event['Session3Date']
    elif event['Session4'] == event_name:
        return event['Session4Date']
    elif event['Session5'] == event_name:
        return event['Session5Date']

    return event['EventDate']


def format_qualifying_time(time: str) -> str:
    return time[10:-3]


class Get:
    __url = r"http://ergast.com/api/f1"
    __tmp_dir = "./tmp"

    @staticmethod
    def init(temp_dir: str):
        Get.__tmp_dir = temp_dir

        if os.path.exists(Get.__tmp_dir):
            shutil.rmtree(Get.__tmp_dir)
        os.mkdir(Get.__tmp_dir)
        fastf1.Cache.enable_cache(Get.__tmp_dir)

    @staticmethod
    def clear():
        fastf1.Cache.clear_cache(Get.__tmp_dir)

    @staticmethod
    def current() -> str:
        'Returns the current race weekend'
        current_date = datetime.now()
        event_schedule = get_event_schedule(current_date.year)

        event = {}
        found = False
        for _, row in event_schedule.iterrows():
            t = to_local_time(row['Location'], row['Session5Date'].to_pydatetime())
            if t != None:
                current_date = datetime.now(t.tzinfo)
                if t > current_date:
                    event = row
                    found = True
                    break

        if not found:
            Console.error("upcoming()", "event is empty")
            return "Error"

        return tabulate([["Location", f"{event['Location']}"],
                        [event['Session1'], f"{to_local_time(event['Location'], event['Session1Date'].to_pydatetime())}"],
                        [event['Session2'], f"{to_local_time(event['Location'], event['Session2Date'].to_pydatetime())}"],
                        [event['Session3'], f"{to_local_time(event['Location'], event['Session3Date'].to_pydatetime())}"],
                        [event['Session4'], f"{to_local_time(event['Location'], event['Session4Date'].to_pydatetime())}"],
                        [event['Session5'], f"{to_local_time(event['Location'], event['Session5Date'].to_pydatetime())}"]],
                        headers=["Country", f"{event['Country']}"], tablefmt='plain')

    @staticmethod
    def next_week() -> str:
        'Returns the race weekend after the upcoming one'

        current_date = datetime.now()
        event_schedule = get_event_schedule(current_date.year)

        event = {}
        found = False
        get_next = False
        for _, row in event_schedule.iterrows():
            if get_next:
                event = row
                found = True
                break

            t = to_local_time(row['Location'], row['Session5Date'].to_pydatetime())
            if t != None:
                current_date = datetime.now(t.tzinfo)
                if t > current_date:
                    get_next = True

        if not found:
            Console.error("next_week()", "event is empty")
            return "Error"

        return tabulate([["Location", f"{event['Location']}"],
                        [event['Session1'], f"{to_local_time(event['Location'], event['Session1Date'].to_pydatetime())}"],
                        [event['Session2'], f"{to_local_time(event['Location'], event['Session2Date'].to_pydatetime())}"],
                        [event['Session3'], f"{to_local_time(event['Location'], event['Session3Date'].to_pydatetime())}"],
                        [event['Session4'], f"{to_local_time(event['Location'], event['Session4Date'].to_pydatetime())}"],
                        [event['Session5'], f"{to_local_time(event['Location'], event['Session5Date'].to_pydatetime())}"]],
                        headers=["Country", f"{event['Country']}"], tablefmt='plain')

    @staticmethod
    def last_qualifying_results() -> tuple:
        'Returns the place where the last qualifying was hosted and the data.'

        current_date = datetime.now()

        session = {}
        found = False
        for i in range(1, 50):
            try:
                tmp = fastf1.get_session(current_date.year, i, 'Q')

                t = to_local_time(tmp.event['Location'], get_time(tmp.event, "Qualifying").to_pydatetime())
                if t != None:
                    current_date = datetime.now(t.tzinfo)
                    if t > current_date:
                        session = fastf1.get_session(current_date.year, max(1, i - 1), 'Q')
                        found = True
                        break
            except:
                break

        if not found:
            Console.error("last_qualifying_results()", "session is empty")
            return ("Error", "")

        session.load(telemetry=False, weather=False, messages=False)
        table = []
        i = 1
        for _, row in session.results.iterrows():
            table.append([f"{i}", row['FullName'],
                          format_qualifying_time(f"{row['Q1']}"),
                          format_qualifying_time(f"{row['Q2']}"),
                          format_qualifying_time(f"{row['Q3']}")])
            i += 1

        return (session.event['Location'], tabulate(table, headers=["Pos", "Driver", "Q1", "Q2", "Q3"], tablefmt='orgtbl', numalign="right", stralign="center"))

    @staticmethod
    def last_race_results() -> tuple:
        'Returns the place where the last race was hosted and the data.'

        current_date = pd.Timestamp(datetime.now())

        session = {}
        found = False
        for i in range(1, 50):
            try:
                tmp = fastf1.get_session(current_date.year, i, 'Race')

                t = to_local_time(tmp.event['Location'], tmp.event['EventDate'].to_pydatetime())
                if t != None:
                    current_date = datetime.now(t.tzinfo)
                    if t > current_date:
                        session = fastf1.get_session(current_date.year, max(1, i - 1), 'Race')
                        found = True
                        break
            except:
                break

        if not found:
            Console.error("last_race_results()", "session is empty")
            return ("Error", "")

        session.load(telemetry=False, weather=False, messages=False)
        table = []
        i = 1
        for _, row in session.results.iterrows():
            table.append([f"{i}", row['FullName'], row['TeamName'], row['Status'], str(row['Points'])])
            i += 1

        return (session.event['Location'], tabulate(table, headers=["Pos", "Driver", "TeamName", "Status", "Points"], tablefmt='orgtbl', numalign="right", stralign="center"))

    @staticmethod
    def driver_standings(year="current") -> str:
        'Returns a tabulated str'

        json_file = requests.get(f"{Get.__url}/{year}/driverStandings.json").json()

        _driver_standings = json2obj(
            json_file)["MRData"]['StandingsTable']['StandingsLists'][0]['DriverStandings']

        table = []
        for pos, ds in enumerate(_driver_standings, 1):
            driver_name = f"{ds['Driver']['givenName']} {ds['Driver']['familyName']}"

            table.append([f"{pos}", f"{driver_name}", f"{ds['points']}"])

        return tabulate(table, headers=["Pos", "Driver", "Points"], tablefmt='orgtbl', numalign="right", stralign="center")

    @staticmethod
    def constructor_standings(year="current") -> str:
        'Returns a tabulated str'

        json_file = requests.get(f"{Get.__url}/{year}/constructorStandings.json").json()

        _constructors_standings = json2obj(json_file)["MRData"]['StandingsTable']['StandingsLists'][0]['ConstructorStandings']

        table = []
        for pos, cs in enumerate(_constructors_standings, 1):
            team_name = cs['Constructor']['name']

            table.append([f"{pos}", f"{team_name}", f"{cs['points']}"])

        return tabulate(table, headers=["Pos", "Driver", "Points"], tablefmt='orgtbl', numalign="right", stralign="center")

    @staticmethod
    def calendar() -> str:
        'Returns a tabulated str'

        current_date = datetime.now()
        event_schedule = get_event_schedule(current_date.year)

        table = []
        for _, row in event_schedule.iterrows():
            t = to_local_time(row['Location'], row['EventDate'].to_pydatetime())
            if t == None:
                t = row['EventDate'].to_pydatetime()
            current_date = datetime.now(t.tzinfo)

            box = "■" if t < current_date else " "
            table.append([row['Country'], row['Location'], t.strftime('%d %b'), box])

        return tabulate(table, headers=["Country", "Location", "Date", " "], tablefmt='orgtbl', stralign="center")
