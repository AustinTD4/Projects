# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 11:13:34 2023

@author: Austin Dickerson
"""
import os
import time
import random
import re
import numpy as np
from gtts import gTTS
from playsound import playsound
from colorama import init, Fore, Style

class blackjack_color():

    def __init__(self):
        self.card_list = ['2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']
        self.value_list = [2,3,4,5,6,7,8,9,10,10,10,10,11]
        
        #These keys contain the optimal actions for the player depending on the current state of the game. They are separated into soft totals,
        #hard totals, and situations where the player has a pair
        self.soft_key = [[2,2,2,3,3,2,2,2,2,2,2,2,2],[2,2,2,3,3,2,2,2,2,2,2,2,2],[2,2,3,3,3,2,2,2,2,2,2,2,2],[2,2,3,3,3,2,2,2,2,2,2,2,2],
                        [2,3,3,3,3,2,2,2,2,2,2,2,2],[3,3,3,3,3,1,1,2,2,2,2,2,2],[1,1,1,1,3,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1]]
        
        self.hard_key = [[2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2],
                         [2,2,2,2,2,2,2,2,2,2,2,2,2],[2,3,3,3,3,2,2,2,2,2,2,2,2],[3,3,3,3,3,3,3,3,2,2,2,2,2],[3,3,3,3,3,3,3,3,3,3,3,3,2],
                         [2,2,1,1,1,2,2,2,2,2,2,2,2],[1,1,1,1,1,2,2,2,2,2,2,2,2],[1,1,1,1,1,2,2,2,2,2,2,2,2],[1,1,1,1,1,2,2,2,2,2,2,2,2],
                         [1,1,1,1,1,2,2,2,2,2,2,2,2],[1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1]]
        
        self.pair_key = [[1,1,1,1,1,1,2,2,2,2,2,2,2],[1,1,1,1,1,1,2,2,2,2,2,2,2],[2,2,2,1,1,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2],
                         [1,1,1,1,1,2,2,2,2,2,2,2,2],[1,1,1,1,1,1,2,2,2,2,2,2,2],[1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,2,1,1,2,2,2,2,2],
                         [2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1]]
        
        #Necessary metrics to keep track of the game state are below
        self.counter = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth"]
        self.deck_stack, self.hands, self.dealerKey, self.playerKeys, self.double_ids = [], [], [], [], []
        self.moves = ["Stay","Hit","Double","Split"]
        self.dealer_total, self.player_total, self.script, self.script2 = None, None, None, None
        self.correct, self.count, self.hand_count, self.hand_wins, self.deck_count, self.multi_split = 0, 0, 0, 0, 0, 0
        self.net = 10
        self.active = True
        self.double_bet = False

    def run_flask_app(self):
        self.app.run()
        
    #Reads aloud any text
    def read_string(self, input_string):
        mytext = input_string
        myobj = gTTS(text=mytext, slow=False)
        if os.path.exists("speech.mp3") : os.remove("speech.mp3")
        myobj.save("speech.mp3") 
        playsound("speech.mp3") 
        os.remove("speech.mp3")
    
    #Creates the desired number of decks at the start of the game
    def generate_decks(self, number):
        for i in range(number): 
            self.deck_stack.append(np.ones((13,4),int))
            
    #Returns all previously drawn cards to the deck pile after half the cards in the stack have been drawn
    def refresh_decks(self):
        for i in range(self.deck_num): 
            self.deck_stack[i] = np.ones((13,4),int)
            
    #Picks an unchosen card from the deck stack within the desired range, returns the required information about that card
    def generate_card(self, name=False, key=False, maximum=12, deck_num=False):

        #Checks if the decks need shuffling
        self.deckCheck(deck_num)

        #Generates a random card if the user has elected not to specify the number of decks to play with
        index = random.randint(0,maximum)
        value = self.value_list[index]
        card = self.card_list[index]   

        #Returns card if the user has elected not to specify the number of decks to play with  
        if not deck_num:
            if not name and not key: 
                return value
            elif not key: 
                return value, card
            else: 
                return value, card, index
            
        #Searches the available cards to see if there are any left of the chosen type
        found = False
        place = 0
        while found == False and place < deck_num:
            for i in range(4):
                if found == False:
                    if self.deck_stack[place][index][i] == 1:
                        self.deck_stack[place][index][i] = 0 
                        found = True
            place += 1    

        #Chooses a new card if none were found previously        
        if found == False:
            recursion = self.generate_card(name, key, maximum, deck_num)
            return recursion
        else:
            if name == False and key == False: 
                return value
            elif key == False: 
                return value, card
            else: 
                return value, card, index

    #Checks all stored hands against the dealer's hand in the case of one or more splits        
    def call_split_winners(self, dealer):
        script = "Player has " and time.sleep(1)
        for hand in self.hands : script += str(int(hand))+", "
        script += "and "+Fore.BLUE+Style.BRIGHT+"Dealer has "+str(dealer)
        print(script) 
        time.sleep(1)
        
        #Declares outcome for each stored hand
        for ind, hand in enumerate(self.hands):
            if hand == dealer and hand < 22: 
                print("Hand "+str(ind+1)+" is a Push\n")
            elif hand > 21 or (hand < dealer and dealer < 22): 
                print(Fore.BLUE+Style.BRIGHT+"Hand "+str(ind+1)+" Loses\n")
            else: 
                print("Hand "+str(ind+1)+" Wins\n")    
            time.sleep(1)
                   
    #Handles the behavior of the dealer and concludes the hand once the player elects to stand
    def player_stands(self, pair=False):
        aces = 0
        dealer_draws = 0

        #Determines how many times the dealer will draw before concluding
        while self.dealer_total < 17:
            dealer_draws += 1
            print("Dealer takes a card\n") 
            time.sleep(1)
            value, card = self.generate_card(True,False,12,self.deck_num)
            self.dealer_total += value
            self.script = self.script+"  "+card
            print(self.script+"\n") 
            time.sleep(1)            
            if self.dealer_total == 21 and dealer_draws == 1:
                print(Fore.BLUE+Style.BRIGHT+"Dealer Has Blackjack, Player Loses") 
                return
            if self.dealer_total > 21 and len(re.findall('Ace',self.script)) != aces:
                self.dealer_total -= 10
                aces+=1  

        #Checks the game state to modify relevant variables
        if pair==True: 
            return       
        while self.player_total > 21: 
            self.player_total -= 10     

        #Determines outcome of the hand
        print("Player: "+str(self.player_total)+" and "+Fore.BLUE+Style.BRIGHT+"Dealer:  "+str(self.dealer_total))
        if self.dealer_total > self.player_total and self.dealer_total < 22: 
            print("Player Loses\n") and self.read_string("Loss")
        elif self.dealer_total == self.player_total: 
            print("Push\n")
        else : 
            print("Player Wins!!\n") 
            self.read_string("Win")
        
    #Handles the player drawing a card
    def player_hits(self, pair=False):
        if self.deck_num != False: 
            value, card = self.generate_card(True,False,12,self.deck_num)
        else: 
            value, card = self.generate_card(True)
        self.player_total += value
        self.script2 = self.script2+"  "+card 
        time.sleep(1) 
        print(self.script2)        

        #Checks if an ace in the player's hand should count as a 1 or an 11
        if self.player_total-10*len(re.findall('Ace',self.script2)) > 21:
            time.sleep(1) 
            print(Fore.BLUE+Style.BRIGHT+"Player busts, Dealer wins\n")
            return
        
        #Query the player's next move
        choice = input("Hit or Stay?\n")        
        if re.search('[hH]it|[hH]|2', choice): 
            self.player_hits(pair)            
        elif re.search('[sS]tay|[sS]|1', choice):
            if pair: return
            else: 
                self.player_stands()
        else: 
            print("I don't understand")

    #Handles the player choosing to double down   
    def player_doubles_down(self, pair=False):
        print("Doubling Down") 
        time.sleep(1)
        value, card = self.generate_card(True,False,12,self.deck_num)
        self.player_total += value
        self.script2 = self.script2+"  "+card 
        print(self.script2)

        #Player must then stand by default
        if pair == False: 
            self.player_stands()
        else: 
            self.player_stands(True)
            
    #Offers the player their possible moves while splitting, given the game state
    def split_choice(self, card, value, counter):
        if value == card: 
            choice = input("Will You Stay, Hit, Double, Or Split With Your "+counter+" Hand?\n") 
        else: 
            choice = input("Will You Stay, Hit, Or Double With Your "+counter+" Hand?\n")
        return choice
    
    #Offers the player their possible moves, given the game state
    def determine_choice(self, pair=True, choice=False):
        if pair and not choice: 
            choice = input("Will You Stay, Hit, Double, Or Split?[s,h,d,sp] Main Menu[m]\n")
        elif not choice: 
            choice = input("Will You Stay, Hit, Or Double? [s,h,d]   Main Menu [m]\n")
            
        if re.search('^[sS]$|^[sS]tay|^1', choice): selection = 1
        elif re.search('^[hH]|^[hH]it|^2', choice): selection = 2
        elif re.search('^[dD]|^[dD]ouble|^3', choice): selection = 3
        elif re.search('^[sS]plit|^4|^[sS]p$', choice) and pair: selection = 4
        elif re.search('^[eE]|^[eE]nd|^5|[qQ]|[qQ]uit|^[mM]|[mM]enu|^[mM]ain', choice): selection = 5
        else: selection = self.determine_choice(pair)   
            
        return selection
    
    #Calls the right method given the player's choice
    def resolve_selection(self, selection, card1, value1):
        if selection == 1: self.player_stands()
        elif selection == 2: self.player_hits()
        elif selection == 3: self.player_doubles_down()
        elif selection == 4: self.split_a_pair(card1, value1)
        elif selection == 5: self.conclude()
    
    #Provides an assessment of the player's decisions after quitting
    def conclude(self):
        if self.count-1 != 0:
            print("Final Accuracy is "+str(self.correct)+" out of "+str(self.count-1)+" or "+str(100*(self.correct/(self.count-1)))+" Percent\n")
            self.read_string("Final Accuracy is "+str(self.correct)+" out of "+str(self.count-1)+" or "+str(100*(self.correct/(self.count-1)))+" Percent")
            
            if (self.correct/(self.count-1)) < 0.25 : self.read_string("You Are Not Good At This")
            elif (self.correct/(self.count-1)) < 0.5 : self.read_string("Keep Trying")
            elif 0.9 > (self.correct/(self.count-1)) > 0.8 : self.read_string("You're Getting There")
            elif (self.correct/(self.count-1)) > 0.9 : self.read_string("Good Job!")
        self.active = False
    
    #Assesses the outcome of each hand in the case of splitting
    def resolve_from_split(self, tally, value, name, second=False, double=False):
        self.player_total = tally + value
        self.script2 += name
        if not double: 
            self.player_hits(True)
        else: 
            self.player_doubles_down(True)

        #Checks the hand for aces and adjusts the hand total accordingly
        aces = self.script2.count('Ace')
        compensate = 0
        while compensate < aces and self.player_total > 21:
            self.player_total -= 10
            compensate += 1        

        if self.player_total > 21:
            if not second: 
                print(Fore.BLUE+Style.BRIGHT+self.counter[0+self.multi_split]+" Hand Bust\n")
            else: 
                print(Fore.BLUE+Style.BRIGHT+self.counter[1+self.multi_split]+" Hand Bust\n")                
        return self.player_total
        
    #Handles the player splitting a pair
    def split_a_pair(self, card1, value1):
        time.sleep(1) 
        print("Player Splits")
        player_total1, player_total2 = self.player_total/2, self.player_total/2 
        time.sleep(1)

        #Generates new cards for the player and dealer
        value3, card3 = self.generate_card(True,False,12,self.deck_num)
        value4, card4 = self.generate_card(True,False,12,self.deck_num)
        self.script2 = "Player Shows: "+card1+"  "+card3+"  and  "+card1+"  "+card4 
        print(self.script2) 
        self.script2 = "Player Shows: "+card1+"  "
        choice = self.split_choice(value1, value3, "First") 
        time.sleep(1)
        choice = self.determine_choice(True, choice)
        
        #Adds the current hand to a list after resolving the player's choice
        if choice == 1: 
            player_total1 += value3
            self.hands.append(player_total1)
        elif choice == 2: 
            self.hands.append(self.resolve_from_split(player_total1, value3, card3))
        elif choice == 3: 
            self.hands.append(self.resolve_from_split(player_total1, value3, card3, double=True))
        elif choice == 4: 
            self.multi_split += 1 
            self.split_a_pair(card1, value1)
        
        time.sleep(1)
        choice2 = self.split_choice(value1, value4, "Second") 
        time.sleep(1) 
        self.script2 = "Player Shows: "+card1+"  "
        choice2 = self.determine_choice(True, choice2)
        
        #Handles the final hand of the split and any decision the player makes for that hand before calling the winners of 
        #each hand vs. the dealer
        if choice2 == 1:
            self.hands.append(player_total2+value4)
            if self.multi_split > 0 : self.multi_split -= 1
            else : 
                self.player_stands(True) 
                self.call_split_winners(self.dealer_total)
        elif choice2 == 2:
            self.hands.append(self.resolve_from_split(player_total2, value4, card4))
            if self.multi_split > 0 : 
                self.multi_split -= 1
            else: 
                self.player_stands(True) 
                self.call_split_winners(self.dealer_total)
        elif choice2 == 3:
            self.hands.append(self.resolve_from_split(player_total2, value4, card4, double=True))
            if self.multi_split > 0: 
                self.multi_split -= 1
            else: 
                self.player_stands(True) 
                self.call_split_winners(self.dealer_total)
        elif choice2 == 4:
            self.multi_split += 1 
            self.split_a_pair(card1, value1)
            if self.multi_split < 1: 
                self.player_stands(True)  
                self.call_split_winners(self.dealer_total)
                
    #Begins the initial state of the game and selects from either all cards, only pairs, or only soft toals for the player
    def traditional_blackjack(self, pair=False, soft=False, deck_num=False):
        self.count, self.correct = 0, 0
        self.active = True
        self.deck_stack = []

        #Calls the deck generator
        if deck_num != False: 
            self.generate_decks(self.deck_num)   

        #Checks how many cards in the deck stack remain        
        while self.active:
            self.hands = []
            self.multi = 0
            if deck_num != False: 
                remain = 0
            for i in range(deck_num): 
                remain += np.count_nonzero(self.deck_stack[i] == 1)
            
            #Checks if half the deck stak has been drawn, requiring reshuffling
            if deck_num != False:
                if remain < (float(deck_num)/2)*52:
                    print("Half The Deck Stack Has Been Dealt, Reshuffling...")
                    time.sleep(1) 
                    self.refresh_decks()
                
            #Generates cards for the player's hand
            if pair:
                value1, card1, key1 = self.generate_card(True,True)
                value2,card2 = value1, card1
            elif soft:
                value1, card1, key1 = self.generate_card(True,True)
                value2, card2 = 11, "Ace"
            else:
                if deck_num != False: 
                    value1, card1, key1 = self.generate_card(True,True,12,self.deck_num)
                else: 
                    value1, card1, key1 = self.generate_card(True,True)
                
                if deck_num != False: 
                    value2, card2 = self.generate_card(True,False,12,deck_num)
                else: 
                    value2, card2 = self.generate_card(True)
                
            #Generates dealer's hand
            if deck_num != False: 
                self.dealer_total, card3, key3 = self.generate_card(True,True,12,deck_num)
            else: 
                self.dealer_total, card3, key3 = self.generate_card(True,True)
            self.player_total = value1 + value2
            
            #Checks for a player getting 'Blackjack'
            if self.player_total == 21:
                self.read_string("Blackjack!")
                print("Player Wins!!")
                continue
            
            #Displays the hands for the player and dealer
            self.count+=1
            time.sleep(1) 
            print("You Draw:  "+card1+"  "+card2+"\n") 
            time.sleep(1)
            print(Fore.BLUE+Style.BRIGHT+"Dealer: #  "+card3) 
            time.sleep(1)
            self.script = Fore.BLUE+Style.BRIGHT+"Dealer Shows: "+card3
            self.script2 = "Player Shows:  "+card1+"  "+card2
            
            #Determines the optimal player action using the strategy tables
            if value1 == 11 and card1 != card2: actual = self.soft_key[value2-2][key3] 
            elif value2 == 11 and card1 != card2: actual = self.soft_key[value1-2][key3]
            elif card1 == card2 and self.pair_key[key1][key3] == 1: actual = 4
            else: actual = self.hard_key[value1+value2-4][key3]
            response = "Incorrect, in this position you should "+self.moves[actual-1]+"\n"

            #Queries player's action choice
            if value1 == value2: selection = self.determine_choice() 
            else: selection = self.determine_choice(False)    

            #Determines the quality of the player's decision
            if selection != actual and selection!= 5:
                print(Style.BRIGHT+Fore.RED+response)
                self.read_string(response)
            elif selection != 5: self.correct+=1

            #Carries out player selection
            self.resolve_selection(selection, card1, value1)

        self.play(False)
        
    #Produces starting states for a hand, letting the player quickly practice strategy
    def flashcards(self, soft=False, pair=False):
        #Generates starting hands
        while self.active:
            self.count += 1
            value1, card1, key1 = self.generate_card(True,True)
            if pair: value2, card2 = value1, card1
            elif soft: value2, card2 = 11, "Ace"
            else:
                value1, card1, key1 = self.generate_card(True,True,11)
                value2, card2, key2 = self.generate_card(True,True,11)
                while card1 == card2 : value2, card2, key2 = self.generate_card(True,True,11)
                    
            #Displays starting hands
            dealer1, dealer2, dealer3 = self.generate_card(True,True)
            print(Style.BRIGHT+Fore.GREEN+"Player Has "+card1+"  "+card2+Fore.BLUE+"  Dealer Has "+dealer2)
            selection = self.determine_choice(pair=pair)
            
            #Determines optimal action
            if soft: 
                actual = self.soft_key[value1-2][dealer3]
            elif pair: 
                actual = self.pair_key[key1][dealer3]
            else: 
                actual = self.hard_key[value1+value2-4][dealer3]
                
            #Assesses player selection
            response = "Incorrect, in this position you should "+self.moves[actual-1]+"\n"
            if selection != actual and selection!= 5:
                print(Style.BRIGHT+Fore.RED+response) and self.read_string(response)
            elif selection != 5 : self.correct+=1
            if selection == 5 : self.conclude()
        self.play(False)

    #Allows external applications to check the deck stack and see if it needs shuffling
    def deckCheck(self, deck_num=False):
        remain = 0
        for i in range(deck_num): 
            remain += np.count_nonzero(self.deck_stack[i] == 1)
            
        if deck_num != False:
            if remain < (float(deck_num)/2)*52:
                self.read_string(str(deck_num)+" Decks, Shuffling...")
                print("Half The Deck Stack Has Been Dealt, Reshuffling...")
                time.sleep(1) 
                self.refresh_decks()

    #Initializes the game
    def play(self, first=True):
        self.deck_num = False

        #Gives an introduction if needed
        if first:
            init(autoreset=True)
            welcome = "Welcome to the Tutorial Blackjack Simulator"
            self.read_string(welcome) 
            print(welcome)
            
        #Checks which selection of cards player wants to draw from and number of decks to play with, allowing specialized practice
        selection = input("To Practice Soft Totals Type Soft, To Practice Pair Splitting Type Pair, To Play Traditional BlackJack Type Jack, or For Flashcards Type Flash\n")
        if re.search('^[sS]oft|^[sS]|^1', selection): 
            self.traditional_blackjack(pair=False,soft=True,deck_num=False)
        elif re.search('^[pP]air|^[pP]|^2', selection): 
            self.traditional_blackjack(pair=True,soft=False,deck_num=False)
        elif re.search('^[jJ]|^[jJ]ack|^[bB]lack[jJ]ack|^3', selection):
            self.deck_num = input("Please Select Standard Type Or Indicate The Number Of Decks You Want To Play With\n")
            if self.deck_num.isnumeric() != True: 
                self.deck_num = False
            elif int(self.deck_num) == 1: 
                self.deck_num = int(self.deck_num) 
                print("Shuffling Deck\n")
            else: 
                self.deck_num = int(self.deck_num) 
            print("Shuffling Decks\n")
            self.traditional_blackjack(pair=False,soft=False,deck_num=self.deck_num)

        #Plays flashcards instead of dealing if the player has selected flashcards
        elif re.search('^[fF]|^[fF]lash|^[fF]lash[cC]ards|^4', selection):
            selection = input("Please Choose Hard Totals, Soft Totals, or Pairs\n")
            if re.search('[hH]|[hH]ard|[hH]ard [tT]otal|1', selection): 
                self.flashcards()
            elif re.search('[sS]|[sS]oft|[sS]oft [tT]otal|2', selection): 
                self.flashcards(soft=True)
            elif re.search('[pP]|[pP]air|3', selection): 
                self.flashcards(pair=True)
            else: 
                print("I don't understand, returning to Menu...") 
                self.play(False)
        else: 
            print("I don't understand, Terminating...")            
        
