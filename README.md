![wide logo](static/logo.png)

# Discord Formula 1 Bot

A simple discord bot that can fetch some useful information.

## Set up

1. Installation: Download the correct [release](https://github.com/weyh/py-discord-bot-f1/releases/latest) for your computer and unpack it.

2. After downloading the files, you need to create a [new discord application](https://discordapp.com/developers/applications/) and get the bot's token. *([Creating a discord bot & getting a token](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token))*

3. If you have the token, you can start the bot. (On **Windows** simply open the .exe, on **Linux** `./F1Bot` in the CLI. [Resolving problems with start.](#startup-problems)).

4. A `usr.cfg` file will be created during the initial start. (Parameters marked with '\*' are essential.)

## Command Line Arguments

Command line arguments will override the saved settings to that specific instance of the bot.

| Parameter          | Argument            |
| :----------------- | :------------------ |
| Version of the bot | `--version`         |
| Help menu          | `-h`, `--help`      |
| Bot's token        | `-t`, `--token`     |
| Prefix             | `-p`, `--prefix`    |
| Debug              | `-d`, `--debug`     |
| Timestamp          | `-T`, `--timestamp` |

E.g: `python f1_bot.py --prefix=-- -d`. In this case: **prefix:** "--", **debug:** True.

## Commands

To access the command list you can always use "--help" in the discord chat. (In this case **prefix** is set to `--`.)

**Command List:**

| Description                    | Command                              |
| :----------------------------- | :----------------------------------- |
| Current race weekend           | `--current`                          |
| The race weekend after current | `--fw`, `--following_week`           |
| Current driver standings       | `--ds`, `--driver_standings`         |
| Current constructors standings | `--cs`, `--constructors_standings`   |
| Championship Calendar          | `--calendar`                         |
| Last race results:             | `--lrr`, `--last_race_results`       |
| Last qualifying results        | `--lqr`, `--last_qualifying_results` |
| Clear bot messages             | `--clear`                            |
| Uptime                         | `--uptime`                           |
| Version                        | `--version`                          |
| Help                           | `--help`                             |

## Troubleshooting

### Startup problems

Check if you downloaded the right executable.

- **Linux:** The files are built on **[Ubuntu 64bit and Raspberry Pi OS (Raspbian) ARM](static/linux.png)**. *(From my brief testing with older versions of Ubuntu (16.04 x86/16.10 x64), the problem is the GLIBC version.)* You can also try to clone the repo and build it yourself or just run the `f1_bot.py` file.
- **Windows:** Files are built in a Win 10  environment. In case of an older version of windows, it is possible that some dlls are missing. Probably: [Microsoft Visual C++ 2010 Redistributable Package (x64)](https://www.microsoft.com/en-us/download/details.aspx?id=14632), [Microsoft Visual C++ 2010 Redistributable Package (x86)](https://www.microsoft.com/en-us/download/details.aspx?id=5555). You can also try to clone the repo and build it yourself or just run the `f1_bot.py` file.

#### Clone and build (Additional package required: `pyinstaller`):

```bash
git clone https://github.com/weyh/py-discord-bot-f1.git
cd py-discord-bot-f1
pip3 install -r requirements.txt
pip3 install pyinstaller
cd ./src/Build
python3 build.py
```

If everything went fine, you will find it in `./bin/{your os}_{your architecture}/`.

#### Clone and run:

```bash
git clone https://github.com/weyh/py-discord-bot-f1.git
cd py-discord-bot-f1
pip3 install -r requirements.txt
cd ./src
python3 f1_bot.py
```

---

### Source:

- [Ergast Developer API](http://ergast.com/mrd/)
- [Fast F1](https://theoehrly.github.io/Fast-F1/)

---

### Requirements:

- [Python (3.8.x)](https://www.python.org)
- [requirements.txt](requirements.txt)

---

### License
This project is licensed under the MIT License - see the [MIT License](LICENSE) file for details.
