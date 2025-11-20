import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import game
from math import sqrt
import scipy.stats as stats
from statsmodels.stats.proportion import proportions_ztest

def analyze_player(df: pd.DataFrame):

    total_hands = len(df)
    hands_played = players_df.at[i, "hands_played"]

    print("------------------------------------------------")
    print(f"Player {df.iloc[0]["player_id"]} performance:")
    print(f"Using strategy: {players_df.at[i, "strategy"]}")    
    print(f"Playing {hands_played} hand(s) per round")
    print(f"Total rounds: {df.iloc[-1]["round_id"]}")
    print(f"Hands played: {total_hands}")
    # final balance
    print(f"Final player balance: {players_df.at[i, "final_balance"]}")
    # number of wins (blackjacks), losses, pushs
    print(f"Number of wins (blackjacks): {df["hand_result"].isin(["Win", "Blackjack"]).sum()} ({len(df[df["hand_result"] == "Blackjack"])})")
    # number of doubles, splits
    print(f"Number of splits: {total_hands-total_rounds*hands_played}")
    # mean return per hand
    print(f"Average/mean return per hand (bet size): {df["profit/loss"].mean()} ({players_df.at[0, "bet_size"]})")
    print(f"Standard deviation (sample): {df["profit/loss"].std()}")
    # starting hand value with most wins
    best_starting_hand_value = (df[df["hand_result"].isin(["Win"])]
                       .groupby(["hand_start_value"])
                       .hand_result
                       .agg("count")
                       .reset_index(name= "count")
                       .nlargest(1, "count")
                       )
    print(f"Best starting hand value (no of wins): {best_starting_hand_value.iat[0,0]} ({best_starting_hand_value.iat[0,1]})")

def balance_plot():
    
    grouped_df = hands_df.groupby(["round_id", "player_id"])["profit/loss"].sum().reset_index()
    fig, ax = plt.subplots()
    ax.set_xlabel("Round number")
    ax.set_ylabel("Balance")
    for i in range(game_df.at[0, "players"]):

        balance_series = grouped_df.loc[grouped_df["player_id"] == i, "profit/loss"].to_numpy().cumsum()

        ax.plot(np.arange(total_rounds), balance_series, label= f"Player {i} ({players_df.at[i, "strategy"]})")
    ax.legend(loc = "upper left")
    plt.show()

def one_sample_ttest(df: pd.DataFrame):

    profit_data = df["profit/loss"]

    results = stats.ttest_1samp(profit_data, popmean=0)
    cohens_d = results.statistic / sqrt(profit_data.size)
    print(f"Sample size: {profit_data.size}")
    print(f"Cohen's d: {cohens_d:.4f}")
    print(f"Sample estimate (SE): {results._estimate:.4f} ({results._standard_error:.4f})")
    print(f"T value: {results._statistic_np:.4f}")
    print(f"P value: {results.pvalue:.4f}")
    conf_interval = results.confidence_interval()
    print(f"95% Conf. Interval: [{conf_interval.low:.4f}, {conf_interval.high:.4f}]")

def win_rate_proportion_test(df: pd.DataFrame):

    number_of_successes = (df[df["hand_result"].isin(["Blackjack", "Win"])]
                .hand_result
                .size)
    
    print(number_of_successes)
    
    number_of_trials = df.hand_result.size
    
    print(number_of_trials)
    win_rate =  number_of_successes / number_of_trials
    
    print(f"Win rate: {win_rate} vs. Null Hypothesis: 0.42")

    stats, pvalue = proportions_ztest(count=number_of_successes, nobs=number_of_trials, value=0.42)

    print(f"P value: {pvalue:.4f}")
    print(f"Z statistic: {stats:.4f}")


hands_df = pd.read_csv("hand_log.csv")
players_df = pd.read_csv("player_log.csv")
game_df = pd.read_csv("game_log.csv")

total_rounds = game_df["rounds"].iloc[0]

for i in hands_df["player_id"].unique():
    subset_df = hands_df[hands_df["player_id"] == i]
    analyze_player(subset_df)
    #one_sample_ttest(subset_df)
    win_rate_proportion_test(subset_df)

balance_plot()
