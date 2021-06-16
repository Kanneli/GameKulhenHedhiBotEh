class Player():
    def __init__(self, user_id, name, character, candy):
        self.user_id = user_id
        self.name = name
        self.candy = candy
        self.character = character
        self.dices = []
        self.items = []
        self.rolled = False
    
    def get_id(self):
        return self.user_id

    def get_name(self):
        return self.name

    def inline_name(self):
        return f'<a href="tg://user?id={self.user_id}">{self.name}</a>'
    
    def game_name(self):
        return f"{self.inline_name()} the {self.character}"

    def get_candy(self):
        return self.candy

    def add_candy(self, num):
        self.candy += num

    def sub_candy(self, num):
        self.candy -= num
    
    def get_character(self):
        return self.character

    def has_rolled(self):
        return self.rolled

    def roll(self, num):
        self.rolled = num

    def __eq__(self, player):
        return self.user_id == player.user_id