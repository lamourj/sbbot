from telegram.ext import Updater


with open("Telegram_API_token.txt", 'r') as Telegram_API_file:
        for line in Telegram_API_file:
            if line.startswith("token="):
                TOKEN = line[len("token="):]

updater = Updater(token=TOKEN)

dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


from telegram.ext import CommandHandler
from start import start
from newTravel import newTravel

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

newTravel_handler = CommandHandler('newTravel', newTravel);
dispatcher.add_handler(newTravel_handler);

updater.start_polling()
