# Uno - Bill Seaton - May 2023

# Main features in the readme
# Switching from curses to colorama, as it is a bit too advanced/ hopefully uneeded functionality

# TODO: Make class structure for Player, Cards, Deck and Game Manager
import json
import random
import curses   

    
# init value changes the type of card (0-9 are normal, 10 - skip, 11 - Reverse, 12 - +2, 13 - +4 wild, 14 - wild)
class Card:
    
    def __init__(self,value,color):
        self.value = value
        self.color = color
    
    def printCard(self):
        print(f'I am a {self.color} colored {self.value} card')

# Holds all 108 cards or whatever it is
class Deck:
    colors = ["blue","yellow","red","green"]
    
    def __init__(self):
        self.cards = []
        for color in self.colors:
            self.cards.append(Card(0,color))
            for i in range(2):  # for each color type (blue,yellow,red,green)
                for j in range(1,10):  # 0-9
                    self.cards.append(Card(j,color))
                self.cards.append(Card("Reverse",color))
                self.cards.append(Card("Skip",color))
                self.cards.append(Card("+2",color))
            self.cards.append(Card("wild","black"))
            self.cards.append(Card("+4","black"))
        self.cards.sort(reverse=True,key=lambda Card: Card.color)

    def Shuffle(self):
        random.shuffle(self.cards)


    def printCards(self):
        for card in self.cards:
            card.printCard()
    
    def printDeckSize(self):
        print(len(self.cards))


# Has an AI setting so it can be used as a CPU Opponent
class Player:
    
    def __init__(self,name,type="CPU"):
        self.name = name
        self.type = type #CPU or Player

class GameManager:
    
    # This will apply any settings on initialization, which will occur before a game starts in a main menu. (for now we will use a settings.txt). The data collected there will be used to create a GameManager that applies the settings given in the inital setup stage.

    def __init__(self,*args):
        self.Deck = Deck()
        # Default Values
        self.playercount = 4
        self.Timer = 60
        self.TurnCount = 0  # 0 = infinite
        self.players = []
        # If a settings json is present, then it will use those values instead
        for arg in args:
            self.playercount = arg['Players']
            self.Timer = arg['Timer']
            self.TurnCount = 0  # 0 = infinite
            for i in range(self.playercount):
                name = arg['CPUNAMES'][random.randint(0,len(arg['CPUNAMES'])-1)]
                if name in self.players:
                    name = arg['CPUNAMES'][random.randint(0,len(arg['CPUNAMES'])-1)] # Re roll name
                self.players.append(Player(name))
        if len(self.players) == 0:
            for i in range(self.playercount):
                self.players.append(Player(input(f"please give us player {i}'s name")))
        
        print([player.name for player in self.players])



if __name__ == "__main__":
    with open('Settings.json','r') as settings:
        settingArgs = []
        settingsJson = json.load(settings)


    GM = GameManager(settingsJson)
    #GM.Deck.printCards()
    GM.Deck.Shuffle()
    GM.Deck.printCards()
    GM.Deck.printDeckSize()


