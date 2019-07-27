![bot logo](img/logo.png)

# Discord Formula 1, Formula 2 Bot

Gives information on upcoming or previous F1, F2 events. 

## Set up

1. Installation:
	- Download the correct [release](https://github.com/weyh/py-discord-bot-f1/releases/latest) for your computer and unpack it.
	- Get a [third party Selenium browser driver](https://www.seleniumhq.org/download/) that matches your browser. *([Geckodriver (v0.17.0 ARM7) for Raspberry Pi 3](https://www.github.com/mozilla/geckodriver/releases/download/v0.17.0/geckodriver-v0.17.0-arm7hf.tar.gz)) Tested browsers: Google Chrome, Mozilla Firefox.*
		 - On **Windows**, browser driver should be located in the root directory (next to the exe)!
		 - On **Linux**, browser driver should be copied to `/usr/local/bin`!
Run: `sudo cp geckodriver /usr/local/bin`

*Unfortunately "marionette" does not seem to work on the ARM Geckodriver builds, so each time a function (which uses selenium) runs a new instance of the browser will be launched.*

2. After downloading the files, you need to create a [new discord application](https://discordapp.com/developers/applications/) and get the bot's token. *([Creating a discord bot & getting a token](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token))*

3. If you have the token, you can start the bot. (On **Windows** simply open the exe, on **Linux** `./F1Bot_v2` in the cli. [What to do if it's not starting?](#what-to-do-if-its-not-starting)). 

4. On the initial start the bot will start the creation process of a new `usr.cfg` file.
The file may or may not contain the following parameters: token\*, prefix (default: "--"), debug (True/False, default: True), browser_path\*\*
	- '\*': essential
	- '\*\*': essential if the f2 module will be used.


## Command Line Arguments

With command line arguments you can modify the settings of usr.cfg to that specific instance of the bot.

| Parameter | Argument |
| :--- | :--- |
| Version of the bot | `--version` |
| Help menu | `-h`, `--help` |
| Bot's token| `--token` |
| Path of your preferred browser| `--browser_path` |
| Prefix | `--prefix` |
| Debug | `--debug` |

Eg.: `F1Bot_v2.exe --prefix=-- --debug=False`

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

**F2 Module Command List:**

| Description | Command |
| :--- | :--- |
| Upcoming race weekend | `--f2 upcoming`, `--f2 coming_up` |
| The race weekend after the upcoming one | `--f2 following_week`, `--f2 fw` |
| Top 10 from last race | `--f2 last_top10` |
| Current Driver Standings | `--f2 driver_standings`, `--f2 ds` |
| Championship Calendar | `--f2 calendar` |
| News | `--f2 news` |
| Help | `--f2 help` |

*Note: You should replace `--` with your prefix.*

## Troubleshooting

Note: **On Mac** the entire repo is not working, for me at least.

### What to do if it's not starting?

Check if you downloaded the right executable.

- **Linux:** The files are built on **[Ubuntu (64bit), Mint (32bit) and Raspbian (ARM)](img/linux.png)**. Because of all the different distros I cannot test on all of them. If it's not working on yours, you can clone the repo and either build it yourself, or just run the .py file. *(From my brief testing with older versions of Ubuntu (16.04 x86/16.10 x64), the problem is the GLIBC version.)*
- **Windows:** Both files are built in a Win 10  environment. If your are using an older version, there might be some DLLs missing. They are probably [Microsoft Visual C++ 2010 Redistributable Package (x64)](https://www.microsoft.com/en-us/download/details.aspx?id=14632), [Microsoft Visual C++ 2010 Redistributable Package (x86)](https://www.microsoft.com/en-us/download/details.aspx?id=5555). If this doesn't fix it, you can clone the repo and try to build it yourself or just run the .py file.

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
