# Python teminal Uno

updated 17/5/2023 

## Outline

This is just basic uno using the colorama module for some basic sprucing up of the temrinal. This is local play only

Blog post explaining code:
https://medium.com/@billseaton19/things-are-harder-than-you-think-91ed35de7e53

### Uno Features

    - A deck containing:
      - Cards 1-9 for each color (red,yellow,green,blue) x2
      
      - Skip next turn for each color x2
      - reverse for each color x2
      - +2 Draw for each color x2

      - 0 Card for each color x1      
      - 4 Wild cards (can be placed on anything and changes the color)
      - 4 Draw four cards - The same as wild, but makes next player draw 4
    
    - Turn Counter
    - Colored terminal for cards using colorama
    - Card stacking
      - Blue 5 can have any other 5 played on top, or a blue 4/6

### The Deck Visualsed

<image src="README\Uno_Card.jpg" width=500>

### Classes



- Deck - will hold all instances of the cards that get drawn, with the methods:
  - Draw: Draw a card from its big array of Card class cards
  - Shuffle: when all the cards have been drawn into a place Pile (probably stored in the Game Manager), it will collect all the cards back (except the last played card)
- Cards ~~(will probably use inheritance for each type of card)~~. Game manager will handle thier actual logic. Each card will hold:
  - Value (0-9,reverse,skip,+2,wild,+4)
- Game manager - Will handle main game logic, such as:
  - Player Turns
  - Checking turn count
  - Displaying status messages
  - Switching between Menu and Game
  - Displaying the information in a nice way
- Player ~~/AI - If Ai, will automatically play turns (could get complicated, so will probably opt for random but legal moves).~~
  - Hold a Hand of drawn cards stored in a list
  - Status effect attribute (such as skip a go, or draw) ~~so the AI knows if it needs to +2. This will allow it to stack if the setting is used.~~

### Actual Uno Rules

from [unorules.com](https://www.unorules.com/):

- 1: Random player is chosen to start (usually left of dealer)
- 2: When the game starts:
  - All players draw 5 or 7 cards (A changeable setting)
  - A card is placed from the draw pile onto the discard pile (If an action card, its effect applies e.g. +2 makes the next player draw 2)
- 3: Each player tries to Match the card in a discard Pile, by:
  - Number
  - Color
  - Action/symbol
- 4: Player Draws 1 if they have no playable cards. If the drawn card is playable, they must use it immidiately. If an action card, its effect applies (e.g. +2 makes the next player draw 2)
- 5: Stacking is not allowed, but this will be a changable setting (stacking is fun). This means no +2, then someone putting another +2 ontop to make +4 for the next player. This results in big chains where it can reach +10 or higher
- 6: Players with 1 card, or a winning play must type **"UNO!"**. if they do not, and make a winning play, they draw 2 cards. This will be enforced by making players type what commands they want to carry out. If they do this, and dont win next turn they will also be drawing 2 (makes it more interesting IMO)
- 7: When a player wins, they get a point value based on the cards in other players hands, with each card making:
  - Numbered cards (0-9) – Face value
  - Draw Two/Skip/Reverse – 20 points each
  - Wild/Wild Draw Four – 50 points each
  - Wild Swap Hands/Wild Customizable cards – 40 points each
These point values will be tracked per player, and a winner is declared at a winning point value (default is 500)

# Random Stuff

CPU Names were taken from: From https://www.keeplaughingforever.com/deez-nuts-jokes