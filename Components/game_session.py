from components.player import Player

class GameSession():
    texts = {
        'game_init': "Aight time for the <strong>Ripped off variant</strong>. Bot may have emotional breakdowns every now and then",
        'join_init': "Ok so select a character within the next 90 seconds ya? But guess what? It got no game ;-;",
        'join_remind': "60 seconds left to join bro"
    }

    def __init__(self, chat_id, remove, bot):
        self.characters = ['Egg', 'Notebook', 'Tuna', 'Toiletbrush', 'Glasses', 'Unicorn', 'Butter', 'Daddy', 'Pumpkin', 'Potato', 'Fox', 'Goose']
        self.chat_id = chat_id
        self.players = []
        self.active = None
        self.state = "join_init"
        self.bot = bot
        self.remove_self = remove

    def join(self, user_id, name, character):
        player = Player(user_id, name, character)
        if len(self.players) < 8 and player not in self.players and 'join' in self.state:
            if character in self.characters:
                self.characters.remove(character)
                self.players.append(player)
                return True
            else:
                self.bot.send_message(self.active.chat.id, f"{character} is already taken")
        return False

    def quit(self, user_id):
        for player in self.players:
            if player.user_id == user_id:
                self.players.remove(player)
                self.characters.append(player.get_character())
                return True
        return False

    def get_join_text(self):
        text = GameSession.texts[self.state]
        if len(self.players) > 0:
            text += "\n\nPlayer List:"
            for player in self.players:
                if self.state != 'join_init': player_name = player.inline_name()
                else: player_name = player.get_name()
                text += f"\n{player_name} the {player.get_character()}"
        return text

    def remind_join(self):
        self.state = 'join_remind'
        markup = self.active.reply_markup
        self.bot.edit_message_text(self.active.text, self.active.chat.id, self.active.id)
        text = self.get_join_text()
        self.active = self.bot.send_message(self.active.chat.id, text, reply_markup=markup)

    def close_join(self):
        self.bot.edit_message_text(self.active.text, self.active.chat.id, self.active.id)
        if (len(self.players) < 3):
            self.active = self.bot.send_message(self.active.chat.id, f"Just {len(self.players)}? You atleast need 3 players to play this :(")
            self.remove_self(self.chat_id)
        else:
            self.active = self.bot.send_message(self.active.chat.id, f"Eyyyy nice {len(self.players)} players! Too bad there is no game yet :(")
            self.remove_self(self.chat_id)

    def set_active(self, message):
        self.active = message

    def count(self):
        return len(self.players)