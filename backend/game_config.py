from backend.game import Game

def config_sim(session_data: dict):
    
    game = Game(session_data.player_no, 1, session_data.rounds)

    for i, player in enumerate(game.players):
        player.hands_played = session_data.players[i].hands
        player.strategy = session_data.players[i].strat
        player.bet_size = session_data.players[i].bet_size

    game.dealer.hit_soft_17 = True if session_data.dealer_mode == "H17" else False
    game.shoe.decks = session_data.shoe_size
    game.shoe.auto_shuffle = True if session_data.shuffle_mode == "Continous" else False
    game.shoe.penetration_level = session_data.penetration

    return game

