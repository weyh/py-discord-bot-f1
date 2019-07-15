# -*- coding: utf-8 -*-
"""
Ergast Developer API Custom Wrapper
"""

import requests, json, time
from collections import namedtuple
from pytz import timezone
from tabulate import tabulate
from datetime import datetime
from bs4 import BeautifulSoup

class Get:
    def __init__(self, timezone = "CET"):
        self.timezone = timezone
        self.time_formats = {'date' : "%Y-%m-%d", 'time' : "%H:%M:%S", 'combined' : "%Y-%m-%d %H:%M:%S", 'show' : "%d %b", 'long': "%a %b %d %Y %H:%M:%S %Z%z"}
        self.__url = r"http://ergast.com/api/f1"

    def __localTime(self, time):
        return time.astimezone(timezone(self.timezone))

    def Upcoming(self):
        """ Returns a string created by 'tabulate' """

        show_format_0 = "%a %d %b"
        show_format_1 = "%H:%M"
        current_date = datetime.now()

        # getting data from autosport
        page = requests.get('https://www.autosport.com/f1')
        soup = BeautifulSoup(page.content, 'html.parser')
        coming_up_div = soup.find_all('div', class_='stats')[1]

        schedule_start = [d.find("td", class_="text-right").get("data-start") for d in coming_up_div.find("div", class_='time-convert').find("table").find("tbody").find_all("tr")]
        schedule_end = [d.find("td", class_="text-right").get("data-end") for d in coming_up_div.find("div", class_='time-convert').find("table").find("tbody").find_all("tr")]

        free_practices_start = [self.__localTime(datetime.strptime(d, self.time_formats['long'])) for d in schedule_start[:3]]
        free_practices_end = [self.__localTime(datetime.strptime(d, self.time_formats['long'])) for d in schedule_end[:3]]
        qualifyings_start = [self.__localTime(datetime.strptime(d, self.time_formats['long'])) for d in schedule_start[3:6]]
        qualifyings_end = [self.__localTime(datetime.strptime(d, self.time_formats['long'])) for d in schedule_end[3:6]]
        race_start = self.__localTime(datetime.strptime(schedule_start[6], self.time_formats['long']))
        race_end = self.__localTime(datetime.strptime(schedule_end[6], self.time_formats['long']))

        race_starts_in = str(race_start - datetime.now(timezone(self.timezone))).split('.')[0]        
        track_info = [d.get_text() for d in coming_up_div.select("ul li")][2].split(': ')[1]

        # getting data from api
        json_file = requests.get(f"{self.__url}/current.json").json()
        races_json = json2obj(json_file)["MRData"]['RaceTable']['Races']

        race = {}
        for i, _race in enumerate(races_json):
            if datetime.strptime(f"{_race['date']} {_race['time']}".replace('Z', ''), self.time_formats['combined']) < datetime.now():
                if _race['Circuit']['Location']['country'] == "UAE":
                    return "End of session"
                else:
                    race = races_json[i+1]

        country = race['Circuit']['Location']['country']
        date = datetime.strptime(race['date'], self.time_formats['date']).strftime(self.time_formats['show'])
        circuit_name = race['Circuit']['circuitName']

        race_info = f"Country: {country}\n"
        race_info += f"Circuit: {circuit_name} ({track_info})\n"
        
        race_info += f"Date: {date} ({race_starts_in})\n\n"
        race_info += "Schedule:\n"

        table = []

        for i in range(3):
            table.append([f"FP{i+1}", f"{free_practices_start[i].strftime(show_format_0)}", f"{free_practices_start[i].strftime(show_format_1)}", f"{free_practices_end[i].strftime(show_format_1)}"])
            
        table.append(["", "", "", ""])

        for i in range(3):
            table.append([f"Q{i+1}", f"{qualifyings_start[i].strftime(show_format_0)}", f"{qualifyings_start[i].strftime(show_format_1)}", f"{qualifyings_end[i].strftime(show_format_1)}"])

        table.append(["", "", "", ""])
        table.append(["Race", f"{race_start.strftime(show_format_0)}", f"{race_start.strftime(show_format_1)}", f"{race_end.strftime(show_format_1)}"])

        race_info += tabulate(table, headers=["", "Date", "Starts", "Ends"], tablefmt='simple', stralign="center")

        return race_info

    def NextWeek(self):
        """ Returns a string created by 'tabulate' """

        json_file = requests.get(f"{self.__url}/current.json").json()
        races_json = json2obj(json_file)["MRData"]['RaceTable']['Races']

        race = {}
        for i, _race in enumerate(races_json):
            if datetime.strptime(f"{_race['date']} {_race['time']}".replace('Z', ''), self.time_formats['combined']) < datetime.now():
                if _race['Circuit']['Location']['country'] == "UAE":
                    return "End of session"
                else:
                    race = races_json[i + 2]

        country = race['Circuit']['Location']['country']
        date = datetime.strptime(race['date'], self.time_formats['date']).strftime(self.time_formats['show'])
        circuit_name = race['Circuit']['circuitName']

        return tabulate([["Circuit", f"{circuit_name}"], ["Date", f"{date}"]], headers=["Country",f"{country}"], tablefmt='plain')

    def LastQualifyingResults(self):
        """ Returns a tuple. 1st index is the place where the race was hosted, 2nd is the data. """

        json_requests = requests.get(f"{self.__url}/current/last/qualifying.json").json()
        json_file = json2obj(json_requests)

        results = json_file["MRData"]['RaceTable']['Races'][0]['QualifyingResults']
        circuit_name = json_file["MRData"]['RaceTable']['Races'][0]['raceName']

        table = []
        for pos, result in enumerate(results, 1):
            driver_name = f"{result['Driver']['givenName']} {result['Driver']['familyName']}"
            q1 = result['Q1'] if 'Q1' in result else "-"
            q2 = result['Q2'] if 'Q2' in result else "-"
            q3 = result['Q3'] if 'Q3' in result else "-"

            table.append([f"{pos}", f"{driver_name}", q1, q2, q3])

        return (circuit_name, tabulate(table, headers=["Pos", "Driver", "Q1", "Q2", "Q3"], tablefmt='orgtbl', numalign="right", stralign="center"))

    def LastRaceResults(self):
        """ Returns a tuple. 1st index is the place where the race was hosted, 2nd is the data. """

        json_requests = requests.get(f"{self.__url}/current/last/results.json").json()
        json_file = json2obj(json_requests)

        results = json_file["MRData"]['RaceTable']['Races'][0]['Results']
        circuit_name = json_file["MRData"]['RaceTable']['Races'][0]['raceName']

        table = []
        for pos, result in enumerate(results, 1):
            driver_name = f"{result['Driver']['givenName']} {result['Driver']['familyName']}"
            s_grid = result['grid'] if result['grid'] != "0" else "Pit"
            status = result['status']

            fl = "■■" if result['FastestLap']['rank'] == "1" else ""

            table.append([f"{pos}", f"{driver_name}", fl, s_grid, status])

        return (circuit_name, tabulate(table, headers=["Pos", "Driver", "FL", "Grid Pos", "Status"], tablefmt='orgtbl', numalign="right", stralign="center"))

    def DriverStandings(self, year="current"):
        """ Returns a string created by 'tabulate' """

        json_file = requests.get(f"{self.__url}/{year}/driverStandings.json").json()

        _driver_standings = json2obj(json_file)["MRData"]['StandingsTable']['StandingsLists'][0]['DriverStandings']

        table = []
        for pos, ds in enumerate(_driver_standings, 1):
            driver_name = f"{ds['Driver']['givenName']} {ds['Driver']['familyName']}"

            table.append([f"{pos}", f"{driver_name}", f"{ds['points']}"])

        return tabulate(table, headers=["Pos", "Driver", "Points"], tablefmt='orgtbl', numalign="right", stralign="center")

    def ConstructorStandings(self, year="current"):
        """ Returns a string created by 'tabulate' """

        json_file = requests.get(f"{self.__url}/{year}/constructorStandings.json").json()

        _constructors_standings = json2obj(json_file)["MRData"]['StandingsTable']['StandingsLists'][0]['ConstructorStandings']

        table = []
        for pos, cs in enumerate(_constructors_standings, 1):
            team_name = cs['Constructor']['name']

            table.append([f"{pos}", f"{team_name}", f"{cs['points']}"])

        return tabulate(table, headers=["Pos", "Driver", "Points"], tablefmt='orgtbl', numalign="right", stralign="center")

    def Calendar(self, year="current"):
        """ Returns a string created by 'tabulate' """

        json_file = requests.get(f"{self.__url}/{year}.json").json()

        races = json2obj(json_file)["MRData"]['RaceTable']['Races']

        table = []
        for race in races:
            country = race['Circuit']['Location']['country']
            circuit_name = race['Circuit']['circuitName']
            date = datetime.strptime(race['date'], self.time_formats['date']).strftime(self.time_formats['show'])

            box = "■" if datetime.strptime(f"{race['date']} {race['time']}".replace('Z', ''), self.time_formats['combined']) < datetime.now() else " "

            table.append([f"{country}", f"{circuit_name}", f"{date}", f"{box}"])

        return tabulate(table, headers=["Country", "Circuit", "Date", " "], tablefmt='orgtbl', stralign="center")

def json2obj(json_file): 
    return json.loads(json.dumps(json_file))
