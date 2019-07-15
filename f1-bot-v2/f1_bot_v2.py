# -*- coding: utf-8 -*-
import os, requests, time
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
from tabulate import tabulate
from stopwatch import Stopwatch

from Core import *

splash_screen.show()

START_TIME = datetime.now()
VERSION = "v2.0.1"
USER_CFG = cfg_dictionary.read()

cfg_dictionary.update_from_argv(USER_CFG, VERSION)
cfg_dictionary.test(USER_CFG)

Debug.debug = USER_CFG.get("debug")
HELP_LIST = [["Upcoming race weekend:", f"{USER_CFG.get('prefix')}upcoming\n{USER_CFG.get('prefix')}coming_up"],
                ["The race weekend after the upcoming one:", f"{USER_CFG.get('prefix')}next_week"],
                ["Current Driver Standings:", f"{USER_CFG.get('prefix')}driver_standings \n{USER_CFG.get('prefix')}ds"],
                ["Current Constructors Standings:", f"{USER_CFG.get('prefix')}constructors_standings\n{USER_CFG.get('prefix')}constructors \n{USER_CFG.get('prefix')}cs"],
                ["Championship Calendar:", f"{USER_CFG.get('prefix')}calendar"],
                ["Last Race Results:", f"{USER_CFG.get('prefix')}last_race_results\n{USER_CFG.get('prefix')}last_race\n{USER_CFG.get('prefix')}lrr"],
                ["Last Qualifying Results:", f"{USER_CFG.get('prefix')}last_qualifying_results\n{USER_CFG.get('prefix')}last_qualifying\n{USER_CFG.get('prefix')}lqr"],
                ["News:", f"{USER_CFG.get('prefix')}news"],
                ["Clear:", f"{USER_CFG.get('prefix')}clear\n{USER_CFG.get('prefix')}clean\n{USER_CFG.get('prefix')}cls"],                
                ["Uptime:", f"{USER_CFG.get('prefix')}uptime"],
                ["Version:", f"{USER_CFG.get('prefix')}version"],
                ["Help:", f"{USER_CFG.get('prefix')}help"]]

client = commands.Bot(command_prefix = USER_CFG.get('prefix'))
client.remove_command("help")

@client.event
async def on_ready():
    Debug.Clear()
    Debug.Log("SYS", "Bot is ready", True)
    Debug.Log("SYS", "Logging started...")
    Debug.Print("----------------")
    return

