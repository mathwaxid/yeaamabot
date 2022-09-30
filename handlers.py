from glob import glob
import os
from random import choice
from utils import choice_emoji, bot_guess_number, has_object_on_image, main_keyboard

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


def check_user_photo_for_cat(update, context):
    update.message.reply_text('Give me a second...')
    os.makedirs('downloads', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join('downloads', f'{update.message.photo[-1].file_id}.jpg')
    photo_file.download(file_name)
    if has_object_on_image(file_name, 'cat'):
        update.message.reply_text('There is a cat! I gonna save it.')
        new_file_name = os.path.join('images', f'cat_{photo_file.file_id}.jpg')
        os.rename(file_name,new_file_name)
    else: 
        os.remove(file_name)
        update.message.reply_text('There is no cat. Don\'t fucking joke with me.')