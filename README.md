
﻿![bot logo](static/logo.png)

# Discord Formula 1 Bot

Gives information on upcoming or previous F1 events.

## Set up

1. Installation: Download the correct [release](https://github.com/weyh/py-discord-bot-f1/releases/latest) for your computer and unpack it.

2. After downloading the files, you need to create a [new discord application](https://discordapp.com/developers/applications/) and get the bot's token. *([Creating a discord bot & getting a token](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token))*

3. If you have the token, you can start the bot. (On **Windows** simply open the .exe, on **Linux** `./F1Bot_v2` in the CLI. [Resolving problems with start.](#startup-problems)).

4. A `usr.cfg` file will be created during the initial start. The file contains the following parameters: token\*, prefix (default: "--"), debug (True/False, default: False), cache (default: True), cache_time_delta (default: 30 min).
Parameters marked with '\*' are essential.

## Command Line Arguments

With command line arguments you can modify the settings of usr.cfg to that specific instance of the bot.

| Parameter             | Argument                   |
| :-------------------- | :------------------------- |
| Version of the bot    | `--version`                |
| Help menu             | `-h`, `--help`             |
| Bot's token           | `-t`, `--token`            |
| Prefix                | `-p`, `--prefix`           |
| Debug                 | `-d`, `--debug`            |
| Timestamp             | `-T`, `--timestamp`        |
| Cache                 | `-c`, `--cache`            |
| Caching time delta \* | `-C`, `--cache_time_delta` |

\*: The time while the cached data is valid.

E.g: `f1_bot.py --prefix=-- -d -C 10`
In this case: **prefix:** "--", **debug:** True, **caching time delta:** 10 sec.

## Commands

To access the command list you can always use "--help" in the discord chat.

**Command List:**

| Description                             | Command                                                   |
| :-------------------------------------- | :-------------------------------------------------------- |
| Upcoming race weekend                   | `--upcoming`, `--coming_up`                               |
| The race weekend after the upcoming one | `--following_week`, `--fw`                                |
| Last Race Results:                      | `--last_race_results`, `--last_race`, `--lrr`             |
| Last Qualifying Results                 | `--last_qualifying_results`, `--last_qualifying`, `--lqr` |
| Current Driver Standings                | `--driver_standings`, `--ds`                              |
| Current Constructors Standings          | `--constructors_standings`, `--constructors`, `--cs`      |
| Championship Calendar                   | `--calendar`                                              |
| Clear                                   | `--clear`                                                 |
| Uptime                                  | `--uptime`                                                |
| Version                                 | `--version`                                               |
| Help                                    | `--help`                                                  |

## Troubleshooting

### Startup problems

Check if you downloaded the right executable.

- **Linux:** The files are built on **[Ubuntu 64bit and Raspberry Pi OS (Raspbian) ARM](static/linux.png)**. *(From my brief testing with older versions of Ubuntu (16.04 x86/16.10 x64), the problem is the GLIBC version.)* You can also try to clone the repo and build it yourself or just run the `f1_bot.py` file.
- **Windows:** Files are built in a Win 10  environment. In case of an older version of windows, it is possible that some dlls are missing. Probably: [Microsoft Visual C++ 2010 Redistributable Package (x64)](https://www.microsoft.com/en-us/download/details.aspx?id=14632), [Microsoft Visual C++ 2010 Redistributable Package (x86)](https://www.microsoft.com/en-us/download/details.aspx?id=5555). You can also try to clone the repo and build it yourself or just run the `f1_bot.py` file.

#### Clone and build (Additional package required: `pyinstaller`):
```bash
git clone https://github.com/weyh/py-discord-bot-f1.git
cd py-discord-bot-f1
pip3 install -r reqs.txt
pip3 install pyinstaller
cd ./f1-bot/Build
python3 build.py
```
If everything went fine, you will find it in `./bin/{your os}_{your architecture}/`.

#### Clone and run:
```bash
git clone https://github.com/weyh/py-discord-bot-f1.git
cd py-discord-bot-f1
pip3 install -r reqs.txt
cd ./f1-bot
python3 f1_bot.py
```

---

### Source:

- [Ergast Developer API](http://ergast.com/mrd/)

---

### Built With

- [Python (3.9.x)](https://www.python.org)
- [pyinstaller](https://www.pyinstaller.org)

#### Packages used: [reqs.txt](reqs.txt)

---

### License
This project is licensed under the MIT License - see the [MIT License](LICENSE) file for details.
