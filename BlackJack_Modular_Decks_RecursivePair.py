# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 11:13:34 2023

@author: Austin Dickerson
"""
#call program in anaconda with: "python *path*\Blackjack_Modular_Decks_RecursivePair.py"
import os
import time
import random
import re
import numpy as np
from gtts import gTTS
from playsound import playsound
from colorama import init, Fore, Style

class black_jack_colorless:
    
    def __init__(self):
        self.card_list = ['2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']
        self.value_list = [2,3,4,5,6,7,8,9,10,10,10,10,11]
        
        self.soft_key = [[2,2,2,3,3,2,2,2,2,2,2,2,2],[2,2,2,3,3,2,2,2,2,2,2,2,2],[2,2,3,3,3,2,2,2,2,2,2,2,2],[2,2,3,3,3,2,2,2,2,2,2,2,2],
                        [2,3,3,3,3,2,2,2,2,2,2,2,2],[3,3,3,3,3,1,1,2,2,2,2,2,2],[1,1,1,1,3,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1]]
        
        self.hard_key = [[2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2],
                         [2,2,2,2,2,2,2,2,2,2,2,2,2],[2,3,3,3,3,2,2,2,2,2,2,2,2],[3,3,3,3,3,3,3,3,2,2,2,2,2],[3,3,3,3,3,3,3,3,3,3,3,3,2],
                         [2,2,1,1,1,2,2,2,2,2,2,2,2],[1,1,1,1,1,2,2,2,2,2,2,2,2],[1,1,1,1,1,2,2,2,2,2,2,2,2],[1,1,1,1,1,2,2,2,2,2,2,2,2],
                         [1,1,1,1,1,2,2,2,2,2,2,2,2],[1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1]]
        
        self.pair_key = [[1,1,1,1,1,1,2,2,2,2,2,2,2],[1,1,1,1,1,1,2,2,2,2,2,2,2],[2,2,2,1,1,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2],
                         [1,1,1,1,1,2,2,2,2,2,2,2,2],[1,1,1,1,1,1,2,2,2,2,2,2,2],[1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,2,1,1,2,2,2,2,2],
                         [2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2,2,2,2,2,2],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1]]
        
        self.counter = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth"]
        self.deck_stack, self.hands = [], []
        self.moves = ["Stay","Hit","Double","Split"]
        self.dealer_total, self.player_total, self.script, self.script2 = None, None, None, None
        self.correct, self.count, self.deck_count, self.deck_num, self.multi_split = 0, 0, 0, 0, 0
        self.active = True
        
    def read_string(self, input_string):
        mytext = input_string
        myobj = gTTS(text=mytext, slow=False)
        if os.path.exists("speech.mp3"):
            os.remove("speech.mp3")
        myobj.save("speech.mp3")
        playsound("speech.mp3")
        os.remove("speech.mp3")
    
    def generate_decks(self, number):
        for i in range(number):
            self.deck_stack.append(np.ones((13,4),int))
            
    def refresh_decks(self):
        for i in range(self.deck_num):
            self.deck_stack[i] = np.ones((13,4),int)
            
    def generate_card(self, name=False, key=False, maximum=12, deck_num=False):
        index = random.randint(0,maximum)
        value = self.value_list[index]
        card = self.card_list[index]
            
        if deck_num == False:
            if name == False and key == False:
                return value
            elif key == False:
                return value, card
            else:
                return value, card, index
                
        found = False
        place = 0
        while found == False:
            for i in range(4):
                if found == False:
                    if self.deck_stack[place][index][i] == 1:
                        self.deck_stack[place][index][i] = 0
                        found = True
            place += 1
            
        if found == False:
            recursion = self.generate_card2(name, key, maximum, self.deck_num)
            return recursion
        else:
            if name == False and key == False:
                return value
            elif key == False:
                return value, card
            else:
                return value, card, index
            
    def call_split_winners(self, dealer):
        time.sleep(1)
        script = "Player has "
        for hand in self.hands:
            script += str(int(hand))+", "
        script += "and "+Fore.BLUE+Style.BRIGHT+"Dealer has "+str(dealer)
        print(script)
        time.sleep(1)
        
        for ind, hand in enumerate(self.hands):
            if hand == dealer and hand < 22:
                print("Hand "+str(ind+1)+" is a Push\n")
            elif hand > 21 or (hand < dealer and dealer < 22):
                print(Fore.BLUE+Style.BRIGHT+"Hand "+str(ind+1)+" Loses\n")
            else:
                print("Hand "+str(ind+1)+" Wins\n")    
            time.sleep(1)
                   
    def player_stands(self, pair=False):
        aces = 0
        dealer_draws = 0
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
                
        if pair==True:
            return       
        
        while self.player_total > 21:
            self.player_total -= 10           
        
        print("Player: "+str(self.player_total)+" and "+Fore.BLUE+Style.BRIGHT+"Dealer:  "+str(self.dealer_total))
        if self.dealer_total > self.player_total and self.dealer_total < 22:
            print("Player Loses\n")
            self.read_string("Loss")
        elif self.dealer_total == self.player_total:
            print("Push\n")
        else:
            print("Player Wins!!\n")
            self.read_string("Win")
        
    def player_hits(self, pair=False):
        if self.deck_num != False:
            value, card = self.generate_card(True,False,12,self.deck_num)
        else:    
            value, card = self.generate_card(True)
        self.player_total += value
        self.script2 = self.script2+"  "+card
        time.sleep(1)
        print(self.script2)
        
        if self.player_total-10*len(re.findall('Ace',self.script2)) > 21:
            time.sleep(1)
            print(Fore.BLUE+Style.BRIGHT+"Player busts, Dealer wins\n")
            return
        
        choice = input("Hit or Stay?\n")
        
        if re.search('[hH]it|[hH]|2', choice):
            self.player_hits(pair)            
        elif re.search('[sS]tay|[sS]|1', choice):
            if pair == True:
                return
            else:
                self.player_stands()
        else:
            print("I don't understand")
            
    def player_doubles_down(self, pair=False):
        print("Doubling Down")
        time.sleep(1)
        value, card = self.generate_card(True,False,12,self.deck_num)
        self.player_total += value
        self.script2 = self.script2+"  "+card
        print(self.script2)
        if pair == False:
            self.player_stands()
        else:
            self.player_stands(True)
            
    def split_choice(self, card, value, counter):
        if value == card:
            choice = input("Will You Stay, Hit, Double, Or Split With Your "+counter+" Hand?\n") 
        else:
            choice = input("Will You Stay, Hit, Or Double With Your "+counter+" Hand?\n")
            
        return choice
    
    def determine_choice(self, pair=True, choice=False):
        if pair == True and choice == False:
            choice = input("Will You Stay, Hit, Double, Or Split?[s,h,d,sp] Main Menu[m]\n")
        elif choice == False:
            choice = input("Will You Stay, Hit, Or Double? [s,h,d]   Main Menu [m]\n")
            
        if re.search('^[sS]$|^[sS]tay|^1', choice):
            selection = 1
        elif re.search('^[hH]|^[hH]it|^2', choice):
            selection = 2
        elif re.search('^[dD]|^[dD]ouble|^3', choice):
            selection = 3
        elif re.search('^[sS]plit|^4|^[sS]p$', choice) and pair == True:
            selection = 4
        elif re.search('^[eE]|^[eE]nd|^5|[qQ]|[qQ]uit|^[mM]|[mM]enu|^[mM]ain', choice):
            selection = 5
        else:
            selection = self.determine_choice(pair)
            
        return selection
    
    def resolve_selection(self, selection, card1, value1):
        if selection == 1:
            self.player_stands()
        elif selection == 2:
            self.player_hits()
        elif selection == 3:
            self.player_doubles_down()
        elif selection == 4:
            self.split_a_pair(card1, value1)
        elif selection == 5:
            self.conclude()
    
    def conclude(self):
        if self.count-1 != 0:
            print("Final Accuracy is "+str(self.correct)+" out of "+str(self.count-1)+" or "+str(100*(self.correct/(self.count-1)))+" Percent\n")
            self.read_string("Final Accuracy is "+str(self.correct)+" out of "+str(self.count-1)+" or "+str(100*(self.correct/(self.count-1)))+" Percent")
        
            if (self.correct/(self.count-1)) < 0.25:
                self.read_string("You Are Terrible At This")
            elif (self.correct/(self.count-1)) < 0.5:
                self.read_string("Keep Trying")
            elif 0.9 > (self.correct/(self.count-1)) > 0.8:
                self.read_string("You're Getting There")
            elif (self.correct/(self.count-1)) > 0.9:
                self.read_string("Good Job!")
        
        self.active = False
    
    def resolve_from_split(self, tally, value, name, second=False, double=False):
        self.player_total = tally + value
        self.script2 += name
        
        if double == False:
            self.player_hits(True)
        else:
            self.player_doubles_down(True)
        
        aces = self.script2.count('Ace')
        compensate = 0
        while compensate < aces and self.player_total > 21:
            self.player_total -= 10
            compensate += 1
            
        if self.player_total > 21:
            if second == False:
                print(Fore.BLUE+Style.BRIGHT+self.counter[0+self.multi_split]+" Hand Bust\n")
            else:
                print(Fore.BLUE+Style.BRIGHT+self.counter[1+self.multi_split]+" Hand Bust\n")
                
        return self.player_total
        
    def split_a_pair(self, card1, value1):
        time.sleep(1)
        print("Player Splits")
        player_total1, player_total2 = self.player_total/2, self.player_total/2
        time.sleep(1)
        value3, card3 = self.generate_card(True,False,12,self.deck_num)
        value4, card4 = self.generate_card(True,False,12,self.deck_num)
        self.script2 = "Player Shows: "+card1+"  "+card3+"  and  "+card1+"  "+card4
        print(self.script2)
        self.script2 = "Player Shows: "+card1+"  "
        choice = self.split_choice(value1, value3, "First")
        time.sleep(1)
        choice = self.determine_choice(True, choice)
        
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
        
        if choice2 == 1:
            self.hands.append(player_total2+value4)
            if self.multi_split > 0:
                self.multi_split -= 1
            else:
                self.player_stands(True)
                self.call_split_winners(self.dealer_total)
        elif choice2 == 2:
            self.hands.append(self.resolve_from_split(player_total2, value4, card4))
            if self.multi_split > 0:
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
                
    def traditional_blackjack(self, pair=False, soft=False, deck_num=False):
        self.count, self.correct = 0, 0
        self.active = True
        self.deck_stack = []
        
        if deck_num != False:
            self.generate_decks(self.deck_num)
            
        while self.active == True:
            self.hands = []
            self.multi = 0
            if deck_num !=False:
                remain = 0
                for i in range(deck_num):
                    remain += np.count_nonzero(self.deck_stack[i] == 1)
                if remain < (float(deck_num)/2)*52:
                    print("Half The Deck Stack Has Been Dealt, Reshuffling...")
                    time.sleep(1)
                    self.refresh_decks()
                
            if pair == True:
                value1, card1, key1 = self.generate_card(True,True)
                value2 = value1
                card2 = card1
            elif soft == True:
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
                
            if deck_num != False:
                self.dealer_total, card3, key3 = self.generate_card(True,True,12,deck_num)
            else:    
                self.dealer_total, card3, key3 = self.generate_card(True,True)
            self.player_total = value1 + value2
            
            if self.player_total == 21:
                self.read_string("Blackjack!")
                print("Player Wins!!")
                continue
            
            self.count+=1
            time.sleep(1)       
            print("You Draw:  "+card1+"  "+card2+"\n")
            time.sleep(1)
            print(Fore.BLUE+Style.BRIGHT+"Dealer: #  "+card3)
            time.sleep(1)
            self.script = Fore.BLUE+Style.BRIGHT+"Dealer Shows: "+card3
            self.script2 = "Player Shows:  "+card1+"  "+card2
            
            if value1 == 11 and card1 != card2:
                actual = self.soft_key[value2-2][key3]
            elif value2 == 11 and card1 != card2:
                actual = self.soft_key[value1-2][key3]
            elif card1 == card2 and self.pair_key[key1][key3] == 1:
                actual = 4
            else:
                actual = self.hard_key[value1+value2-4][key3]
            
            response = "Incorrect, in this position you should "+self.moves[actual-1]+"\n"
                
            if value1 == value2:
                selection = self.determine_choice() 
            else:
                selection = self.determine_choice(False)
            
            if selection != actual and selection!= 5:
                print(Style.BRIGHT+Fore.RED+response)
                self.read_string(response)
            elif selection != 5:
                self.correct+=1
            
            self.resolve_selection(selection, card1, value1)
            
        self.run(False)
                
    def run(self, first=True):
        if first == True:
            init(autoreset=True)
            welcome = "Welcome to the Tutorial Blackjack Simulator"
            print(welcome)
            self.read_string(welcome)
            
        selection = input("To Practice Soft Totals Type Soft, To Practice Pair Splitting Type Pair, To Play Traditional BlackJack Type Jack\n")
        
        if re.search('[sS]oft|[sS]|1', selection):
            self.traditional_blackjack(pair=False,soft=True,deck_num=False)
        elif re.search('[pP]air|[pP]|2', selection):
            self.traditional_blackjack(pair=True,soft=False,deck_num=False)
        elif re.search('[jJ]|[jJ]ack|[bB]lack[jJ]ack|3', selection):
            self.deck_num = input("Please Select Standard Type Or Indicate The Number Of Decks You Want To Play With\n")
            if self.deck_num.isnumeric() != True or self.deck_num == 0 :
                self.deck_num = False
            elif int(self.deck_num) == 1:
                print("Shuffling Deck\n")
                self.deck_num = int(self.deck_num)
            else:
                print("Shuffling Decks\n")
                self.deck_num = int(self.deck_num)
            self.traditional_blackjack(pair=False,soft=False,deck_num=self.deck_num)
        else:
            print("I don't understand, Terminating...")            

bj = black_jack_colorless()
bj.run()

#call program in anaconda with: "python *path*\Blackjack_Modular_Decks_RecursivePair.py"
