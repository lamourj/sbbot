from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler)

from sbbCffBot import logger

PICK_DAY, FROM_PROPOSTION, FROM_CONFIRMACTION,  TO, VIA = range(5)

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

    bot.sendMessage(chat_id=update.message.chat_id, text="Where will you be leaving from ?")

    return ConversationHandler.END

def fromConfirm(bot, update):
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

    FROM_PROPOSTION: [RegexHandler('^(Unique|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)$', fromProposition)], 

    FROM_CONFIRMACTION: [MessageHandler(Filters.text, fromConfirm)],

    TO: [], 
    
    VIA: []
}

FALLBACKS=[CommandHandler('cancel', cancel)]
