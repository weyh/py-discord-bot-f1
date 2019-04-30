import os, requests, time, discord
from discord.ext import commands
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
from random import randrange
from tabulate import tabulate
from stopwatch import Stopwatch

from debug import Debug

Debug.Warning("SYS", "Loading...")

USER_CFG = {k:v.replace("\n", "").replace(" ", "") for k, v in (l.split(':') for l in open("usr.cfg"))}
TIME_FORMAT = "%a %b %d %Y %H:%M:%S %Z%z"
VERSION = "v1.0.2"
HELP_LIST = [["Upcoming race weekend:", "--upcoming\n--coming_up"],
                ["The race weekend after the upcoming one:", "--next_week"],
                ["Top 10 from last race:", "--last_top10"],
                ["Current Driver Standings:", "--driver_standings \n--ds"],
                ["Current Constructors Standings:", "--constructors_standings\n--constructors \n--cs"],
                ["Championship Calendar:", "--calendar"],
                ["News:", "--news\n--short_news"],
                ["Long News (6 articles):", "--long_news"],
                ["Random Kimi:", "--bwoah\n--mwoah"],
                ["Version:", "--version"],
                ["Help:", "--help"]]

client = commands.Bot(command_prefix = USER_CFG.get('prefix'))
client.remove_command("help")

@client.event
async def on_ready():
    Debug.Clear()
    Debug.Warning("SYS", "Bot is ready")
    Debug.Warning("SYS", "Logging started...")
    Debug.Print("----------------")
    return

