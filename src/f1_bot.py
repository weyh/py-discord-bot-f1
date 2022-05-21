# -*- coding: utf-8 -*-
import atexit
import time
from typing import Iterable, Union
from datetime import datetime
from tabulate import tabulate
from stopwatch import Stopwatch
from colorama import Fore
from Core import *
from discord.ext import commands
import logging

VERSION = "v3.0.0"
START_TIME = datetime.now()

logging.getLogger('discord').setLevel(level=logging.ERROR)
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
HELP_LIST = [["Current race weekend:", f"{USER_CFG.prefix}current"],
             ["The race weekend after current:", f"{USER_CFG.prefix}fw\n{USER_CFG.prefix}following_week"],
             ["Current driver standings:", f"{USER_CFG.prefix}ds\n{USER_CFG.prefix}driver_standings"],
             ["Current constructors standings:", f"{USER_CFG.prefix}cs\n{USER_CFG.prefix}constructors_standings"],
             ["Championship calendar:", f"{USER_CFG.prefix}calendar"],
             ["Last race results:", f"{USER_CFG.prefix}lrr\n{USER_CFG.prefix}last_race_results"],
             ["Last qualifying results:", f"{USER_CFG.prefix}lqr\n{USER_CFG.prefix}last_qualifying_results"],
             ["Clear bot messages:", f"{USER_CFG.prefix}clear"],
             ["Uptime:", f"{USER_CFG.prefix}uptime"],
             ["Version:", f"{USER_CFG.prefix}version"],
             ["Help:", f"{USER_CFG.prefix}help"]]

client = commands.Bot(command_prefix=USER_CFG.prefix)
client.remove_command("help")


@client.event
async def on_ready():
    Console.log("SYS", "Bot is ready", True)
    Console.log("SYS", "Logging started!")
    print("-------------------------")


@client.command()
async def current(ctx: commands.Context):
    Console.printc(f"user: {ctx.author} Started current", Fore.LIGHTBLUE_EX)

    sw = Stopwatch()

    race_info = f"```json\n{API.Get.current()}```"

    Console.log("current", race_info)
    await send_msg(ctx, race_info)

    Console.log("SYS (current)", f"Total time taken: {round(sw.duration * 1000)} ms")
    sw.reset()


@client.command(aliases=["fw"])
async def following_week(ctx: commands.Context):
    Console.printc(f"user: {ctx.author} Started following_week", Fore.LIGHTBLUE_EX)

    sw = Stopwatch()

    race_info = f"Following Week:\n```json\n{API.Get.next_week()}```"

    Console.log("following_week", race_info)
    await send_msg(ctx, race_info)

    Console.log("SYS (following_week)", f"Total time taken: {round(sw.duration * 1000)} ms")
    sw.reset()


@client.command(aliases=["ds"])
async def driver_standings(ctx: commands.Context):
    Console.printc(f"user: {ctx.author} Started driver_standings", Fore.LIGHTBLUE_EX)

    sw = Stopwatch()

    ds = API.Get.driver_standings()

    Console.log("driver_standings", ds)
    await send_msg(ctx, f"Driver Standings:\n```{ds}```")

    Console.log("SYS (driver_standings)", f"Total time taken: {round(sw.duration * 1000)} ms")
    sw.reset()


@client.command(aliases=["cs"])
async def constructors_standings(ctx: commands.Context):
    Console.printc(f"user: {ctx.author} Started constructors_standings", Fore.LIGHTBLUE_EX)

    sw = Stopwatch()

    cs = API.Get.constructor_standings()

    Console.log("constructors_standings", cs)
    await send_msg(ctx, f"Constructors Standings:\n```{cs}```")

    Console.log("SYS (constructors_standings)", f"Total time taken: {round(sw.duration * 1000)} ms")
    sw.reset()


@client.command()
async def calendar(ctx: commands.Context):
    Console.printc(f"user: {ctx.author} Started calendar", Fore.LIGHTBLUE_EX)

    sw = Stopwatch()

    _calendar = API.Get.calendar()

    Console.log("calendar", _calendar)
    await send_msg(ctx, f"Calendar:\n```{_calendar}```")

    Console.log("SYS (calendar)", f"Total time taken: {round(sw.duration * 1000)} ms")
    sw.reset()


