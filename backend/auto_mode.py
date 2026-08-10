
def get_action(input_type:str, player=None, hand=None, dealer_upcard=None):

    match input_type:

        case "action":
            
            if hand.is_pair(): 
                return player.strategy["pair"][hand.cards[0].value][dealer_upcard.value]
            elif hand.is_soft():
                return player.strategy["soft"][hand.value][dealer_upcard.value]
            else:
                return player.strategy["hard"][hand.value][dealer_upcard.value]
        
        case "insurance":

            return player.pay_insurance
        
        case "invalid_split":

            return player.strategy["hard"][hand.value][dealer_upcard.value]
        
        case "invalid_double":

            return "H"
        
def no_output(message):
    pass