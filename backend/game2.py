import numpy as np
import random, csv, uuid
from . import strategies as strat
from pathlib import Path

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

    def __init__(self, decks: int = 4, penetration_level: float = 0.8 , auto_shuffle = False):
        self.auto_shuffle = auto_shuffle
        self.rng = np.random.default_rng()
        self.penetration_level = penetration_level if 0.2 <= penetration_level <= 1 else 0.8
        self.decks = decks if 1 <= decks <= 8 else 4
        self.cards = [card for i in range(self.decks) for card in Deck().cards]
        self.next_card_index = -1
        self.shuffles = 0
        self.rng.shuffle(self.cards)

    def shuffle(self):
        self.rng.shuffle(self.cards)
        self.next_card_index = 0
        self.shuffles += 1

    def next_card(self):
        
        if self.auto_shuffle:
            return self.rng.choice(self.cards, 1)
        
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
    
    def add_card(self, card: Card):
        self.cards.append(card)

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

    def is_valid_double(self):
        return len(self.cards) == 2

    def is_valid_split(self,):
        return self.is_pair()

    def __str__(self):
        string = ""
        for card in self.cards:
            string += str(card) + ", "
        
        string += f"Value: {self.value}, #Cards: {len(self.cards)}, Bet: {self.bet}, Player: {self.player.id}"

        return string

class Player:

    def __init__(self, id = 1, hands_played: int = 1, strategy = strat.BASIC_STRAT, bet_size: int = 1, pay_insurance = False):
        self.id = id
        self.strategy = strategy
        self.balance: float = 0
        self.bet_size = bet_size
        self.hands_played: int = hands_played
        self.hands: list[Hand] = [] 
        self.pay_insurance = pay_insurance

    @property
    def total_split_count(self):
        return self.normal_split_count + self.ace_split_count
    
    def get_bet_size(self):
        return self.bet_size

    def determine_action(self, hand: Hand, dealer_upcard):

        # we need value of hand and check if ace or pair
        if hand.is_pair(): 
            return self.strategy["pair"][hand.cards[0].value][dealer_upcard]
        elif hand.is_soft():
            return self.strategy["soft"][hand.value][dealer_upcard]
        else:
            return self.strategy["hard"][hand.value][dealer_upcard]

class Dealer:

    def __init__(self, hit_soft_17: bool = False, shoe = Shoe()):
        self.hand: Hand = None
        self.shoe = shoe
        self.id = 999
        self.balance = 0
        self.hit_soft_17 = hit_soft_17

    @property
    def upcard(self):
        if self.hand.cards[0]:
            return self.hand.cards[0]
        else:
            return None    
        
    def is_insurance_case(self):
        return self.upcard.rank == "A"
    
    def deal(self):
        return self.shoe.next_card()

    def hit_hand(self, hand: Hand):
        hand.add_card(self.deal())
        hand.actions += "H"

    def stand_hand(self, hand: Hand):
        hand.actions += "S"

    def double_hand(self, hand: Hand):
        hand.add_card(self.deal())
        hand.player.balance -= hand.bet
        hand.bet *= 2 
        hand.actions += "D"

    def split_hand(self, hand: Hand): # creates new hand and appends to player hands, returns True if aces were splitted
        hand.actions += "P"

        new_hand = Hand(hand.player, bet = hand.bet)
        hand.player.balance -= hand.bet
        split_card = hand.cards.pop()
        new_hand.cards.append(split_card)
        
        hand.add_card(self.deal())
        new_hand.add_card(self.deal())

        if split_card.rank == "A":
            hand.player.hands.insert(hand.player.hands.index(hand), new_hand) # insert hand before old hand
            return True
        else:
            hand.player.hands.insert(hand.player.hands.index(hand) + 1, new_hand) # insert hand after old hand
        

    def play_hand(self):

        while self.hand.value < 17:
            self.hand.add_card(self.deal()) 

        if self.hit_soft_17 and self.hand.value == 17 and self.hand.is_soft():
            self.hand.add_card(self.deal())

    
    