@client.command(aliases=["lrr"])
async def last_race_results(ctx: commands.Context):
    Console.printc(f"user: {ctx.author} Started last_race_results", Fore.LIGHTBLUE_EX)

    sw = Stopwatch()

    lrr = API.Get.last_race_results()

    Console.log("last_race_results", lrr[1])
    await send_msg(ctx, f"Last Race Results: {lrr[0]}\n```{lrr[1]}```")

    Console.log("SYS (last_race_results)", f"Total time taken: {round(sw.duration * 1000)} ms")
    sw.reset()


@client.command(aliases=["lqr"])
async def last_qualifying_results(ctx: commands.Context):
    Console.printc(f"user: {ctx.author} Started last_qualifying_results", Fore.LIGHTBLUE_EX)

    sw = Stopwatch()

    lqr = API.Get.last_qualifying_results()

    Console.log("last_qualifying_results", lqr[1])
    await send_msg(ctx, f"Last Qualifying Results: {lqr[0]}\n```{lqr[1]}```")

    Console.log("SYS (last_qualifying_results)", f"Total time taken: {round(sw.duration * 1000)} ms")
    sw.reset()


@client.command()
async def uptime(ctx: commands.Context):
    global START_TIME
    Console.printc(f"user: {ctx.author} Started uptime", Fore.LIGHTBLUE_EX)

    sw = Stopwatch()

    timedelta = datetime.now() - START_TIME

    Console.log("uptime", f"Uptime: {timedelta}")
    await send_msg(ctx, f"Uptime: ```json\n{timedelta}```")

    Console.log("SYS (uptime)", f"Total time taken: {round(sw.duration * 1000)} ms")
    sw.reset()


@client.command()
async def clear(ctx: commands.Context):
    Console.printc(f"user: {ctx.author} Started clear", Fore.LIGHTBLUE_EX)

    sw = Stopwatch()
    messages = await ctx.message.channel.history().flatten()

    Console.log(f"clear", f"Msg list length {len(messages)}")

    for message in messages:
        time.sleep(0.2)  # To avoid rate limit
        if message.author.bot or message.content[:len(USER_CFG.prefix)] == USER_CFG.prefix:
            await message.delete()

    Console.log("SYS (clear)", f"Total time taken: {round(sw.duration * 1000)} ms")
    sw.reset()


@client.command()
async def help(ctx: commands.Context):
    Console.printc(f"user: {ctx.author} Started help", Fore.LIGHTBLUE_EX)

    sw = Stopwatch()
    await ctx.send(f"Help: ```{tabulate(HELP_LIST, headers=[' ', ' '], stralign='left', tablefmt='plain')}```")

    Console.log("SYS (help)", f"Total time taken: {round(sw.duration * 1000)} ms")
    sw.reset()


@client.command()
async def version(ctx: commands.Context):
    Console.printc(f"user: {ctx.author} Started version", Fore.LIGHTBLUE_EX)

    sw = Stopwatch()
    await send_msg(ctx, f"```yaml\nVersion: {VERSION}\n```")

    Console.log("SYS (version)", f"Total time taken: {round(sw.duration * 1000)} ms")
    sw.reset()


async def send_embed_msg(ctx: commands.Context, msg: Union[str, Iterable]):
    if isinstance(msg, list):
        for m in msg:
            await ctx.send(embed=m)
    else:
        await ctx.send(embed=msg)


async def send_msg(ctx: commands.Context, msg: str):
    await ctx.send(msg)


def exit_cleanup():
    API.Get.clear()


if __name__ == "__main__":
    Console.warning("Start", f"Version: {VERSION}")
    Console.log("Start", f"Token found: {len(USER_CFG.token) != 0}")
    Console.log("Start", f"Prefix: {USER_CFG.prefix}")
    Console.log("Start", f"Debug: {USER_CFG.debug}")
    Console.log("Start", f"Temp dir: {USER_CFG.temp_dir}")
    Console.log("Start", f"Time zone: {time.tzname[0]}")

    API.Get.init(USER_CFG.temp_dir)
    atexit.register(exit_cleanup)
    client.run(USER_CFG.token)
