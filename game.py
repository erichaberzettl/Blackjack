import numpy as np
import random, strategies as strat


class Card:

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    @property
    def value(self):
        if self.rank in range(2, 11):
            return self.rank
        elif self.rank in ["J", "Q", "K"]:
            return 10
        else:
            return 1 # rank is "A"
            
    def __str__(self):

        match self.suit:
            case "Hearts":
                return f"({self.rank} ❤)"
            case "Diamonds":
                return f"({self.rank} ♦)"
            case "Clubs":
                return f"({self.rank} ♣️)"
            case "Spades":
                return f"({self.rank} ♠️)"
                
        
class Deck:

    def __init__(self, penetration_level: float = 0.8):

        self.penetration_level = penetration_level if 0.2 <= penetration_level <= 1 else 0.8
        ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        self.next_card_index = -1
        self.cards: list[Card] = [Card(rank, suit) for rank in ranks for suit in suits]

    def shuffle(self):
        random.shuffle(self.cards)
        self.next_card_index = -1

    def deal(self):
        self.next_card_index += 1
        if self.next_card_index/52 >= self.penetration_level:
            self.shuffle()        
        return self.cards[self.next_card_index]

    def __str__(self):
        list = [str(card) for card in self.cards]
        return str(list)

 
class Shoe: 

    def __init__(self, penetration_level: float = 0.8, decks: int = 4):
        self.penetration_level = penetration_level if 0.2 <= penetration_level <= 1 else 0.8
        self.decks = decks if 1 <= decks <= 8 else 4
        self.cards = [card for i in range(decks) for card in Deck().cards]
        self.next_card_index = -1
        
    def shuffle(self):
        random.shuffle(self.cards)
        self.next_card_index = -1

    def deal(self):
        self.next_card_index += 1
        if self.next_card_index/(52*self.decks) >= self.penetration_level:
            self.shuffle()
            
        return self.cards[self.next_card_index]
    
class Hand:

    def __init__(self, player, bet = 1):
        self.cards: list[Card] = []
        self.player: Player | Dealer = player
        self.bet = bet

    @property
    def value(self):
        value = sum(card.value for card in self.cards)
        aces_no = sum(1 for card in self.cards if card.rank == "A")

        if aces_no > 0 and value + 10 <= 21:
            return value + 10

        return value

    def add_card(self, shoe: Shoe):
        self.cards.append(shoe.deal())

    def is_blackjack(self):
        return len(self.cards) == 2 and self.value == 21
      
    def is_bust(self):
        return self.value > 21
    
    def is_pair(self):
        return len(self.cards) == 2 and self.cards[0].value == self.cards[1].value
    
    def is_soft(self):

        value = sum(card.value for card in self.cards)
        aces_no = sum(1 for card in self.cards if card.rank == "A")
        return aces_no > 0 and value + 10 < 22

    def __str__(self):
        string = ""
        for card in self.cards:
            string += str(card) + ","
        
        string += f"Value: {self.value}, #Cards: {len(self.cards)}, Bet: {self.bet}, Player: {self.player.id}"

        return string

class Player:

    def __init__(self, id, hands_played = 1):
        self.id = id
        self.strategy = None
        self.balance: float = None
        self.hands_played: int = hands_played
        self.hands: list[Hand] = [] 

    def place_bet():
        ...

    def determine_action(self, hand: Hand, dealer_upcard):

        # we need value of hand and check if ace or pair
        hand_type = None

        if hand.is_pair():
            hand_type = "pair"
            return strat.BASIC_STRAT[hand_type][hand.cards[0].value][dealer_upcard]
        elif hand.is_soft():
            hand_type = "soft"
            return strat.BASIC_STRAT[hand_type][hand.value][dealer_upcard]
        else:
            hand_type = "hard"
            if hand.value > 17:
                return "stand"
            if hand.value < 9:
                return "hit"
            return strat.BASIC_STRAT[hand_type][hand.value][dealer_upcard]

        

    def split():
        ...

class Dealer:

    def __init__(self):
        self.hand: Hand = None
        self.id = 999
        

    

class Game:

    def __init__(self, player_no: int):
        
        self.players = [Player(i) for i in range(player_no)]
        self.dealer = Dealer()
        
        self.shoe = Shoe()
        self.shoe.shuffle()
        self.rounds = 1

    def play_round(self):

        total_player_hands = self.init_hands()

        for hand_no, player in total_player_hands:
            self.playout_hands(hand_no, player)

    def test_split(self):

        split_hand = Hand(self.players[0])
        split_hand.cards = [Card(2, "Spades"), Card(2, "Hearts")]

        self.players[0].hands = [split_hand]

        print("Reset Hand to 2-2:", str(self.players[0].hands[0]))


    def init_hands(self):
        
        total_player_hands = [(hand_no, player) for player in self.players for hand_no in range(player.hands_played)] # list of all hands in the round represented by Player object
        total_hands = [] # list of all Hand objects in the round

        print(total_player_hands)

        # init hands for players and add 1 card to each hand
        for hand_no, player_hand in total_player_hands:
            hand = Hand(player_hand, 1)
            player_hand.hands.append(hand)  
            player_hand.hands[hand_no].add_card(self.shoe)
            total_hands.append(hand)

            print(str(hand))

        # init dealer hand and add 1 card
        self.dealer.hand = Hand(self.dealer, 0)
        self.dealer.hand.add_card(self.shoe)      
        print(str(self.dealer.hand))

        # add second card to each hand
        for hand_no, player_hand in total_player_hands:
            player_hand.hands[hand_no].add_card(self.shoe)

            print(str(player_hand.hands[hand_no]))

        # add second card to dealer hand
        self.dealer.hand.add_card(self.shoe)
        print(str(self.dealer.hand))

        return total_player_hands
    
    def split(self, hand_no, player: Player, current_hand: Hand):

        # creates a new Hand that is added to the players hands list
        # one of the split cards is removed from current hand and added to new hand

        new_hand = Hand(player, current_hand.bet)
        new_hand_no = hand_no + 1
        player.hands.insert(new_hand_no, new_hand) # insert new split hand into hands list of player
        print("New Hand inserted:", str(player.hands[new_hand_no]))
        print("expected hands list length is 2:", len(player.hands))
        split_card = current_hand.cards.pop() # take and remove last card of to-be-splitted hand 
        new_hand.cards.append(split_card) # add this card to new hand
        print("New Hand with one 2:", str(player.hands[new_hand_no]))
        print("old Hand with ond 2:", str(player.hands[hand_no]))

        self.playout_hands(new_hand_no, player)
        #split_count += 1

    
    def playout_hands(self, hand_no, player: Player):
        # take each hand and play according to strategy
    
        current_hand: Hand = player.hands[hand_no]

        while True:
            if current_hand.is_blackjack():
                print("Blackjack")
                break
            if current_hand.is_bust():
                print("Bust")
                break

            action = player.determine_action(current_hand)
            # Actions: Stand S, Hit H, Double D, Split S 

            match action:
                case "Stand":
                    print("Stand")
                    break
                case "Hit":
                    print("Hit")
                    current_hand.add_card(self.shoe)
                case "Double":
                    print("Double")
                    current_hand.add_card(self.shoe)
                    current_hand.bet *= 2
                    break
                case "Split":
                    print("Split")

                    self.split(hand_no, player, current_hand)
                    
                    break


    def resolve_hand():
        ...

    def start(self):

        for _ in range(self.rounds):
            self.init_hands
    ()
    


game = Game(1)


game.play_round()