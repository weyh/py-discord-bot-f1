# -*- coding: utf-8 -*-
import os, requests, time, discord
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
from tabulate import tabulate

from debug import Debug

HELP_LIST = [["The race weekend after the upcoming one:", "|prefix|f2 next_week"],
                ["Top 10 from last race:", "|prefix|f2 last_top10"],
                ["Current Driver Standings:", "|prefix|f2 driver_standings \n|prefix|f2 ds"],
                ["Championship Calendar:", "|prefix|f2 calendar"],
                ["News:", "|prefix|f2 news\n|prefix|f2 short_news"],
                ["Long News (6 articles):", "|prefix|f2 long_news"],
                ["Help:", "|prefix|f2 help"]]

def resolve(msg, prefix):
    if msg == "next_week":
        return "str", next_week()
    elif msg == "last_top10":
        return "str", last_top10()
    elif msg == "driver_standings" or msg == "ds":
        return "str", driver_standings()
    elif msg == "calendar":
        return "str", calendar()
    elif msg == "long_news":
        return "embed", long_news()
    elif msg == "short_news" or msg == "news":
        return "embed", news()
    elif msg == "help":
        return "str", help(prefix)

    return "str", "Error!"

def calendar():
    race_info = ""

    if isSiteUp():
        page = requests.get('https://www.autosport.com/f2/calendar')
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

    return str("Calendar: ```"+race_info+"```")

def news():
    news = []

    if isSiteUp():
        page = requests.get('https://www.autosport.com/f2')
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

    return news

def long_news():
    news = []

    if isSiteUp():
        page = requests.get('https://www.autosport.com/f2')
        soup = BeautifulSoup(page.content, 'html.parser')
        news_soup = list(soup.find('div', class_='columnsContainer').find('div', 'leftColumn').find("div", class_="row small-up-2 medium-up-3").select("div div .newsitem"))

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

    return news

def driver_standings():
    r_text = ""

    if isSiteUp():
        page = requests.get('https://www.autosport.com/f2/standings')
        soup = BeautifulSoup(page.content, 'html.parser')

        _driver_standings = soup.find('div', class_='columnsContainer').find('div', 'leftColumn').select("table:nth-child(1) tbody tr")[1:]

        table = []
        for tr in _driver_standings:
            pos = tr.select("td:nth-child(1)")[0].get_text()
            if pos == "Pos": # somehow there is a "Pos" in the soup
                break
            driver = tr.select("td:nth-child(2) a")[0].get_text()
            points = tr.select("td:nth-child(3)")[0].get_text()

            table.append([f"{pos}", f"{driver}", f"{points}"])

        r_text += tabulate(table, headers=["Pos", "Driver", "Points"], tablefmt='orgtbl', numalign="right", stralign="center")
        Debug.Log("driver_standings", r_text)
    else:
        Debug.Error("SYS (driver_standings)", "Site is down")
        r_text = "Error: Unable to reach https://www.autosport.com"

    return "Driver Standings: ```"+r_text+"```"

def last_top10():
    r_text = ""

    if isSiteUp():
        page = requests.get('https://www.autosport.com/f2')
        soup = BeautifulSoup(page.content, 'html.parser')

        drivers = [d.get_text() for d in soup.find_all('div', class_='stats')[0].select("table tbody tr td:nth-child(2) a")]
        teams = [t.get_text() for t in soup.find_all('div', class_='stats')[0].select("table tbody tr td:nth-child(3)")]

        table = []
        for i, (driver, team) in enumerate(zip(drivers, teams), start=1):
            table.append([f"{i}", f"{driver}", f"{team}"])

        r_text += tabulate(table, headers=["Pos", "Driver", "Points"], tablefmt='orgtbl', numalign="right", stralign="center")
        Debug.Log("last_top10", r_text)
    else:
        Debug.Error("SYS (last_top10)", "Site is down")
        r_text = "Error: Unable to reach https://www.autosport.com"

    return "Last week's top 10: ```" + r_text + "```"

def next_week():
    race_info = ""

    if isSiteUp():
        page = requests.get('https://www.autosport.com/f2/calendar')
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

    return race_info

def help(prefix):
    for e in HELP_LIST:
        e[1] = e[1].replace("|prefix|", prefix)
    return "Help: ```" + tabulate(HELP_LIST, headers=[" ", " "], stralign="left", tablefmt='plain') + "```"

isSiteUp = lambda: requests.head('https://www.autosport.com/f2').status_code == 200