@client.command(aliases=["coming_up"])
async def upcoming(ctx):
    Debug.Log(f"user: {ctx.author}", "Started upcoming")

    sw = Stopwatch()
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

    await send_msg(ctx, race_info)

    Debug.Warning("SYS", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()
    return

@client.command()
async def next_week(ctx):
    Debug.Log(f"user: {ctx.author}", "Started next_week")

    sw = Stopwatch()
    race_info = ""

    if isSiteUp():
        page = requests.get('https://www.autosport.com/f1/calendar')
        soup = BeautifulSoup(page.content, 'html.parser')
        calendar = soup.find('div', class_='columnsContainer').find('div', 'leftColumn').select("table tbody tr td")

        i = 3

        while i < len(calendar):
            if len(calendar[i].contents) == 0:
                n_race = [r.get_text() for r in calendar[i + 1:i + 4]]
                race_info = tabulate([["Circuit", f"{n_race[1]}"], ["Date",f"{n_race[2]}"]], headers=["Race",f"{n_race[0]}"], tablefmt='plain')
                break
            else:
                i += 4

        Debug.Log("next_week", race_info)
    else:
        Debug.Error("SYS (next_week)", "Site is down")
        race_info = "Error: Unable to reach https://www.autosport.com"

    await send_msg(ctx, race_info)

    Debug.Warning("SYS", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()
    return

@client.command()
async def last_top10(ctx):
    Debug.Log(f"user: {ctx.author}", "Started last_top10")

    sw = Stopwatch()
    r_text = ""

    if isSiteUp():
        page = requests.get('https://www.autosport.com/f1')
        soup = BeautifulSoup(page.content, 'html.parser')

        drivers = [d.get_text() for d in soup.find_all('div', class_='stats')[0].select("table tbody tr td:nth-child(2) a")]
        teams = [t.get_text() for t in soup.find_all('div', class_='stats')[0].select("table tbody tr td:nth-child(3)")]

        table = []
        index = 0
        while index < len(drivers):
            table.append([f"{index+1}", f"{drivers[index]}", f"{teams[index]}"])
            index += 1

        r_text += tabulate(table, headers=["Pos", "Driver", "Points"], tablefmt='orgtbl', numalign="right", stralign="center")
        Debug.Log("last_top10", r_text)
    else:
        Debug.Error("SYS (last_top10)", "Site is down")
        r_text = "Error: Unable to reach https://www.autosport.com"

    await send_msg(ctx, "Last week's top 10: ```" + r_text + "```")

    Debug.Warning("SYS", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()
    return

@client.command(aliases=["ds"])
async def driver_standings(ctx):
    Debug.Log(f"user: {ctx.author}", "Started driver_standings")

    sw = Stopwatch()
    r_text = ""

    if isSiteUp():
        page = requests.get('https://www.autosport.com/f1/standings')
        soup = BeautifulSoup(page.content, 'html.parser')

        _driver_standings = soup.find('div', class_='columnsContainer').find('div', 'leftColumn').select("table:nth-child(1) tbody tr")[1:]

        table = []

        for tr in _driver_standings:
            pos = tr.select("td:nth-child(1)")[0].get_text()
            driver = tr.select("td:nth-child(2) a")[0].get_text()
            points = tr.select("td:nth-child(3)")[0].get_text()

            table.append([f"{pos}", f"{driver}", f"{points}"])

        r_text += tabulate(table, headers=["Pos", "Driver", "Points"], tablefmt='orgtbl', numalign="right", stralign="center")
        Debug.Log("driver_standings", r_text)
    else:
        Debug.Error("SYS (driver_standings)", "Site is down")
        r_text = "Error: Unable to reach https://www.autosport.com"

    await send_msg(ctx, "Driver Standings: ```"+r_text+"```")

    Debug.Warning("SYS", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()
    return

@client.command(aliases=["constructors", "cs"])
async def constructors_standings(ctx):
    Debug.Log(f"user: {ctx.author}", "Started constructors_standings")

    sw = Stopwatch()
    r_text = ""

    if isSiteUp():
        page = requests.get('https://www.autosport.com/f1/standings')
        soup = BeautifulSoup(page.content, 'html.parser')

        _constructors_standings = soup.find('div', class_='columnsContainer').find('div', 'leftColumn').select("table:nth-child(2) tbody tr")[1:]

        table = []

        for tr in _constructors_standings:
            pos = tr.select("td:nth-child(1)")[0].get_text()
            team = tr.select("td:nth-child(2)")[0].get_text()
            points = tr.select("td:nth-child(3)")[0].get_text()

            table.append([f"{pos}", f"{team}", f"{points}"])

        r_text += tabulate(table, headers=["Pos", "Constructor", "Points"], tablefmt='orgtbl', numalign="right", stralign="center")
        Debug.Log("constructors_standings", r_text)
    else:
        Debug.Error("SYS (constructors_standings)", "Site is down")
        r_text = "Error: Unable to reach https://www.autosport.com"

    await send_msg(ctx, "Constructors Standings:\n ```"+r_text+"```")

    Debug.Warning("SYS", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()
    return

@client.command()
async def calendar(ctx):
    Debug.Log(f"user: {ctx.author}", "Started calendar")

    sw = Stopwatch()
    race_info = ""

    if isSiteUp():
        page = requests.get('https://www.autosport.com/f1/calendar')
        soup = BeautifulSoup(page.content, 'html.parser')

        calendar = soup.find('div', class_='columnsContainer').find('div', 'leftColumn').select("table tbody tr td")

        table = []

        for i in range(len(calendar)):
            if (i + 1) % 4  == 0:
                n_race = [r.get_text() for r in calendar[i - 3:i]]
                if len(calendar[i].contents) == 0:
                    table.append([f"{n_race[0]}", f"{n_race[1]}", f"{n_race[2]}", " "])
                else:
                    table.append([f"{n_race[0]}", f"{n_race[1]}", f"{n_race[2]}", "■"])

        race_info += tabulate(table, headers=["Race", "Circuit", "Date", " "], tablefmt='orgtbl', stralign="center")
        Debug.Log("calendar", race_info)
    else:
        Debug.Error("SYS (calendar)", "Site is down")
        race_info = "Error: Unable to reach https://www.autosport.com"

    await send_msg(ctx, "Calendar: ```"+race_info+"```")
    return

@client.command(aliases=["short_news"])
async def news(ctx):
    Debug.Log(f"user: {ctx.author}", "Started news")

    sw = Stopwatch()
    news = []

    if isSiteUp():
        page = requests.get('https://www.autosport.com/f1')
        soup = BeautifulSoup(page.content, 'html.parser')
        news_soup = list(soup.find('div', class_='columnsContainer').find('div', 'leftColumn').find("div", class_="row small-up-2 medium-up-3").select("div div .newsitem"))[:3]

        for n_soup in news_soup:
            article_url = n_soup.find("a").get("href")
            article_img = "http://"+n_soup.find("a").find("img").get("data-src")[2:]
            article_title = article_url.split('/')[4].replace('-', ' ').capitalize()
            article_description = n_soup.find("span", class_="sell").get_text() 

            embed = discord.Embed(title=article_title, colour=discord.Colour(0xff2800), url=str("https://www.autosport.com"+article_url), description=article_description)
            embed.set_thumbnail(url=article_img)

            news.append(embed)

        Debug.Log("news", news)
    else:
        Debug.Error("SYS (news)", "Site is down")
        news = "Error: Unable to reach https://www.autosport.com"

    await send_msg(ctx, "News:")
    await send_embed_msg(ctx, news)

    Debug.Warning("SYS", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()
    return

@client.command()
async def long_news(ctx):
    Debug.Log(f"user: {ctx.author}", "Started long_news")

    sw = Stopwatch()
    news = []

    if isSiteUp():
        page = requests.get('https://www.autosport.com/f1')
        soup = BeautifulSoup(page.content, 'html.parser')
        news_soup = list(soup.find('div', class_='columnsContainer').find('div', 'leftColumn').find("div", class_="row small-up-2 medium-up-3").select("div div .newsitem"))

        for n_soup in news_soup:
            article_url = n_soup.find("a").get("href")
            article_img = "http://"+n_soup.find("a").find("img").get("data-src")[2:]
            article_title = article_url.split('/')[4].replace('-', ' ').capitalize()
            article_description = n_soup.find("span", class_="sell").get_text() 

            embed = discord.Embed(title=article_title, colour=discord.Colour(0xff2800), url=str("https://www.autosport.com"+article_url), description=article_description)
            embed.set_thumbnail(url=article_img)

            news.append(embed)

        Debug.Log("news", news)
    else:
        Debug.Error("SYS (news)", "Site is down")
        news = "Error: Unable to reach https://www.autosport.com"

    await send_msg(ctx, "News:")
    await send_embed_msg(ctx, news)

    Debug.Warning("SYS", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()
    return

@client.command(aliases=["mwoah"])
async def bwoah(ctx):
    Debug.Log(f"user: {ctx.author}", "Started bwoah")

    sw = Stopwatch()
    rnd = randrange(file_len("kimi.txt"))

    with open("kimi.txt") as fp:
        for i, l in enumerate(fp):
            if rnd == i:
                Debug.Log("bwoah", "random kimi: " + l)
                await send_msg(ctx, l)
                break

    Debug.Warning("SYS", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()
    return

@client.command()
async def help(ctx):
    Debug.Print(f">> user: {ctx.author} > Help was called")

    sw = Stopwatch()
    await ctx.channel.send("Help: ```" + tabulate(HELP_LIST, headers=[" ", " "], stralign="left", tablefmt='plain') + "```")

    Debug.Warning("SYS", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()
    return

@client.command()
async def version(ctx):
    Debug.Print(f">> user: {ctx.author} > Version was called")

    sw = Stopwatch()
    await send_msg(ctx, f"```css \nVersion: {VERSION}```")

    Debug.Warning("SYS", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()
    return

async def send_embed_msg(ctx, msg):
    if isinstance(msg, list):
        for m in msg:
            await ctx.channel.send(embed=m)
    else:
        await ctx.channel.send(embed=msg)
    return

async def send_msg(ctx, msg):
    await ctx.channel.send(msg)
    return

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def localTime(time):
    return time.astimezone(timezone(USER_CFG.get('timezone')))

def isSiteUp():
    return requests.head('https://www.autosport.com/f1').status_code == 200

Debug.Warning("SYS", f"Version: {VERSION}")
Debug.Warning("SYS", f"Token found: {len(USER_CFG.get('token')) != 0}")
Debug.Warning("SYS", f"Time zone: {USER_CFG.get('timezone')}")
Debug.Warning("SYS", f"Site up: {isSiteUp()}")
Debug.Warning("SYS", f"Prefix: {USER_CFG.get('prefix')}")

client.run(USER_CFG.get("token"))
