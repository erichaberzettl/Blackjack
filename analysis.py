import pandas as pd
import game


game.main()

hands_df = pd.read_csv("hand_log.csv")
players_df = pd.read_csv("player_log.csv")

#print(df.describe())

#print(df["hand_result"].value_counts())
#print(df.groupby("player_id")["profit/loss"].sum())
#print(df["profit/loss"].sum())


def analyze_player(df: pd.DataFrame):

    print(f"Player {df.iloc[0]["player_id"]} performance:")
    print("------------------------------------------------")
    # total hands played
    
    df.index[-1]
    
    total_hands = len(df)
    total_rounds = df.iloc[-1]["round_id"]
    print(f"Total rounds: {df.iloc[-1]["round_id"]}")
    print(f"Hands played: {total_hands}")
    # final balance
    print(f"Final player balance: {players_df[players_df["player_id"] == i]["final_balance"]}")
    # number of wins (blackjacks), losses, pushs
    print(f"Number of wins (blackjacks): {df["hand_result"].isin(["Win", "Blackjack"]).sum()} ({len(df[df["hand_result"] == "Blackjack"])})")
    # number of doubles, splits
    print(f"Number of splits: {total_hands-total_rounds}")
    
    #

for i in hands_df["player_id"].unique():
    analyze_player(hands_df[hands_df["player_id"] == i])