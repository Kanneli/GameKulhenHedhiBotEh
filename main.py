import telebot
import json
import threading
from telebot import types
from components.scheduler import Scheduler
from components.game_session import GameSession

# Bot API
key = open('.key').read()
bot = telebot.TeleBot(key, parse_mode='html')
commands = [
    types.BotCommand('start', 'Start the game'),
    types.BotCommand('quit', 'Quit the game')
]
bot.set_my_commands(commands)

characters = ['Egg', 'Notebook', 'Tuna', 'Toiletbrush', 'Glasses', 'Unicorn', 'Butter', 'Daddy', 'Pumpkin', 'Potato', 'Fox', 'Goose']
bot_messages = []
game_sessions = {}
scheduler_thread = Scheduler()

# Main Bot Commands
@bot.message_handler(commands=['start'])
def init_handler(message):
    if (not message.chat.id in game_sessions):
        global scheduler_thread
        markup = types.InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(
            types.InlineKeyboardButton("Select Character", switch_inline_query_current_chat="Character")
        )

        time_limit = 90
        reminder = 30
        game_sessions[message.chat.id] = GameSession(message.chat.id, remove_session, bot)
        if (not scheduler_thread.is_alive()):
            scheduler_thread = Scheduler()
            scheduler_thread.add_event(reminder, game_sessions[message.chat.id].remind_join)
            scheduler_thread.add_event(time_limit, game_sessions[message.chat.id].close_join)
            scheduler_thread.start()
        else:
            scheduler_thread.add_event(reminder, game_sessions[message.chat.id].remind_join)
            scheduler_thread.add_event(time_limit, game_sessions[message.chat.id].close_join)

        bot.send_message(message.chat.id, GameSession.texts['game_init'])
        join_msg = bot.send_message(message.chat.id, game_sessions[message.chat.id].get_join_text(), reply_markup=markup)
        game_sessions[message.chat.id].set_active(join_msg)
    else:
        bot.send_message(
            message.chat.id,
            "There is already a game running in this chat"
        )

@bot.message_handler(commands=['quit'])
def quit_handler(message):
    if (message.chat.id in game_sessions):
        if (game_sessions[message.chat.id].quit(message.from_user.id)):
            game = game_sessions[message.chat.id]
            text = game.get_join_text()
            bot.edit_message_text(text, game.active.chat.id, game.active.id, reply_markup=game.active.reply_markup)
            bot.send_message(message.chat.id, "You have quit the game")
        else:
            bot.send_message(message.chat.id, "Are you even in the game?")
    else:
        bot.send_message(message.chat.id, "Is there even a game to quit?")

@bot.inline_handler(lambda query: query.query == 'Character')
def query_text(query):
    try:
        options = []
        count = 0
        for item in characters:
            options.append(types.InlineQueryResultArticle(
                str(count),
                item,
                types.InputTextMessageContent(item), description="Choose the " + item,
                thumb_url=f"https://raw.githubusercontent.com/Kanneli/GameKulhenHedhiBotEh/develop/assets/characters/{item}.png?20210508"
            ))
            count += 1
        bot.answer_inline_query(query.id, options)
    except Exception as e:
        print(e)

@bot.message_handler(func=lambda message: 'via_bot' in message.json, content_types=['text'])
def game_handler(message):
    if (message.chat.id in game_sessions):
        if message.text in characters:
            game = game_sessions[message.chat.id]
            if game.join(message.from_user.id, message.from_user.first_name, message.text):
                text = game.get_join_text()
                bot.edit_message_text(text, game.active.chat.id, game.active.id, reply_markup=game.active.reply_markup)
                game.active.text = text

def remove_session(chat_id):
    game_sessions.pop(chat_id)

bot.polling()
