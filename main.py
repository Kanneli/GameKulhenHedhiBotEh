import telebot

key = open('.key').read()
bot = telebot.TeleBot(key, parse_mode='html')

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Hello there")

bot.polling() 