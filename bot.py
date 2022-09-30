import logging
from telegram.ext import (Updater, CommandHandler,
    MessageHandler, Filters)

from handlers import (greet_user, guess_number_game, get_a_cat_pic, 
                      user_coordinates, repeat_after_me)

from settings import BOT_API_KEY

logging.basicConfig(filename='bot.log', level=logging.INFO)

def main():
    mybot = Updater(BOT_API_KEY, use_context=True)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('guess', guess_number_game))
    dp.add_handler(CommandHandler('cat', get_a_cat_pic))
    dp.add_handler(MessageHandler(Filters.regex('^(Gimme a cat!)$'), get_a_cat_pic))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.text, repeat_after_me))

    logging.info('Bot started.')
    mybot.start_polling()
    mybot.idle()
    

if __name__ == '__main__':
    main()
