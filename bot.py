from ast import alias
import logging
from glob import glob
from random import randint, choice
import emoji
from telegram.ext import (Updater, CommandHandler,
    MessageHandler, Filters)
from emoji import emojize

from settings import BOT_API_KEY, USER_EMOJI

logging.basicConfig(filename='bot.log', level=logging.INFO)


def choice_emoji(user_data):
    if 'emoji' not in user_data:
        emoji = choice(USER_EMOJI)
        return emojize(emoji, language='alias')
    return user_data['emoji']


def greet_user(update, context):
    print('Start is called.')
    context.user_data['emoji'] = choice_emoji(context.user_data)
    emoji = context.user_data['emoji']
    update.message.reply_text(f'Hello. {emoji}')


def repeat_after_me(update, context):
    context.user_data['emoji'] = choice_emoji(context.user_data)
    text = update.message.text + context.user_data['emoji']
    update.message.reply_text(text)


def bot_guess_number(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f'Your number is {user_number}. My number is {bot_number}. It is a victory.'
    elif user_number == bot_number:
        message = f'Your number is {user_number}. My number is {bot_number}. It is a tie.'
    else:
        message= f'Your number is {user_number}. My number is {bot_number}. It is a loss.'
    return message


def guess_number_game(update, context):
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = bot_guess_number(user_number)
        except(ValueError, TypeError):
            message = 'Please, enter any integer after /guess command.'
    else:
        message = 'Please, enter any integer (!) after /guess command.'
    update.message.reply_text(message)


def get_a_cat_pic(update, context):
    cat_pic_list = glob('images/cat*.jpg')
    cat_pic_filename = choice(cat_pic_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))


def main():
    mybot = Updater(BOT_API_KEY, use_context=True)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('guess', guess_number_game))
    dp.add_handler(CommandHandler('cat', get_a_cat_pic))
    dp.add_handler(MessageHandler(Filters.text, repeat_after_me))

    logging.info('Bot started.')
    mybot.start_polling()
    mybot.idle()
    

if __name__ == '__main__':
    main()
