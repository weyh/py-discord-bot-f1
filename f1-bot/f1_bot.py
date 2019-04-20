import os
from random import randrange
from datetime import datetime
import discord
from discord.ext import commands

from SeeSharp import Console

client = commands.Bot(command_prefix = '--')

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
        if message.content[2:].find("this_week") != -1:
            await this_week(message)

        if message.content[2:].find("next_week") != -1:
            await next_week(message)

        if message.content[2:].find("last_weeks_top10") != -1:
            await last_weeks_top10(message)

        if message.content[2:].find("bwoah") != -1:
            await bwoah(message)

        if message.content[2:].find("help") != -1:
            log("help", "help was called")
            await message.channel.send(HELP_LIST)
    return

async def this_week(message):
    race_line = ""
    i=0

    for line in F1CALENDAR:
        current_date = datetime.now()
        date_of_race = datetime.strptime(str(line.split('|')[0]), '%Y-%m-%d')

        race_h = int(line.split('|')[6].split(',')[1].split(':')[0])        
        current_h = int(current_date.hour)
        
        if date_of_race >= current_date:
            race_line = line

            if current_h >= race_h and date_of_race == current_date:
                race_line = F1CALENDAR[i+1]

            break

        i += 1

    log("this_week", "\n"+sytle_text(race_line))            
    await send_msg(message, sytle_text(race_line))
    return

async def next_week(message):
    race_line = ""
    i=0

    for line in F1CALENDAR:
        current_date = datetime.now()
        date_of_race = datetime.strptime(str(line.split('|')[0]), '%Y-%m-%d')

        if date_of_race >= current_date:
            race_line = F1CALENDAR[i+1]
            break

        i += 1

    log("next_week", "\n" + sytle_text(race_line))            
    await send_msg(message, sytle_text(race_line))
    return

async def last_weeks_top10(message):
    from bs4 import BeautifulSoup
    import requests

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

Console.StartColor(Console.Color.Foreground.LIGHTRED())

log("sys", "Reading files...")

USER_CFG = {k:v for k, v in (l.split(':') for l in open("usr.cfg"))}

#date|location|FP1|FP2|FP3|Qualifying|Race, Race HU|
_temp_file = open(USER_CFG.get("fallback_calendar"), mode='r')
F1CALENDAR = _temp_file.readlines()
_temp_file.close()

log("sys", "Loading...")

HELP_LIST = str("Teljes információ az elkövetkező verseny hétről: --this_week \n"+
                "Teljes információ a következő utáni verseny hétről: --next_week \n"+
                "Előző hét top 10: --last_weeks_top10 \n"+
                "Random Kimi: --bwoah")

client.run(USER_CFG.get("token"))