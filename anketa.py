from telegram import ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from utils import main_keyboard

def anketa_start(update, context):
    update.message.reply_text(
        'What is your name?',
        reply_markup=ReplyKeyboardRemove()
        )
    return 'name'


def anketa_name(update, context):
    user_name = update.message.text
    if len(user_name.split()) < 2:
        update.message.reply_text('Please, enter name and surname.')
        return 'name'
    else:
        context.user_data['anketa'] = {'name': user_name}
        reply_keyboard = [['1', '2', '3', '4', '5']]
        update.message.reply_text(
            'Please, rate the bot.',
            reply_markup = ReplyKeyboardMarkup(
                reply_keyboard,
                one_time_keyboard=True)
        )
    return 'rating'


def anketa_rating(update, context):
    context.user_data['anketa']['rating'] = int(update.message.text)
    update.message.reply_text('Please, write a comment about our bot or press /skip.')
    return 'comment'


def anketa_comment(update, context):
    context.user_data['anketa']['comment'] = update.message.text.title()
    user_text = f"""
<b>Full name:</b>
{context.user_data['anketa']['name'].capitalize()}
<b>You rated the bot as:</b>
{context.user_data['anketa']['rating']}
<b>Your comment:</b>
{context.user_data['anketa']['comment'].capitalize()} 
    """
    update.message.reply_text(
        user_text, 
        parse_mode=ParseMode.HTML,
        reply_markup=main_keyboard())
    return ConversationHandler.END

def anketa_skip(update, context):
    user_text = f"""
<b>Full name:</b>
{context.user_data['anketa']['name'].title()}
<b>You rated the bot as:</b>
{context.user_data['anketa']['rating']} 
    """
    update.message.reply_text(
        user_text, 
        parse_mode=ParseMode.HTML,
        reply_markup=main_keyboard())
    return ConversationHandler.END