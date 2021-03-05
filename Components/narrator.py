class Narrator():
    def __init__(self):
        self.start = "Ah... hello there? Rude of you to just barge in out of nowhere. What's that? You want to start an adventure?"
        self.start_yes = "Haha what a wierd fellow, asking for an adventure on a social media app, what the world has come to huh.\nAnyways, tell me a little about yourself?"
        self.start_no = "Sigh, barging and disturbing my peace, kids these days"

    @staticmethod
    def class_select(player_class):
        if player_class == "human":
            return "Ah a human, a simple being, but quite powerful when brough together.\nBut how would you handle a fight on your own?"
        elif player_class == "dwarf":
            return "Interesting, a dwarf you say? Now that you mention it, you are pretty short haha.\nWell tell me, how does a mighty dwarf handle a fight"
        elif player_class == "elf":
            return "Hmmmm an elf? Haven't met one in a while. Hmmmm I wonder, how would you handle a battle"

    @staticmethod
    def combat_select(player_class, player_combat):
        if player_class == "human":
            if player_combat == "stealth":
                return "Hmhm humans can be quite sneaky in nature"
            elif player_combat == "offense":
                return "Haha a brave one, or is this pretend?"
            elif player_combat == "defense":
                return "Hohoho a human that wants to tank hits? My, how daring you are"
            elif player_combat == "magic":
                return "Ahhh Ya a wizard Harry! Hahaha"
        elif player_class == "dwarf": 
            if player_combat == "stealth":
                return "A stealthy dwarf you say? I mean with that height you might be onto something"
            elif player_combat == "offense":
                return "Aye hopefully ya legs can carry you to the frontlines on time"
            elif player_combat == "defense":
                return "Ahhh quite dense you are for someone so small huh"
            elif player_combat == "magic":
                return "A dwarf using magic? Not at all familiar with that"
        elif player_class == "elf":
            if player_combat == "stealth":
                return "Haha I barely noticed walk in here, you elven people freak me out sometimes"
            elif player_combat == "offense":
                return "Ahhh a brave one, maybe you have got something special in you"
            elif player_combat == "defense":
                return "Hmmm? An elf that is taking it slow and heavy? Well ok"
            elif player_combat == "magic":
                return "Ahh I have know elves mages, they can be quite terrifying honestly"