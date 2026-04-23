import pandas as pd
import statsmodels as stats
from scipy.stats import ttest_1samp
from statsmodels.stats.proportion import proportions_ztest
import matplotlib.pyplot as plt


def main(game_id: str = "8af4bbcc-2f3f-11f1-90ac-d2dcc4e548ff"):

    global hands_df, players_df, game_df
    hands_df = pd.read_csv(f"data/hand_log_{game_id}.csv",
                           dtype={"round_id": "int32",
                                  "player_id": "int16",
                                  "dealer_upcard": "int8",
                                  "dealer_hand_value": "int8",
                                  "hand_start_value": "int8",
                                  "hand_final_value": "int8",
                                  "bet": "int16",
                                  "profit/loss": "float64",
                                  "hand_result": "category"})

    players_df = pd.read_csv(f"data/player_log_{game_id}.csv")
    game_df = pd.read_csv(f"data/game_log_{game_id}.csv")

    total_analysis = {}
    total_analysis["total_rounds"] = game_df.loc[0, "rounds"]
    total_analysis["total_shuffles"] = game_df.loc[0, "shuffles"]
    total_analysis["dealer_balance"] = game_df.loc[0, "dealer_balance"]
    total_analysis["balance_plot"] = get_balance_plot_data()
    total_analysis["static_balance_plot"] = create_static_balance_plot(total_analysis["balance_plot"])

    players_analysis = {}
    for i in hands_df["player_id"].unique():
        players_analysis[int(i)] = analyze_player(int(i))

    total_analysis["players_analysis"] = players_analysis

    return total_analysis

def get_balance_plot_data():

    players_profit_cumsum = (hands_df
                                .pivot_table(index="round_id",
                                            columns="player_id",
                                            values="profit/loss",
                                            aggfunc="sum")
                                .cumsum())
    
    return players_profit_cumsum   

def create_static_balance_plot(df):

    fig, ax = plt.subplots()
    df.plot(ax=ax, xlabel="Round Number", ylabel="Balance").legend(bbox_to_anchor=(1,1))
    return fig

def create_static_start_hand_freq_plot(players_df):

    fig, ax = plt.subplots()
    df = players_df.hand_start_value.value_counts().sort_index()
    df.plot.bar(ax=ax, xlabel="Start hand value", ylabel="Frequency", figsize=(4,2), rot=0, fontsize=8)
    return fig


def analyze_player(id):

    player_hands_df: pd.DataFrame = hands_df.loc[hands_df["player_id"] == id].reset_index()
    player_metadata_df: pd.DataFrame = players_df.loc[players_df["player_id"] == id].reset_index()
    analysis = {}

    # Player strategy
    analysis["strategy"] = player_metadata_df.at[0, "strategy"]
    # Hands played per round
    analysis["hands_played"] = player_metadata_df.loc[0, "hands_played"]
    # total hands played
    analysis["total_hands"] = player_hands_df.shape[0]
    # bet size
    analysis["bet_size"] = player_metadata_df.loc[0, "bet_size"]

    # final balance
    analysis["final_balance"] =  player_metadata_df.loc[0, "final_balance"]
        # wins
    analysis["result_freqs"] = player_hands_df.hand_result.value_counts().to_dict()

    # doubles
    analysis["double_freq"] = player_hands_df.loc[player_hands_df.actions == "D"].count()
    # splits
    analysis["split_freq"] = player_hands_df.actions.str.startswith("P").sum()

    # mean return
    analysis["mean_return"] = player_hands_df["profit/loss"].mean()
    # Population std
    analysis["std_pop"] = player_hands_df["profit/loss"].std(ddof=0)

    # winner starting hands by wins&blackjacks
    winner_starting_hand_value = (player_hands_df
     .loc[player_hands_df.hand_result.isin(["Blackjack", "Win"])]
     .groupby("hand_start_value")
     .agg({"hand_start_value": "count"})
     .nlargest(3, "hand_start_value")
     .to_dict()["hand_start_value"])
    
    winner_hand_str = ""
    for j, (key, value) in enumerate(winner_starting_hand_value.items(), start=1):
        winner_hand_str += f"{j}. {key} ({value})\n"
    analysis["winner_start_hands"] = winner_hand_str

    # loser starting hands by losss&busts
    loser_starting_hand_value = (player_hands_df
     .loc[player_hands_df.hand_result.isin(["Loss", "Bust"])]
     .groupby("hand_start_value")
     .agg({"hand_start_value": "count"})
     .nlargest(3, "hand_start_value")
     .to_dict()["hand_start_value"])
    
    loser_hand_str = ""
    for j, (key, value) in enumerate(loser_starting_hand_value.items(), start=1):
        loser_hand_str += f"{j}. {key} ({value})\n"
    analysis["loser_start_hands"] = loser_hand_str
    
    # most pushed hands by end value
    push_final_hand_value = (player_hands_df
     .loc[player_hands_df.hand_result == "Push"]
     .groupby("hand_final_value")
     .agg({"hand_final_value": "count"})
     .nlargest(3, "hand_final_value")
     .to_dict()["hand_final_value"])
    
    push_hand_str = ""
    for j, (key, value) in enumerate(push_final_hand_value.items(), start=1):
        push_hand_str += f"{j}. {key} ({value})\n"
    analysis["push_final_hands"] = push_hand_str
    
    # Starting hand frequencies
    analysis["start_hand_freq"] = (player_hands_df.hand_start_value
     .value_counts()
     .to_dict())
    
    analysis["static_start_hand_freq_plot"] = create_static_start_hand_freq_plot(player_hands_df)

    # cumsum profits
    analysis["profit_cumsum"] = (player_hands_df["profit/loss"]
        .cumsum()
        .to_list())
    
    analysis["mean_return_test"] = ttest_mean_return(player_hands_df)
    analysis["win_rate_test"] = proptest_win_rate(player_hands_df)

    return analysis

def ttest_mean_return(player_hands_df: pd.DataFrame):

    results = ttest_1samp(player_hands_df["profit/loss"], popmean=0)
    conf_interval = results.confidence_interval()

    return [results, conf_interval]

def proptest_win_rate(player_hands_df: pd.DataFrame):

    wins = (player_hands_df
            .loc[:,"hand_result"]
            .value_counts()[["Blackjack", "Win"]]
            .sum())
    
    observations = (player_hands_df
                    .loc[:,"hand_result"]
                    .count())

    zstat, pvalue = proportions_ztest(count=wins, nobs=observations, value=0.42)
    return {"winrate": round(wins/observations, 4), "zstat": zstat, "pvalue": pvalue}

if __name__ == "__main__":
    result = main()
    print(result)