class Game:

    def __init__(self, players: list[Player], dealer: Dealer, debug_mode = True, rounds = 1, blackjack_pays = 1.5, input_provider = None, output_provider = None):
        self.id = uuid.uuid1()
        self.players = players
        self.dealer = dealer
        self.debug = debug_mode
        self.rounds = rounds
        self.blackjack_pays = blackjack_pays
        self.input_provider = input_provider
        self.output_provider = output_provider
        self.hand_data = []

    def play(self, export_hand_data=True, export_meta_data=True):

        with open(f"data/hand_log_{self.id}.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["round_id", "player_id", "dealer_upcard", "dealer_hand_value", "hand_start_value", "hand_final_value", "hand_result", "actions", "cards", "bet", "profit/loss"])
            writer.writeheader()
            for i in range(1, self.rounds+1):
                self.play_round()
                if export_hand_data:
                    self.write_hands(writer, self.hand_data, i)
                self.hand_data = []

        if export_meta_data:
            self.write_metadata_to_csv()
    
    def write_hands(self, writer, round_hands, round_index):

        for hand in round_hands:
            writer.writerow({"round_id": round_index, "player_id": hand.player.id, 
                                    "dealer_upcard": round_hands[-1].cards[0].value, 
                                    "dealer_hand_value": round_hands[-1].value,
                                    "hand_start_value": hand.start_value,
                                    "hand_final_value": hand.value, "hand_result": hand.result, 
                                    "actions": hand.actions, "cards": [card.rank for card in hand.cards],
                                    "bet": hand.bet, "profit/loss": hand.profit})

    def play_round(self):

        # 1. Deal cards
        self.deal_cards()
        # 2. Handle insurance
        insurance_players = self.handle_insurance()
        # 3. Play player hands
        play_dealer_hand = self.play_hands()
        # 4. Play dealer hand
        if play_dealer_hand:
            self.output_provider(f"--> Now playing Dealer hand: {self.dealer.hand}")
            self.dealer.play_hand()
            self.output_provider(f"\t{str(self.dealer.hand)}")
        else:
            self.output_provider(f"\tDealer hand: {str(self.dealer.hand)}")
        # 4.5 Resolve possible insurance
        if self.dealer.hand.is_blackjack():
            self.resolve_insurance(insurance_players)
        # 5. Settle bets
        self.resolve_hands()

        
                

    def play_hands(self) -> bool: # returns if dealer hand has to be played
        
        # how to handle blackjack? 
        # player blackjack payed out immediately if dealer cannot have blackjack
        # player blackjack pushes against dealer blackjack and wins against dealer 21 (with 3+ cards)
        # player with blackjack can buy insurance
        # play each hand according to user input and valid ioptions, play while not bust or not 21
        # flag if dealer has to play hand or not
        
        play_dealer_hand_flag = False

        for player in self.players:
            
            for hand in player.hands:
                
                self.output_provider(f"--> Now playing {player.id=}: {hand}")
                # identify blackjack 
                if hand.is_blackjack():
                    self.output_provider(f"\t 21 Blackjack 21")
                    continue
                play_dealer_hand_flag = True
                hand_is_open = True
                while hand_is_open:

                    action = self.input_provider(input_type="action", player=player, hand=hand, dealer_upcard=self.dealer.upcard)

                    try:
                        ace_split_flag = self.execute_user_action(action, hand)

                        if action == "S" or hand.value == 21:
                            
                            hand_is_open = False

                        if hand.value > 21:
                            hand_is_open = False
                        
                        if action == "D":
                            hand_is_open = False

                        if action == "P" and ace_split_flag:
                            hand_is_open = False

                    except Exception as e:
                        
                        self.output_provider(f"Exception caught: {e.args}")

        return play_dealer_hand_flag
                        
    def deal_cards(self):# deals all players and the dealer 2 cards in correct order, deducts hand bets from player balance

        # get bet for each player for each hand
        # 1. deal cards: for each player, for each hand + for dealer
        # dealer hand
        
        for player in self.players:
            # reset player hands each round
            player.hands.clear()

            for _ in range(player.hands_played):
                hand = Hand(player, player.get_bet_size())
                hand.add_card(self.dealer.deal()) 
                player.hands.append(hand)
                player.balance -= hand.bet

        
        hand = Hand(self.dealer, 0)
        hand.add_card(self.dealer.deal()) 
        self.dealer.hand = hand

        for player in self.players:
            
            for hand in player.hands:
        
                hand.add_card(self.dealer.deal()) 
                
                self.output_provider(str(hand))
            
        self.dealer.hand.add_card(self.dealer.deal())
        self.output_provider(str(self.dealer.hand))

    def handle_insurance(self):# checks if insurance is possible and asks players for insurance if yes

        if self.dealer.is_insurance_case():

            self.output_provider(f"Insurance Case: {self.dealer.upcard.rank=}")

            return self.ask_insurance()  
        else:
            return []

    def ask_insurance(self): # asks each player if they want to pay insurance and deducts insurance from player balance
        insurance_payed_players = []
        for player in self.players:
            pay_insurance = self.input_provider(input_type="insurance", player=player)
            if pay_insurance:
                player.balance -= (amount:=(player.get_bet_size() * player.hands_played / 2))
                insurance_payed_players.append((player, amount))

                self.output_provider(f"{player.id=} pays {player.get_bet_size() * player.hands_played / 2} insurance")

        return insurance_payed_players
    
    def resolve_insurance(self, insurance_players: list[tuple[Player, float]]):

        if self.dealer.hand.is_blackjack():
            # pay insurance
            for player, insurance_amount in insurance_players:
                player.balance += 2* insurance_amount 

                self.output_provider(f"Insurance payed: new {player.id=} balance is {player.balance}") 

    def execute_user_action(self, action, hand: Hand):
        # match action to following exectuion of action

        match action:
            case "S":
                self.dealer.stand_hand(hand)
                self.output_provider("\tStand")

            case "H":
                self.dealer.hit_hand(hand)
                self.output_provider("\tHit")
                self.output_provider(f"\t{str(hand)}")

            case "P":
                if hand.is_valid_split():
                    ace_split_flag = self.dealer.split_hand(hand)
                    
                    self.output_provider("\tSplit")
                    self.output_provider(f"\t{str(hand)}")
                    return ace_split_flag
                else:
                    action = self.input_provider("invalid_split", player=hand.player, hand=hand, dealer_upcard=self.dealer.upcard)
                    self.execute_user_action(action, hand)

            case "D":
                if hand.is_valid_double():
                    self.dealer.double_hand(hand)

                    self.output_provider("\tDouble")
                    self.output_provider(f"\t{str(hand)}")
                else:
                    action = self.input_provider("invalid_double", player=hand.player, hand=hand, dealer_upcard=self.dealer.upcard)
                    self.execute_user_action(action, hand)
            
        return False

    def resolve_hands(self):

        dealer_val = self.dealer.hand.value
        
        for player in self.players:
            
            self.output_provider(f"Current balance of player {player.id}: {player.balance}")

            for hand in player.hands:

                if hand.is_blackjack():
                    if self.dealer.hand.is_blackjack():
                        hand.result = "Push"
                        hand.player.balance += hand.bet
                        hand.profit = 0
                        
                    else:
                        hand.result = "Blackjack"
                        hand.player.balance += 2.5 * hand.bet
                        hand.profit = 1.5 * hand.bet
                        self.dealer.balance -=  1.5 * hand.bet
                    
                    self.output_provider(f"Player's {hand.value} vs. Dealer's {dealer_val}: {hand.result}")
                    self.hand_data.append(hand)
                    continue

                if (x:=hand.value) > 21: # bust player
                    hand.result = "Bust"
                    hand.profit = - hand.bet
                    self.dealer.balance += hand.bet

                elif (dealer_val > 21) or dealer_val < x: # bust dealer or better hand
                    hand.result = "Win"
                    hand.player.balance += 2 * hand.bet
                    hand.profit = hand.bet
                    self.dealer.balance -= hand.bet

                elif (dealer_val > x): # loss
                    hand.result = "Loss"
                    hand.profit = - hand.bet
                    self.dealer.balance += hand.bet
                
                elif (x == dealer_val): # push
                    hand.result = "Push"
                    hand.player.balance += hand.bet
                    hand.profit = 0
                else:
                    raise Exception(f"Unclassified hand: {hand.value=}, {dealer_val=}")

                self.output_provider(f"Player's {hand.value} vs. Dealer's {dealer_val}: {hand.result}")
                self.hand_data.append(hand)

            self.output_provider(f"New balance of player {player.id}: {player.balance}")  

    def write_metadata_to_csv(self):

        with open(f"data/player_log_{self.id}.csv", "w", newline= "") as file:
            fieldnames = ["player_id", "hands_played", "bet_size", "strategy", "final_balance"]

            csv_writer = csv.DictWriter(file, fieldnames = fieldnames, extrasaction = "ignore", restval = "")
            csv_writer.writeheader()

            for player in self.players:
                csv_writer.writerow({"player_id": player.id, 
                                    "hands_played": player.hands_played, 
                                    "strategy": player.strategy["name"],
                                    "bet_size": player.bet_size, 
                                    "final_balance": player.balance})
                
        with open(f"data/game_log_{self.id}.csv", "w", newline="") as file:
            fieldnames = ["seed", "players", "rounds", "dealer_rule", "blackjack_pays", "decks", "penetration_rate", "dealer_balance", "shuffles"]

            csv_writer = csv.DictWriter(file, fieldnames = fieldnames, extrasaction = "ignore", restval = "")
            csv_writer.writeheader()
            csv_writer.writerow({"players": len(self.players), 
                                "rounds": self.rounds, 
                                "dealer_rule": self.dealer.hit_soft_17, 
                                "blackjack_pays": self.blackjack_pays, 
                                "decks": self.dealer.shoe.decks, 
                                "penetration_rate": self.dealer.shoe.penetration_level,
                                "dealer_balance": self.dealer.balance,
                                "shuffles": self.dealer.shoe.shuffles,
                                })
                    
    def write_round_to_csv(self, round_hands, round_index):

        file_exists = Path(f"data/hand_log_{self.id}.csv").exists()
        with open(f"data/hand_log_{self.id}.csv", "a", newline= "") as file:

            fieldnames = ["round_id", "player_id", "dealer_upcard", "dealer_hand_value", "hand_start_value", "hand_final_value", "hand_result", "actions", "cards", "bet", "profit/loss"]

            csv_writer = csv.DictWriter(file, fieldnames = fieldnames, extrasaction = "ignore", restval = "")

            if not file_exists:
                csv_writer.writeheader()
            
            for hand in round_hands[:-1]:
                csv_writer.writerow({"round_id": round_index, "player_id": hand.player.id, 
                                        "dealer_upcard": round_hands[-1].cards[0].value, 
                                        "dealer_hand_value": round_hands[-1].value,
                                        "hand_start_value": hand.start_value,
                                        "hand_final_value": hand.value, "hand_result": hand.result, 
                                        "actions": hand.actions, "cards": [card.rank for card in hand.cards],
                                        "bet": hand.bet, "profit/loss": hand.profit})
                

