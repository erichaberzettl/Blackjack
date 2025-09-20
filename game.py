

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
            return [11, 1]
            
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

    def __init__(self):
        
        self.cards = []

        for rank in [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]:
            for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]:
                self.cards.append(Card(rank, suit))

    def __str__(self):
        dict = []
        for card in self.cards:
            dict.append(str(card))
        return str(dict)


king = Card("A", "Hearts")

print(king.value())

print(str(king))
print([range(2,10), "J", "Q", "K", "A"])

d = Deck()
print(str(d))

print(len(d.cards))
