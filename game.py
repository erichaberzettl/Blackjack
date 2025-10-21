import numpy as np
import random, strategies as strat, time
from collections import deque


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
        self.result = None

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
            string += str(card) + ", "
        
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
            return strat.BASIC_STRAT["pair"][hand.cards[0].value][dealer_upcard]
        elif hand.is_soft():
            return strat.BASIC_STRAT["soft"][hand.value][dealer_upcard]
        else:
            if hand.value >= 17:
                return "stand"
            if hand.value <= 8:
                return "hit"
            return strat.BASIC_STRAT["hard"][hand.value][dealer_upcard]

    

class Dealer:

    def __init__(self, hit_soft_17: bool = True):
        self.hand: Hand = None
        self.id = 999
        self.balance = 0
        self.hit_soft_17 = hit_soft_17

    @property
    def upcard(self):
        if self.hand.cards[0]:
            return self.hand.cards[0]
        else:
            return None    



class Game:

    def __init__(self, player_no: int, hands_per_player: int, rounds: int, blackjack_pays = 1.5):
        
        self.players = [Player(i, hands_per_player) for i in range(player_no)]
        self.dealer = Dealer()
        self.shoe = Shoe()
        self.shoe.shuffle()
        self.rounds = rounds
        self.blackjack_payout = blackjack_pays
        round_data = []

    def play_round(self):
        # init hands, playout hands, check if hands left, play dealer hand, resolve hands
        print("Initializing hands...")
        total_player_hands = self.init_hands()
        hands_to_resolve = self.playout_hands(total_player_hands)


        time.sleep(3)
        # check first if there is an open hand left

        if hands_to_resolve:
            self.playout_dealer_hand()

            self.resolve_hands(total_player_hands, self.dealer.hand.value)

        print([hand.result for hand in total_player_hands])

            

    def playout_dealer_hand(self):

        print("Playing dealer hand...")
        print(str(self.dealer.hand))
        time.sleep(3)
        while self.dealer.hand.value <= 17:
            self.dealer.hand.add_card(self.shoe)
            print(str(self.dealer.hand))

    def test_split(self):

        split_hand = Hand(self.players[0])
        split_hand.cards = [Card(2, "Spades"), Card(2, "Hearts")]

        self.players[0].hands = [split_hand]

        print("Reset Hand to 2-2:", str(self.players[0].hands[0]))


    def init_hands(self):
        
        total_player_hands = [(hand_no, player) for player in self.players for hand_no in range(player.hands_played)] # list of all hands in the round represented by Player object
        total_hands = [] # list of all Hand objects in the round

        # init hands for players and add 1 card to each hand
        for hand_no, player_hand in total_player_hands:
            hand = Hand(player_hand, 1)
            player_hand.hands.append(hand)  
            player_hand.hands[hand_no].add_card(self.shoe)
            total_hands.append(hand)


        # init dealer hand and add 1 card
        self.dealer.hand = Hand(self.dealer, 0)
        self.dealer.hand.add_card(self.shoe)      
        print("Dealer upcard:", str(self.dealer.hand))

        # add second card to each hand
        for hand_no, player_hand in total_player_hands:
            player_hand.hands[hand_no].add_card(self.shoe)


        # add second card to dealer hand
        self.dealer.hand.add_card(self.shoe)

        return total_hands
    
    def split(self, hand: Hand, total_hands: list[Hand]):
        # assumes hand parameter is a splittable hand
        # creates a new Hand 
        # one of the split cards is removed from current hand and added to new hand

        new_hand = Hand(hand.player, hand.bet)
        
        card = hand.cards.pop()
        hand_index = total_hands.index(hand)

        new_hand.cards.append(card) 

        # Special case: split aces -> only one more card
        if card.rank == "A":
            new_hand.add_card(self.shoe)
            hand.add_card(self.shoe)
            total_hands.remove(hand)
        else:
            total_hands.insert(hand_index + 1, new_hand)
        #split_count += 1

    
    def playout_hands(self, total_hands: list[Hand]):
        # take each hand and play according to strategy
    
        hands_to_resolve: bool = False

        for hand in total_hands:

            print("Playing hand:", str(hand), "...")
            time.sleep(3)

            while True:
                if hand.is_blackjack():
                    print("Blackjack")
                    hand.result = "Blackjack"
                    hands_to_resolve = True
                    break
                if hand.is_bust():
                    print("Bust")
                    hand.result = "Bust"
                    break

                action = hand.player.determine_action(hand, self.dealer.upcard.value)
                print("Determined action:", action)
                # Actions: Stand S, Hit H, Double D, Split S 

                match action:
                    case "stand" :
                        print("Stand")
                        hands_to_resolve = True
                        break
                    case "hit":
                        hand.add_card(self.shoe)
                        print("Hit:", str(hand))
                        time.sleep(2)

                    case "double":

                        if len(hand.cards) != 2:
                            hand.add_card(self.shoe)
                            print("Hit (double not possible):", str(hand))
                            
                        else:
                            hand.add_card(self.shoe)
                            hand.bet *= 2
                            print("Double:", str(hand))
                            
                            if hand.is_bust():
                                print("Bust")
                                hand.result = "Bust"
                            else:
                                hands_to_resolve = True

                            break

                    case "split":
                        print("Split")
                        # new split hand has to be created and inserted into the hands queue
                    
                        self.split(hand, total_hands)

                        


        return hands_to_resolve
                    
                    


    def resolve_hands(self, hands: list[Hand], dealer_hand_value):
        

        for hand in hands:
            if hand.result is None:
                if hand.value > dealer_hand_value | dealer_hand_value > 21:
                    hand.result = "Win" 
                elif 21 >= hand.value == dealer_hand_value:
                    hand.result = "Push" 
                else:
                    hand.result = "Loss"
                
                
            elif hand.result == "Blackjack" and dealer_hand_value == 21:
                hand.result = "Push"
                

    def update_balances(self, hands: list[Hand]):
        # balances start at 0 and are not changed
        # balance is updated according to a hands outcome
        for hand in hands: 

            match hand.result:
                case "Blackjack":
                    hand.player.balance += hand.player.bet * self.blackjack_payout
                    self.dealer.balance -= hand.player.bet * self.blackjack_payout
                
                case "Win":
                    hand.player.balance += hand.player.bet 
                    self.dealer.balance -= hand.player.bet 


                case "Bust" | "Loss":
                    hand.player.balance -= hand.player.bet
                    self.dealer.balance += hand.player.bet 

                case _:
                    continue

            
    



    def start(self):

        for _ in range(self.rounds):
            self.init_hands


if __name__ == "__main__":

    game = Game(
        1, 1, 2
    )


    game.play_round()