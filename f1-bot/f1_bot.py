import os, requests, discord
from discord.ext import commands
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
from random import randrange
from colorama import Fore

from debug import Debug

client = commands.Bot(command_prefix = '--')
TIME_FORMAT = "%a %b %d %Y %H:%M:%S %Z%z"

@client.event
async def on_ready():    
    Debug.Clear()
    Debug.Warning("SYS", "Bot is ready")
    Debug.Warning("SYS", "Logging started...")
    Debug.Print("----------------")
    return

@client.event
async def on_message(message):
    
    if message.content[:2] == "--":
        if message.content[2:].find("upcoming") != -1:
            Debug.Log(f"user: {message.author}", "Started upcoming")
            await upcoming(message)

        if message.content[2:].find("next_week") != -1:
            Debug.Log(f"user: {message.author}", "Started next_week")
            await next_week(message)

        if message.content[2:].find("last_top10") != -1:
            Debug.Log(f"user: {message.author}", "Started last_top10")
            await last_top10(message)

        if message.content[2:].find("bwoah") != -1:
            Debug.Log(f"user: {message.author}", "Started bwoah")
            await bwoah(message)

        if message.content[2:].find("help") != -1:
            Debug.Print(f">> user: {message.author} > Help was called")
            await message.channel.send(HELP_LIST)
    return

async def upcoming(message):
    race_info = ""

    if isSiteUp():
        show_format_1 = "%a %d %b %H:%M"
        show_format_2 = "%H:%M"
        current_date = datetime.now()

        page = requests.get('https://www.autosport.com/f1')
        soup = BeautifulSoup(page.content, 'html.parser')
        coming_up_div = soup.find_all('div', class_='stats')[1]

        location = [d.get_text() for d in coming_up_div.select("span")][1].split(' / ')[0]
        date = [d.get_text() for d in coming_up_div.select("span")][1].split(' / ')[1]

        schedule_start = [d.find("td", class_="text-right").get("data-start") for d in coming_up_div.find("div", class_='time-convert').find("table").find("tbody").find_all("tr")]
        schedule_end = [d.find("td", class_="text-right").get("data-end") for d in coming_up_div.find("div", class_='time-convert').find("table").find("tbody").find_all("tr")]
        
        #todo: refactor with dictionary

        free_practices_start = [localTime(datetime.strptime(d, TIME_FORMAT)) for d in schedule_start[:3]]
        free_practices_end = [localTime(datetime.strptime(d, TIME_FORMAT)) for d in schedule_end[:3]]
        qualifyings_start = [localTime(datetime.strptime(d, TIME_FORMAT)) for d in schedule_start[3:6]]
        qualifyings_end = [localTime(datetime.strptime(d, TIME_FORMAT)) for d in schedule_end[3:6]]
        race_start = localTime(datetime.strptime(schedule_start[6], TIME_FORMAT))
        race_end = localTime(datetime.strptime(schedule_end[6], TIME_FORMAT))

        race_starts_in = str(race_start - datetime.now(timezone(USER_CFG.get('timezone')))).split('.')[0]
        circuit = [d.get_text() for d in coming_up_div.select("ul li")][1].split(': ')[1]
        track = [d.get_text() for d in coming_up_div.select("ul li")][2].split(': ')[1]

        race_info = "COMING UP:\n"
        race_info += f"{location} / {date}\n"
        race_info += f"Race starts in: {race_starts_in}\n"
        race_info += f"Circuit: {circuit}\n"
        race_info += f"Track information: {track}\n"
        race_info += "\nSCHEDULE:\n"
        
        for i in range(3):
            race_info += f"FP{i+1}: {free_practices_start[i].strftime(show_format_1)} - {free_practices_end[i].strftime(show_format_2)}\n"

        race_info += "\n"

        for i in range(3):
            race_info += f"Q{i+1}: {qualifyings_start[i].strftime(show_format_1)} - {qualifyings_end[i].strftime(show_format_2)}\n"

        race_info += "\n"

        race_info += f"Race: {race_start.strftime(show_format_1)} - {race_end.strftime(show_format_2)}\n"
        
        Debug.Log("upcoming", race_info)
    else:
        Debug.Error("SYS (upcoming)", "Site is down")
        race_info = "Error: Unable to reach https://www.autosport.com"
    
    await send_msg(message, race_info)
    return

async def next_week(message):
    race_info = ""
    
    if isSiteUp():
        page = requests.get('https://www.autosport.com/f1/calendar')
        soup = BeautifulSoup(page.content, 'html.parser')
        calendar = soup.find('div', class_='columnsContainer').find('div', 'leftColumn').select("table tbody tr td")

        i = 3

        while i < len(calendar):
            if len(calendar[i].contents) == 0:
                n_race = [r.get_text() for r in calendar[i + 1:i + 4]]
                race_info = f"Race:    {n_race[0]}\nCircuit: {n_race[1]}\nDate:    {n_race[2]}"
                break
            else:
                i += 4

        Debug.Log("next_week", race_info)
    else:
        Debug.Error("SYS (next_week)", "Site is down")
        race_info = "Error: Unable to reach https://www.autosport.com"

    await send_msg(message, race_info)
    return

async def last_top10(message):
    r_text = ""

    if isSiteUp():
        page = requests.get('https://www.autosport.com/f1')
        soup = BeautifulSoup(page.content, 'html.parser')

        drivers = [d.get_text() for d in soup.find_all('div', class_='stats')[0].select("table tbody tr td:nth-child(2) a")]
        teams = [t.get_text() for t in soup.find_all('div', class_='stats')[0].select("table tbody tr td:nth-child(3)")]

        index = 0

        while index < len(drivers):
            r_text += f"{str_extra0(index+1)}| {str(drivers[index])} - {str(teams[index])} \n"
            index += 1

        Debug.Log("last_top10", r_text)
    else:
        Debug.Error("SYS (last_top10)", "Site is down")
        r_text = "Error: Unable to reach https://www.autosport.com"

    await send_msg(message, r_text)
    return

async def bwoah(message):
    rnd = randrange(file_len("kimi.txt"))

    with open("kimi.txt") as fp:
        for i, l in enumerate(fp):
            if rnd == i:
                Debug.Log("bwoah", "random kimi: " + l)
                await send_msg(message, l)
                break
    return

async def send_msg(message, msg):
    if msg == "":
        msg = "Err"
    await message.channel.send(msg)
    return

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def str_extra0(num):
    _r = ""

    if int(num) < 10:
        _r = "0" + str(num)
    
    if num == 10:
        _r = str(num)

    if num == 1 or num == 10:
        _r += " "

    return _r

def localTime(time):
    return time.astimezone(timezone(USER_CFG.get('timezone')))

def isSiteUp():
    return requests.head('https://www.autosport.com/f1').status_code == 200

Debug.Warning("SYS", "Reading files...")

USER_CFG = {k:v[:-1] for k, v in (l.split(':') for l in open("usr.cfg"))} # there is a \n somehow

Debug.Warning("SYS", "Loading...")

Debug.Warning("SYS", f"Token found: {len(USER_CFG.get('token')) != 0}")
Debug.Warning("SYS", f"Time zone: {USER_CFG.get('timezone')}")
Debug.Warning("SYS", f"Site up: {isSiteUp()}")

HELP_LIST = str("Upcoming race weekend: --upcoming \n"+
                "The race weekend after the upcoming one: --next_week \n"+
                "Top 10 from last race: --last_top10 \n"+
                "Random Kimi: --bwoah")

client.run(USER_CFG.get("token"))