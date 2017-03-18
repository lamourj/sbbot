from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler)

from sbbCffBot import logger

PROCESS_FRIEND = range(1)

def newFriend(bot, update):
    user = update.message.from_user
    logger.info("User %s started a new connection." % (user.first_name))

    reply_keyboard = telegram.KeyboardButton(text="send_contact", request_contact=True)
    update.message.reply_text(
        'Choose a contact to add?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return PROCESS_FRIEND

    
def processFriend(bot, update):

    return -1;

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

ENTRY_POINTS = [CommandHandler('newFriend', newFriend)]


STATES={
    PROCESS_FRIEND: [MessageHandler(Filters.contact, processFriend)]
}

FALLBACKS=[CommandHandler('cancel', cancel)]
