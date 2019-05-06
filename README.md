# Discord Formula 1 Bot

Gives information on upcoming or previous F1 events. 
Data is pulled from [autosport.com](https://www.autosport.com/f1) (thx :wink:).

## Set up

- Make sure you have the correct packages and version of python installed

- Download files (f1_bot.py, debug.py, cfg_dictionary.py, splash_screen.py, kimi.txt)

- Getting a token: [link](https://youtu.be/nW8c7vT6Hl4?t=289)

- To configure the bot you need to create a file called "usr.cfg" in the same directory where the f1_bot.py is located. 

	- Must contain (except if you plan to use cli args): token

	- Optional: prefix (default: "--"), timezone (CET, UTC, GMT etc), debug (True/False), default: True)

```
token:{token}
timezone:{timezone}
prefix:{prefix}
.
.
```

Your file should look like this:
```
token:a.really.long.string
timezone:CET
prefix:--
debug:False
```

- You are now done with the setup, you can run f1_bot.py.

#### Recommendation

I recommend running it on something that is always online like a raspberry pi.

## Command Line Arguments

With command line arguments you can modify the settings of usr.cfg to that specific instance.

| Parameter | Command |
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
| Current Constructors Standings | `--upcoming`, `--coming_up` |
| Current Constructors Standings | `--constructors_standings`, `--constructors`, `--cs` |
| Championship Calendar | `--calendar` |
| News | `--news`, `--short_news` |
| Long News (6 articles) | `--long_news` |
| Random Kimi | `--bwoah`, `--mwoah` |
| Version | `--version` |
| Uptime | `--uptime` |
| Help | `--help` |

## Built With

- [Python (3.7.2)](https://www.python.org) (but should work with 3.5.3+)

#### Packages

* [discord.py](https://github.com/Rapptz/discord.py)
* [bs4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [pytz](https://pypi.org/project/pytz/)
* [python-tabulate](https://github.com/gregbanks/python-tabulate)
* [stopwatch.py](https://pypi.org/project/stopwatch.py/)


## Author

[Bak Gergely János](https://github.com/weyh)

## License
This project is licensed under the MIT License - see the [MIT License](LICENSE) file for details.
