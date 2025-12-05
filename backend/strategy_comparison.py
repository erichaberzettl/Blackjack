import backend.game as g
import backend.strategies as strats
import scipy.stats as stats
import statsmodels.stats.power as smp
import pandas as pd
import numpy as np

# compare two strategies based on avg return per hand

# power analysis to get sample size

def power_analysis():
    power = smp.TTestIndPower()

    pooled_variance = (((player_1_df.size - 1) * player_1_df.var() 
                       + (player_2_df.size - 1) * player_2_df.var()) 
                        / (player_1_df.size + player_2_df.size - 2))

    d = (player_1_df.mean() - player_2_df.mean()) / np.sqrt(pooled_variance)
    print(f"Calculated Cohen's d: {d:4f}")

    n = power.solve_power(effect_size=0.05, alpha=0.05, alternative="two-sided", power=0.8)
    print(f"Calculated sample size {n:3f}, rounded: {np.ceil(n)}")
    
    return np.ceil(n)

def run_simulation(n):

    game = g.Game(player_no=2, hands_per_player=1, rounds=n)
    game.players[0].strategy = strats.BASIC_STRAT
    game.players[1].strategy = strats.NO_BUST_STRAT
    game.shoe.auto_shuffle = True

    game.start()
    game.export_as_csv()


hands_df = pd.read_csv("hand_log.csv")

player_1_df = hands_df.loc[hands_df["player_id"] == 0, "profit/loss"]
player_2_df = hands_df.loc[hands_df["player_id"] == 1, "profit/loss"]

print(f"Player 1 Variance: {player_1_df.var()} vs. Player 2 Variance: {player_2_df.var()}")

sample_size = power_analysis()

run_simulation(sample_size)


results = stats.ttest_ind(player_1_df, player_2_df, equal_var=True)

print(results)