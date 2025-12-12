import streamlit as st
import backend
import pandas as pd

import backend.analysis

st.title("Blackjack Simulator")

st.header(f"Simulation Results")
st.write("Game ID:")
st.code(st.session_state.id, "Python")
analysis = backend.analysis.main(st.session_state.id)

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
        col5.metric("Avg return per hand", value=player_data["mean_return"])
        col2.metric("Number of Blackjacks", value=player_data["blackjacks"])
        col3.metric("Number of wins", value=player_data["wins"])
        col4.metric("Number of splits", value=player_data["splits"])
        
