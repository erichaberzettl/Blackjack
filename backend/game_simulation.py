from backend.game2 import Game, Shoe, Player, Dealer
import backend.auto_mode
import backend.strategies as strats

def config_game(session_data: dict):

    player_list = []
    for i, player in session_data.players.items():

        if i == session_data.player_no:
            break
        player = Player(id=i,     
                        hands_played=player["hands"],
                        bet_size=player["bet_size"],
                        strategy=match_player_strat(player["strategy"]),
                        pay_insurance=player["insurance"])
        
        player_list.append(player)

    decks = session_data.shoe_size or 4
    penetration_level = session_data.penetration or "0.8"
    shoe = Shoe(decks=decks, penetration_level=penetration_level)
    hit_soft_17 = True if session_data.dealer_mode == "H17" else False
    dealer = Dealer(hit_soft_17, shoe=shoe)

    if session_data.blackjack_payout:
        blackjack_pays = float(eval(session_data.blackjack_payout.replace(":", "/")))
    else:
        blackjack_pays = 1.5
    game = Game(players=player_list,
                dealer=dealer,
                rounds=session_data.rounds,
                blackjack_pays=blackjack_pays,
                input_provider=backend.auto_mode.get_action,
                output_provider=backend.auto_mode.output)
    
    return game

def match_player_strat(strategy: str):

    match strategy:
            case "Basic Strategy":
                return strats.BASIC_STRAT
            case "No Bust Strategy":
                return strats.NO_BUST_STRAT
            case "Dealer Mimic S17 Strategy":
                return strats.DEALER_MIMIC_S17_STRAT
            case "Dealer Mimic H17 Strategy":
                return strats.DEALER_MIMIC_H17_STRAT
            case "Always Split Strategy":
                return strats.ALWAYS_SPLIT_STRAT
            case _:
                return strats.BASIC_STRAT

def run_simulation(game: Game):

    game.play(export_data=True)

    return game.id
