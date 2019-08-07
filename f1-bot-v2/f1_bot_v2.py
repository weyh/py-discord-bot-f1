# -*- coding: utf-8 -*-
import requests, time, discord
from discord.ext import commands
from bs4 import BeautifulSoup
from datetime import datetime
from tabulate import tabulate
from stopwatch import Stopwatch

from Core import *

VERSION = "v2.0.5"
START_TIME = datetime.now()

#args
args = Start.load_args(VERSION)

Start.splash_screen()

if Start("usr.cfg").is_first():
    USER_CFG : UserConfig = UserConfig.creation_ui()
else:
    USER_CFG : UserConfig = UserConfig.load()
USER_CFG.update(args)

Console.debug = USER_CFG.debug
CacheManager.cache_enabled = USER_CFG.cache
CacheManager.time_delta = USER_CFG.cache_time_delta
HELP_LIST = [["Upcoming race weekend:", f"{USER_CFG.prefix}upcoming\n{USER_CFG.prefix}coming_up"],
                ["The race weekend after the upcoming one:", f"{USER_CFG.prefix}following_week \n{USER_CFG.prefix}fw"],
                ["Current Driver Standings:", f"{USER_CFG.prefix}driver_standings \n{USER_CFG.prefix}ds"],
                ["Current Constructors Standings:", f"{USER_CFG.prefix}constructors_standings\n{USER_CFG.prefix}constructors \n{USER_CFG.prefix}cs"],
                ["Championship Calendar:", f"{USER_CFG.prefix}calendar"],
                ["Last Race Results:", f"{USER_CFG.prefix}last_race_results\n{USER_CFG.prefix}last_race\n{USER_CFG.prefix}lrr"],
                ["Last Qualifying Results:", f"{USER_CFG.prefix}last_qualifying_results\n{USER_CFG.prefix}last_qualifying\n{USER_CFG.prefix}lqr"],
                ["News:", f"{USER_CFG.prefix}news"],
                ["Clear cache:", f"{USER_CFG.prefix}clear_cache"],
                ["Clear:", f"{USER_CFG.prefix}clear\n{USER_CFG.prefix}clean\n{USER_CFG.prefix}cls"],                
                ["Uptime:", f"{USER_CFG.prefix}uptime"],
                ["Version:", f"{USER_CFG.prefix}version"],
                ["Help:", f"{USER_CFG.prefix}help"]]

client = commands.Bot(command_prefix = USER_CFG.prefix)
client.remove_command("help")

@client.event
async def on_ready():
    Console.clear()
    Console.log("SYS", "Bot is ready", True)
    Console.log("SYS", "Logging started...")
    print("-------------------------")

