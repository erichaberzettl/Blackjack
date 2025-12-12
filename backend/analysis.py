import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
import scipy.stats as stats
from statsmodels.stats.proportion import proportions_ztest

def analyze_player(i, df: pd.DataFrame):

    analysis = {}

    total_hands = len(df)
    hands_played = players_df.at[i, "hands_played"]

    print("------------------------------------------------")
    print(f"Player {df.iloc[0]["player_id"]} performance:")
    print(f"Using strategy: {players_df.at[i, "strategy"]}")
    analysis["strat"] = players_df.at[i, "strategy"]
    print(f"Playing {hands_played} hand(s) per round")
    analysis["hands"] = hands_played
    print(f"Total rounds: {df.iloc[-1]["round_id"]}")
    print(f"Hands played: {total_hands}")
    analysis["total_hands"] = total_hands
    analysis["bet"] = players_df.at[i, "bet_size"]

    # final balance
    print(f"Final player balance: {players_df.at[i, "final_balance"]}")
    analysis["final_balance"] = players_df.at[i, "final_balance"]

    # number of wins (blackjacks), losses, pushs
    print(f"Number of wins (blackjacks): {df["hand_result"].isin(["Win", "Blackjack"]).sum()} ({len(df[df["hand_result"] == "Blackjack"])})")
    analysis["wins"] = df["hand_result"].isin(["Win", "Blackjack"]).sum()
    analysis["blackjacks"] = len(df[df["hand_result"] == "Blackjack"])
    # number of doubles, splits
    print(f"Number of splits: {total_hands-total_rounds*hands_played}")
    analysis["splits"] = total_hands - total_rounds*hands_played
    # mean return per hand
    print(f"Average/mean return per hand (bet size): {df["profit/loss"].mean()} ({players_df.at[0, "bet_size"]})")
    analysis["mean_return"] = round(float(df["profit/loss"].mean()), 4)
    print(f"Standard deviation (sample): {df["profit/loss"].std()}")
    analysis["std"] = df["profit/loss"].std()
    # starting hand value with most wins
    winner_starting_hand_value = df[df["hand_result"].isin(["Blackjack", "Win"])].groupby("hand_start_value").hand_result.size().nlargest(3).to_dict()
    analysis["winner_start_hand"] = winner_starting_hand_value
    
    starting_hand_frequencies = (df[["hand_start_value", "hand_result"]]
                    .groupby(["hand_start_value"])
                    .agg("count"))
    analysis["start_hand_freq"] = starting_hand_frequencies.to_dict()["hand_result"]

    print(winner_starting_hand_value)
    print(f"Best starting hand value (no of wins): {winner_starting_hand_value})")

    analysis["cumsum_profit"] = df["profit/loss"].cumsum().to_list()

    return analysis

def balance_plot():
    
    grouped_df = hands_df.groupby(["round_id", "player_id"])["profit/loss"].sum().reset_index()
    fig, ax = plt.subplots()
    ax.set_xlabel("Round number")

    streamlit_plot_df = pd.DataFrame(
        {
            "Round number": np.arange(total_rounds),
        }
    )

    ax.set_ylabel("Balance")
    for i in range(game_df.at[0, "players"]):

        balance_series = grouped_df.loc[grouped_df["player_id"] == i, "profit/loss"].to_numpy().cumsum()
        ax.plot(np.arange(total_rounds), balance_series, label= f"Player {i} ({players_df.at[i, "strategy"]})")

        streamlit_plot_df[f"Player {i}"] = grouped_df.loc[grouped_df["player_id"] == i, "profit/loss"].to_numpy().cumsum()
    ax.legend(loc = "upper left")
    #plt.show()

    return streamlit_plot_df

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

def main(game_id: str):
    global hands_df, players_df, game_df, total_rounds
    hands_df = pd.read_csv(f"data/hand_log_{game_id}.csv")
    players_df = pd.read_csv(f"data/player_log_{game_id}.csv")
    game_df = pd.read_csv(f"data/game_log_{game_id}.csv")

    total_rounds = game_df["rounds"].iloc[0]


    total_analysis = {}
    for i in hands_df["player_id"].unique():
        subset_df = hands_df[hands_df["player_id"] == i]
        player_analysis = analyze_player(i, subset_df)
        total_analysis[int(i)] = player_analysis
        one_sample_ttest(subset_df)
        win_rate_proportion_test(subset_df)

    total_analysis["total_rounds"] = total_rounds
    total_analysis["total_shuffles"] = game_df["shuffles"].iloc[0]
    total_analysis["dealer_balance"] = game_df["dealer_balance"].iloc[0]
    total_analysis["balance_plot_df"] = balance_plot()

    return total_analysis

if __name__ == "__main__":
    main()