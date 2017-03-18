from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler)

from sbbCffBot import logger

import re, arrow

import sbbbackend.handlers.query_handler as qh
import sbbbackend.interfaces.parser as parser

PICK_DAY, FROM_PROPOSTION, FROM_CONFIRMACTION, TO_PROPOSTION, TO_CONFIRMACTION, TO, VIA, ARRIVE_DEPART, TIME = range(9)

def connectionType(bot, update):
    user = update.message.from_user
    logger.info("User %s started a new connection." % (user.first_name))

    reply_keyboard = [['/unique', '/weekly']]
    update.message.reply_text(
        'Hi, do you want to add a unique connection or a weekly one?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

def pickDay(bot, update):
    reply_keyboard = [['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 
            'Sarturday', 'Sunday']]

    update.message.reply_text(
        'On which day of the week ?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return FROM_PROPOSTION


def fromProposition(bot, update):
    user = update.message.from_user
    logger.info("New connection day of %s: %s" % (user.first_name, update.message.text))

    update.message.reply_text("Where will you be leaving from?")

    return FROM_CONFIRMACTION

def fromConfirm(bot, update):
    logger.info("Trying to leave from %s" % update.message.text)
    listFrom = qh.QueryHandler().getStationsFromName(update.message.text)
    listFrom = parser.Parser().parseStations(listFrom)
    reply_keyboard = [[el] for el in listFrom]
    print("We received these proposition")
    print(listFrom)
    update.message.reply_text("Please choose one of the following:", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return TO_PROPOSTION


def toProposition(bot, update):
    print("Hleloo")
    user = update.message.from_user
    logger.info("New connection day of %s: %s" % (user.first_name, update.message.text))

    update.message.reply_text("Where will you be going to?")

    return TO_CONFIRMACTION

def toConfirm(bot, update):
    logger.info("Trying to go to %s" % update.message.text)
    listTo = qh.QueryHandler().getStationsFromName(update.message.text)
    listTo = parser.Parser().parseStations(listTo)
    reply_keyboard = [[el] for el in listTo]
    print("We received these proposition")
    print(listTo)
    update.message.reply_text("Please choose one of the following:", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return ARRIVE_DEPART  

def whenStartArrive(bot, update):
    logger.info("Going to %s" % update.message.text)
    reply_keyboard = [["Depart by ..h.."], ["Arrive by ..h.."]]
    update.message.reply_text("Do you want to arrive or depart by a certain time?", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return TIME
      

def whenTime(bot, update):
    logger.info("Wanting to \"%s\" " % update.message.text)

    update.message.reply_text("Please type the time you want to %s. Possible input ..h.., now, in .. hours " % update.message.text[:-8])
    return ConversationHandler.END    

def getConnexion(bot, update):
    logger.info("Wanting to  leave at %s " % update.message.text)
    if re.match('^now$'):
        present = arrow.now()
        time = present.hour + ":" + prensent.minute
    elif re.match('^in \d{1,2} hours$'):
        print()
    elif re.match('^\d{0,2}h\d{0,2}$'):
        print()
    else:
        logger.warn("problem with time regex")



def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

ENTRY_POINTS = [CommandHandler('newConnection', connectionType),
        CommandHandler('unique', fromProposition),
        CommandHandler('weekly', pickDay)]

STATES={
    PICK_DAY: [RegexHandler('^(Unique|Weekly)$', pickDay)],

    FROM_PROPOSTION: [RegexHandler('^(Confirmed|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)$', fromProposition)], 

    FROM_CONFIRMACTION: [MessageHandler(Filters.text, fromConfirm)],

    TO_PROPOSTION: [MessageHandler(Filters.text, toProposition)],

    TO_CONFIRMACTION: [MessageHandler(Filters.text, toConfirm)],
    
    VIA: [],

    ARRIVE_DEPART: [MessageHandler(Filters.text, whenStartArrive)],

    TIME: [RegexHandler('^(now|in \d{1,2} hours|\d{0,2}h\d{0,2})$', getConnexion)]
}

FALLBACKS=[CommandHandler('cancel', cancel)]