@client.command(aliases=["coming_up"])
async def upcoming(ctx):
    Debug.Warning(f"user: {ctx.author}", "Started upcoming")

    sw = Stopwatch()
    race_info = "Coming Up:\n"
    race_info += "```json\n"

    race_info += EDAW.Get(USER_CFG.get('timezone')).Upcoming()

    race_info += "```"

    Debug.Log("upcoming", race_info)

    await send_msg(ctx, race_info)

    Debug.Warning("SYS (upcoming)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()
    return

@client.command()
async def next_week(ctx):
    Debug.Warning(f"user: {ctx.author}", "Started next_week")

    sw = Stopwatch()
    race_info = "Next Race:\n"
    race_info += "```json\n"

    race_info += EDAW.Get().NextWeek()

    race_info += "```"

    Debug.Log("next_week", race_info)
    await send_msg(ctx, race_info)

    Debug.Warning("SYS (next_week)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()
    return

@client.command(aliases=["ds"])
async def driver_standings(ctx):
    Debug.Warning(f"user: {ctx.author}", "Started driver_standings")

    sw = Stopwatch()

    ds = EDAW.Get().DriverStandings()

    Debug.Log("driver_standings", ds)
    await send_msg(ctx, "Driver Standings:\n```" + ds + "```")

    Debug.Warning("SYS (driver_standings)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()
    return

@client.command(aliases=["constructors", "cs"])
async def constructors_standings(ctx):
    Debug.Warning(f"user: {ctx.author}", "Started constructors_standings")

    sw = Stopwatch()

    cs = EDAW.Get().ConstructorStandings()

    Debug.Log("constructors_standings", cs)
    await send_msg(ctx, "Constructors Standings:\n```" + cs + "```")

    Debug.Warning("SYS (constructors_standings)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()
    return

@client.command()
async def calendar(ctx):
    Debug.Warning(f"user: {ctx.author}", "Started calendar")

    sw = Stopwatch()

    _calendar = EDAW.Get().Calendar()

    Debug.Log("calendar", _calendar)
    await send_msg(ctx, "Calendar:\n```" + _calendar + "```")

    Debug.Warning("SYS (calendar)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()
    return

@client.command(aliases=["last_race", "lrr"])
async def last_race_results(ctx):
    Debug.Warning(f"user: {ctx.author}", "Started last_race_results")

    sw = Stopwatch()

    lrr = EDAW.Get().LastRaceResults()

    Debug.Log("last_race_results", lrr[1])
    await send_msg(ctx, f"Last Race Results: {lrr[0]} \n```" + lrr[1] + "```")

    Debug.Warning("SYS (last_race_results)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()
    return

@client.command(aliases=["last_qualifying", "lqr"])
async def last_qualifying_results(ctx):
    Debug.Warning(f"user: {ctx.author}", "Started last_qualifying_results")

    sw = Stopwatch()

    lqr = EDAW.Get().LastQualifyingResults()

    Debug.Log("last_qualifying_results", lqr[1])
    await send_msg(ctx, f"Last Qualifying Results: {lqr[0]} \n```" + lqr[1] + "```")

    Debug.Warning("SYS (last_qualifying_results)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()
    return

@client.command(aliases=["short_news"])
async def news(ctx):
    Debug.Warning(f"user: {ctx.author}", "Started news")

    sw = Stopwatch()
    news = []

    if isSiteUp():
        page = requests.get('https://www.autosport.com/f1')
        soup = BeautifulSoup(page.content, 'html.parser')
        news_soup = list(soup.find('div', class_='columnsContainer').find('div', 'leftColumn').find("div", class_="row small-up-2 medium-up-3").select("div div .newsitem"))[:3]

        for n_soup in news_soup:
            article_url = n_soup.find("a").get("href")
            article_img = "http://" + n_soup.find("a").find("img").get("data-src")[2:]
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

    Debug.Warning("SYS (news)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()
    return

@client.command(aliases=["f2", "formula2"], pass_context=True)
async def _f2_modele(ctx, *, message):
    try:
        import f2_module
    except ModuleNotFoundError:
        Debug.Error(f"SYS", f"f2_module was called but its not installed!")
        return

    Debug.Warning(f"user: {ctx.author}", f"Started f2_modele({message})")
    sw = Stopwatch()

    msg_type, msg = f2_module.resolve(message, USER_CFG)

    if msg_type == "embed":
        await send_msg(ctx, "News:")
        await send_embed_msg(ctx, msg)
    else:
        await send_msg(ctx, msg)

    Debug.Warning(f"SYS f2_modele({message})", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()
    return

@client.command()
async def uptime(ctx):
    global START_TIME
    Debug.Warning(f"user: {ctx.author}", "Started bwoah")

    sw = Stopwatch()

    timedelta = datetime.now() - START_TIME

    Debug.Log("uptime", "Uptime: " + str(round(timedelta.total_seconds())) + "s")
    await send_msg(ctx, "Uptime: " + str(round(timedelta.total_seconds())) + "s")

    Debug.Warning("SYS (uptime)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()
    return

@client.command(aliases=["clean", "cls"])
async def clear(ctx):
    Debug.Warning(f"user: {ctx.author}", "Started clear")

    sw = Stopwatch()
    messages = await ctx.message.channel.history().flatten()

    Debug.Log(f"clear", f"Msg list length {len(messages)}")

    for message in messages:
        if message.author.bot or message.content[:len(USER_CFG.get('prefix'))] == USER_CFG.get('prefix'):
            await message.delete()
        
    Debug.Warning("SYS (clear)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()
    return

@client.command()
async def help(ctx):
    Debug.Print(f">> user: {ctx.author} > Help")

    sw = Stopwatch()
    await ctx.channel.send("Help: ```" + tabulate(HELP_LIST, headers=[" ", " "], stralign="left", tablefmt='plain') + "```")

    Debug.Warning("SYS", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()
    return

@client.command()
async def version(ctx):
    Debug.Print(f">> user: {ctx.author} > Version")

    sw = Stopwatch()
    await send_msg(ctx, f"```yaml\nVersion: {VERSION}\n```")

    Debug.Warning("SYS (version)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
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

isSiteUp = lambda: requests.head('https://www.autosport.com/f1').status_code == 200

Debug.Warning("Boot", "Version: {VERSION}")
Debug.Log("Boot", f"Token found: {len(USER_CFG.get('token')) != 0}")
Debug.Log("Boot", f"Time zone: {USER_CFG.get('timezone')}")
Debug.Log("Boot", f"Site up: {isSiteUp()}")
Debug.Log("Boot", f"Prefix: {USER_CFG.get('prefix')}")

client.run(USER_CFG.get("token"))