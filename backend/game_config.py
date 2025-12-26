from backend.game import Game, Shoe
import backend.strategies as strats

def config_sim(session_data: dict):
    
    game = Game(session_data.player_no, 1, session_data.rounds)

    for i, player in enumerate(game.players):
        
        player.bet_size = session_data.players[i]["bet_size"]

        match session_data.players[i]["strat"]:
            case "Basic Strategy":
                player.strategy = strats.BASIC_STRAT
            case "No Bust Strategy":
                player.strategy = strats.NO_BUST_STRAT
            case "Dealer Mimic S17 Strategy":
                player.strategy = strats.DEALER_MIMIC_S17_STRAT
            case "Dealer Mimic H17 Strategy":
                player.strategy = strats.DEALER_MIMIC_H17_STRAT
            case "Always Split Strategy":
                player.strategy = strats.ALWAYS_SPLIT_STRAT
            case _:
                player.strategy = strats.BASIC_STRAT

        player.hands_played = session_data.players[i]["hands"]

    
    decks = session_data.shoe_size or 4
    auto_shuffle = session_data.auto_shuffle or False
    penetration_level = session_data.penetration or "0.8"
    shoe = Shoe(decks=decks, penetration_level=penetration_level, auto_shuffle=auto_shuffle)
    game.shoe = shoe

    game.dealer.hit_soft_17 = True if session_data.dealer_mode == "H17" else False
    game.allow_ace_resplit = session_data.ace_resplit or "True"
    
    if session_data.blackjack_payout:
        game.blackjack_payout = float(eval(session_data.blackjack_payout.replace(":", "/")))
    else:
        game.blackjack_payout = 1.5
    
    return game
