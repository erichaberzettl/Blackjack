import streamlit as st
import backend
import pandas as pd
import time
import backend.analysis

st.title("Blackjack Simulator")

st.header(f"Simulation Results")


st.write("Game ID:")
try:
    st.code(st.session_state.id, "Python")
except AttributeError:
    st.warning("Please run a valid simulation first!", icon="⚠️")
    time.sleep(5)
    st.switch_page("app.py")
    
try:
    analysis = backend.analysis.main(st.session_state.id)
except FileNotFoundError:
    st.warning("The entered Game ID does not exist. Please try again or configure a new simulation.", icon="⚠️")
    st.stop()
except Exception:
    st.warning("There has been an error retrieving the data. Please try again.", icon="⚠️")
    st.stop()
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
        chart_data = player_data["cumsum_profit"]
        st.metric("Final profit/loss", value=player_data["final_balance"], chart_data=chart_data, chart_type="area")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total hands played", value=player_data["total_hands"])
        col2.metric("Avg return per hand", value=player_data["mean_return"])
        col3.metric("Number of Blackjacks", value=player_data["blackjacks"])
        col4.metric("Number of wins", value=player_data["wins"])
        col5.metric("Number of splits", value=player_data["splits"])
        
        col6, col7, col8, col9, col10 = st.columns(5)
        col6.metric("Standard Deviation", value=player_data["std"])
        col7.metric("Best starting hand", value=list(player_data["winner_start_hand"].keys())[0])

        st.markdown("### Significance Tests")
        st.markdown("#### Is the average return different from 0?")

        st.write("Null hypothesis H0: \mu = 0")
        st.write("Alternative hypothesis H1 != 0")

        st.write("This performs a one sample t-test on the player's profit/loss data. " \
            "It tests if the average return per hand is significantly different from the fair 0 or not")
        col1, col2 = st.columns(2, border=True)
        with col1:
            st.markdown("#### Parameters")
            st.write(f"- Sample size n: {player_data["total_hands"]}")
            st.write(f"- Sample mean: {player_data["return_test"][0]._estimate:.4f}")
            st.write(f"- Standard error: {player_data["return_test"][0]._standard_error:.4f}")
        with col2:
            st.markdown("#### Results")
            st.write(f"- T value: {player_data["return_test"][0]._statistic_np:.4f}")
            st.write(f"- P value: {player_data["return_test"][0].pvalue:.4f}")
            st.write(f"- 95% Confidence interval: [{player_data["return_test"][1].low:.4f}; \
                    {player_data["return_test"][1].high:.4f}]")

        st.markdown("#### Is the winrate different from 0.42?")