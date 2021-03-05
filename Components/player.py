from telebot import types

class Player():
    def __init__(self, player, player_class, player_combat):
        self.id = player.id
        self.name = player.first_name
        self.inventory = self.init_inventory(player_combat)
        self.p_class = player_class
        self.stats = self.init_stats(player_class)
        self.level = 1
        self.xp = 0

    def get_details(self):
        out_msg = "<b>Player Stats:</b>\n"
        out_msg += f"<b>Class:</b> {self.p_class}\n"
        out_msg += f"<b>Level:</b> {self.level}\n"
        out_msg += f"<b>XP:</b> {self.xp}\n"

        out_msg += f"\n<b>Stats:</b>\n"
        for stat in self.stats:
            out_msg += f"<b>{stat}:</b> {self.stats[stat]}\n"

        out_msg += f"\n<b>Inventory:</b>\n"
        for item in self.inventory:
            out_msg += f"<b>{item}:</b> {self.inventory[item]}\n"

        return out_msg

        
    @staticmethod
    def init_stats(player_class):
        if player_class == "human":
            return {"hp": 10}
        elif player_class == "dwarf":
            return {"hp": 20}
        elif player_class == "elf":
            return {"hp": 15}

    @staticmethod
    def init_inventory(combat):
        if combat == "stealth":
            return {"weapons": ["dagger"]}
        elif combat == "offense":
            return {"weapons": ["sword"]}
        elif combat == "defense":
            return {"weapons": ["sword", "shield"]}
        elif combat == "magic":
            return {"weapons": ["staff"]}

    @staticmethod
    def inline_start():
        markup = types.InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(
            types.InlineKeyboardButton("Yes", callback_data=f"init-start"),
            types.InlineKeyboardButton("Hell naw", callback_data=f"init-end")
        )
        return markup

    @staticmethod
    def inline_class():
        markup = types.InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(
            types.InlineKeyboardButton("Human", callback_data="class-human"),
            types.InlineKeyboardButton("Dwarf", callback_data="class-dwarf"),
            types.InlineKeyboardButton("Elf", callback_data="class-elf")
        )
        return markup

    @staticmethod
    def inline_combat(player_class):
        markup = types.InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(
            types.InlineKeyboardButton("Stealth", callback_data=f"combat-{player_class}|steath"),
            types.InlineKeyboardButton("Offense", callback_data=f"combat-{player_class}|offense"),
            types.InlineKeyboardButton("Defense", callback_data=f"combat-{player_class}|defense"),
            types.InlineKeyboardButton("Magic", callback_data=f"combat-{player_class}|mage")
        )
        return markup