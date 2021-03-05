import telebot
from telebot import types
from Components.player import Player
from Components.narrator import Narrator

# Bot API
key = open('.key').read()
bot = telebot.TeleBot(key, parse_mode='html')

# Variables
players = {}
narration = Narrator()

# Main Bot Commands
@bot.message_handler(commands=['start'])
def game_handler(message):
    out_msg = narration.start
    markup = Player.inline_start()
    bot.send_message(message.chat.id, out_msg, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True and "init" in call.data)
def call_handler(call):
    if call.data == "init-start":
        out_msg = narration.start_yes
        bot.edit_message_text(out_msg, call.message.chat.id, call.message.id, reply_markup=Player.inline_class())
    elif call.data == "init-end":
        out_msg = narration.start_no
        bot.edit_message_text(out_msg, call.message.chat.id, call.message.id, reply_markup=None)

@bot.callback_query_handler(func=lambda call: True and "class" in call.data)
def call_handler(call):
    player_class = call.data.split('-')[1]
    out_msg = narration.class_select(player_class)
    bot.edit_message_text(out_msg, call.message.chat.id, call.message.id, reply_markup=Player.inline_combat(player_class))

@bot.callback_query_handler(func=lambda call: True and "combat" in call.data)
def call_handler(call):
    player_id = call.from_user.id
    call_data = call.data.split('-')[1].split('|')
    player_class = call_data[0]
    player_combat = call_data[1]

    # Initiate Player
    players[player_id] = Player(call.from_user, player_class, player_combat)
    out_msg = narration.combat_select(player_class, player_combat)

    bot.edit_message_text(out_msg, call.message.chat.id, call.message.id)
    bot.send_message(call.message.chat.id, players[player_id].get_details())

bot.polling()
