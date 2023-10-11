import os, random, time, socket
from flask import Flask, jsonify, request, render_template, make_response
from BlackJack_Plain import blackjack_color

#Initializes the blackjack object, which contains the majority of variables and methods needed to play
bj = blackjack_color()

#Initializes lists
cards2, face1, face2, num1, num1copy, num2, num2copy, values, hands = [], [], [], [], [], [], [], [], []

#Contains paths to all card images
master_path_reg = ["static/images/2_of_clubs.png", "static/images/2_of_diamonds.png", "static/images/2_of_hearts.png", "static/images/2_of_spades.png", 
    "static/images/3_of_clubs.png", "static/images/3_of_diamonds.png", "static/images/3_of_hearts.png", "static/images/3_of_spades.png", 
    "static/images/4_of_clubs.png", "static/images/4_of_diamonds.png", "static/images/4_of_hearts.png", "static/images/4_of_spades.png", 
    "static/images/5_of_clubs.png", "static/images/5_of_diamonds.png", "static/images/5_of_hearts.png", "static/images/5_of_spades.png", 
    "static/images/6_of_clubs.png", "static/images/6_of_diamonds.png", "static/images/6_of_hearts.png", "static/images/6_of_spades.png", 
    "static/images/7_of_clubs.png", "static/images/7_of_diamonds.png", "static/images/7_of_hearts.png", "static/images/7_of_spades.png", 
    "static/images/8_of_clubs.png", "static/images/8_of_diamonds.png", "static/images/8_of_hearts.png", "static/images/8_of_spades.png", 
    "static/images/9_of_clubs.png", "static/images/9_of_diamonds.png", "static/images/9_of_hearts.png", "static/images/9_of_spades.png", 
    "static/images/10_of_clubs.png", "static/images/10_of_diamonds.png", "static/images/10_of_hearts.png", "static/images/10_of_spades.png", 
    "static/images/101_jack_of_clubs2.png", "static/images/101_jack_of_diamonds2.png", "static/images/101_jack_of_hearts2.png", "static/images/101_jack_of_spades2.png", 
    "static/images/102_queen_of_clubs2.png", "static/images/102_queen_of_diamonds2.png", "static/images/102_queen_of_hearts2.png", "static/images/102_queen_of_spades2.png", 
    "static/images/103_king_of_clubs2.png", "static/images/103_king_of_diamonds2.png", "static/images/103_king_of_hearts2.png", "static/images/103_king_of_spades2.png", 
    "static/images/ace_of_clubs.png", "static/images/ace_of_diamonds.png", "static/images/ace_of_hearts.png", "static/images/ace_of_spades.png"]

ace_paths = ["static/images/ace_of_clubs.png", "static/images/ace_of_diamonds.png", "static/images/ace_of_hearts.png", "static/images/ace_of_spades.png"]

#Initializes Flask
app = Flask(__name__)


#Reads next move aloud
def do_action(button_id):
    responses = ['Stay','Hit','Double Down','Pair Splitting', 'Exiting...', 'Standard Cards', 'Soft Hands Only', 'Pairs Only']
    bj.read_string(responses[button_id-1])

#Opens initial HTML page
@app.route('/')
def index():
    return render_template('BlackJack1.html')

