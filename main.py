# Uno - Bill Seaton - May 2023

# Main features in the readme
# TODO: 16/5/23 
#               //Cancelled//
#               - game end (could use a ranking page before match closes out)
#               - Create random CPU players
#       //Refactoring//
#       - Make each method more readable e.g. make obtuse things into one liners, or saved as variables
#       - Make some logic easier to get through (atm its just whatever I slapped together)
#       - Put independant things into functions (perhaps )
# 
# //Cancelled// - I hate making this so I'm not doing this
# Extended milestones: 
# If adding time works out fine, look into p2p or maybe host a linux server with players who can connect in terminal with uno

import json
import random
import time
import sys
import os
import colorama

UniqueCards = ["Reverse","Skip","+2","+4","wild"]

    
# Values and colors are created from the decks init
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

# Holds all 108 cards
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
        return li

    def Shuffle(self):
        random.shuffle(self.cards)

    # Return the top level Card
    def Draw(self):
        return self.cards.pop()

class Player:
    
    def __init__(self,name):
        self.name = name    # Name
        self.hand = []      # cards held
        self.UNO = False    # if true, they think they have a winning hand

class GameManager:

    # /_____________________________/SETUP/_____________________________/
    
    # This will apply any settings on initialization, which will occur before a game starts in a main menu. (for now we will use a settings.json). The data collected there will be used to create a GameManager that applies the settings given in the inital setup stage.
    def __init__(self,*args):
        
        colorama.init(autoreset=True)   # resets all colorama calls after use

        # Decks
        self.Deck = Deck()
        self.Discard = Deck(discard=True)

        # Turn Movement
        self.Clockwise = True   # Direction of gameplay
        self.playerIndex = 0    # How we pick player after each turn
        self.DrawStack = 0      # +2/+4 for next player to draw
        self.SkipStack = 0      # +1 for each skip
        # Dynamic Values
        self.LastTurn = None    # The display message of the last turn taken in format : Last turn: 'player' played 'Card'
        self.drawstate = False  # initiates the draw turn

        # Default Values
        self.playercount = 4
        self.TurnCount = 0  # if 0 = infinite, else -1 per turn
        # self.Turns = 1  # if 0 = infinite, else -1 per turn

        self.players = []
        self.CardCount = 7

        # If a settings json is present, then it will use those values instead
        try:
            for arg in args:
                self.playercount = arg['Players']
                self.TurnCount = 0  # 0 = infinite
                
                for i in range(self.playercount):
                    name = arg['CPUNAMES'][random.randint(0,len(arg['CPUNAMES'])-1)]
                    while name in self.players: # ensures random playercount
                        name = arg['CPUNAMES'][random.randint(0,len(arg['CPUNAMES'])-1)] # Re roll name
                    self.players.append(Player(name))
        except:
            print('No settings file')
        if len(self.players) == 0:
            for i in range(self.playercount):
                self.players.append(Player(input(f"please give us player {i}'s name: ")))
    
    # Distibute cards to players
    def GameSetup(self):
        for i in range(self.CardCount): # distribute starting hand
            for player in self.players: # for each player
                player.hand.append(self.Deck.Draw())
        
        # place the 1st discard card
        self.Discard.cards.append(self.Deck.Draw())

        if self.Discard.GetTopCard().color == 'black':
            self.Discard.GetTopCard().color = random.choice(["blue","yellow","red","green"])
            self.Discard.GetTopCard().colorama = self.Discard.GetTopCard().SetColorama(self.Discard.GetTopCard().color)
        
        # Unique Cards = ["Reverse","Skip","+2","+4","wild"]
        if self.Discard.GetTopCard().value == "Reverse":
            self.Clockwise = not self.Clockwise
        if self.Discard.GetTopCard().value == "Skip":
            self.playerIndex +=1
        if self.Discard.GetTopCard().value == "+2":
            self.drawstate = True
            self.DrawStack += 2
        if self.Discard.GetTopCard().value == "+4":
            self.drawstate = True
            self.DrawStack += 4

    # /_____________________________/TURNS/_____________________________/

    # Draw class variables - Turn counter, Time
    def DrawGlobals(self):
        print(f'Turn: {self.TurnCount+1}')
        
    def DrawOpponents(self,Player):
        for i,player in enumerate(self.players):
            if player == Player: continue   # skip current player
            endstring = f'{i+1}//{player.name}: |{len(player.hand)}|'
            if player.UNO: endstring += ' UNO! '
            print(endstring)
        
    def DrawHand(self,Player):
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
        self.Discard.cards = [topCard,] # new discard pile of single card

    def DrawCards(self,Player,drawNo):
        if len(self.Deck.cards) <= drawNo:  # make sure there are always cards to draw
            self.ShuffleDraw()
        for i in range(drawNo):   # Draw no given at method call
            Player.hand.append(self.Deck.Draw())
    
    def SetWild(self,Card):
        if Card.color == "black":   # black cards need to be set colors
            Card.color = self.WildColor()
            Card.colorama = Card.SetColorama(Card.color)
            return True
        return False

    def WildColor(self):
        colors = ["blue","yellow","red","green"]
        newColor = None
        while newColor not in colors:
            # Long but just shows r in red, g in green etc.
            inputColor = input(f"Please input a color ({colorama.Fore.RED}r{colorama.Style.RESET_ALL},{colorama.Fore.GREEN}g{colorama.Style.RESET_ALL},{colorama.Fore.BLUE}b{colorama.Style.RESET_ALL},{colorama.Fore.YELLOW}y{colorama.Style.RESET_ALL}): ").lower()
            
            for color in colors:
                if color[0] == inputColor:
                    newColor = color
        return newColor

    # Check if chosen card is a valid playable card
    # returns True and gets card ready for play if wild 
    def ValidPlay(self,Choice,Player,First=False):

        #10 - skip, 11 - Reverse, 12 - +2, 13 - +4 wild, 14 - wild
        CurrentDiscard = self.Discard.GetTopCard() # get the current top card
        
        # Make sure input is a number
        try:
            Card = Player.hand[int(Choice)-1]
        except (IndexError,ValueError):
            return False

        # if a wild card
        if self.SetWild(Card): return True

        # 1ST CARD
        if First:
            # SAME VALUES
            if Card.value == CurrentDiscard.value or Card.color == CurrentDiscard.color:    # if same value or color
                return True
            
        # multiple cards per turn
        else:   
            # MATCHING CARDS
            if Card.value == CurrentDiscard.value and Card.color == CurrentDiscard.color:
                return True
            # 0-9 CARDS
            if CurrentDiscard.value not in ["Reverse","Skip","+2","+4","wild"]:
                minRange = CurrentDiscard.value-1
                maxRange = CurrentDiscard.value+1
                # Definitely a better way for this
                if minRange < 0: minRange = 0
                if maxRange > 9: maxRange = 0
                matches = [minRange,CurrentDiscard.value,maxRange]
                if Card.value in matches and Card.color == CurrentDiscard.color:
                    return True
                if Card.value == CurrentDiscard.value:
                    return True
            else:
                # UNIQUE CARDS
                if Card.value == CurrentDiscard.value:
                    return True 

    # switch players when ending turn 
    def RotatePlayers(self):
        # Direction (1 liners for easier reading)
        self.playerIndex += 1 if self.Clockwise else -1 \
        # if oob
        if self.playerIndex > self.playercount-1: self.playerIndex = 0 
        if self.playerIndex < 0: self.playerIndex = self.playercount-1 

    def drawTurn(self,Player):
        # while in loop
        while self.drawstate:
            os.system('cls')
            playerValues = [card.value for card in Player.hand]
            if "+2" not in playerValues and "+4" not in playerValues:
                print(f'{Player.name} cannot stack and must draw {self.DrawStack} cards')
                input('Press enter to continue')

                self.DrawCards(Player,self.DrawStack)

                self.drawstate = False
                self.DrawStack = 0
                return
                
            lol = '------------------------'
            print(lol + " DRAW " + lol)

            print(f'Player: {Player.name}')
            
            print(f'Stack Card: {self.Discard.cards[-1].colorama}')
            print(f'Draw Amount: {self.DrawStack}')

            print('------------------------')
            self.DrawHand(Player)
            print('------------------------')
            choice = input('play stack card: [#], or End Turn and draw[E]').upper()

            # stack size is (SHOULD) updated per validplay call
            if choice == 'E':
                print(f"{colorama.Fore.MAGENTA}{Player.name} draws {self.DrawStack} cards{colorama.Style.RESET_ALL}")
                self.DrawCards(Player,self.DrawStack)
                self.drawstate = False
                self.DrawStack = 0
            else:
                try:
                    playerval = Player.hand[int(choice)-1].value
                    if playerval == "+2" or playerval == "+4" :
                        if playerval == "+4":
                            self.SetWild(Player.hand[int(choice)-1])
                        print(playerval[1])
                        self.DrawStack+=int(playerval[1])  # Add value to stack
                        self.Discard.cards.append(Player.hand.pop(int(choice)-1))
                except: # exception for all, because if its not a choice or e wtf???
                    print('invalid choice')
            input('Press enter to continue')
            return

    # Draws, then gets input
    def Turn(self,Player):
        
        # unique instance, so return when finished
        if self.drawstate == True:
            self.drawTurn(Player)
            return
  
        if self.SkipStack > 0:
            self.SkipStack -=1
            return
        
        # only runs if above isnt true
        CardsPlayed = 0

        DrawPlay = False
        SkipPlay = False

        EndTurn = False
        currentUno = False
        


        while not EndTurn:
            os.system('cls')
            self.DrawGlobals()
            print('------------------------')
            self.DrawOpponents(Player)
            print('------------------------')
            print(f'Current Top Card: {self.Discard.cards[-1].colorama}')
            print(f'Cards played: {CardsPlayed}')
            print('------------------------')
            self.DrawHand(Player)
            print('------------------------')
            print('play card: [#],Call uno [UNO!] or End Turn [E]')
            Choice = input('').upper()  # all inputs in upper, so i dont have to worry about case issues

            if Choice == 'Q':
                print('Quitting')
                sys.exit()

            if self.ValidPlay(Choice,Player,CardsPlayed == 0):
                # will only run if card is playble
                choiceVal = str(Player.hand[int(Choice)-1].value)

                # Checks if topcard is played this turn. Don't think this is an elegant solution, but its the easiest                
                DrawPlay = True if "+" in choiceVal else False
                SkipPlay = True if "skip" == choiceVal else False
                    
                self.Discard.cards.append(Player.hand.pop(int(Choice)-1)) # add card to top of discard pile
                CardsPlayed +=1
                continue                
            elif Choice == 'UNO!':
                Player.UNO = True
                currentUno = True
                continue
            # Win Condition
            elif Choice == 'E':
                EndTurn = True
                topcard = self.Discard.GetTopCard().value
                # START DRAW STACK
                try:
                    if "+" in topcard:
                        if DrawPlay:    # needs to check it was played this turn
                            self.drawstate = True
                            # Draw Topvalues
                            if topcard == "+2": self.DrawStack += 2
                            if topcard == "+4": self.DrawStack += 4
                except:
                    pass
                # REVERSE DIRECTION
                if self.Discard.GetTopCard().value == "Reverse":
                    self.Clockwise = not self.Clockwise
                # SKIP NEXT 
                if self.Discard.GetTopCard().value == "Skip" and SkipPlay:
                    self.SkipStack +=1
                
                print('Ending Turn')
                if Player.UNO:
                    if currentUno is False:
                        if len(Player.hand) == 0:
                            print(f'{Player.name} Won :)')
                            input('Press enter to Quit.')
                            sys.exit()
                        else:
                            print('You did not win despite claiming UNO >:(')
                            print(f'{Player.name} Draws 2')
                            self.DrawCards(Player,2)
                            Player.UNO = False
                elif CardsPlayed == 0 or len(Player.hand) == 0:
                    Player.hand.append(self.Deck.Draw())
            else:
                print('Invalid Choice')
                # resets uno 
                if Player.UNO and currentUno is False:
                    Player.UNO = False
                self.DrawCards(Player,2)
                EndTurn = True

            
            time.sleep(1)
    
    # turn loop
    def GameLoop(self):
        
        self.GameSetup()    # gets stuff ready 2 game

        Gaming = True
        while Gaming:
            input(f'Press enter for {self.players[self.playerIndex].name} to begin')            
            self.Turn(self.players[self.playerIndex])
            self.RotatePlayers()
            self.TurnCount +=1
            os.system('cls')
            

if __name__ == "__main__":
    with open('Settings.json','r') as settings:
        settingArgs = []
        settingsJson = json.load(settings)
    # Give the GM the data stored in settings.json
    GM = GameManager(settingsJson)
    GM.GameLoop()