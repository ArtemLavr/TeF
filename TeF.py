

import logging
import requests
from lxml import html 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,  CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup




"https://habr.com/ru/"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("Отправь команду /habr для получения актуальных статей")
    

def echo(update, context):

    """Echo the user message."""    
    update.message.reply_text(update.message.text)


def habr(update, context):
    
    keyboard = [
        [InlineKeyboardButton("Главная страница", callback_data= "habr_main")],
        [InlineKeyboardButton("Машинное обучение", callback_data="habr_ml")
        ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def get_articls(query, URL):
    r = requests.get(url= URL)
    tree = html.fromstring(r.content)
    post_link_list = tree.xpath("//a[contains(@class, 'post__title_link')]/@href") 
    for link in post_link_list:
        query.message.reply_text(link)

def callback_query_handler(update, context):
    query = update.callback_query
    query.answer()
    cqd = query.data
    if cqd == "habr_main":
        URL = "https://habr.com/ru/"
        get_articls(query, URL)
    elif cqd == "habr_ml":
        URL = "https://habr.com/ru/hub/machine_learning/"
        get_articls(query, URL)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("885804154:AAG7x6IV9lVDlehyNvSovXwMvHFiLtV8-rY", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("habr", habr))
    dp.add_handler(CallbackQueryHandler(callback_query_handler))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()