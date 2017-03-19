from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler)

from sbbCffBot import (logger, tablesManager)

import re, datetime

import handlers.query_handler as qh
import interfaces.parser as parser
import interfaces.helper as helper

PICK_DAY, FROM_PROPOSTION, FROM_CONFIRMATION, TO_PROPOSTION, \
TO_CONFIRMATION, VIA_PROPOSTION, VIA_CONFIRMATION, ARRIVE_DEPART, \
TIME, GET_CONNECTION, CHOOSE_TRAIN= range(11) 

NUMBER_OF_TRAINS = 3
NO_CONNECTION_MESSAGE = "Quit :-/"

mapUserCurrent = {}

def connectionType(bot, update):
    user = update.message.from_user
    logger.info("User %s started a new connection." % (user.first_name))


    reply_keyboard = [['/unique', '/weekly']]
    update.message.reply_text(
        'Hi, do you want to add a unique connection or a weekly one?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))




def pickDay(bot, update):
    daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 
            'Saturday', 'Sunday']
    userId = str(update.message.from_user.id)
    if update.message.text == '/weekly':
        mapUserCurrent[userId] = {'typeOrWeekly': []}
    elif update.message.text in daysOfWeek:
        mapUserCurrent[userId]['typeOrWeekly'].append(update.message.text)


    logger.info("%s" % (update.message.text))
    if update.message.text == 'Done':
        reply_keyboard = [['Proceed to next step']]
        update.message.reply_text(
            'Please',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return FROM_PROPOSTION
    else:
        reply_keyboard = [[i] for i in daysOfWeek if i not in mapUserCurrent[userId]['typeOrWeekly']]
        reply_keyboard.append(['Done'])
        update.message.reply_text(
            'On which day of the week ?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return PICK_DAY

def fromProposition(bot, update):
    userId = str(update.message.from_user.id)
    if update.message.text == '/unique':
        mapUserCurrent[userId] = {'typeOrWeekly': []}

    user = update.message.from_user
    logger.info("New connection day of %s: %s" % (user.first_name, mapUserCurrent[userId]['typeOrWeekly']))

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
    print(mapUserCurrent)
    mapUserCurrent[str(update.message.from_user.id)]['from'] = update.message.text
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
    mapUserCurrent[str(update.message.from_user.id)]['to'] = update.message.text
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
    res = update.message.text
    if res == 'Yes' or res == 'No': #only if not conrifmed
        mapUserCurrent[str(update.message.from_user.id)]['via'] = None
    else:
        mapUserCurrent[str(update.message.from_user.id)]['via'] = update.message.text

    logger.info("Going via  %s" % update.message.text)
    reply_keyboard = [["Depart by ..h.."], ["Arrive by ..h.."]]

    update.message.reply_text("Do you want to arrive or depart by a certain time?", 
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return TIME

def whenTime(bot, update):

    mapUserCurrent[str(update.message.from_user.id)]['by'] =  update.message.text == "Depart by ..h.."
    logger.info("Wanting to \"%s\" " % update.message.text)

    update.message.reply_text("Please type the time you want to %s. Possible input ..:.., now" % update.message.text[:-8])
    return GET_CONNECTION

def getConnection(bot, update):
    idReq = str(update.message.from_user.id)
    logger.info("Wanting to  %s at %s " % (mapUserCurrent[idReq]['by'] , update.message.text))
    time = datetime.datetime.now()
    timeStr = ''
    # if re.match('^now$', update.message.text):
    if re.match('^\d:\d{0,2}$', update.message.text):
        h = int(update.message.text[0:1])
        m = int(update.message.text[2:])
        if h > time.hour or (h == time.hour and m >= time.minute):
            time = time.replace(hour = h, minute = m)
        else:
            time = time.replace(hour = h, minute = m) + datetime.timedelta(days=1)
        timeStr = str(int(time.timestamp()*1000))
    elif re.match('^\d\d:\d{0,2}$', update.message.text):
        h = int(update.message.text[0:2])
        m = int(update.message.text[3:])
        if h > time.hour or (h == time.hour and m >= time.minute):
            time = time.replace(hour = h, minute = m)
        else:
            time = time.replace(hour = h, minute = m) + datetime.timedelta(days=1)
        timeStr = str(int(time.timestamp()*1000))

    elif re.match('^(?i)now$', update.message.text):
        timeStr = None
    else:
        logger.warn("problem with time regex")
        return -1

    mapUserCurrent[idReq]['time'] = timeStr
    print(mapUserCurrent[idReq])
    # try:
    qhandler = qh.QueryHandler()
    queryResponse = qhandler.getConnexion( mapUserCurrent[idReq]['from'], mapUserCurrent[idReq]['to'], 
        mapUserCurrent[idReq]['via'], mapUserCurrent[idReq]['time'], 
        mapUserCurrent[idReq]['by'])

    mapUserCurrent[idReq]['fullJsons'] = queryResponse;

    parsedResponse = [parser.Parser().parseConnexion(i) for i in queryResponse['connections']]
    mapUserCurrent[idReq]['jsons'] = parsedResponse;

    response = helper.Helper().getConnexionsStrings(queryResponse['connections'][:NUMBER_OF_TRAINS]);
    update.message.reply_text("Which train do you want?", 
        reply_markup=ReplyKeyboardMarkup(response, one_time_keyboard=True))
    # except:
    #     logger.warn("error somewhere")
    #     update.message.reply_text("No connection available?", 
    #         reply_markup=ReplyKeyboardMarkup([[NO_CONNECTION_MESSAGE]], one_time_keyboard=True))

    return CHOOSE_TRAIN

def chooseTrain(bot, update): 
    msg = update.message.text
    if not msg == NO_CONNECTION_MESSAGE:
        idReq = str(update.message.from_user.id)
        userMap = mapUserCurrent[idReq]
        strings = helper.Helper().getConnexionsStrings(mapUserCurrent[idReq]['fullJsons']['connections'][:NUMBER_OF_TRAINS]);
        index = 0
        for i in range(len(strings)):
            if strings[i] == update.message.text:
                index = i

        weekly = userMap['typeOrWeekly']
        if weekly == [] :
            tablesManager.addSingularEntry(update.message.from_user.id, mapUserCurrent[idReq]['jsons'][index])
            print("From newTravel: " + str(tablesManager))
        else: 
            for i in range(len(weekly) - 1):
                tablesManager.addRegularEntry(weekly[i], update.message.from_user.id, mapUserCurrent[idReq]['jsons'][index])

    return -1;


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
    PICK_DAY: [RegexHandler('^(Unique|Weekly|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|Done)$', pickDay)],

    FROM_PROPOSTION: [RegexHandler('^(Proceed to next step)$', fromProposition)], 

    FROM_CONFIRMATION: [MessageHandler(Filters.text, fromConfirm)],

    TO_PROPOSTION: [MessageHandler(Filters.text, toProposition)],

    TO_CONFIRMATION: [MessageHandler(Filters.text, toConfirm)],
    
    VIA_PROPOSTION: [MessageHandler(Filters.text, viaProposition)],

    VIA_CONFIRMATION: [MessageHandler(Filters.text, viaConfirm), 
        CommandHandler('skip', skipViaConfirm)], 

    ARRIVE_DEPART: [MessageHandler(Filters.text, whenStartArrive)],

    TIME: [MessageHandler(Filters.text, whenTime)],

    GET_CONNECTION: [MessageHandler(Filters.text, getConnection)],

    CHOOSE_TRAIN: [MessageHandler(Filters.text, chooseTrain)]
}

FALLBACKS=[CommandHandler('cancel', cancel)]
