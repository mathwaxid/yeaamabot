import logging
from telegram.ext import (Updater, CommandHandler, ConversationHandler,
    MessageHandler, Filters)

from anketa import anketa_start, anketa_name, anketa_rating, anketa_skip, anketa_comment
from handlers import (check_user_photo_for_cat, greet_user, guess_number_game, get_a_cat_pic, 
                      user_coordinates, repeat_after_me)

from settings import BOT_API_KEY

logging.basicConfig(filename='bot.log', level=logging.INFO)

def main():
    mybot = Updater(BOT_API_KEY, use_context=True)
    
    dp = mybot.dispatcher

    anketa = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(Anketa)$'), anketa_start)],
        states={
            'name': [MessageHandler(Filters.text, anketa_name)],
            'rating': [MessageHandler(Filters.regex('^(1|2|3|4|5)$'), anketa_rating,)],
            'comment': [
                CommandHandler('skip', anketa_skip),
                MessageHandler(Filters.text, anketa_comment)
            ],
            },
        fallbacks=[],
                    )
    
    dp.add_handler(anketa)
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('guess', guess_number_game))
    dp.add_handler(CommandHandler('cat', get_a_cat_pic))
    dp.add_handler(MessageHandler(Filters.regex('^(Gimme a cat!)$'), get_a_cat_pic))
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo_for_cat))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.text, repeat_after_me))

    logging.info('Bot started.')
    mybot.start_polling()
    mybot.idle()
    

if __name__ == '__main__':
    main()
