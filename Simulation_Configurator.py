import streamlit as st
from backend.game_simulation import config_game, run_simulation
st.set_page_config("Configurator", "🂡", layout="wide")
st.title("Blackjack Simulator")
st.header("Simulation Configurator")

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
            rounds = st.slider(label=" ", min_value=1, max_value=100000, value=100, key="rounds")

    if "players" not in st.session_state:
        st.session_state.players = {}
    
    for i in range(st.session_state.player_no):
        
        if i not in st.session_state.players:
            st.session_state.players[i] = {"hands": 1, "strat": "Basic Strategy", "bet_size": 10}

        with st.container(border=True):
            col1, col2, col3, col4, col5= st.columns([2,2,2,2,2], gap="small")
            col1.text(f"Player {i}")
            hands = col2.number_input("Hands per round", min_value=1, max_value = 3, value =st.session_state.players[i]["hands"], key=f"hands{i}")
            strats = ["Basic Strategy", "No Bust Strategy", "Dealer Mimic S17 Strategy", "Dealer Mimic H17 Strategy", "Always Split Strategy", "Custom [WIP]"]
            strat = col3.selectbox("Strategy", strats, index=strats.index(st.session_state.players[i]["strat"]), key=f"strat{i}")
            bet_size = col4.number_input("Bet per hand", min_value=1, max_value=100, value= st.session_state.players[i]["bet_size"], key=f"bet{i}")
            insurance = col5.checkbox("Pay insurance", value=False, key=f"insurance{i}")
            st.session_state.players[i]["hands"] = hands
            st.session_state.players[i]["strategy"] = strat
            st.session_state.players[i]["bet_size"] = bet_size
            st.session_state.players[i]["insurance"] = insurance



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

with st.container(border=True):
    st.markdown("Blackjack Payout")
    blackjack_payout = st.segmented_control(" ", ["3:2", "6:5", "1:1", "2:1"], selection_mode="single", default="3:2", width="stretch")
    st.session_state.blackjack_payout = blackjack_payout  

with st.container(border=True):
        st.markdown("Shoe penetration level")
        penetration_level = st.number_input(format="%0.1f", label="Shoe penetration until shuffle as decimal", min_value=0.1, 
                                            max_value=1.0, value=0.8, step=0.1, key="penetration")

st.markdown("#### Rules that can't be changed:")     
st.markdown("- the dealer is dealt his second card before the players play")
st.markdown("- double after split is always allowed")
st.markdown("- no surrender" )
st.markdown("- player's Blackjack pushes against dealer's blackjack")
st.markdown("- player's Blackjack wins against dealer's 21")  
st.markdown("#### Advice to run a successful simulation:")
st.markdown("- disable static graphs only when running well under 100k total hands")
st.markdown("- Load times with static graphs: 8 seconds / 100k hands")
st.markdown("- Load times with interactive graphs: 20-25 seconds / 100k hands")

game_id_input = st.text_input("Load existing dataset with Game ID:", placeholder="Game ID")
st.session_state["static_graphs"] = st.checkbox("Display static visualizations (Recommended when simulating 10000s of hands)", value=True)

if st.button("Run Simulation", icon="🔥", use_container_width=True):
    config = config_game(st.session_state)
    st.session_state["id"] = game_id_input if game_id_input else run_simulation(config)
    st.switch_page("pages/Simulation_Results.py")