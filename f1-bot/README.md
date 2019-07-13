# No Longer Supported!

![bot logo](logo.png)

# Discord Formula 1, Formula 2 Bot

Gives information on upcoming or previous F1, F2 events. 

## Set up

1. Installation:
	- Make sure Python 3.6.6 or later is installed.
	- Run the following commands:
```bash
git clone https://github.com/weyh/py-discord-bot-f1.git
cd py-discord-bot-f1/f1-bot/
pip install -r reqs.txt
```

*F2 module is optional, so you can delete "f2_module.py" if you are not planning to use it.*


2. [How to get a token](https://youtu.be/nW8c7vT6Hl4?t=289)

4. To configure the bot you need to create a file called "usr.cfg" in the same directory where the f1_bot.py is located. 

	- Must contain (except if you plan to use cli args): token

	- Optional: prefix (default: "--"), timezone (CET, UTC, GMT etc), debug (True/False), default: True)

Your file should look like this:

```
token=a.really.long.string
timezone=CET
prefix=--
debug=False
```

---

If you want to use **f2_module** then you must define the browser's path in user.cfg. *Supported: Google Chrome, Mozilla Firefox. (Make sure your browser is up-to-date.)*
Eg.: `browser_path=C:\Program Files\Mozilla Firefox\firefox.exe`
You also need to download a [third party browser driver](https://www.seleniumhq.org/download/) which matches the browser that is defined in browser_path. *([Geckodriver (v0.17.0 ARM7) for Raspberry Pi 3](https://www.github.com/mozilla/geckodriver/releases/download/v0.17.0/geckodriver-v0.17.0-arm7hf.tar.gz))*

- On **Windows**, browser driver should be located in the root directory!
- On **Linux**, browser driver should be copied to `/usr/local/bin`!
Run: `sudo cp geckodriver /usr/local/bin`

*Unfortunately "marionette" does not seem to work on Raspbian, so each time a function (which uses selenium) runs a new instance of the browser will be launched.*

---

5. You are now done with the setup, you can run f1_bot.py. *(I recommend running it on a single board computer.)*

## Command Line Arguments

With command line arguments you can modify the settings of usr.cfg to that specific instance of the bot.

| Parameter | Argument |
| :--- | :--- |
| Version | `--version` |
| Help | `-h`, `--help` |
| Token | `--token` |
| Timezone | `--timezone` |
| Prefix | `--prefix` |
| Debug | `--debug` |

Eg.: `python f1_bot.py --prefix=-- --debug=False`

## Commands

To access the command list you can always use "--help" in the discord chat.

Command List:

| Description | Command |
| :--- | :--- |
| Upcoming race weekend | `--upcoming`, `--coming_up` |
| The race weekend after the upcoming one | `--next_week` |
| Top 10 from last race | `--last_top10` |
| Current Driver Standings | `--driver_standings`, `--ds` |
| Current Constructors Standings | `--constructors_standings`, `--constructors`, `--cs` |
| Championship Calendar | `--calendar` |
| News | `--news`, `--short_news` |
| Long News (6 articles) | `--long_news` |
| Clear | `--clear`, `--clean`, `--cls` |
| Uptime | `--uptime` |
| Version | `--version` |
| Help | `--help` |

F2 Module Command List:

| Description | Command |
| :--- | :--- |
| Upcoming race weekend | `--f2 upcoming`, `--f2 coming_up` |
| The race weekend after the upcoming one | `--f2 next_week` |
| Top 10 from last race | `--f2 last_top10` |
| Current Driver Standings | `--f2 driver_standings`, `--f2 ds` |
| Championship Calendar | `--f2 calendar` |
| News | `--f2 news`, `--f2 short_news` |
| Long News (6 articles) | `--f2 long_news` |
| Help | `--f2 help` |

---

### Built With

- [Python (3.7.2)](https://www.python.org)

#### Packages

* [discord.py](https://github.com/Rapptz/discord.py)
* [bs4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [selenium](https://www.seleniumhq.org)
* [pytz](https://pypi.org/project/pytz/)
* [python-tabulate](https://github.com/gregbanks/python-tabulate)
* [stopwatch.py](https://pypi.org/project/stopwatch.py/)
* [colorama](https://github.com/tartley/colorama)

---

### Author

[Bak Gergely János](https://github.com/weyh)

### License
This project is licensed under the MIT License - see the [MIT License](LICENSE) file for details.