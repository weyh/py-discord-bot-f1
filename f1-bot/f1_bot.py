# -*- coding: utf-8 -*-

import time
import discord
from discord.ext import commands
from datetime import datetime
from tabulate import tabulate
from stopwatch import Stopwatch
from colorama import Fore

from Core import *

VERSION = "v2.2.1"
START_TIME = datetime.now()

# args
args = Start.load_args(VERSION)

Start.splash_screen()

if Start("usr.cfg").is_first():
    USER_CFG: UserConfig = UserConfig.creation_ui()
else:
    USER_CFG: UserConfig = UserConfig.load()

if args is not None:
    USER_CFG.update(args)

Console.debug = USER_CFG.debug
Console.timestamp = USER_CFG.timestamp
CacheManager.cache_enabled = USER_CFG.cache
CacheManager.time_delta = USER_CFG.cache_time_delta
HELP_LIST = [["Upcoming race weekend:", f"{USER_CFG.prefix}upcoming\n{USER_CFG.prefix}coming_up"],
             ["The race weekend after the upcoming one:", f"{USER_CFG.prefix}following_week \n{USER_CFG.prefix}fw"],
             ["Current Driver Standings:", f"{USER_CFG.prefix}driver_standings \n{USER_CFG.prefix}ds"],
             ["Current Constructors Standings:", f"{USER_CFG.prefix}constructors_standings\n{USER_CFG.prefix}constructors \n{USER_CFG.prefix}cs"],
             ["Championship Calendar:", f"{USER_CFG.prefix}calendar"],
             ["Last Race Results:", f"{USER_CFG.prefix}last_race_results\n{USER_CFG.prefix}last_race\n{USER_CFG.prefix}lrr"],
             ["Last Qualifying Results:", f"{USER_CFG.prefix}last_qualifying_results\n{USER_CFG.prefix}last_qualifying\n{USER_CFG.prefix}lqr"],
             ["Clear cache:", f"{USER_CFG.prefix}clear_cache"],
             ["Clear:", f"{USER_CFG.prefix}clear\n{USER_CFG.prefix}clean\n{USER_CFG.prefix}cls"],
             ["Uptime:", f"{USER_CFG.prefix}uptime"],
             ["Version:", f"{USER_CFG.prefix}version"],
             ["Help:", f"{USER_CFG.prefix}help"]]

client = commands.Bot(command_prefix=USER_CFG.prefix)
client.remove_command("help")


@client.event
async def on_ready():
    # Console.clear()
    Console.log("SYS", "Bot is ready", True)
    Console.log("SYS", "Logging started!")
    print("-------------------------")


