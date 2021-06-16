import telebot
import json
import threading
from telebot import types
from components.game_session import GameSession

# Bot API
key = open('.key').read()
bot = telebot.TeleBot(key, parse_mode='html')

# Bot Command List
commands = [
    types.BotCommand('start', 'Start the game'),
    types.BotCommand('quit', 'Quit the game')
]
bot.set_my_commands(commands)

# Vairable declarations
characters = ['Egg', 'Notebook', 'Tuna', 'Toiletbrush', 'Glasses', 'Unicorn', 'Butter', 'Daddy', 'Pumpkin', 'Potato', 'Fox', 'Goose']
sessions = {}

# Main Bot Commands
@bot.message_handler(commands=['start'])
def init_handler(message):
    if not message.chat.id in sessions:
        # Inits game session
        sessions[message.chat.id] = GameSession(message, characters, remove_session, bot)
    else:
        # Rejects if a game is already running
        bot.send_message(message.chat.id, "There is already a game running in this chat")

@bot.message_handler(commands=['quit'])
def quit_handler(message):
    if message.chat.id in sessions:
        sessions[message.chat.id].quit(message.from_user.id)
    else:
        bot.send_message(message.chat.id, "Is there even a game to quit?")

@bot.message_handler(func=lambda message: 'via_bot' in message.json, content_types=['text'])
def game_handler(message):
    if message.chat.id in sessions:
        if message.text in characters:
            sessions[message.chat.id].join(message.from_user.id, message.from_user.first_name, message.text)

@bot.inline_handler(lambda query: query.query == 'Character')
def query_text(query):
    try:
        options = []
        count = 0
        for item in characters:
            options.append(types.InlineQueryResultArticle(
                str(count), item, types.InputTextMessageContent(item),
                description="Choose the " + item,
                thumb_url=f"https://raw.githubusercontent.com/Kanneli/GameKulhenHedhiBotEh/develop/assets/characters/{item}.png?20210508"
            ))
            count += 1
        bot.answer_inline_query(query.id, options)
    except Exception as e:
        print(e)

@bot.callback_query_handler(func=lambda call: True)
def call_handler(call):
    if (call.message.chat.id in sessions):
        sessions[call.message.chat.id].init_roll(call.from_user.id, call.id, call.message)
    else:
        bot.answer_callback_query(call.id, "This game is currently not available")
        bot.edit_message_text(call.message.text, call.message.chat.id, call.message.id)

# Util Methods
def remove_session(chat_id):
    sessions.pop(chat_id)

bot.polling()