#Handles button clicks on the HTML page, carries out necessary actions
@app.route('/button_click', methods=['POST'])
def button_click():
    #Colects information about the game state
    button_id = int(request.json['button_id'])
    clicks = int(request.json['buttonClickCount'])
    handNum = int(request.json['hands'])
    split = request.json['split']
    isRecursive = request.json['isRecursiveCall']
    global cards2, num2, num2copy, values
    if button_id == 1: 
        time.sleep(1)
    if isRecursive == False: 
        do_action(button_id)
        bj.double_ids.append(0)

    #Generates the next card
    value, card, image, ind = cardgen()
    
    #Handles the choice to stand
    if button_id == 1: 

        #In the case of a split, this stores important information about the latest hand and prepares to send the next hand to the HTML page
        if split == True and handNum != 1:
            bj.read_string("Next Hand")
            bj.hands.append(bj.player_total)
            bj.player_total = int(values[0] + value)
            copy1 = cards2[0]
            copy2 = num2[0]
            cards2, num2 = [], []
            cards2.append(copy1)
            num2.append(copy2)
            cards2.append(image)
            num2.append(ind)
            num2copy = num2
            sending = {'imagePaths' : cards2, 'hand_total' : bj.player_total}

        else:
            #Handles the dealer's hand once a player who has split stands on their last hand
            if split == True and isRecursive == False:
                bj.hands.append(bj.player_total)
            if cards1[0] == "static/images/card_back.jpg": 
                cards1[0] = image
            else: 
                cards1.append(image)
            face1.append(card)
            num1.append(ind)
            bj.dealer_total += value

            #Checks for a dealer 'Blackjack'
            if bj.dealer_total == 21 and len(cards1) == 2: 
                bj.read_string("BlackJack! Dealer Wins")
                bj.dealer_total = 0

            #Checks to see who won the hand
            if bj.dealer_total > 16 and bj.dealer_total < 22 and split == False:
                if bj.dealer_total > bj.player_total: 
                    bj.read_string("Dealer Wins")
                    bj.dealer_total = 0
                elif bj.dealer_total == bj.player_total: 
                    bj.read_string("Push, Nobody Wins")
                    bj.dealer_total = 0
                    if bj.double_bet == True:
                        bj.net += 2
                    else:
                        bj.net += 1
                elif bj.dealer_total < bj.player_total: 
                    bj.hand_wins += 1
                    if bj.double_bet == True:
                        bj.net += 4
                    else:
                        bj.net += 2
                    bj.read_string("Player Wins!")
                    bj.dealer_total = 0

            #Checks if the dealer has aces and needs their hand total modified
            elif bj.dealer_total > 21 and 12 in num1:
                bj.dealer_total -= 10
                num1.pop(num1.index(12))
            #Checks for the dealer busting
            if bj.dealer_total > 21: 
                bj.read_string("Dealer Busts")
                bj.hand_wins += 1
                if bj.double_bet == True:
                    bj.net += 4
                else:
                    bj.net += 2
                bj.dealer_total = 0
            sending = {'imagePaths' : cards1, 'hand_total' : bj.dealer_total, 'net' : bj.net}

        #Returns the image paths and relevant tallies to the HTML page
        return jsonify(sending)
    
    #Adds a card to the current hand, due to selecting 'hit' 
    elif button_id == 2:
        cards2.append(image)
        face2.append(card)
        num2.append(ind)
        bj.player_total += value
        #Checks if the hand contains an ace and needs its total modified
        if bj.player_total > 21 and 12 in num2copy:
            print("num2copy "+str(num2copy))
            bj.player_total -= 10
            num2copy.pop(num2copy.index(12))
        #Checks for a bust
        if bj.player_total > 21:
            bj.read_string("Player Busts")
            bj.player_total = 0
        sending = {'imagePaths' : cards2, 'hand_total' : bj.player_total, 'net' : bj.net}

        #Returns the image paths and relevant tallies to the HTML page
        return jsonify(sending)
    
    #Handles the player doubling down
    elif button_id == 3: 
        #Checks to see if the move is valid
        if clicks == 1 or clicks == 0:
            #Checks if there are multiple hands
            if split == True:
                bj.hands.append(bj.player_total)
            #Handles extra betting from double down and tracks which hands doubled down
            bj.double_ids.append(1)
            bj.net -= 1
            bj.double_bet = True

            #Generates next card
            cards2.append(image)
            face2.append(card)
            num2.append(ind)
            num2copy.append(ind)
            bj.player_total += value

            #Checks if the hand contains an ace and needs its total modified
            if bj.player_total > 21 and 12 in num2copy:
                bj.player_total -= 10
                num2copy.pop(num2copy.index(12))
            #Checks for a bust
            if bj.player_total > 21:
                nj.read_string("Player Busts")
                bj.player_total = 0
            sending = {'imagePaths' : cards2, 'hand_total' : bj.player_total, 'net' : bj.net}
            #Returns the image paths and relevant tallies to the HTML page
            return jsonify(sending)
        else:
            #Handles case of the move being invalid
            bj.read_string("You Cannot Double Now")
            return make_response('', 200)
    
    #Handles the player splitting a pair
    elif button_id == 4:
        #Generates new card and returns relevent variables and image paths to the HTML page
        if pair_id != None:
            bj.net -= 1
            bj.hand_count += 1
            num2[1] = ind
            cards2[1] = image
            bj.player_total = int(values[0] + value)
            sending = {'imagePaths' : cards2, 'hand_total' : bj.player_total, 'net' : bj.net}
            return jsonify(sending)
        else:
            #Handles the case of the split choice being invalid
            bj.read_string("Not a Pair")
            return make_response('', 200)
        
    #Handles the player selecting 'Quit'
    elif button_id == 5:
        #Reads aloud a grading of the player's decision making, hand outcomes, and financial position
        bj.read_string("Your decision making was "+str(bj.correct)+" out of "+str(bj.count)+". Which is "+str(int((bj.correct/bj.count)*100))+" percent.")
        bj.read_string("You won "+str(int((bj.hand_wins/max(1,bj.hand_count-1))*100))+" percent of your hands.")
        bj.read_string("You started with 10 credits and now you have "+str(bj.net)+" credits.")
        time.sleep(1)
        #Displays an ending image on the HTML page
        sending = {'imagePaths': [cardback,cardback,cardback,cardback,cardback,cardback], 'hand_total' : bj.player_total}
        return jsonify(sending)    
    
    #Changes the cards drawn to be from all cards
    elif button_id == 6:
        globals() ['draw_type'] = 1
        return make_response('', 200)
    #Changes the player hand to always contain one ace
    elif button_id == 7:
        globals() ['draw_type'] = 2
        return make_response('', 200)
    #Changes the player hand to always be a pair
    elif button_id == 8:
        globals() ['draw_type'] = 3
        return make_response('', 200)

