from telegram.ext import Updater


with open("Telegram_API_token.txt", 'r') as Telegram_API_file:
        for line in Telegram_API_file:
            if line.startswith("token="):
                TOKEN = line[len("token="):]

updater = Updater(token=TOKEN)

dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update): bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")



from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()




def echo(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text)

from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)