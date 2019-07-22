# -*- coding: utf-8 -*-
import sys, os, requests, platform, time, discord
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChomreOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
from tabulate import tabulate

from Core.debug import Debug

__addPath = True

HELP_LIST = [["Upcoming race weekend:", "|prefix|f2 upcoming\n|prefix|f2 coming_up"],
                ["The race weekend after the upcoming one:", "|prefix|f2 following_week \n|prefix|f2 fw"],
                ["Top 10 from last race:", "|prefix|f2 last_top10"],
                ["Current Driver Standings:", "|prefix|f2 driver_standings \n|prefix|f2 ds"],
                ["Championship Calendar:", "|prefix|f2 calendar"],
                ["News:", "|prefix|f2 news"],
                ["Help:", "|prefix|f2 help"]]

def resolve(msg, USER_CFG):
    if msg == "upcoming" or msg == "coming_up":
        return "str", upcoming(USER_CFG)
    elif msg == "following_week" or msg == "fw":
        return "str", following_week()
    elif msg == "last_top10":
        return "str", last_top10()
    elif msg == "driver_standings" or msg == "ds":
        return "str", driver_standings()
    elif msg == "calendar":
        return "str", calendar()
    elif msg == "news":
        return "embed", news()
    elif msg == "help":
        return "str", help(USER_CFG.get('prefix'))

    Debug.Error("f2_modele(resolve)", f"Incorrect command \"{msg}\"")
    return "str", f"Incorrect command \"{msg}\""

def upcoming(USER_CFG):
    if(USER_CFG.get('browser_path') == "undefined"):
        Debug.Error("SYS (upcoming)", "Browser is not defined!")
        Debug.Pause()

    race_info = "COMING UP:\n"

    if isSiteUp("http://www.fiaformula2.com"):
        global __addPath

        binary = r"%s"%USER_CFG.get('browser_path')

        if "firefox" in binary.lower():
            options = FirefoxOptions()
            options.set_headless(headless=True)
            options.binary = binary
            cap = DesiredCapabilities().FIREFOX
            cap["marionette"] = True

            if __addPath and platform.system() == "Windows":
                sys.path.append(os.path.join(os.getcwd(), "geckodriver.exe"))
                __addPath = False

            driver = webdriver.Firefox(firefox_options=options, capabilities=cap)
        elif "chrome" in binary.lower():
            options = ChomreOptions()
            options.set_headless(headless=True)
            options.binary_location = binary
            options.add_argument('--hide-scrollbars')
            options.add_argument('--disable-gpu')
            options.add_argument("--log-level=3")  

            if platform.system() == "Windows":
                driver = webdriver.Chrome(r"%s"%"chromedriver.exe", options=options)
            else:
                driver = webdriver.Chrome(options=options)
        else:
            Debug.Error("SYS (upcoming)", "Not supported browser!")
            Debug.Pause()
       

        driver.get("http://www.fiaformula2.com")

        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "countdown")))

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            _upcoming = soup.find("div", class_="module")

            location = _upcoming.find('div', id="raceName").select("h4")[0].get_text().split(', ')[1]
            circuit = _upcoming.find('div', id="raceName").select("h4")[0].get_text().split(', ')[0]
            
            d = _upcoming.find('div', id='countdownClock').find('span', id='day').get_text()
            h = _upcoming.find('div', id='countdownClock').find('span', id='hour').get_text()
            s = _upcoming.find('div', id='countdownClock').find('span', id='min').get_text()
            m = _upcoming.find('div', id='countdownClock').find('span', id='sec').get_text()
            race_starts_in = f"{d} {__days_or_day_help(d)}, {h}:{s}:{m}"

            free_practices = _upcoming.find('div', id='session-0').find('span', class_="gmttime").get_text()
            qualifying = _upcoming.find('div', id='session-1').find('span', class_="gmttime").get_text()
            race_1 = _upcoming.find('div', id='session-2').find('span', class_="gmttime").get_text()
            race_2 = _upcoming.find('div', id='session-3').find('span', class_="gmttime").get_text()

            date = race_1[3:10]

            race_info += str(f"{location} / {date}\n" + 
                        f"Race starts in: {race_starts_in}\n" +
                        f"Circuit: {circuit}\n\n" +
                        "SCHEDULE:\n" +
                        f"Practice: {free_practices}\n" +
                        f"Qualifying: {qualifying}\n" +
                        f"Race 1: {free_practices}\n" +
                        f"Race 2: {free_practices}"
                        )
        
            Debug.Log("upcoming", race_info)
        except TimeoutException:
              Debug.Error("SYS (upcoming)", "Loading took too much time!")
        finally:
            driver.quit()
    else:
        Debug.Error("SYS (upcoming)", "Site is down")
        race_info = "Error: Unable to reach http://www.fiaformula2.com"

    return race_info

def following_week():
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

        Debug.Log("following_week", race_info)
    else:
        Debug.Error("SYS (following_week)", "Site is down")
        race_info = "Error: Unable to reach https://www.autosport.com"

    return race_info

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

def help(prefix):
    for e in HELP_LIST:
        e[1] = e[1].replace("|prefix|", prefix)
    return "Help: ```" + tabulate(HELP_LIST, headers=[" ", " "], stralign="left", tablefmt='plain') + "```"

def isSiteUp(url = "https://www.autosport.com/f2"):
    return requests.head(url).status_code == 200

def __days_or_day_help(s):
    if int(s) > 1:
        return "days"
    return "day"
