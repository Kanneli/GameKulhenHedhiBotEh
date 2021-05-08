class Player():
    def __init__(self, user_id, name, character):
        self.user_id = user_id
        self.name = name
        self.character = character
    
    def get_name(self):
        return self.name

    def inline_name(self):
        return f'<a href="tg://user?id={self.user_id}">{self.name}</a>'
    
    def get_character(self):
        return self.character

    def __eq__(self, player):
        return self.user_id == player.user_id