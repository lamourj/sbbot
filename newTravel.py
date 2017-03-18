from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler)

from sbbCffBot import logger

import re, datetime

import sbbbackend.handlers.query_handler as qh
import sbbbackend.interfaces.parser as parser

PICK_DAY, FROM_PROPOSTION, FROM_CONFIRMATION, TO_PROPOSTION, TO_CONFIRMATION, VIA_PROPOSTION, VIA_CONFIRMATION, ARRIVE_DEPART, TIME, GET_CONNECTION = range(10) 

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

    return FROM_CONFIRMATION

def fromConfirm(bot, update):
    logger.info("Trying to leave from %s" % update.message.text)
    listFrom = qh.QueryHandler().getStationsFromName(update.message.text)
    listFrom = parser.Parser().parseStations(listFrom)
    reply_keyboard = [[el] for el in listFrom]
    update.message.reply_text("Please choose one of the following:", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return TO_PROPOSTION

def toProposition(bot, update):
    user = update.message.from_user
    logger.info("From of %s: %s" % (user.first_name, update.message.text))

    update.message.reply_text("Where will you be going to?")

    return TO_CONFIRMATION

def toConfirm(bot, update):
    logger.info("Trying to go to %s" % update.message.text)
    listTo = qh.QueryHandler().getStationsFromName(update.message.text)
    listTo = parser.Parser().parseStations(listTo)
    reply_keyboard = [[el] for el in listTo]
    update.message.reply_text("Please choose one of the following:", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return VIA_PROPOSTION     

      
def viaProposition(bot, update):
    user = update.message.from_user
    logger.info("To of %s: %s" % (user.first_name, update.message.text))

    update.message.reply_text("Use /skip if you do not need to stop in between" +
            " (via), otherwise please enter where you'd wish to stop")

    return VIA_CONFIRMATION  

def viaConfirm(bot, update):
    logger.info("Trying to go via %s" % update.message.text)
    listTo = qh.QueryHandler().getStationsFromName(update.message.text)
    listTo = parser.Parser().parseStations(listTo)
    reply_keyboard = [[el] for el in listTo]
    update.message.reply_text("Please choose one of the following:", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return ARRIVE_DEPART


def skipViaConfirm(bot, update):
    reply_keyboard = [['Yes', 'No']]

    update.message.reply_text(
        'Are you sure ?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return ARRIVE_DEPART 

def whenStartArrive(bot, update):
    logger.info("Going via  %s" % update.message.text)
    reply_keyboard = [["Depart by ..h.."], ["Arrive by ..h.."]]
    update.message.reply_text("Do you want to arrive or depart by a certain time?", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return TIME

def whenTime(bot, update):
    logger.info("Wanting to \"%s\" " % update.message.text)

    update.message.reply_text("Please type the time you want to %s. Possible input ..:.., now" % update.message.text[:-8])
    return GET_CONNECTION


def getConnection(bot, update):
    logger.info("Wanting to  leave at %s " % update.message.text)
    present = datetime.datetime.now()
 
    # if re.match('^now$', update.message.text):
    if re.match('^\d:\d{0,2}$', update.message.text):
        h = int(update.message.text[0:1])
        m = int(update.message.text[2:])
        if h > present.hour or (h == present.hour and m >= present.minute):
            present = present.replace(hour = h, minute = m)
        else:
            present = present.replace(hour = h, minute = m) + datetime.timedelta(days=1)
    elif re.match('^\d\d:\d{0,2}$', update.message.text):
        h = int(update.message.text[0:2])
        m = int(update.message.text[3:])
        if h > present.hour or (h == present.hour and m >= present.minute):
            present = present.replace(hour = h, minute = m)
        else:
            present = present.replace(hour = h, minute = m) + datetime.timedelta(days=1)
    else:
        logger.warn("problem with time regex")
        return -1
    print(present)
    return ConversationHandler.END    


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

    FROM_CONFIRMATION: [MessageHandler(Filters.text, fromConfirm)],

    TO_PROPOSTION: [MessageHandler(Filters.text, toProposition)],

    TO_CONFIRMATION: [MessageHandler(Filters.text, toConfirm)],
    
    VIA_PROPOSTION: [MessageHandler(Filters.text, viaProposition)],

    VIA_CONFIRMATION: [MessageHandler(Filters.text, viaConfirm), 
        CommandHandler('skip', skipViaConfirm)], 

    ARRIVE_DEPART: [MessageHandler(Filters.text, whenStartArrive)],

    TIME: [MessageHandler(Filters.text, whenTime)],

    GET_CONNECTION: [MessageHandler(Filters.text, getConnection)]
}

FALLBACKS=[CommandHandler('cancel', cancel)]
