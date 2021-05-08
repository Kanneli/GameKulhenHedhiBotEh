import telebot
import pprint
from telebot import types
from components.game_session import GameSession

# Bot API
key = open('.key').read()
bot = telebot.TeleBot(key, parse_mode='html')

characters = ['Egg', 'Notebook', 'Tuna', 'Toiletbrush', 'Glasses', 'Unicorn', 'Butter', 'Daddy', 'Pumpkin', 'Potato', 'Fox', 'Goose']
bot_messages = []
game_sessions = {}

# Main Bot Commands
@bot.message_handler(commands=['start'])
def game_handler(message):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        types.InlineKeyboardButton("Select Character", switch_inline_query_current_chat="Characters")
    )
    game_sessions[message.chat.id] = GameSession(message.chat.id, bot)
    bot.send_message(
        message.chat.id,
        "Aight time for the <strong>Ripped off variant</strong>. Bot may have emotional breakdowns every now and then"
    )
    join_msg = bot.send_message(
        message.chat.id,
        "Ok so select a character ya? But guess what? It got no game ;-;",
        reply_markup=markup
    )
    game_sessions[message.chat.id].set_active(join_msg)

@bot.callback_query_handler(func=lambda call: True)
def call_handler(call):
    print(call)

@bot.inline_handler(lambda query: query.query == 'Characters')
def query_text(query):
    try:
        options = []
        count = 0
        for item in characters:
            options.append(types.InlineQueryResultArticle(
                str(count),
                item,
                types.InputTextMessageContent(item), description="Choose the " + item,
                thumb_url=f"https://raw.githubusercontent.com/Kanneli/GameKulhenHedhiBotEh/develop/assets/characters/{item}.png"
            ))
            count += 1
        bot.answer_inline_query(query.id, options)
    except Exception as e:
        print(e)

@bot.message_handler(func=lambda message: 'via_bot' in message.json, content_types=['text'])
def game_handler(message):
    if message.text in characters:
        game = game_sessions[message.chat.id]
        text = game.active.text
        if game.join(message.from_user.id, message.from_user.first_name, message.text):
            if (game.count() == 1):
                text += "\n\nPlayer List:\n"
            text += f"{message.from_user.first_name} the {message.text}\n"
            game.active.text = text
            bot.edit_message_text(text, game.active.chat.id, game.active.id, reply_markup=game.active.reply_markup)

bot.polling()
