import streamlit as st
from backend.game import run_simulation
from backend.game_config import config_sim

st.title("Blackjack Simulator")

st.header("Simlution Configurator")




with st.container():

    c1, c2 = st.columns(2)

    with c1:
        with st.container(border=True):

            st.markdown("Number of players")
            player_no = st.slider(label=" ", min_value=1, max_value=6, value=1, key="player_n")
            st.session_state.player_no = player_no

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
            hands = col2.number_input("Hands per round", min_value=1, max_value = 5, value =st.session_state.players[i]["hands"], key=f"hands{i}")
            strats = ["Basic Strategy", "No Bust Strategy", "Custom"]
            strat = col3.selectbox("Strategy", strats, index=strats.index(st.session_state.players[i]["strat"]), key=f"strat{i}")
            bet_size = col4.number_input("Bet per hand", min_value=1, max_value=100, value= st.session_state.players[i]["bet_size"], key=f"bet{i}")
            st.session_state.players[i]["hands"] = hands
            st.session_state.players[i]["strat"] = strat
            st.session_state.players[i]["bet_size"] = bet_size


col1, col2 = st.columns(2)
with col1:

    with st.container(border=True):
        st.markdown("Dealer: Hit/Stand on soft 17")
        dealer_mode = st.segmented_control(" ", ["S17", "H17"], selection_mode="single", default="S17", width="stretch")
        st.session_state.dealer_mode = dealer_mode  

with col2:
    with st.container(border=True):
        st.markdown("Shoe size")

        shoe_size = st.segmented_control("Number of decks used", [1, 2, 4, 6, 8], selection_mode="single", default= 4, width="stretch")
        st.session_state.shoe_size = shoe_size

col1, col2 = st.columns(2)
with col1:

    with st.container(border=True):
        st.markdown("Blackjack Payout")
        blackjack_payout = st.segmented_control(" ", ["3:2", "6:5", "1:1", "2:1"], selection_mode="single", default="3:2", width="stretch")
        st.session_state.blackjack_payout = blackjack_payout  

with col2:
    with st.container(border=True):
        st.markdown("Ace resplitting")
        ace_resplit = st.radio(" ", [True, False], width="stretch", horizontal=True)
        st.session_state.ace_resplit = ace_resplit


with st.container(border=True):
        st.markdown("Shuffle mode")
        shuffle_mode = st.segmented_control(" ", ["Cut-card", "Continuous"], 
                             selection_mode="single", key="shuffle_mode", default="Cut-card", width="stretch")
        
        auto_shuffle = True if shuffle_mode == "Continuous" else False
        st.session_state.auto_shuffle = auto_shuffle
        st.markdown("Shoe penetration level")
        penetration_level = st.number_input(format="%0.1f", label="Shoe penetration until shuffle as decimal", min_value=0.1, 
                                            max_value=1.0, value=0.8, step=0.1, disabled=auto_shuffle, key="penetration")


st.markdown("#### Rules that can't be changed:")
            
st.markdown("- the dealer is dealt his second cards before the players play")
st.markdown("- double after split is always allowd")
st.markdown("- no surrender or insurance" )
st.markdown("- only natural (initial first 2 cards) Blackjack counts as Blackjack")
st.markdown("- player's Blackjack pushes against dealer's 21")  

st.session_state

    
if st.button("Run Simulation", icon="🔥", use_container_width=True):
    config = config_sim(st.session_state)
    st.session_state["id"] = run_simulation(config)
    st.session_state
    st.switch_page("pages/simulation_results.py")