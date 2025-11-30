import numpy as np
import random, strategies as strat, time, csv
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

    def __init__(self, penetration_level: float = 0.8, decks: int = 4, auto_shuffle = True):
        self.auto_shuffle = auto_shuffle
        self.penetration_level = penetration_level if 0.2 <= penetration_level <= 1 else 0.8
        self.decks = decks if 1 <= decks <= 8 else 4
        self.cards = [card for i in range(decks) for card in Deck().cards]
        self.next_card_index = -1
        self.shuffles = 0
        
    def shuffle(self):
        random.shuffle(self.cards)
        self.next_card_index = -1
        self.shuffles += 1

    def deal(self):

        if self.auto_shuffle:
            return random.choice(self.cards)
        
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
        self.profit = 0
        self.to_resolve = True
        self.actions = ""


    @property
    def start_value(self):
        value = sum(card.value for card in self.cards[:2])
        aces_no = sum(1 for card in self.cards if card.rank == "A")

        if aces_no > 0 and value + 10 <= 21:
            return value + 10

        return value

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

    def __init__(self, id, hands_played = 1, strategy = strat.BASIC_STRAT, bet_size = 1):
        self.id = id
        self.strategy = strategy
        self.balance: float = 0
        self.bet_size = bet_size
        self.split_count = 0
        self.ace_split_count = 0
        self.hands_played: int = hands_played
        self.hands: list[Hand] = [] 

    @property
    def total_split_count(self):
        return self.split_count + self.ace_split_count

    def place_bet(self):
        return 10

    def determine_action(self, hand: Hand, dealer_upcard):

        # we need value of hand and check if ace or pair
        if hand.is_pair(): 
            return self.strategy["pair"][hand.cards[0].value][dealer_upcard]
        elif hand.is_soft():
            return self.strategy["soft"][hand.value][dealer_upcard]
        else:
            return self.strategy["hard"][hand.value][dealer_upcard]

    

