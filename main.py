# Uno - Bill Seaton - May 2023

# Main features in the readme
# TODO: Make class structure for Player, Cards, Deck and Game Manager

# Holds all 108 cards or whatever it is
class Deck:
    pass

class CardTemplate:
    
    def __init__(self,value,color):
        self.value = value
        self.color = color
    
    def printCard(self):
        print(f'I am a {self.color} colored {self.value} card')
    
# init value changes the type of card (0-9 are normal, 10 - skip, 11 - Reverse, 12 - +2, 13 - +4 wild, 14 - wild)
class Card:
    pass

# Has an AI setting so it can be used as a CPU Opponent
class Player:
    pass

class GameManager:
    pass
