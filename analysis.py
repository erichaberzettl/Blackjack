import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import game
from math import sqrt
import scipy.stats as stats


game.main()

hands_df = pd.read_csv("hand_log.csv")
players_df = pd.read_csv("player_log.csv")
game_df = pd.read_csv("game_log.csv")

#print(df.describe())

#print(df["hand_result"].value_counts())
#print(df.groupby("player_id")["profit/loss"].sum())
#print(df["profit/loss"].sum())

total_rounds = game_df["rounds"].iloc[0]
def analyze_player(df: pd.DataFrame):

    total_hands = len(df)
    total_rounds = game_df["rounds"].iloc[0]
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

    one_sample_ttest(i)

    
def balance_plot():
    
    # data: y = int balance , x = number of round
    # plot line for each player
    grouped_df = hands_df.groupby(["round_id", "player_id"])["profit/loss"].sum().reset_index()
    fig, ax = plt.subplots()

    for i in range(game_df.at[0, "players"]):

        balance_series = grouped_df.loc[grouped_df["player_id"] == i, "profit/loss"].to_numpy().cumsum()

        ax.plot(np.arange(total_rounds), balance_series)

    plt.show()

def one_sample_ttest(player_id):

    player_data = hands_df[hands_df["player_id"] == player_id]["profit/loss"]



    results = stats.ttest_1samp(player_data, popmean=0)
    cohens_d = results.statistic / sqrt(player_data.size)
    print(player_data.size, cohens_d)
    print(results)

    print(results.confidence_interval())
    print(results._estimate)




for i in hands_df["player_id"].unique():
    analyze_player(hands_df[hands_df["player_id"] == i])

balance_plot()