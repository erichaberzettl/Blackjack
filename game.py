import numpy as np
import random


class Card:

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def value(self):
        if self.rank in range(2, 10):
            return self.rank
        elif self.rank in ["J", "Q", "K"]:
            return 10
        else:
            return 1 #TODO
            
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

    rng = np.random.default_rng()

    def __init__(self, penetration_level: float = 0.8):

        self.penetration_level = penetration_level if 0.2 <= penetration_level <= 1 else 0.8
        ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        self.next_card_index = -1
        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]

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
        self.cards = []
        self.player = player
        self.bet = bet

    def value(self):
        value = 0

        for card in self.cards:
            value += card.value()

        return value

    def add_card(self, shoe: Shoe):
        self.cards.append(shoe.deal())

    def is_blackjack(self):
        return True if len(self.cards) == 2 and self.value() == 21 else False
      
    def is_bust(self):
        return True if self.value() > 21 else False

    def __str__(self):
        string = ""
        for card in self.cards:
            string += str(card) + ","
        
        string += f"Value: {self.value()}, #Cards: {len(self.cards)}, Bet: {self.bet}"

        return string

class Player:

    def __init__(self, id, hands_played = 1):
        self.id = id
        self.strategy = None
        self.balance = None
        self.hands_played = hands_played
        self.hands = [] 

    def place_bet():
        ...

    def determine_action():
        ...

    def split():
        ...

class Dealer:

    def __init__(self):
        ...

    

class Game:

    def __init__(self, player_no: int):
        
        self.players = [Player(i) for i in range(player_no)]
        self.dealer = Dealer()
        self.shoe = Shoe()
        self.shoe.shuffle()
        self.rounds = 1

    def play_round(self):
        
        total_player_hands = [player for player in self.players for hand in range(player.hands_played)]

        print(total_player_hands)
        # give each player one card

    def resolve_hand():
        ...

    def start(self):

        for _ in range(self.rounds):
            self.play_round()
    


    


    



shoe = Shoe()
shoe.shuffle()
hand = Hand(10)

hand.add_card(shoe)
print(str(hand))
print(shoe.next_card_index)

hand.add_card(shoe)
print(str(hand))
print(shoe.next_card_index)


game = Game(3)

game.players[0].hands_played = 1
game.players[1].hands_played = 2
game.players[2].hands_played = 3

game.play_round()