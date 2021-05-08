from components.player import Player

class GameSession():
    def __init__(self, chat_id, bot):
        self.characters = ['Egg', 'Notebook', 'Tuna', 'Toiletbrush', 'Glasses', 'Unicorn', 'Butter', 'Daddy', 'Pumpkin', 'Potato', 'Fox', 'Goose']
        self.chat_id = chat_id
        self.start_timer = 0
        self.players = []
        self.running = False
        self.active = None
        self.bot = bot

    def join(self, user_id, name, character):
        player = Player(user_id, name, character)
        if len(self.players) < 8 and player not in self.players and not self.running:
            if character in self.characters:
                self.characters.remove(character)
                self.players.append(player)
                return True
            else:
                self.bot.send_message(self.active.chat.id, f"{character} is already taken")
        return False

    def set_active(self, message):
        self.active = message

    def count(self):
        return len(self.players)