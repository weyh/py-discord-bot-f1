# Discord F1 Bot

Gives information on upcoming or previous f1 events.

## Set up

- Make sure you have the correct packages and version of python installed

- Download files (debug.py, f1_bot.py, kimi.txt)

- To configure the bot you need to create a file called "usr.cfg" in the same directory where the f1_bot.py file located . Currently the file must contain 2 paramaters: token, timezone.

Timezone eg.: CET, UTC, GMT

```
token:{token}
timezone:{timezone}
```

Note: In the file do not include {}

Your file should look like this:
```
token:a.really.long.string
timezone:CET
```

- You are now done with the setup, you can run the file.

#### Recommendation

To have the robot running day and night, use something like a raspberry pi.

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
