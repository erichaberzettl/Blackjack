import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import game


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

    print("------------------------------------------------")
    print(f"Player {df.iloc[0]["player_id"]} performance:")
    print(f"Using strategy: {players_df.at[i, "strategy"]}")    
    
    total_hands = len(df)
    total_rounds = game_df["rounds"].iloc[0]
    print(f"Total rounds: {df.iloc[-1]["round_id"]}")
    print(f"Hands played: {total_hands}")
    # final balance
    print(f"Final player balance: {players_df.at[i, "final_balance"]}")
    # number of wins (blackjacks), losses, pushs
    print(f"Number of wins (blackjacks): {df["hand_result"].isin(["Win", "Blackjack"]).sum()} ({len(df[df["hand_result"] == "Blackjack"])})")
    # number of doubles, splits
    print(f"Number of splits: {total_hands-total_rounds}")
    
def balance_plot():
    
    # data: y = int balance , x = number of round
    # plot line for each player
    grouped_df = hands_df.groupby(["round_id", "player_id"])["profit/loss"].sum().reset_index()
    fig, ax = plt.subplots()

    for i in range(game_df.at[0, "players"]):

        balance_series = grouped_df.loc[grouped_df["player_id"] == i, "profit/loss"].to_numpy().cumsum()

        ax.plot(np.arange(total_rounds), balance_series)

    plt.show()



for i in hands_df["player_id"].unique():
    print(i)
    analyze_player(hands_df[hands_df["player_id"] == i])

balance_plot()