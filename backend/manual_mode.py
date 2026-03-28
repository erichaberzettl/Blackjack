import sys

def get_input(input_type:str, hand= None, player = None, dealer_upcard = None) -> str:

    match input_type:

        case "action":
            action = None 
            fail_counter = 0

            while action not in ["S", "H", "P", "D"] and fail_counter < 10:
                action = input((f"\tAction required: Dealer's {dealer_upcard.value} vs. Player's {hand.value}\n\tS = Stand | H = Hit | P = Split | D = Double: ")).strip().upper()
                fail_counter += 1

            if fail_counter == 10 and action not in ["S", "H", "P", "D"]:
                print("You failed to enter a valid input 10 times. You are unworthy of playing. Bye.")
                sys.exit()
            
            return action

        case "insurance":
            return input(f"Pay insurance for all hands of player {player.id} (Y/N) ? ") == "Y"

        case "invalid_split":
            print("Error: Split not allowed!")
            action = None 
            fail_counter = 0

            while action not in ["S", "H", "D"] and fail_counter < 10:
                action = input((f"\tAction required: Dealer's {dealer_upcard.value} vs. Player's {hand.value}\n\tS = Stand | H = Hit | D = Double: ")).strip().upper()
                fail_counter += 1

            if fail_counter == 10 and action not in ["S", "H", "D"]:
                print("You failed to enter a valid input 10 times. You are unworthy of playing. Bye.")
                sys.exit()
            
            return action
        
        case "invalid_double":
            print("Error: Split not allowed!")
            action = None 
            fail_counter = 0

            while action not in ["S", "H"] and fail_counter < 10:
                action = input((f"\tAction required: Dealer's {dealer_upcard.value} vs. Player's {hand.value}\n\tS = Stand | H = Hit: ")).strip().upper()
                fail_counter += 1

            if fail_counter == 10 and action not in ["S", "H"]:
                print("You failed to enter a valid input 10 times. You are unworthy of playing. Bye.")
                sys.exit()
            
            return action


def output(message):
    print(message)