﻿
﻿![bot logo](img/logo.png)

# Discord Formula 1 Bot

Gives information on upcoming or previous F1 events. 

## Set up

1. Installation: Download the correct [release](https://github.com/weyh/py-discord-bot-f1/releases/latest) for your computer and unpack it.

2. After downloading the files, you need to create a [new discord application](https://discordapp.com/developers/applications/) and get the bot's token. *([Creating a discord bot & getting a token](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token))*

3. If you have the token, you can start the bot. (On **Windows** simply open the .exe, on **Linux** `./F1Bot_v2` in the cli. [Resolving problems with start.](#resolving-problems-concerning-the-start-of-the-program)). 

4. On the initial start the bot will start the creation process of a new `usr.cfg` file.
The file contains the following parameters: token\*, prefix (default: "--"), debug (True/False, default: False), cache (default: True), cache_time_delta (default: 30 min)
Parameters marked with '\*' are essential.

## Command Line Arguments

With command line arguments you can modify the settings of usr.cfg to that specific instance of the bot.

| Parameter | Argument |
| :--- | :--- |
| Version of the bot | `--version` |
| Help menu | `-h`, `--help` |
| Bot's token| `-t`, `--token` |
| Prefix | `-p`, `--prefix` |
| Debug | `-d`, `--debug` |
| Timestamp | `-T`, `--timestamp` |
| Cache| `-c`, `--cache` |
| Caching time delta \* | `-C`, `--cache_time_delta` |
| Path of your preferred browser| `-b`, `--browser_path` |

\*: The time while the cached data is valid.

E.g: `F1Bot_v2.exe --prefix=-- -d -C 10`
In this case: **prefix:** "--", **debug:** True, **caching time delta:** 10 sec.

## Commands

To access the command list you can always use "--help" in the discord chat.

**Command List:**

| Description | Command |
| :--- | :--- |
| Upcoming race weekend | `--upcoming`, `--coming_up` |
| The race weekend after the upcoming one | `--following_week`, `--fw` |
| Last Race Results: | `--last_race_results`, `--last_race`, `--lrr` |
| Last Qualifying Results | `--last_qualifying_results`, `--last_qualifying`, `--lqr` |
| Current Driver Standings | `--driver_standings`, `--ds` |
| Current Constructors Standings | `--constructors_standings`, `--constructors`, `--cs` |
| Championship Calendar | `--calendar` |
| News | `--news` |
| Clear | `--clear`, `--clean`, `--cls` |
| Uptime | `--uptime` |
| Version | `--version` |
| Help | `--help` |

## Troubleshooting

Note: **On Mac** the entire repo is not working, for me at least.

### Resolving problems concerning the start of the program

Check if you downloaded the right executable.

- **Linux:** The files are built on **[Ubuntu 64bit and Raspberry Pi OS (Raspbian) ARM](img/linux.png)**. *(From my brief testing with older versions of Ubuntu (16.04 x86/16.10 x64), the problem is the GLIBC version.)* You can also try to clone the repo and build it yourself or just run the `f1_bot_v2.py` file. 
- **Windows:** Both files are built in a Win 10  environment. In case of an older version of windows, it is possible that some dlls are missing. Probably: [Microsoft Visual C++ 2010 Redistributable Package (x64)](https://www.microsoft.com/en-us/download/details.aspx?id=14632), [Microsoft Visual C++ 2010 Redistributable Package (x86)](https://www.microsoft.com/en-us/download/details.aspx?id=5555). You can also try to clone the repo and build it yourself or just run the `f1_bot_v2.py` file. 

#### Clone and build (Additional package required: `pyinstaller`):
```bash
git clone https://github.com/weyh/py-discord-bot-f1.git
cd py-discord-bot-f1
pip3 install -r reqs.txt
pip3 install pyinstaller
cd ./f1-bot-v2/Build
python3 build.py
```
If everything went fine, you will find it in `./bin/{your os}_{your architecture}/`.

#### Clone and run:
```bash
git clone https://github.com/weyh/py-discord-bot-f1.git
cd py-discord-bot-f1
pip3 install -r reqs.txt
cd ./f1-bot-v2
python3 f1_bot_v2.py
```

---

### Sources:

- [Ergast Developer API](http://ergast.com/mrd/)
- [autosport.com](https://www.autosport.com/f1)

---

### Built With

- [Python (3.7.x)](https://www.python.org)
- [pyinstaller](https://www.pyinstaller.org)

#### Packages used: [reqs.txt](reqs.txt)

---

### License
This project is licensed under the MIT License - see the [MIT License](LICENSE) file for details.