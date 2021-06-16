from random import randint
from telebot import types
from components.player import Player
from components.scheduler import Scheduler

class GameSession():
    init_candy = 5
    player_limit = 3
    reminder = 30
    time_limit = 60 
    animations = {
        'mainmenu': 'CgACAgUAAxkDAAIYtmDJ9n9ikuL5s3B5f42_IEz02yqcAAL5AgACuIxRVuPGLpqU6lCJHwQ'
    }
    texts = {
        'join_init': f"<b>Welcome to the world of Candy Critters!</b>\n\nYou have {time_limit} seconds to join.\nYou need atleast 3 people in the party.\nBut guess what? It got no game ;-;",
        'join_remind': f"You have {time_limit - reminder} seconds left to join the party",
        'game_start': "None of this shit is final but badabing badabomb and some how you guys are toiny little people in a candy world or something. So who is going to get outta here with the most candy? 👀"
    }

    # Introductionary phase
    # =====================
    def __init__(self, message, characters, remove, bot):
        self.scheduler = Scheduler()
        self.characters = characters
        self.chat_id = message.chat.id
        self.players = []
        self.curr_player = None
        self.active = None
        self.state = "join_init"
        self.bot = bot
        self.remove_self = remove
        self.init_messages(message)

    def init_messages(self, message):
        markup = types.InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(types.InlineKeyboardButton("Select Character", switch_inline_query_current_chat="Character"))

        if GameSession.animations['mainmenu']:
            video = GameSession.animations['mainmenu']
        else:
            video = open('./assets/videos/mainmenu.mp4', 'rb')
        self.bot.send_animation(message.chat.id, video)

        join_msg = self.bot.send_message(self.chat_id, self.join_list(), reply_markup=markup)
        self.set_active(join_msg)

        self.add_schedule(GameSession.reminder, self.remind_join)
        self.add_schedule(GameSession.time_limit, self.close_join)

    def join(self, user_id, name, character):
        player = Player(user_id, name, character, GameSession.init_candy)
        if self.player_count() < 8 and player not in self.players and 'join' in self.state:
            if character in self.characters:
                self.characters.remove(character)
                self.players.append(player)
                self.update_join()
            else:
                self.bot.send_message(self.active.chat.id, f"{character} is already taken")

    def remind_join(self):
        self.state = 'join_remind'
        markup = self.active.reply_markup
        self.close_active()
        text = self.join_list()
        self.active = self.bot.send_message(self.active.chat.id, text, reply_markup=markup)

    def update_join(self):
        text = self.join_list()
        self.active = self.bot.edit_message_text(text, self.active.chat.id, self.active.id, reply_markup=self.active.reply_markup)

    def join_list(self):
        text = GameSession.texts[self.state]
        if self.player_count() > 0:
            text += "\n\n<b>Player List:</b>"
            for player in self.players:
                text += f"\n{player.game_name()}"
        return text

    def close_join(self):
        self.close_active()
        limit = GameSession.player_limit
        if (self.player_count() < limit):
            self.active = self.bot.send_message(self.active.chat.id, f"Just {self.player_count()}? You atleast need {limit} players to play this :(")
            self.remove_self(self.chat_id)
        else:
            self.init_players()

    def quit(self, user_id):
        player = self.get_player(user_id)
        if player:
            self.players.remove(player)
            self.characters.append(player.get_character())
            self.update_join()
            self.bot.send_message(self.chat_id, "You have quit the game")
            return
        self.bot.send_message(self.chat_id, "Are you even in the game?")

    # Player initiation
    # =================
    def init_players(self):
        self.state = "game_start"
        text = GameSession.texts[self.state] + '\n'
        for player in self.players:
            text += f"\n{player.get_candy()} 🍬 - {player.game_name()}"
        self.bot.send_message(self.chat_id, text)

        text = "<i>Everyone gets one mysterious ticket 🎫</i>"
        self.bot.send_message(self.chat_id, text)

        text = "<b>NOW ROLL THE DAMN DICE\n</b>"
        markup = types.InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(types.InlineKeyboardButton("🎲", callback_data=f"init_roll"))
        self.active = self.bot.send_message(self.chat_id, text, reply_markup=markup)
        # self.add_schedule(GameSession.time_limit, self.init_area_1)
        self.add_schedule(20, self.init_area_1)

    def init_roll(self, user_id, call_id, message):
        roll = self.roll_dice(call_id, message, user_id, 20)
        if roll:
            self.active = self.bot.edit_message_text(self.roll_list(), self.active.chat.id, self.active.id, reply_markup=self.active.reply_markup)
            self.bot.answer_callback_query(call_id)

    def roll_list(self):
        text = "<b>NOW ROLL THE DAMN DICE\n</b>"
        for player in self.players:
            if player.has_rolled():
                text += f"\n{player.game_name()} has rolled a <b>{player.has_rolled()}</b>"
        return text

    # Area 1
    # ======
    def init_area_1(self):
        self.close_active()
        self.players = self.quicksort_players()
        self.reset_rolls()

        text = "Sooo for a test game hehe\nWrite a word that starts with last letter of the previous word, first player can start with any.\nNo repeat words and if u can't write one you are out\nAnd you have 5 seconds to write one :D\n"
        for player in self.players:
            text += f"\n{player.game_name()}"
        self.bot.send_message(self.chat_id, text)

        self.curr_player = 0
        self.add_schedule(15, self.start_test)

    # Utilities
    # =========
    def set_active(self, message):
        self.active = message

    def close_active(self, text=None):
        if text is None:
            self.bot.edit_message_text(self.active.text, self.active.chat.id, self.active.id)
        else:
            self.bot.edit_message_text(text, self.active.chat.id, self.active.id)

    def get_player(self, user_id):
        for player in self.players:
            if (user_id == player.get_id()): return player

    def quicksort_players(self, array=None):
        if array is None:
            array = self.players
        if len(array) < 2:
            return array

        low, same, high, null = [], [], [], []
        # Select your `pivot` element randomly
        while True:
            pivot = array[randint(0, len(array) - 1)].has_rolled()
            if pivot: break

        for player in array:
            roll = player.has_rolled()
            if roll:
                if roll < pivot:
                    low.append(player)
                elif roll == pivot:
                    same.append(player)
                elif roll > pivot:
                    high.append(player)
            else:
                null.append(player)

        return self.quicksort_players(high) + same + self.quicksort_players(low) + null

    def roll_dice(self, call_id, message, user_id, dice):
        if (self.state == "game_start"):
            player = self.get_player(user_id)
            if player:
                if not player.has_rolled():
                    roll_num = randint(1, dice)
                    player.roll(roll_num)
                    return True
                else:
                    self.bot.answer_callback_query(call_id, "You have already rolled")
            else:
                self.bot.answer_callback_query(call_id, "You are not in this party")
        else:
            self.bot.answer_callback_query(call_id)
            self.bot.edit_message_text(message.text, message.chat.id, message.id)

    def reset_roll(self, user_id):
        self.get_player(user_id).roll(False)

    def reset_rolls(self):
        for player in self.players:
            player.roll(False)

    def player_count(self):
        return len(self.players)

    def add_schedule(self, time, func):
        if (not self.scheduler.is_alive()): self.scheduler = Scheduler()
        self.scheduler.add_event(time, func, self.chat_id)

    def remove_last_schedule(self):
        self.scheduler.remove_event(self.chat_id)