#Returns a list of image paths to display on the first row of the HTML page
@app.route('/get_image_path_row1', methods=['GET'])
def get_image_path_row1():
    return jsonify(cards1)

#Returns a list of image paths to display on the second row of the HTML page
@app.route('/get_image_path_row2', methods=['GET'])
def get_image_path_row2():
    return jsonify(cards2)

#Resets the game state to a fresh hand after the last hand concludes
@app.route('/reset', methods=['POST'])
def reset():
    bj.read_string("Dealing...")
    initial(globals()['draw_type'])
    return make_response('', 200)

#Advises the player on the optimal decision if a different decision was made
@app.route('/get_message', methods=['POST'])
def send_message():
    button_id = int(request.json['button_id'])

    #Uses strategy tables to find optimal move
    if num2[0] == 12 and num2[0] != num2[1]: 
        actual = bj.soft_key[num2[1]][num1[0]] 
    elif num2[1] == 12 and num2[0] != num2[1]: 
        actual = bj.soft_key[num2[0]][num1[0]]
    elif num2[0] == num2[1] and bj.pair_key[num2[0]][num1[0]] == 1: 
        actual = 4
    else: 
        actual = bj.hard_key[bj.player_total-4][num1[0]]

    #Reads aloud strategy correction if needed
    print("Player Total: "+str(bj.player_total)+",  Player Card Indexes: "+str(num2[0])+",  "+str(num2[1])+",  Dealer Index: "+str(num1[0]))
    print("Computer Says: "+str(actual)+",  Player Says: "+str(button_id))
    response = str("Incorrect, in this position you should "+bj.moves[actual-1])

    #Cancels assessment if button pressed is a non-game move
    if button_id == 5 or button_id == 6 or button_id == 7 or button_id == 8:
        return make_response('', 200)
    bj.count += 1

    #Returns message to HTML page
    if button_id != actual:
        bj.read_string(response)
        return jsonify({'message' : response})
    else: 
        bj.correct += 1
        return jsonify({'message' : "Correct"})

