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
        self.colorama = self.SetColorama(color)
        
    
    def SetColorama(self,color):
        returnColorama = None
        match color:
            case "blue":
                returnColorama = colorama.Fore.BLUE + f'{self.value}'
            case "yellow":
                returnColorama = colorama.Fore.YELLOW + f'{self.value}'
            case "red":
                returnColorama = colorama.Fore.RED + f'{self.value}'
            case "green":
                returnColorama = colorama.Fore.GREEN + f'{self.value}'
            case "black":
                returnColorama = f'{self.value}'
        return returnColorama
    
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

    def GetTopCard(self):
        return self.cards[-1]
    
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
        self.name = name    # Name
        self.type = type    # CPU or Player - Used to automate CPU gameplay by GM
        self.hand = []      # cards held
        self.UNO = False    # if true, they think they have a winning hand

class GameManager:
    
    # This will apply any settings on initialization, which will occur before a game starts in a main menu. (for now we will use a settings.json). The data collected there will be used to create a GameManager that applies the settings given in the inital setup stage.

    # /_____________________________/SETUP/_____________________________/


    def __init__(self,*args):
        
        colorama.init(autoreset=True)

        # Decks
        self.Deck = Deck()
        self.Discard = Deck(discard=True)

        # Turn Movement
        self.Clockwise = True   # Direction of gameplay
        self.playerIndex = 0    # How we pick player after each turn
        self.DrawStack = 0      # +2/+4 for next player to draw

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
            


    # /_____________________________/TURNS/_____________________________/

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


    # if draw pile is empty, move discard pile into draw pile execpt the top and shuffle draw
    def ShuffleDraw(self):
        topCard = self.Discard.cards.pop(-1)    # remove top card and append rest
        for card in self.Discard.cards:
            self.Deck.cards.append(card)
        self.Deck.Shuffle()
        print(self.Deck.cards)
        self.Discard.cards = [topCard,] #new discard pile of single card

    def DrawCards(self,Player,drawNo):
        if len(self.Deck.cards) <= drawNo:
            self.ShuffleDraw()
        for i in range(drawNo+1):   # +1 so it draws correct (goes up to, but not including using range)
            Player.hand.append(self.Deck.Draw())
            
    def WildColor(self,color):
        colors = ["blue","yellow","red","green"]
        newColor = None
        while newColor not in colors:
            inputColor = input(f"Please input a color ({colorama.Fore.RED}r{colorama.Style.RESET_ALL},{colorama.Fore.GREEN}g{colorama.Style.RESET_ALL},{colorama.Fore.BLUE}b{colorama.Style.RESET_ALL},{colorama.Fore.YELLOW}y{colorama.Style.RESET_ALL}): ").lower()
            for color in colors:
                if color[0] == inputColor:
                    newColor = color
        return newColor

    # Check if chosen card is a valid playable card
    # returns True and gets card ready for play if wild 
    def ValidPlay(self,Choice,Player):
        
        #10 - skip, 11 - Reverse, 12 - +2, 13 - +4 wild, 14 - wild
        try:
            print(f'Played Card: {int(Choice)}')
            Card = Player.hand[int(Choice)-1]
            CurrentDiscard = self.Discard.GetTopCard()
            # If none of these go through, return false for bad choice

            #print(Card.value)
            #print(CurrentDiscard.value)

            # if matching Play and return
            if Card.value == CurrentDiscard.value or Card.color == CurrentDiscard.color:
                return True
            
            if Card.color == "black":
                # in both cases set color
                Card.color = self.WildColor(Card)
                print(f'New color: {Card.color}')
                Card.colorama = Card.SetColorama(Card.color)
                return True

            discardValue = CurrentDiscard.value
            
            p1 = discardValue+1
            m1 = discardValue-1
            # if values not in 0-9 range, then loop around to start/end
            # Wanted to use lambdas but seems to not use conditionals
            if p1 >= 10:
                p1 = 0
            if m1 <= -1:
                m1 = 9

            if Card.value == p1 or Card.value == m1:
                if Card.color == CurrentDiscard.color:
                    return True

            if Card.color == CurrentDiscard.color:
                # skip next, checked in turn start
                if Card.value == "Skip":
                    return True
                # Reverse play order
                if Card.value == "Reverse":
                    self.Clockwise = not self.Clockwise
                    return True
                # +2 next, checked in turn start
                if Card.value == "+2":
                    return True

            else:
                return False

        except ValueError:
            return False

    # switch players when ending turn 
    def RotatePlayers(self):
        pass

    # Draws, then gets input
    def Turn(self,Player):
        CardsPlayed = 0
        if self.TurnCount == 1 and self.Discard.cards[0].color == "black":
            self.Discard.cards[0].color = self.WildColor(Card)
        validChoice = False
        #Player.UNO = True
        while not validChoice:
            os.system('cls')
            self.DrawGlobals()
            print('------------------------')
            self.DrawOpponents(Player)
            print('------------------------')
            print(f'Current Top Card: {self.Discard.cards[-1].colorama}')
            print('------------------------')
            self.DrawHand(Player)
            print('------------------------')
            print('play card: [#],Call uno [UNO!] or End Turn [E]')
            Choice = input('').upper()  # all inputs in upper, so i dont have to worry about case issues

            if self.ValidPlay(Choice,Player):
                # will only run if card is playble
                print('Card was played')

                self.Discard.cards.append(Player.hand.pop(int(Choice)-1)) # add card to top of discard pileq
                
                validChoice = True
            elif Choice == 'UNO!':
                Player.UNO = True
                validChoice = True
            # Win Condition
            elif Choice == 'E':
                validChoice = True
                print('Ending Turn')
                if Player.UNO:
                    if len(Player.hand) == 0:
                        print(f'{Player.name} Won :)')
                        
                        #TODO
                        #self.WinningPoints()
                    else:
                        print('You did not win despite claiming UNO >:(')
                        print(f'{Player.name} Draws 2')
                        self.DrawCards(Player,2)
            else:
                print('Invalid Choice')
                self.DrawCards(Player,2)

            if Choice == 'Q':
                sys.exit()

            validChoice = False
            time.sleep(1)            
    # turns
    def GameLoop():
        pass



if __name__ == "__main__":
    with open('Settings.json','r') as settings:
        settingArgs = []
        settingsJson = json.load(settings)


    GM = GameManager(settingsJson)
    GM.GameSetup()
    GM.players[1].UNO = True
    GM.Turn(GM.players[0])