@client.command(aliases=["coming_up"])
async def upcoming(ctx):
    Console.warning(f"user: {ctx.author}", "Started upcoming")

    sw = Stopwatch()

    if CacheManager.valid_cache_exists("upcoming"):
        Console.log("upcoming", "From cache.")
        race_info = CacheManager.load("upcoming").data
    else:
        race_info = f"Coming Up:\n```json\n{EDAW.Get.Upcoming()}```"
        
        if CacheManager.cache_enabled:
            c = Cache(str(datetime.now()), "upcoming", race_info)
            c.save()

    Console.log("upcoming", race_info)
    await send_msg(ctx, race_info)

    Console.warning("SYS (upcoming)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()

@client.command(aliases=["fw"])
async def following_week(ctx):
    Console.warning(f"user: {ctx.author}", "Started following_week")

    sw = Stopwatch()

    if CacheManager.valid_cache_exists("following_week"):
        Console.log("following_week", "From cache.")
        race_info = CacheManager.load("following_week").data
    else:
        race_info = f"Following Week:\n```json\n{EDAW.Get.NextWeek()}```"

        if CacheManager.cache_enabled:
            c = Cache(str(datetime.now()), "following_week", race_info)
            c.save()

    Console.log("following_week", race_info)
    await send_msg(ctx, race_info)

    Console.warning("SYS (following_week)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()

@client.command(aliases=["ds"])
async def driver_standings(ctx):
    Console.warning(f"user: {ctx.author}", "Started driver_standings")

    sw = Stopwatch()
    if CacheManager.valid_cache_exists("driver_standings"):
        Console.log("driver_standings", "From cache.")
        ds = CacheManager.load("driver_standings").data
    else:
        ds = EDAW.Get.DriverStandings()

        if CacheManager.cache_enabled:
            c = Cache(str(datetime.now()), "driver_standings", ds)
            c.save()

    Console.log("driver_standings", ds)
    await send_msg(ctx, f"Driver Standings:\n```{ds}```")

    Console.warning("SYS (driver_standings)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()

@client.command(aliases=["constructors", "cs"])
async def constructors_standings(ctx):
    Console.warning(f"user: {ctx.author}", "Started constructors_standings")

    sw = Stopwatch()

    if CacheManager.valid_cache_exists("constructors_standings"):
        Console.log("constructors_standings", "From cache.")
        cs = CacheManager.load("constructors_standings").data
    else:
        cs = EDAW.Get.ConstructorStandings()

        if CacheManager.cache_enabled:
            c = Cache(str(datetime.now()), "constructors_standings", cs)
            c.save()

    Console.log("constructors_standings", cs)
    await send_msg(ctx, f"Constructors Standings:\n```{cs}```")

    Console.warning("SYS (constructors_standings)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()

@client.command()
async def calendar(ctx):
    Console.warning(f"user: {ctx.author}", "Started calendar")

    sw = Stopwatch()

    if CacheManager.valid_cache_exists("calendar"):
        Console.log("calendar", "From cache.")
        _calendar = CacheManager.load("calendar").data
    else:
        _calendar = EDAW.Get.Calendar()

        if CacheManager.cache_enabled:
            c = Cache(str(datetime.now()), "calendar", _calendar)
            c.save()

    Console.log("calendar", _calendar)
    await send_msg(ctx, f"Calendar:\n```{_calendar}```")

    Console.warning("SYS (calendar)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()

@client.command(aliases=["last_race", "lrr"])
async def last_race_results(ctx):
    Console.warning(f"user: {ctx.author}", "Started last_race_results")

    sw = Stopwatch()

    if CacheManager.valid_cache_exists("last_race_results"):
        Console.log("last_race_results", "From cache.")
        lrr = CacheManager.load("last_race_results").data.split('~$~')
    else:
        lrr = EDAW.Get.LastRaceResults()

        if CacheManager.cache_enabled:
            c = Cache(str(datetime.now()), "last_race_results", '~$~'.join(i for i in lrr))
            c.save()

    Console.log("last_race_results", lrr[1])
    await send_msg(ctx, f"Last Race Results: {lrr[0]} \n```{lrr[1]}```")

    Console.warning("SYS (last_race_results)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()

@client.command(aliases=["last_qualifying", "lqr"])
async def last_qualifying_results(ctx):
    Console.warning(f"user: {ctx.author}", "Started last_qualifying_results")

    sw = Stopwatch()

    if CacheManager.valid_cache_exists("last_qualifying_results"):
        Console.log("last_qualifying_results", "From cache.")
        lqr = CacheManager.load("last_qualifying_results").data.split('~$~')
    else:
        lqr = EDAW.Get.LastQualifyingResults()

        if CacheManager.cache_enabled:
            c = Cache(str(datetime.now()), "last_qualifying_results", '~$~'.join(i for i in lqr))
            c.save()

    Console.log("last_qualifying_results", lqr[1])
    await send_msg(ctx, f"Last Qualifying Results: {lqr[0]} \n```{lqr[1]}```")

    Console.warning("SYS (last_qualifying_results)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()

@client.command(aliases=["short_news"])
async def news(ctx):
    Console.warning(f"user: {ctx.author}", "Started news")

    sw = Stopwatch()
    news = []
    
    if is_site_up():
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

        Console.log("news", news)
    else:
        Console.error("SYS (news)", "Site is down")
        news = "Error: Unable to reach https://www.autosport.com"

    await send_msg(ctx, "News:")
    await send_embed_msg(ctx, news)

    Console.warning("SYS (news)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()

@client.command(aliases=["f2", "formula2"], pass_context=True)
async def _f2_modele(ctx, *, message):
    try:
        import f2_module
    except ModuleNotFoundError:
        Console.error(f"SYS", f"f2_module was called but its not installed!")
        return

    Console.warning(f"user: {ctx.author}", f"Started f2_modele({message})")
    sw = Stopwatch()

    msg_type, msg = f2_module.resolve(message, USER_CFG)

    if msg_type == "embed":
        await send_msg(ctx, "News:")
        await send_embed_msg(ctx, msg)
    else:
        await send_msg(ctx, msg)

    Console.warning(f"SYS f2_modele({message})", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()

@client.command()
async def uptime(ctx):
    global START_TIME
    Console.warning(f"user: {ctx.author}", "Started bwoah")

    sw = Stopwatch()

    timedelta = datetime.now() - START_TIME

    Console.log("uptime", "Uptime: " + str(round(timedelta.total_seconds())) + "s")
    await send_msg(ctx, "Uptime: " + str(round(timedelta.total_seconds())) + "s")

    Console.warning("SYS (uptime)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()

@client.command()
async def clear_cache(ctx):
    Console.warning(f"user: {ctx.author}", "Started clear_cache")

    sw = Stopwatch()

    CacheManager.clear()
    await send_msg(ctx, "Cache cleared!")
        
    Console.warning("SYS (clear)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()

@client.command(aliases=["clean", "cls"])
async def clear(ctx):
    Console.warning(f"user: {ctx.author}", "Started clear")

    sw = Stopwatch()
    messages = await ctx.message.channel.history().flatten()

    Console.log(f"clear", f"Msg list length {len(messages)}")

    for message in messages:
        if message.author.bot or message.content[:len(USER_CFG.prefix)] == USER_CFG.prefix:
            await message.delete()
        
    Console.warning("SYS (clear)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()

@client.command()
async def help(ctx):
    Console.warning(f"user: {ctx.author}", "Started help")

    sw = Stopwatch()
    await ctx.channel.send(f"Help: ```{tabulate(HELP_LIST, headers=[' ', ' '], stralign='left', tablefmt='plain')}```")

    Console.warning("SYS", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()

@client.command()
async def version(ctx):
    Console.warning(f"user: {ctx.author}", "Started version")

    sw = Stopwatch()
    await send_msg(ctx, f"```yaml\nVersion: {VERSION}\n```")

    Console.warning("SYS (version)", "Total time taken: " + str(round(sw.duration*1000)) + " ms")
    sw.reset()
    return

async def send_embed_msg(ctx, msg):
    if isinstance(msg, list):
        for m in msg:
            await ctx.channel.send(embed=m)
    else:
        await ctx.channel.send(embed=msg)

async def send_msg(ctx, msg):
    await ctx.channel.send(msg)

#region Logs
Console.warning("Boot", f"Version: {VERSION}")
Console.log("Boot", f"Token found: {len(USER_CFG.token) != 0}")
Console.log("Boot", f"Prefix: {USER_CFG.prefix}")
Console.log("Boot", f"Debug: {USER_CFG.debug}")
Console.log("Boot", f"Cache: {USER_CFG.cache}")
Console.log("Boot", f"Cache time delta: {USER_CFG.cache_time_delta} sec")
Console.log("Boot", f"Browser path: {USER_CFG.browser_path}")
Console.log("Boot", f"Time zone: {time.tzname[0]}")
#endregion

client.run(USER_CFG.token)