from dataclasses import dataclass
from constants import CLBK_GAME_CANCEL, CLBK_GAME_JOIN
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


# Telegram API and bot
key = open('.key').read()
bot = telebot.TeleBot(key, parse_mode='html')


# A GameBoss is the user who initiated and oversees a game.
@dataclass
class GameBoss:
    id: int
    first_name: str
    chat_id: int
    join_msg_id: str


game_bosses: list[GameBoss] = []


# When a user calls this command, sets them up as a
# game boss and creates a message allowing others to join
# Game boss can cancel the game too.
@bot.message_handler(commands=['start'])
def start_handler(message):

    if any(message.from_user.id == b.id for b in game_bosses):
        return

    # Apparently Python is getting pattern matching in 3.10. Neat.
    if message.chat.type == "private" or message.chat.type == "channel":
        return

    boss = GameBoss(
        message.from_user.id,
        message.from_user.first_name,
        message.chat.id,
        '' # We'll fill this in later. (join_msg_id)
        )

    game_bosses.append(boss)

    btns = InlineKeyboardMarkup(row_width=1)

    btns.add(
        InlineKeyboardButton("Join", callback_data=CLBK_GAME_JOIN),
        InlineKeyboardButton("Cancel", callback_data=CLBK_GAME_CANCEL)
        )

    # Fill in the remaining field.
    # Depends on this message successfully being sent; any failsafes needed?
    boss.join_msg_id = bot.send_message(
        message.chat.id,
        f"Join {message.from_user.first_name}'s game!",
        reply_markup=btns
        ).id


@bot.callback_query_handler(func=lambda c: c.data == CLBK_GAME_JOIN)
def game_join_handler(callback):
    msg = None

    if any(callback.message.from_user.id == b.id for b in game_bosses):
        msg = "You're the game boss!"

    bot.answer_callback_query(callback.id, text=msg)


@bot.callback_query_handler(func=lambda c: c.data == CLBK_GAME_CANCEL)
def game_cancel_handler(callback):
    print(callback.message.id)
    print(callback.inline_message_id)
    bot.answer_callback_query(callback.id)


bot.polling() 