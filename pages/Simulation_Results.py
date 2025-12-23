import streamlit as st
import backend
import pandas as pd
import time, os
import backend.analysis
from zipfile import ZipFile
from io import BytesIO

st.set_page_config("Simulation Results", "🂡", layout="wide")

st.title("Blackjack Simulator")

st.header(f"Simulation Results")


st.write("Game ID:")
try:
    st.code(st.session_state.id, "Python")
except AttributeError:
    st.warning("Please run a valid simulation first!", icon="⚠️")
    time.sleep(5)
    st.switch_page("Simulation_Configurator.py")


    
try:
    analysis = backend.analysis.main(st.session_state.id)
except FileNotFoundError:
    st.warning("The entered Game ID does not exist. Please try again or configure a new simulation.", icon="⚠️")
    st.stop()
except Exception:
    st.warning("There has been an error retrieving the data. Please try again.", icon="⚠️")
    st.stop()

def create_zip():
    
    game_id = st.session_state.id
    file_list = [
        f"data/hand_log_{game_id}.csv",
        f"data/player_log_{game_id}.csv",
        f"data/game_log_{game_id}.csv",
    ]

    zip_buffer = BytesIO()

    with ZipFile(zip_buffer, "w") as zipf:
        for file in file_list:
            if not os.path.exists(file):
                st.error(f"Missing file: {file}")
                return None
            zipf.write(file)

    zip_buffer.seek(0)
    return zip_buffer


st.download_button(
    label="Download Zip",
    data=create_zip(),
    file_name=f"data_{st.session_state.id}.zip",
    mime="application/zip",
    icon=":material/download:",
)

tabs = [f"Player {i}" for i in range(st.session_state.player_no)]
tabs.insert(0, "General")
tabs.append("Data")

general, *players, data = st.tabs(tabs)

hands_df = pd.read_csv(f"data/hand_log_{st.session_state.id}.csv")
with data:
    st.dataframe(hands_df)

with general:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total rounds", analysis["total_rounds"])
    col2.metric("Shuffles", analysis["total_shuffles"])
    col3.metric("Final dealer balance", analysis["dealer_balance"])

    st.line_chart(analysis["balance_plot_df"], x="Round number")
    
 
for i, player in enumerate(players):
    if i >= st.session_state.player_no:
        break

    player_data = analysis[int(i)]
    with player:
        st.markdown(f"Player {i} uses **{player_data["strat"]}**, plays **{player_data["hands"]}** hand(s)\
                    with a bet of **{player_data["bet"]}** per round")
        st.markdown("### Metrics")

        chart_data = player_data["cumsum_profit"]
        st.metric("Final profit/loss", value=player_data["final_balance"], chart_data=chart_data, chart_type="area")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total hands played", value=player_data["total_hands"])
        col2.metric("Avg return per hand", value=player_data["mean_return"])
        col3.metric("Number of Blackjacks", value=player_data["blackjacks"])
        col4.metric("Number of wins", value=player_data["wins"])
        col5.metric("Number of splits", value=player_data["splits"])
        
        col1, col2, col3 = st.columns([1,2,2], )
        col1.metric("Standard Deviation", value=player_data["std_pop"])
        col2.metric("Win rate", value=player_data["winrate_test"]["winrate"])

        col1, col2 = st.columns(2)
        col1.markdown("**Most successful starting hand (wins)**")
        col1.write(player_data["winner_start_hand"])
        col2.markdown("**Worst starting hand (losses)**")
        col2.write(player_data["loser_start_hand"])
        
        st.markdown("### Starting hand value frequencies")
        st.bar_chart(player_data["start_hand_freq"], x_label="Starting hand value", y_label="Number of hands")

        st.markdown("### Significance Tests")
        st.markdown("#### Fair game: Is the average return different from 0?")

        col1, col2 = st.columns(2)
        col1.write("Null hypothesis $H_0: \mu_0 = 0$")
        col2.write("Alternative hypothesis $H_1: \mu_0 ≠ 0$")

        st.write("This performs a two-sided one sample t-test on the player's profit/loss data. " \
            "It tests if the average return per hand is significantly different from the fair 0 or not.")
        col1, col2 = st.columns(2, border=True)
        with col1:
            st.markdown("#### Parameters")
            st.write(f"- Sample size: ${player_data["total_hands"]}$")
            st.write(f"- Sample mean: ${player_data["return_test"][0]._estimate:.4f}$")
            st.write(f"- Standard error: ${player_data["return_test"][0]._standard_error:.4f}$")
        with col2:
            st.markdown("#### Results")
            st.write(f"- t value: ${player_data["return_test"][0]._statistic_np:.4f}$")
            st.write(f"- p value: ${player_data["return_test"][0].pvalue:.4f}$")
            st.write(f"- 95% CI: $[{player_data["return_test"][1].low:.4f}; \
                    {player_data["return_test"][1].high:.4f}]$")

        if player_data["return_test"][0].pvalue <= 0.05:
            st.write("At a significance level of $ α = 5\% $ the null hypothesis can be rejected. The average return per hand is probably not 0.")
        else:
            st.write("At a significance level of $ α = 5\% $ the null hypothesis can't be rejected. We can't say that the average return per hand is not 0.")

        st.markdown("#### Is the winrate different from 0.42?")

        col1, col2 = st.columns(2)
        col1.write("Null hypothesis $H_0: p_0 = 0.42$")
        col2.write("Alternative hypothesis $H_1: p_0 ≠ 0.42$")

        st.write("This performs a two-sided one sample proportion test on the player's hand result data. " \
            "The general win rate in Blackjack using Basic Strategy is said to be at around 42%. " \
            "This test checks if the sample proportin supports this hypthesis.")
        col1, col2 = st.columns(2, border=True)
        with col1:
            st.markdown("#### Parameters")
            st.write(f"- Sample size: ${player_data["total_hands"]}$")
            st.write(f"- Sample proportion: ${player_data["winrate_test"]["winrate"]}$")
            st.write(f"- Known proportion: $0.42$")
        with col2:
            st.markdown("#### Results")
            st.write(f"- z value: ${player_data["winrate_test"]["zstat"]:.4f}$")
            st.write(f"- p value: ${player_data["winrate_test"]["pvalue"]:.4f}$")
            st.write(f"- 95% Confidence interval: ")

        if player_data["return_test"][0].pvalue <= 0.05:
            st.write("At a significance level of $ α = 5\% $ the null hypothesis can be rejected. The win rate is probably not 0.42.")
        else:
            st.write("At a significance level of $ α = 5\% $ the null hypothesis can't be rejected. We can't say that the win rate is not 0.42.")
