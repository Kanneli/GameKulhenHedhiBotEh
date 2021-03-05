import telebot

# Bot API
key = open('.key').read()
bot = telebot.TeleBot(key, parse_mode='html')

# Main Bot Commands
@bot.message_handler(commands=['start'])
def tictactoe_handler(message):
    bot.send_message(message.chat.id, "Hello there")

bot.polling() 