class Dealer:

    def __init__(self, hit_soft_17: bool = False):
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

    def __init__(self, player_no: int, hands_per_player: int, rounds: int, blackjack_pays = 1.5, ace_resplit = True, seed = None):
        
        self.seed = seed
        random.seed(seed)
        self.players = [Player(i, hands_per_player) for i in range(player_no)]
        self.dealer = Dealer()
        self.shoe = Shoe()
        self.shoe.shuffle()
        self.rounds = rounds
        self.blackjack_payout = blackjack_pays
        self.allow_ace_resplit = ace_resplit
        self.max_splits = 4
        self.dealer_rule = "Hit all 17" if self.dealer.hit_soft_17 else "Stand on soft 17"
        self.hand_data = []


    def play_round(self):
        # init hands, playout hands, check if hands left, play dealer hand, resolve hands
        print("Initializing hands...")
        total_hands = self.init_hands()
        hands_to_resolve = self.playout_hands(total_hands)

        if hands_to_resolve:
            self.playout_dealer_hand()
            self.resolve_hands(total_hands, self.dealer.hand.value)
        
        self.update_balances(total_hands)

        print([hand.result for hand in total_hands])

        total_hands.append(self.dealer.hand) # append dealer hand for data log

        self.hand_data.append(total_hands)
            
    def new_round_reset(self):

        for player in self.players:
            player.split_count = 0
            player.hands = []

    def playout_dealer_hand(self):

        print("Playing dealer hand...", str(self.dealer.hand))

        while self.dealer.hand.value < (18 if self.dealer.hit_soft_17 else 17):
            self.dealer.hand.add_card(self.shoe)
            print(str(self.dealer.hand))

    def test_split(self):

        split_hand = Hand(self.players[0])
        split_hand.cards = [Card(2, "Spades"), Card(2, "Hearts")]

        self.players[0].hands = [split_hand]

        print("Reset Hand to 2-2:", str(self.players[0].hands[0]))

    def init_hands(self):
        
        total_hands = [] # list of all Hand objects in the round

        for player in self.players:
            for hand in range(player.hands_played):
                hand = Hand(player, player.bet_size)
                hand.add_card(self.shoe)
                player.hands.append(hand)
                total_hands.append(hand)

        # init dealer hand and add 1 card
        self.dealer.hand = Hand(self.dealer, 0)
        self.dealer.hand.add_card(self.shoe)      
        print("Dealer upcard:", str(self.dealer.hand))

        # add second card to each hand
        for hand in total_hands:
            hand.add_card(self.shoe)

        # add second card to dealer hand
        self.dealer.hand.add_card(self.shoe)

        return total_hands
    
    def normal_split(self, hand: Hand, total_hands: list[Hand]):
        # assumes hand parameter is a splittable hand
        # creates a new Hand 
        # one of the split cards is removed from current hand and added to new hand

        if hand.player.total_split_count < self.max_splits:

            hand.player.split_count += 1
            hand.actions += "P"

            new_hand = Hand(hand.player, hand.bet)
            card = hand.cards.pop()
            new_hand.cards.append(card) 

            new_hand.add_card(self.shoe)
            hand.add_card(self.shoe)

            hand_index = total_hands.index(hand)
            total_hands.insert(hand_index + 1, new_hand)
        else:
            hand.to_resolve = False
            # Force Stand
            # TODO Determine action for hard hand


    def ace_split(self, hand: Hand, total_hands: list[Hand]):
        # 3 options: no allow resplit but no split yet, no allow resplit and already split, allow resplit
        if not self.allow_ace_resplit:

            if hand.player.ace_split_count > 0:
                hand.to_resolve = False
                return
            
            hand.player.ace_split_count += 1
            hand.actions += "P"

            new_hand = Hand(hand.player, hand.bet)
            card = hand.cards.pop()
            new_hand.cards.append(card) 

            hand_index = total_hands.index(hand)

            new_hand.add_card(self.shoe)
            hand.add_card(self.shoe)

            if new_hand.is_blackjack():
                new_hand.result = "Win"
            if hand.is_blackjack():
                hand.result = "Win"

            total_hands.insert(hand_index + 1, new_hand)
            new_hand.to_resolve = False
            hand.to_resolve = False

        else:

            if hand.player.total_split_count < self.max_splits:
                hand.player.ace_split_count += 1
                hand.actions += "P"

                new_hand = Hand(hand.player, hand.bet)
                card = hand.cards.pop()
                new_hand.cards.append(card) 

                new_hand.add_card(self.shoe)
                hand.add_card(self.shoe)

                hand_index = total_hands.index(hand)
                total_hands.insert(hand_index + 1, new_hand)

                if new_hand.is_blackjack():
                    new_hand.result = "Win"
                if hand.is_blackjack():
                    hand.result = "Win"
                if not new_hand.is_pair():
                    new_hand.to_resolve = False
                if not hand.is_pair():
                    hand.to_resolve = False

            else:
                hand.to_resolve = False

    
    def playout_hands(self, total_hands: list[Hand]):
        # take each hand and play according to strategy
    
        hands_to_resolve: bool = False

        for hand in total_hands:

            print("\nPlaying hand:", str(hand), "...")

            while hand.to_resolve:

                if hand.is_blackjack():
                    print("Blackjack")
                    hand.result = "Blackjack"
                    hands_to_resolve = True
                    break

                if hand.is_bust():
                    print("Bust")
                    hand.result = "Bust"
                    hand.to_resolve = False
                    break

                action = hand.player.determine_action(hand, self.dealer.upcard.value)
                print("Determined action:", action)
                # Actions: Stand S, Hit H, Double D, Split S 

                match action:
                    case "stand" :
                        print("Stand:", str(hand))
                        hands_to_resolve = True
                        hand.to_resolve = False
                        hand.actions += "S" 

                    case "hit":
                        print("Hit:", str(hand))
                        hand.add_card(self.shoe)
                        hand.actions += "H" 


                    case "double":

                        if len(hand.cards) != 2:
                            hand.add_card(self.shoe)
                            print("Hit (double not possible):", str(hand))
                            hand.actions += "H"
                            
                        else:
                            print("Double:", str(hand))
                            hand.add_card(self.shoe)
                            hand.bet *= 2
                            hand.actions += "D"
                            
                            if hand.is_bust():
                                print("Bust")
                                hand.result = "Bust"
                            else:
                                hands_to_resolve = True

                            hand.to_resolve = False

                    case "split":
                        print("Split:", str(hand))
                        if not hand.is_pair():
                            print("Hand is not a pair")
                            hands_to_resolve = True
                            hand.to_resolve = False
                            hand.actions += "S" 
                            break
                        elif hand.is_pair() and hand.cards[0].rank == "A" and hand.cards[1].rank == "A":    
                            self.ace_split(hand, total_hands)
                        else:
                            self.normal_split(hand, total_hands)

        return hands_to_resolve
                    

    def resolve_hands(self, hands: list[Hand], dealer_hand_value):

        for hand in hands:
            
            if hand.result is None:
                if hand.value > dealer_hand_value or dealer_hand_value > 21:
                    hand.result = "Win" 
                elif hand.value == dealer_hand_value:
                    hand.result = "Push" 
                else:
                    hand.result = "Loss"
                        
            elif hand.result == "Blackjack" and dealer_hand_value == 21:
                hand.result = "Push"
            print(f"Player's {hand.value} vs. dealer's {dealer_hand_value}: {hand.result}")
                

    def update_balances(self, hands: list[Hand]):
        # balances start at 0 and are not changed
        # balance is updated according to a hands outcome
        for hand in hands: 

            match hand.result:
                
                case "Blackjack":
                    hand.player.balance += hand.bet * self.blackjack_payout
                    self.dealer.balance -= hand.bet * self.blackjack_payout
                    hand.profit = hand.bet * self.blackjack_payout
                
                case "Win":
                    hand.player.balance += hand.bet 
                    self.dealer.balance -= hand.bet 
                    hand.profit = hand.bet


                case "Bust" | "Loss":
                    hand.player.balance -= hand.bet
                    self.dealer.balance += hand.bet 
                    hand.profit -= hand.bet

                case _:
                    continue

                
                

    def start(self):

        for i in range(self.rounds):
            print(" ")
            print(f"Playing round {i+1}")
            print("-----------------------------------", end = "\n\n")
            self.play_round()
            self.new_round_reset()

    def export_as_csv(self):
        # create csv with column names
        # append the data for each round accordingly
        # columns: round_id, hand_no, player_id, dealer_upcard, hand_value, hand_result, bet, profit/loss,

        with open("hand_log.csv", "w", newline= "") as file:
            fieldnames = ["round_id", "hand_no", "player_id", "dealer_upcard", "dealer_hand_value", "hand_start_value", "hand_final_value", "hand_result", "actions", "cards", "bet", "profit/loss", "balance"]

            csv_writer = csv.DictWriter(file, fieldnames = fieldnames, extrasaction = "ignore", restval = "")
            csv_writer.writeheader()

            for index, round_hands in enumerate(self.hand_data, start = 1):
                for hand in round_hands[:-1]:
                    csv_writer.writerow({"round_id": index, "player_id": hand.player.id, 
                                         "dealer_upcard": round_hands[-1].cards[0].value, 
                                         "dealer_hand_value": round_hands[-1].value,
                                         "hand_start_value": hand.start_value,
                                          "hand_final_value": hand.value, "hand_result": hand.result, 
                                          "actions": hand.actions, "cards": [card.rank for card in hand.cards],
                                          "bet": hand.bet, "profit/loss": hand.profit})
                
            # basic game info: num of players, hands per player, num of rounds

        with open("player_log.csv", "w", newline= "") as file:
            fieldnames = ["player_id", "hands_played", "bet_size", "strategy", "final_balance"]

            csv_writer = csv.DictWriter(file, fieldnames = fieldnames, extrasaction = "ignore", restval = "")
            csv_writer.writeheader()

            for player in self.players:
                csv_writer.writerow({"player_id": player.id, 
                                     "hands_played": player.hands_played, 
                                     "strategy": player.strategy["name"],
                                     "bet_size": player.bet_size, 
                                     "final_balance": player.balance})
                
        with open("game_log.csv", "w", newline="") as file:
            fieldnames = ["seed", "players", "rounds", "dealer_rule", "blackjack_pays", "decks", "penetration_rate", "dealer_balance", "shuffles"]

            csv_writer = csv.DictWriter(file, fieldnames = fieldnames, extrasaction = "ignore", restval = "")
            csv_writer.writeheader()
            csv_writer.writerow({"players": len(self.players), 
                                 "rounds": self.rounds, 
                                 "dealer_rule": self.dealer_rule, 
                                 "blackjack_pays": self.blackjack_payout, 
                                 "decks": self.shoe.decks, 
                                 "penetration_rate": self.shoe.penetration_level,
                                 "dealer_balance": self.dealer.balance,
                                 "shuffles": self.shoe.shuffles,
                                 "seed": self.seed})
                    


def main():

    game = Game(
        5, 1, 100,
    )
    #game.players[0].strategy = strat.NO_BUST_STRAT
    game.shoe.auto_shuffle = False


    game.start()
    game.export_as_csv()


if __name__ == "__main__":
    main()