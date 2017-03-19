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

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Bot)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
        ConversationHandler)
from handlers import *
from data_structures import *
from interfaces import *
import time
import datetime as dt
import newTravel as NT
# import newFriend as NF
from config import *

import logging
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
logger = logging.getLogger(__name__)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def createMessage(currentTime, connexion):
    msg = "The train from " + connexion.departure + " to " + connexion.arrival + " is leaving from platform " + connexion.departurePlatform + " at " + connexion.departureTime
    return msg


def main():
    # betweenChecks = 1 * 60 * 1000 # 1 minute millis
    sentNotifications = dict()

    betweenChecks = 15 # 20 seconds 
    prevChecked = time.time()
    deleteAfterMinutes = 30
    checkIntervalMillis = Parser().minutesToMillis(2 * 60) # 2 hours
    notificationMillis = 5 * 60 * 1000

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


    bot = Bot(TOKEN)

    while(True):
        currentTime = time.time()
        if(currentTime - prevChecked > betweenChecks):
            prevChecked = currentTime
            # tablesManager.removePastTrains(Parser.millisToMinutes(currentTime), deleteAfterMinutes)
            tidsToCheck = tablesManager.getTidsToCheck(currentTime, checkIntervalMillis)

            # print("todaysTrainTable: " + str(tablesManager.getTodaysTrainTable()))
            # print("todaysTable: " + str(tablesManager.todaysTable.table))
            # print('tidsToCheck: ' + str(tidsToCheck))

            for uid in tablesManager.todaysTable.table:
                for tid, connexion in tablesManager.todaysTable.table[uid]:
                    depart = dt.datetime.strptime(connexion.departureTime, "%m/%d/%y %I:%M %p").timestamp()
                    if tid in tidsToCheck and depart - currentTime < notificationMillis:
                        if (uid, connexion) not in sentNotifications:
                            message = createMessage(currentTime, connexion)
                            bot.sendMessage(uid, message)
                            sentNotifications[(uid, connexion)] = True


    print('exit while')

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
