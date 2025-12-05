import streamlit as st
import pandas as pd

st.title("Blackjack Simulator")

st.header("Simlution Results")

tabs = [f"Player {i}" for i in st.session_state.players]
tabs.insert(0, "General")
tabs.append("Data")

general, *players, data = st.tabs(tabs)

df = pd.read_csv("/Users/eric/Desktop/BJ/hand_log.csv")

with data:
    st.dataframe(df)

with general:

    st.session_state
    st.session_state["player_no"]


