from emoji import emojize
from random import randint, choice
from telegram import ReplyKeyboardMarkup, KeyboardButton

from settings import USER_EMOJI


def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Gimme a cat!', KeyboardButton('Take my location.', request_location=True)],
        ])


def choice_emoji(user_data):
    if 'emoji' not in user_data:
        emoji = choice(USER_EMOJI)
        return emojize(emoji, language='alias')
    return user_data['emoji']


def bot_guess_number(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f'Your number is {user_number}. My number is {bot_number}. It is a victory.'
    elif user_number == bot_number:
        message = f'Your number is {user_number}. My number is {bot_number}. It is a tie.'
    else:
        message= f'Your number is {user_number}. My number is {bot_number}. It is a loss.'
    return message