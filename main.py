# Uno - Bill Seaton - May 2023

# Main features in the readme
# Switching from curses to colorama, as it is a bit too advanced/ hopefully uneeded functionality

# TODO: Make class structure for Player, Cards, Deck and Game Manager
import json
import random
import time
import sys
import os
#import curses   
import colorama

    
# init value changes the type of card (0-9 are normal, 10 - skip, 11 - Reverse, 12 - +2, 13 - +4 wild, 14 - wild)
class Card:
    
    def __init__(self,value,color):
        self.value = value
        self.color = color
        self.colorama = None
        match color:
            case "blue":
                self.colorama = colorama.Fore.BLUE + f'{value}'
            case "yellow":
                self.colorama = colorama.Fore.YELLOW + f'{value}'
            case "red":
                self.colorama = colorama.Fore.RED + f'{value}'
            case "green":
                self.colorama = colorama.Fore.GREEN + f'{value}'
            case "black":
                self.colorama = f'{value}'
            
    
    def printCard(self):
        print(f'I am a {self.color} colored {self.value} card')


# Holds all 108 cards or whatever it is
class Deck:
    colors = ["blue","yellow","red","green"]
    
    def __init__(self,discard=False):
        if not discard:
            self.cards = Deck.GenerateDeck() # 920 bits total - 48 per cardish
            self.Shuffle()
        else:
            self.cards = [] # empty discard pile

        
    def GenerateDeck():
        li = []
        for color in Deck.colors:   
            li.append(Card(0,color))
            for i in range(2):  # for each color type (blue,yellow,red,green)
                for j in range(1,10):  # 0-9
                    li.append(Card(j,color))
                li.append(Card("Reverse",color))
                li.append(Card("Skip",color))
                li.append(Card("+2",color))
            li.append(Card("wild","black"))
            li.append(Card("+4","black"))
        #li.sort(reverse=True,key=lambda Card: Card.color)
        return li

    def Shuffle(self):
        random.shuffle(self.cards)

    def printCards(self):
        for card in self.cards:
            card.printCard()
    
    def printDeckSize(self):
        print(len(self.cards))

    # Return the top level Card
    def Draw(self):
        returncard = self.cards.pop()
        print(f'drew {returncard.value}')
        return returncard

# Has an AI setting so it can be used as a CPU Opponent
class Player:
    
    def __init__(self,name,type="CPU"):
        self.name = name
        self.type = type # CPU or Player - Used to automate CPU gameplay by GM
        self.hand = []  # cards held
        self.UNO = False    # if true, they think they have a winning hand

class GameManager:
    
    # This will apply any settings on initialization, which will occur before a game starts in a main menu. (for now we will use a settings.txt). The data collected there will be used to create a GameManager that applies the settings given in the inital setup stage.

    def __init__(self,*args):
        
        colorama.init(autoreset=True)


        self.Deck = Deck()
        self.Discard = Deck(discard=True)
        
        # Dynamic Values
        self.LastTurn = None    # The display message of the last turn taken in format : Last turn: 'player' played 'Card'

        # Default Values
        self.playercount = 4
        self.Timer = 60
        self.TurnCount = 0  # if 0 = infinite, else -1 per turn
        self.Turns = 1  # if 0 = infinite, else -1 per turn

        self.players = []
        self.CardCount = 7

        
        # If a settings json is present, then it will use those values instead
        try:
            for arg in args:
                self.playercount = arg['Players']
                self.Timer = arg['Timer']
                self.TurnCount = 0  # 0 = infinite
                
                for i in range(self.playercount):
                    name = arg['CPUNAMES'][random.randint(0,len(arg['CPUNAMES'])-1)]
                    if name in self.players:
                        name = arg['CPUNAMES'][random.randint(0,len(arg['CPUNAMES'])-1)] # Re roll name
                    self.players.append(Player(name))
        except:
            print('No settings file')
        if len(self.players) == 0:
            for i in range(self.playercount):
                self.players.append(Player(input(f"please give us player {i}'s name")))
        print([player.name for player in self.players])
    
    # Distibute cards to players
    def GameSetup(self):
        for i in range(self.CardCount): # distribute starting hand
            for player in self.players: # for each player
                player.hand.append(self.Deck.Draw())
        # place the 1st discard card
        self.Discard.cards.append(self.Deck.Draw())

        # print(f'Discard top = {self.Discard.cards[0].value}')        
        # for player in self.players:
        #     print(f'{player.name} has:')
        #     print([card.value for card in player.hand])

    # Draw class variables - Turn counter, Time
    def DrawGlobals(self):
        print(f'Turn #:{self.TurnCount}')
        print(f'Time Left: {int(time.time())}')
        
    def DrawOpponents(self,Player):
        for player in self.players:
            if player == Player: continue   # skip current player
            endstring = f'{player.name}: |{len(player.hand)}|'
            if player.UNO: endstring += ' UNO! '
            print(endstring)
        
    def DrawHand(self,Player):
        finalString = ''
        for i,card in enumerate(Player.hand):
            print(card.colorama,f'[{i+1}]')
            colorama.Fore.RESET
            colorama.Back.RESET


    def Turn(self,Player):
        os.system('cls')
        self.DrawGlobals()
        print('------------------------')
        self.DrawOpponents(Player)
        print('------------------------')
        self.DrawHand(Player)


            

    # turns
    def GameLoop():
        pass



if __name__ == "__main__":
    with open('Settings.json','r') as settings:
        settingArgs = []
        settingsJson = json.load(settings)


    GM = GameManager(settingsJson)
    GM.GameSetup()
    #GM.players[1].UNO = True
    GM.Turn(GM.players[0])