@client.command(aliases=["coming_up"])
async def upcoming(ctx):
    Console.printc(f"user: {ctx.author} Started upcoming", Fore.LIGHTBLUE_EX)

    sw = Stopwatch()

    if CacheManager.valid_cache_exists("upcoming"):
        Console.log("upcoming", "From cache.")
        race_info = CacheManager.load("upcoming").data
    else:
        race_info = f"Coming Up:\n```json\n{EDAW.Get.Upcoming()}```"

        if CacheManager.cache_enabled:
            c = Cache(str(datetime.now()), "upcoming", race_info)
            CacheManager.save(c)

    Console.log("upcoming", race_info)
    await send_msg(ctx, race_info)

    Console.log("SYS (upcoming)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()


@client.command(aliases=["fw"])
async def following_week(ctx):
    Console.printc(f"user: {ctx.author} Started following_week", Fore.LIGHTBLUE_EX)

    sw = Stopwatch()

    if CacheManager.valid_cache_exists("following_week"):
        Console.log("following_week", "From cache.")
        race_info = CacheManager.load("following_week").data
    else:
        race_info = f"Following Week:\n```json\n{EDAW.Get.NextWeek()}```"

        if CacheManager.cache_enabled:
            c = Cache(str(datetime.now()), "following_week", race_info)
            CacheManager.save(c)

    Console.log("following_week", race_info)
    await send_msg(ctx, race_info)

    Console.log("SYS (following_week)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()


@client.command(aliases=["ds"])
async def driver_standings(ctx):
    Console.printc(f"user: {ctx.author} Started driver_standings", Fore.LIGHTBLUE_EX)

    sw = Stopwatch()
    if CacheManager.valid_cache_exists("driver_standings"):
        Console.log("driver_standings", "From cache.")
        ds = CacheManager.load("driver_standings").data
    else:
        ds = EDAW.Get.DriverStandings()

        if CacheManager.cache_enabled:
            c = Cache(str(datetime.now()), "driver_standings", ds)
            CacheManager.save(c)

    Console.log("driver_standings", ds)
    await send_msg(ctx, f"Driver Standings:\n```{ds}```")

    Console.log("SYS (driver_standings)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()


@client.command(aliases=["constructors", "cs"])
async def constructors_standings(ctx):
    Console.printc(f"user: {ctx.author} Started constructors_standings", Fore.LIGHTBLUE_EX)

    sw = Stopwatch()

    if CacheManager.valid_cache_exists("constructors_standings"):
        Console.log("constructors_standings", "From cache.")
        cs = CacheManager.load("constructors_standings").data
    else:
        cs = EDAW.Get.ConstructorStandings()

        if CacheManager.cache_enabled:
            c = Cache(str(datetime.now()), "constructors_standings", cs)
            CacheManager.save(c)

    Console.log("constructors_standings", cs)
    await send_msg(ctx, f"Constructors Standings:\n```{cs}```")

    Console.log("SYS (constructors_standings)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()


@client.command()
async def calendar(ctx):
    Console.printc(f"user: {ctx.author} Started calendar", Fore.LIGHTBLUE_EX)

    sw = Stopwatch()

    if CacheManager.valid_cache_exists("calendar"):
        Console.log("calendar", "From cache.")
        _calendar = CacheManager.load("calendar").data
    else:
        _calendar = EDAW.Get.Calendar()

        if CacheManager.cache_enabled:
            c = Cache(str(datetime.now()), "calendar", _calendar)
            CacheManager.save(c)

    Console.log("calendar", _calendar)
    await send_msg(ctx, f"Calendar:\n```{_calendar}```")

    Console.log("SYS (calendar)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()


@client.command(aliases=["last_race", "lrr"])
async def last_race_results(ctx):
    Console.printc(f"user: {ctx.author} Started last_race_results", Fore.LIGHTBLUE_EX)

    sw = Stopwatch()

    if CacheManager.valid_cache_exists("last_race_results"):
        Console.log("last_race_results", "From cache.")
        lrr = CacheManager.load("last_race_results").data.split('~$~')
    else:
        lrr = EDAW.Get.LastRaceResults()

        if CacheManager.cache_enabled:
            c = Cache(str(datetime.now()), "last_race_results", '~$~'.join(i for i in lrr))
            CacheManager.save(c)

    Console.log("last_race_results", lrr[1])
    await send_msg(ctx, f"Last Race Results: {lrr[0]} \n```{lrr[1]}```")

    Console.log("SYS (last_race_results)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()


@client.command(aliases=["last_qualifying", "lqr"])
async def last_qualifying_results(ctx):
    Console.printc(f"user: {ctx.author} Started last_qualifying_results", Fore.LIGHTBLUE_EX)

    sw = Stopwatch()

    if CacheManager.valid_cache_exists("last_qualifying_results"):
        Console.log("last_qualifying_results", "From cache.")
        lqr = CacheManager.load("last_qualifying_results").data.split('~$~')
    else:
        lqr = EDAW.Get.LastQualifyingResults()

        if CacheManager.cache_enabled:
            c = Cache(str(datetime.now()), "last_qualifying_results", '~$~'.join(i for i in lqr))
            CacheManager.save(c)

    Console.log("last_qualifying_results", lqr[1])
    await send_msg(ctx, f"Last Qualifying Results: {lqr[0]} \n```{lqr[1]}```")

    Console.log("SYS (last_qualifying_results)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()


@client.command()
async def uptime(ctx):
    global START_TIME
    Console.printc(f"user: {ctx.author} Started uptime", Fore.LIGHTBLUE_EX)

    sw = Stopwatch()

    timedelta = datetime.now() - START_TIME

    Console.log("uptime", f"Uptime: {timedelta}")
    await send_msg(ctx, f"Uptime: ```json\n{timedelta}```")

    Console.log("SYS (uptime)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()


@client.command()
async def clear_cache(ctx):
    Console.printc(f"user: {ctx.author} Started clear_cache", Fore.LIGHTBLUE_EX)

    sw = Stopwatch()

    CacheManager.clear()
    await send_msg(ctx, "Cache cleared!")

    Console.log("SYS (clear_cache)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()


@client.command()
async def clear(ctx):
    Console.printc(f"user: {ctx.author} Started clear", Fore.LIGHTBLUE_EX)

    sw = Stopwatch()
    messages = await ctx.message.channel.history().flatten()

    Console.log(f"clear", f"Msg list length {len(messages)}")

    for message in messages:
        if message.author.bot or message.content[:len(USER_CFG.prefix)] == USER_CFG.prefix:
            await message.delete()

    Console.log("SYS (clear)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()


@client.command()
async def help(ctx):
    Console.printc(f"user: {ctx.author} Started help", Fore.LIGHTBLUE_EX)

    sw = Stopwatch()
    await ctx.channel.send(f"Help: ```{tabulate(HELP_LIST, headers=[' ', ' '], stralign='left', tablefmt='plain')}```")

    Console.log("SYS (help)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()


@client.command()
async def version(ctx):
    Console.printc(f"user: {ctx.author} Started version", Fore.LIGHTBLUE_EX)

    sw = Stopwatch()
    await send_msg(ctx, f"```yaml\nVersion: {VERSION}\n```")

    Console.log("SYS (version)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()


async def send_embed_msg(ctx, msg):
    if isinstance(msg, list):
        for m in msg:
            await ctx.channel.send(embed=m)
    else:
        await ctx.channel.send(embed=msg)


async def send_msg(ctx, msg):
    await ctx.channel.send(msg)


if __name__ == "__main__":
    # region Logs
    Console.warning("Start", f"Version: {VERSION}")
    Console.log("Start", f"Token found: {len(USER_CFG.token) != 0}")
    Console.log("Start", f"Prefix: {USER_CFG.prefix}")
    Console.log("Start", f"Debug: {USER_CFG.debug}")
    Console.log("Start", f"Cache: {USER_CFG.cache}")
    Console.log("Start", f"Cache time delta: {USER_CFG.cache_time_delta} sec")
    Console.log("Start", f"Time zone: {time.tzname[0]}")
    # endregion

    client.run(USER_CFG.token)
