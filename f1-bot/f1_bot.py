import os, requests, discord
from discord.ext import commands
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
from random import randrange
from SeeSharp import Console

client = commands.Bot(command_prefix = '--')
TIME_FORMAT = "%a %b %d %Y %H:%M:%S %Z%z"

@client.event
async def on_ready():    
    Console.EndColor()
    Console.Clear()
    log("sys", "Bot is ready")
    log("sys", "Logging started:")
    print("----------------")
    return

@client.event
async def on_message(message):
    
    if message.content[:2] == "--":
        if message.content[2:].find("upcoming") != -1:
            await upcoming(message)

        if message.content[2:].find("next_week") != -1:
            await next_week(message)

        if message.content[2:].find("last_top10") != -1:
            await last_top10(message)

        if message.content[2:].find("bwoah") != -1:
            await bwoah(message)

        if message.content[2:].find("help") != -1:
            log("help", "help was called")
            await message.channel.send(HELP_LIST)
    return

async def upcoming(message):
    race_info = ""
    i=0

    if not isSiteUp():
        for line in F1CALENDAR_FALLBACK:
            current_date = datetime.now()
            date_of_race = datetime.strptime(str(line.split('|')[0]), '%Y-%m-%d')

            race_h = int(line.split('|')[6].split(',')[1].split(':')[0])        
            current_h = int(current_date.hour)
        
            if date_of_race >= current_date:
                race_info = line

                if current_h >= race_h and date_of_race == current_date:
                    race_info = F1CALENDAR_FALLBACK[i+1]

                break

            i += 1
        
        log("upcoming", "OFFLINE")
        race_info = sytle_text(race_info)
    else:
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

    log("upcoming", "\n"+race_info)          
    await send_msg(message, race_info)
    return

async def next_week(message):
    race_line = ""
    i=0

    for line in F1CALENDAR_FALLBACK:
        current_date = datetime.now()
        date_of_race = datetime.strptime(str(line.split('|')[0]), '%Y-%m-%d')

        if date_of_race >= current_date:
            race_line = F1CALENDAR_FALLBACK[i+1]
            break

        i += 1

    log("next_week", "\n" + sytle_text(race_line))            
    await send_msg(message, sytle_text(race_line))
    return

async def last_top10(message):
    r_text = ""

    page = requests.get('https://www.autosport.com/f1')
    soup = BeautifulSoup(page.content, 'html.parser')

    drivers = [d.get_text() for d in soup.find_all('div', class_='stats')[0].select("table tbody tr td:nth-child(2) a")]
    teams = [t.get_text() for t in soup.find_all('div', class_='stats')[0].select("table tbody tr td:nth-child(3)")]

    log("team/drivers",f"{drivers}/{teams}")

    index = 0

    while index < len(drivers):
        r_text += f"{str_extra0(index+1)}| {str(drivers[index])} - {str(teams[index])} \n"
        index += 1

    await send_msg(message, r_text)
    return

async def bwoah(message):
    rnd = randrange(file_len("kimi.txt"))

    with open("kimi.txt") as fp:
        for i, l in enumerate(fp):
            if rnd == i:
                log("bwoah", "random kimi: " + l)
                await send_msg(message, l)
                break
    return

async def send_msg(message, msg):
    if msg == "":
        msg = "Err"
    await message.channel.send(msg)
    return

def sytle_text(text):
    arr = text.split('|')
    r_text = f"Verseny (hely/dátuma): {arr[1]}/{arr[0]} \nMagyar idő: {arr[6].split(',')[1]}Helyi idő: {arr[6].split(',')[0]} \nIdőmérő: {arr[5]} \nFP1: {arr[2]}, FP2: {arr[3]}, FP3: {arr[4]}"

    return r_text

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

id_count = 0

def log(type, msg):
    global id_count

    print(f"> {type} ({id_count}): {msg}")
    id_count += 1
    return

def localTime(time):
    return time.astimezone(timezone(USER_CFG.get('timezone')))

def isSiteUp():
    return requests.head('https://www.autosport.com/f1').status_code == 200

Console.StartColor(Console.Color.Foreground.LIGHTRED())

log("sys", "Reading files...")

USER_CFG = {k:v[:-1] for k, v in (l.split(':') for l in open("usr.cfg"))} # there is a \n somehow

#date|location|FP1|FP2|FP3|Qualifying|Race, Race HU|
_temp_file = open(USER_CFG.get("fallback_calendar"), mode='r') 
F1CALENDAR_FALLBACK = _temp_file.readlines()
_temp_file.close()

log("sys", "Loading...")

log("sys", f"Token found: {len(USER_CFG.get('token')) != 0}")
log("sys", f"Time zone: {USER_CFG.get('timezone')}")
log("sys", f"Fallback calendar: {USER_CFG.get('fallback_calendar')}")
log("sys", f"Site up: {isSiteUp()}")

HELP_LIST = str("Upcoming race weekend: --upcoming \n"+
                "The race weekend after the upcoming one: --next_week \n"+
                "Top 10 from last race: --last_top10 \n"+
                "Random Kimi: --bwoah")

client.run(USER_CFG.get("token"))