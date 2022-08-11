# Version 1: Console-based

# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 13:27:55 2022

@author: SO-PC
"""

# Card credit:
    # https://superdevresources.com/free-playing-cards-set/

# Clear variables
from IPython import get_ipython
get_ipython().magic('reset -sf')

import numpy as np
import pandas as pd
from numpy.random import default_rng
rng = default_rng()




   

def buildDeck():
    # Build deck card types here
    cardRanks = np.array(['2' , '3' ,'4' ,'5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace'])
    cardSuits = np.array(['Spade', 'Heart', 'Club', 'Diamond'])
    #cardNums = np.array(['02' , '03' ,'04' ,'05', '06', '07', '08', '09', '10', '11', '12', '13', '14']) # Relative rank, makes everything easier later
    cardNums = np.arange(2,15, dtype='int') # Relative rank, makes everything easier later
    cardInDeck = np.ones(52, dtype='bool')
    
    # Contingent on build deck
    nSuits = cardSuits.size
    nRanks = cardRanks.size
    #nCards = nSuits * nRanks
    #cardRankValues = np.arange(14)
    
    # Build deck
    allSuits = np.tile(cardSuits, nRanks) # SHCD,SHCD,SHCD...
    allRanks = np.repeat(cardRanks, nSuits) # 2 3 4...QKA,234...QKA
    allRankNums = np.repeat(cardNums, nSuits) # 2 3 4...12 13 14
    allCards = np.array([allRanks, allSuits, allRankNums, cardInDeck])
    dictCols = {'Rank': allRanks, 'Suits': allSuits, 'nRank': allRankNums, 'cardInDeck': cardInDeck}
    
    df = pd.DataFrame(data=dictCols)
    return df

def shuffleDeck(inDeck):
    # Shuffle entire deck and make sure all cards are "in" deck
    inDeck['cardInDeck'] = 1 # Reset all to unused
    return inDeck.reindex(rng.permutation(inDeck.index), axis=0)


def deal(deck, nCards):
    # Deal out cards from available
    
    # Draw top n cards
    numCardsUnused = np.shape(deck)[0] # Total number of cards, 52 
    
    ### Get indices
    
    deck.iloc[0:nCards, 3] = 0 # Mark the cards as 'used'
    newCards = deck.iloc[0:nCards] # Draw hand
    deck = deck.sort_values(by = 'cardInDeck', ascending = 0)
    
    return deck, newCards
    
'''
    cardsUsed = np.sum(deck['cardInDeck']==0) # Cards marked used
    nUsed = deck['cardInDeck']
    # Sort 0 to end at end
    
    # Draw cards
    drawnIdx = rng.permutation(deck.shape[0])[0:nCards] # Randomize all cards, get first 5
    drawnCards = deck.iloc[drawnIdx,:] # Draw the actual cards
    deck.drop(drawnIdx, inplace=True) # Remove taken cards, inplace ensures they stay out
    
    return drawnCards#.squeeze()#, deck # Remove extraneous dimension
    '''
def nameCard(card):
    # Output string with formatted card name
    nameTuple = (card[0], ' of ', card[1], 's')
    nameStr = ''.join(nameTuple)
    print(nameStr)
    return nameStr
        

def sortCards(hand):
    # Get the sorted order of cards, this is called in other functions only 
    hand = hand.sort_values(by = 'nRank', ascending = 0)
    # = hand[:, np.argsort(hand[2])]
    return hand
  
def checkHand(hand):
    # Check hand for winning combinations

    # Need to sort first
    sortedHand = sortCards(hand.copy()) # Avoid changing actual order?

   # Check
    #nCards = sortedHand.shape[0]
    #nProps = sortedHand.shape[1] # Should be 4 regardless
    
    
    #ranks = sortHand[0,:]
    #suits = sortHand[1,:]
    relRanks = sortedHand['nRank'].astype(int)
    uRank, uRankCount = np.unique(sortedHand['Rank'], return_counts=True)
    uSuits = np.unique(sortedHand['Suits'])
    
    #firstHalf = np.where(ranks==uRank[0])[0]
    #secondHalf = np.where(ranks==uRank[1])[0]
    
    
        # ORDER
        # royal flush, straight flush, 4 of a kind, full house ...
        # flush, straight, 3 of a kind, 2 pair, 1 pair
        
        # LEFT
        
        # 3 of a kind, 2 pair, 1 pair
    retWin = ''
    if len(uSuits) == 1:
        if np.sum(sortedHand['Rank'] == ['Ace','King','Queen','Jack','10']) == 5:
            # Royal flush
            retWin = 'Royal Flush'
        elif np.equal(abs(np.sum(np.diff(relRanks))), 4):
            #Straight flush, excluded by RF because no fallthrough
            retWin = 'Straight Flush'
        else:
            # Flush
            retWin = 'Flush'
    elif len(uRank) == 2:
        # Split the deckat 2/3 or 3/2 depending
        firstHalf = np.where(sortedHand['Rank']==uRank[0])[0]
        secondHalf = np.where(sortedHand['Rank']==uRank[1])[0]
        if np.logical_or(len(firstHalf) == 2, len(secondHalf) == 2):
            retWin = 'Full House'
        elif np.logical_or(len(firstHalf) == 4, len(secondHalf) ==4):
            retWin = 'Four of a kind'
    elif np.all(np.diff(np.diff(relRanks))==0):
    #elif abs(np.sum(np.diff(relRanks))) == 4:
        retWin = 'Straight'
    elif len(uRank) == 3:
        if np.max(uRankCount) == 3:
            retWin = '3 of a kind'
        elif np.max(uRankCount) == 2:
            retWin = '2 pairs'
       
    
    elif len(uRank) == 4:
        # Pair
        retWin = 'Pair'


        #if np.sum(uRank[0:4]) == 1
        #4
        #elif
        #fh
    else:
        retWin = 'Nothing good'    
        pass
    return retWin
    

def hold(deck, hand, cardNumsToHold):
    # Get n new cards with deal() and replace locations
    cardNumsToHold = cardNumsToHold - 1 # Request 1-5 for users, want 0-4
    numCardsInHand = len(hand) # Usually 5
    numCardsToDraw = numCardsInHand - len(cardNumsToHold)
    if numCardsToDraw == numCardsInHand:
        cardsToDrawIdx = np.arange(numCardsInHand)
        deck, newCards = deal(deck, numCardsToDraw) # Get new cards, change deck
        hand = newCards
    else:     
        # Now remove the cards we want to hold from the draw
        cardsToDrawIdx = np.asarray(np.delete(np.arange(numCardsInHand), cardNumsToHold))
        deck, newCards = deal(deck, numCardsToDraw) # Get new cards, change deck
        hand.iloc[cardsToDrawIdx, :] = newCards[:] # Replace cards
    return deck, hand
    '''
    if numCardsToDraw != numCardsInHand:
        deck, newCards = deal(deck, numCardsToDraw)
        return deck, hand
    else:     
        # Now remove the cards we want to hold from the draw
        cardsToDrawIdx = np.asarray(np.delete(np.arange(numCardsInHand), cardNums))
        deck, newCards = deal(deck, numCardsToDraw) # Get new cards, change deck
        hand.iloc[[cardsToDrawIdx]] = newCards # Replace cards
        return deck, hand
    '''


def cheat():
    # For testing
    '''
    r = np.array(['King','Jack','Queen','9','10'])
    s = np.array(['Club','Club','Club','Club','Club'])
    n = np.array(['13','11','12','9','10'],dtype='int')
    notIn = np.array(['0','0','0','0','0'],dtype='int')
    

    #FH
    r = np.array(['King','King','9','9','9'])
    s = np.array(['Club','Heart','Club','Spade','Diamond'])
    n = np.array(['13','13','9','9','9'],dtype='int')
    notIn = np.array(['0','0','0','0','0'],dtype='int')
    
    #4
    r = np.array(['King','9','9','9','9'])
    s = np.array(['Club','Heart','Club','Spade','Diamond'])
    n = np.array(['13','9','9','9','9'],dtype='int')
    notIn = np.array(['0','0','0','0','0'],dtype='int')
    
    #Straight
    r = np.array(['8','Jack','Queen','9','10'])
    s = np.array(['Club','Spade','Club','Club','Club'])
    n = np.array(['8','11','12','9','10'],dtype='int')
    notIn = np.array(['0','0','0','0','0'],dtype='int')
    
    
    #3
    r = np.array(['8','Jack','Queen','8','8'])
    s = np.array(['Club','Spade','Club','Spade','Diamond'])
    n = np.array(['8','11','12','8','8'],dtype='int')
    notIn = np.array(['0','0','0','0','0'],dtype='int')
    
    
    #2 Pair
    r = np.array(['8','8','Queen','9','9'])
    s = np.array(['Club','Spade','Club','Club','Club'])
    n = np.array(['8','8','12','9','9'],dtype='int')
    notIn = np.array(['0','0','0','0','0'],dtype='int')
    '''
    
    
    '''
    #2
    r = np.array(['8','8','Queen','9','10'])
    s = np.array(['Club','Spade','Club','Club','Club'])
    n = np.array(['8','8','12','9','10'],dtype='int')
    notIn = np.array(['0','0','0','0','0'],dtype='int')
    
    
    dictCols = {'Rank': r, 'Suits': s, 'nRank': n, 'cardInDeck': notIn}
    
    cheatCards = pd.DataFrame(data=dictCols)

   
    return cheatCards
'''
'''
def askPrompt(prompt):
    if prompt == 'restart':
        newDeck, myCards = deal(newDeck, 5)
        win = checkHand(myCards)
    elif prompt == 'hold':
        deck, hand = hold(deck, hand, cardNumsToHold)
    elif prompt == 'again':
        pass
'''
def onePlay(money):
    # One round of play: new shuffled deck, draw 5, hold N, check win
    newDeck = buildDeck()
    newDeck = shuffleDeck(newDeck)

    print("Here's your first hand.")
    newDeck, myCards = deal(newDeck, 5)
    print('mc=',myCards)
    win = checkHand(myCards)
    print('\n\tThese cards give you: ', win)
    print('\tDo you wish to hold any?')
    whichToHold = input('Enter card numbers 1-5 separated by spaces for cards you want to keep: ')
    whichToHold = np.asarray(whichToHold.split()).astype(int) # Convert string input to split ints
    newDeck, myCards = hold(newDeck, myCards, whichToHold)
    win = checkHand(myCards)
    print('You got: ')
    print(myCards)
    print('\n\t' + win)

# Main Code
money = 20
bet = 1
play = 1
while play:
    onePlay(money)
    playAgain = input('Do you wish to continue playing? Y/N ')
    if playAgain.upper() == 'N':
        play = 0
        print('\nThanks for playing!\n')