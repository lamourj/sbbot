# SBBot

This is a [Telegram](https://telegram.org) bot that provide public transport information in Switzerland. It fetch data from [Viadi](https://www.ubique.ch/projects/viadi/) that also power the SBB/CFF/FFS app.
It was built during StartHack 2017, a hackathon taking place at the University of St Gallen, by a team of 4 students of EPFL and ETHZ.

## Install

You can just click on this [link](https://telegram.me/SbbCffBot) and either directly talk to the bot or first install Telegram. 

## Running your own bot instance
If you'd like to run you own instance of the bot, you'll need to register for an Telegram Bot API key by talking with the [BotFather](https://telegram.me/BotFather). This key have to be place in the 
[Telegram_API_token.txt](../Telegram_API_token.txt) file.
You'll also need to install [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot). Instructions can be found by following the previous link.
```
$ pip install python-telegram-bot
```

Additionally, you will have to install [request](http://docs.python-requests.org/en/master/user/install/). 
```
$ pip install requests 
```

To launch the bot server, ````cd into sbbot````and run 
```
python3 sbbCffBot.py
```
Your bot should then be available under the username you registred by the GodFather.