#Determines outcomes of each hand in case of a split
@app.route('/call_split')
def call_split():
    print("Hands: "+str(bj.hands))
    print("Dealer total: "+str(bj.dealer_total))

    #Compares each hand to the dealer's, reads outcomes, and tallies wins/credits won
    for i, score in enumerate(bj.hands):
        if bj.dealer_total == 0 and score != 0:
            bj.read_string("Hand "+str(i+1)+" Win")
            if bj.double_ids[i] == 1:
                bj.net += 4
            else:
                bj.net += 2
            bj.hand_wins += 1
        elif score < bj.dealer_total:
            bj.read_string("Hand "+str(i+1)+" Loss")
        elif score == bj.dealer_total:
            bj.read_string("Hand "+str(i+1)+" Push")
            if bj.double_ids[i] == 1:
                bj.net += 2
            else:
                bj.net += 1
        elif score > bj.dealer_total:
            if bj.double_ids[i] == 1:
                bj.net += 4
            else:
                bj.net += 2
            bj.hand_wins += 1
            bj.read_string("Hand "+str(i+1)+" Win")
    return make_response('', 200)

#Initializes the game state variables
def startup(deck_num=2):
    welcome = "Welcome to the Tutorial Blackjack Simulator"
    global draw_type
    bj.read_string(welcome) 
    print(welcome)
    draw_type = 1
    bj.deck_num = deck_num
    bj.generate_decks(bj.deck_num) 
    bj.net = 10

#Generates cards within a specific range
def cardgen(maximum=12):
    #Uses blackjack_color object's deck stack variables to track decks and remaining cards
    value, card, ind = bj.generate_card(name=True, key=True, maximum=maximum, deck_num=2)
    suit = random.randint(0,3)
    img_ind = ind*4+suit
    #Finds image path for generated card
    image = master_path_reg[img_ind]
    return value, card, image, ind

#Sets up the initial state for each new round
def initial(draw_type=1):
    #Resets hand lists and updates game/credit trackers
    globals()['draw_type'] = draw_type
    bj.net -= 1
    bj.double_bet = False
    bj.hand_count += 1
    bj.double_ids = []
    print("Draw Type: "+str(draw_type))

    global cards1, cards2, face1, face2, num1, num1copy, num2, num2copy, pair_id, values, cardback, hard_total, numb1, numb2, numb3
    
    pair_id = None
    cardback = "static/images/card_back.jpg"
    cards1 = [cardback]
    cards2, face1, face2, num1, num1copy, num2, num2copy, values, bj.hands = [], [], [], [], [], [], [], [], []
    bj.player_total, bj.dealer_total, hard_total = 0, 0, 0

    #Genrates the dealer's hand
    value3, card3, image3, numb3 = cardgen()
    bj.dealer_total = value3
    cards1.append(image3)
    face1.append(card3)
    num1.append(numb3)
    num1copy = num1
    
    #Generates player hand from all possible cards
    if draw_type == 1:
        value1, card1, image1, numb1 = cardgen()
        value2, card2, image2, numb2 = cardgen()
        if numb1 == numb2:
            pair_id = numb1
        values = [value1,value2]
        bj.player_total = value1+value2
        cards2 = [image1,image2]
        face1 = [card3]
        face2 = [card1,card2]
        num2 = [numb1,numb2]
        num2copy = num2
        #Checks for Blackjack
        if bj.player_total == 21 and draw_type == 1: 
            bj.net += 2
            bj.hand_wins += 1
            bj.read_string("BlackJack! Next Hand")
            initial(draw_type)

    #Generates player hand with one ace and another card between 2 and 8
    if draw_type == 2:
        numb1 = 12
        value2, card2, image2, numb2 = cardgen(maximum=6)    
        bj.player_total = int(11 + value2)
        cards2 = [ace_paths[random.randint(0,3)],image2]
        face2 = ["Ace", card2]
        num2 = [numb1, numb2]
        num2copy = num2

    #Generates player hand with only pairs between 2 and 9 possible
    if draw_type == 3:
        value1, card1, image1, numb1 = cardgen(maximum=7)
        values = [value1,value1]
        pair_id = numb1
        numb2 = numb1
        bj.player_total = int(value1 + value1)
        cards2 = [image1,image1]
        face2 = [card1,card1]
        num2 = [numb1,numb1]
        num2copy = num2

    print("Num2 after gen: "+str(num2))

#Finds a usable port to run flask
def available_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

if __name__ == '__main__':
    
    port = available_port()
    startup()
    initial()
    app.run(debug=False, port=port)
