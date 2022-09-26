import logging
from telegram.ext import (Updater, CommandHandler,
    MessageHandler, Filters)

from settings import BOT_API_KEY

logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update, context):
    print('Start is called.')
    update.message.reply_text('Hello.')


def repeat_after_me(update, context):
    text = update.message.text
    update.message.reply_text(text)


def main():
    mybot = Updater(BOT_API_KEY, use_context=True)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.text, repeat_after_me))

    logging.info('Bot started.')
    mybot.start_polling()
    mybot.idle()
    

if __name__ == '__main__':
    main()
