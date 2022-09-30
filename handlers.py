from glob import glob
from random import choice
from utils import choice_emoji, bot_guess_number, main_keyboard

def greet_user(update, context):
    context.user_data['emoji'] = choice_emoji(context.user_data)
    emoji = context.user_data['emoji']
    update.message.reply_text(
        f'Hello. {emoji}',
        reply_markup=main_keyboard()
        )


def guess_number_game(update, context):
    if context.args:
        try:
            user_number = int(context.args[0])
            message = bot_guess_number(user_number)
        except(ValueError, TypeError):
            message = 'Please, enter any integer after /guess command.'
    else:
        message = 'Please, enter any integer (!) after /guess command.'
    update.message.reply_text(
        message,
        reply_markup=main_keyboard())


def get_a_cat_pic(update, context):
    cat_pic_list = glob('images/cat*.jpg')
    cat_pic_filename = choice(cat_pic_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(
        chat_id=chat_id,
        photo=open(cat_pic_filename, 'rb'),
        reply_markup=main_keyboard())


def user_coordinates(update, context):
    coords = update.message.location
    message = f'Your coordinates are latitude: {coords["latitude"]}; longitude: {coords["longitude"]}. {context.user_data["emoji"]}'
    update.message.reply_text(message)


def repeat_after_me(update, context):
    context.user_data['emoji'] = choice_emoji(context.user_data)
    text = update.message.text + context.user_data['emoji']
    update.message.reply_text(
        text,
        reply_markup=main_keyboard())
