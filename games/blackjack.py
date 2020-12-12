import discord
import os
import random as r
from games.Game import Game

class Blackjack(Game):
    
    def __init__(self):
        self.deck = [] 

    def welcome(self):
        border = '='*20
        s = 'Welcome to Blackjack by Kanin\nPlease use the respective tutorial command if you wish to learn how to play.'
        return f'{border}\n{s}\n{border}\n'

    #loads in cards to self.deck and then shuffles
    def resetDeck(self):
        self.deck.clear()
        types = {'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'}
        for kind in types: #add 13 of each card
            for i in range(4):
                self.deck.append(kind)
        for i in range(200): #shuffle
            spot = r.randint(0,51) #randomly swap cards
            spot2 = r.randint(0,51)
            self.deck[spot], self.deck[spot2] = self.deck[spot2], self.deck[spot]
            
    #returns a list where the elements are strings that make the shape of a card with the value in the middle
    def card(self, value):
        top = '-----------'
        side = '|         |'
        center = f'|    {value}    |'
        if len(center) > 11:
            center = center.replace(' ', '', 1)
        return [top,side,side,center,side,side,top]

    #append new cards horizontally to 'card1', returns a list of parts
    def displayAppend(self, card1, card2):
        for i in range(7):
            card1[i] += f'   {card2[i]}'
        return card1

    #build the parts into a display to send to a discord channel
    def printCards(self, card1, card2):
        set1 = set2 = ''
        for i in range(7):
            set1 += card1[i]+'\n'
            set2 += card2[i]+'\n'
        return f'**=== Dealer Cards ===**\n```{set1}```**=== Your Cards ===**\n```{set2}```'

    #calculate total value of cards
    def getValue(self, cardSet):
        total = 0
        numAces = 0
        for card in cardSet:
            if card == 'J' or card == 'Q' or card == 'K':
                total += 10
            elif card == 'A':
                numAces += 1
            else:
                total += int(card)
        if numAces >= 2:
            total += 1*numAces
        elif numAces == 1:
            if total+11<=21:
                total += 11
            else:
                total+=1
        return total

    #draw new card, add it to the card set and update display
    def hit(self, cardSet, cardSetDisplay):
        cardSet.append(self.deck.pop()) 
        return cardSet, self.displayAppend(cardSetDisplay, self.card(cardSet[-1]))

    #determine who wins as a string based on totals
    def win(self, pv, dv):
        winner = 0 # 0 = tie ; 1 = player ; 2 = dealer
        result = ''
        if pv == dv:
            result = '**PUSH**'
        elif pv <= 21:
            if dv < pv or dv>21:
                result = '**YOU WIN**'
                winner = 1
            else:
                result = '**DEALER WINS**'
                winner = 2
        else:
            result = '**DEALER WINS**'
            winner = 2
        return winner, f'{result} Your Total: {pv} / Dealer Total: {dv}'

    #main runner
    async def play(self, pysino, bot):
        error = True
        while error: #Initial Bet
            await bot.channel.send(f'{bot.author.mention}, how much would you like to bet?')
            response = await pysino.wait_for('message', check=lambda message: message.author == bot.author)
            try: 
                bet = int(response.content)
                if bet > 0:
                    await bot.channel.send(f'{bot.author.mention}, you have successfully bet **${bet}**.')
                    break
                else:
                    raise Exception
            except:
                await bot.channel.send(f'{bot.author.mention}, unfortunately your input was invalid. Please try again.')
        #Load Deck
        self.resetDeck()
        #Draw Cards
        playerCards = [self.deck.pop(), self.deck.pop()]
        dealerCards = [self.deck.pop(), self.deck.pop()]
        #Card Displays
        playerCardsDisplay = self.displayAppend(self.card(playerCards[0]), self.card(playerCards[1]))
        dealerCardsDisplay = self.displayAppend(self.card(dealerCards[0]), self.card(dealerCards[1]))
        dealerCardsHidden = self.displayAppend(self.card(dealerCards[0]), self.card('?'))
        #Check BlackJack
        if self.getValue(playerCards) == 21:
            await bot.channel.send(self.printCards(dealerCardsDisplay, playerCardsDisplay))
            await bot.channel.send(f'{bot.author.mention}, ***BLACKJACK*** - You have just won **${bet*2}**')
        elif self.getValue(dealerCards) == 21:
            await bot.channel.send(self.printCards(dealerCardsDisplay, playerCardsDisplay))
            await bot.channel.send(f'{bot.author.mention}, ***DEALER BLACKJACK*** - You have just lost your bet of **${bet}**')
        else: #Player Plays
            choice = 3 
            while self.getValue(playerCards)<21 and choice!=1: #choice == 1 means stand
                if choice == 0: #Hit
                    playerCards, playerCardsDisplay = self.hit(playerCards, playerCardsDisplay)
                    if self.getValue(playerCards)>=21:
                        break
                elif choice == 2: #x2
                    bet*=2
                    playerCards, playerCardsDisplay = self.hit(playerCards, playerCardsDisplay)
                    break
                await bot.channel.send(self.printCards(dealerCardsHidden, playerCardsDisplay)) #display cards
                await bot.channel.send(f':zero: - **HIT**\n:one: - **STAND**\n:two: - **x2**\n\n\n**Select an Action:**') #display actions
                error = True
                lim = 3
                while error: #wait for action
                    try:
                        sel = await pysino.wait_for('message', check=lambda message: message.author == bot.author)
                        choice = int(sel.content.strip())
                        error = choice > 3 or choice < 0
                        if error:
                            raise Exception
                    except:
                        await bot.channel.send(f'{bot.author.mention}, Invalid Input. Please try again.')
                        lim+=2 #2 for error message and input
                await bot.channel.purge(limit=lim)
            #Dealer Plays
            while self.getValue(dealerCards)<21 and self.getValue(playerCards)<21:
                chance2Stand = r.randint(0,21-self.getValue(dealerCards))
                if chance2Stand > 2:
                    dealerCards, dealerCardsDisplay = self.hit(dealerCards, dealerCardsDisplay)
                else:
                    break
            await bot.channel.send(self.printCards(dealerCardsDisplay, playerCardsDisplay)) #print end-card results
            winner, winScreen = self.win(self.getValue(playerCards), self.getValue(dealerCards))
            if winner == 1:
                betResult = f'{bot.author.mention}, you have just won your bet of: **${bet}**'
            elif winner == 2:
                betResult = f'{bot.author.mention}, you have just lost your bet of: **${bet}**'
            else:
                betResult = f'{bot.author.mention}, as this was a tie, you keep your bet of: **${bet}**'
            await bot.channel.send(f'{winScreen}\n{betResult}') #determine who wins
            self.handleBalance()