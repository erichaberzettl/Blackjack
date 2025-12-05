import streamlit as st
from backend.game import run_simulation
from backend.game_config import config_sim

st.title("Blackjack Simulator")

st.header("Simlution Configurator")




with st.container():

    c1, c2 = st.columns(2)

    if "player_no" not in st.session_state:
        st.session_state.player_no = 1
    with c1:
        with st.container(border=True):
            st.markdown("Number of players")
            st.slider(label=" ", min_value=1, max_value=6, value=1, key="player_no")

    with c2:
        with st.container(border=True):
            st.markdown("Number of rounds")
            rounds = st.slider(label=" ", min_value=1, max_value=10000, value=100, key="rounds")

    if "players" not in st.session_state:
        st.session_state.players = {}
    
    for i in range(st.session_state.player_no):
        
        if i not in st.session_state.players:
            st.session_state.players[i] = {"hands": 1, "strat": "Basic Strategy", "bet_size": 1}

        with st.container(border=True):
            col1, col2, col3, col4 = st.columns([2,3,3,3], gap="small")
            col1.text(f"Player {i+1}")
            hands = col2.selectbox("Hands per round", [1,2,3,4,5], index=st.session_state.players[i]["hands"] -1)
            strats = ["Basic Strategy", "No Bust Strategy", "Custom"]
            strat = col3.selectbox("Strategy", strats, index=strats.index(st.session_state.players[i]["strat"]))
            bet_size = col4.number_input("Bet per hand", min_value=1, max_value=100, value= st.session_state.players[i]["bet_size"])
            st.session_state.players[i]["hands"] = hands
            st.session_state.players[i]["strat"] = strat
            st.session_state.players[i]["bet_size"] = bet_size

            if st.session_state.players[i]["strat"] == "Custom":
                st.popover("Create your own strategy")


col1, col2 = st.columns(2)
with col1:

    with st.container(border=True):
        st.markdown("Dealer: Hit/Stand on soft 17")
    
        st.segmented_control(" ", ["H17", "S17"], selection_mode="single", key="dealer_mode", default="S17", width="stretch")

with col2:
    with st.container(border=True):
        st.markdown("Shoe size")
        st.segmented_control("Number of decks used", [1, 2, 4, 6, 8], selection_mode="single", default= 4, key="shoe_size", width="stretch")


with st.container(border=True):
        st.markdown("Shuffle mode")
        shuffle_mode = st.segmented_control(" ", ["Cut-card", "Continuous"], 
                             selection_mode="single", key="shuffle_mode", default="Cut-card", width="stretch")
        auto_shuffle = True if shuffle_mode == "Continuous" else False
        st.markdown("Shoe penetration level")
        penetration_level = st.number_input(format="%0.1f", label="Shoe penetration until shuffle as decimal", min_value=0.1, 
                                            max_value=1.0, value=0.8, step=0.1, disabled=auto_shuffle, key="penetration")




    
if st.button("Run Simulation", icon="🔥", use_container_width=True):
    st.session_state
    config = config_sim(st.session_state)
    id = run_simulation(config)

    #st.switch_page("pages/simulation_results.py")