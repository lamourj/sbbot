#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import newTravel as NT
# import newFriend as NF

import logging
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():

    with open("Telegram_API_token.txt", 'r') as Telegram_API_file:
        for line in Telegram_API_file:
            if line.startswith("token="):
                TOKEN = line[len("token="):]

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=NT.ENTRY_POINTS,
        states= NT.STATES,
        fallbacks=NT.FALLBACKS,
        allow_reentry=True
    )
    dp.add_handler(conv_handler)

    # conv_handler_friend = ConversationHandler(
    #     entry_points=NF.ENTRY_POINTS,
    #     states= NF.STATES,
    #     fallbacks=NF.FALLBACKS,
    #     allow_reentry=True
    # )
    # dp.add_handler(conv_handler_friend)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
