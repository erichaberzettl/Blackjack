import game as g
import strategies as strats
import scipy.stats as stats
import pandas as pd
import numpy as np

# compare two strategies based on avg return per hand

# power analysis to get sample size

def run_simulation():

    game = g.Game(player_no=2, hands_per_player=1, rounds=10000)
    game.players[0].strategy = strats.BASIC_STRAT
    game.players[1].strategy = strats.NO_BUST_STRAT
    game.shoe.auto_shuffle = False

    game.start()
    game.export_as_csv()

run_simulation()

hands_df = pd.read_csv("hand_log.csv")

player_1_df = hands_df.loc[hands_df["player_id"] == 0, "profit/loss"]
player_2_df = hands_df.loc[hands_df["player_id"] == 1, "profit/loss"]

print(f"Player 1 Variance: {player_1_df.var()} vs. Player 2 Variance: {player_2_df.var()}")

results = stats.ttest_ind(player_1_df, player_2_df, equal_var=True)

print(results)