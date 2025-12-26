# Blackjack Simulator and Analysis [WIP]

This project is an interactive, customizable Blackjack simulator and analysis platform. It allows users to run large-scale Blackjack games under configurable rules and strategies and then analyze player performance using descriptive statistics, visualizations and hypothesis testing.
A Streamlit web app provides an intuitive interface to run the simulation and explore the results and download the underlying data.
Background on the game:
[Blackjack explained by Britannica](https://www.britannica.com/topic/blackjack-card-game)	

#### Preview
<img width="1633" height="767" alt="Screenshot_BJSim" src="https://github.com/user-attachments/assets/aa89b628-2e25-4f59-8f53-377ecb024a0f" />
<img width="1639" height="798" alt="SC_BJSIMp1" src="https://github.com/user-attachments/assets/813f304b-832b-4116-95bb-6bc5ca750652" />
<img width="1634" height="758" alt="SC_BJSIMp2" src="https://github.com/user-attachments/assets/5ca3244b-b024-44ca-8b3b-52672760af16" />

#### Project Goals
- Simulate Blackjack games correctly and flexibly
- Compare and try out different player strategies
- Apply statistical inference to evaluate the outcome
- Create an easy-to-use web interface for others to use
- Extend the simulation and analysis platform toward prediction models

## Description

The project consists of two parts. First, there is the implementation of the game itself. This is done using OOP in Python. The game is played according to the specified parameters, such as the player's strategy. The simulation results are stored as the following csv files:

1. hands_log.csv: tracking important information on every hand 
2. game_log.csv: basic information about the game parameters and results
3. player_log.csv: basic information about the players and their final balance

In the second part, the analysis layer computes the following:
- Descriptive statistics (returns, number of wins, volatility)
- Visualization of player balance over the course of the simulation
- Hypothesis tests
    - One-sample t-test (mean return vs. zero)
    - Proportion z-test (win rate vs. benchmark)
- (Strategy comparison test)

## Game Parameters 

The simulator can be personalised. Currently, the following parameters can be modified:

**1. Player settings**

* Number of players
* Strategy for each player (Basic Strategy, No Bust Strategy...)
* Number of hands per player per round
* Bet size

**2. General settings**

* Seed for shoe shuffles
* Number of rounds to be played
* Dealer stands or hits a soft 17
* Shoe size
* Shuffle mode (deck penetration, random-card)
* Allow resplitting of aces 
* Blackjack payout 

## CSV structure

1. hands_log.csv: ["round_id", "hand_no", "player_id", "dealer_upcard", "dealer_hand_value", "hand_start_value", "hand_final_value", "hand_result", "actions", "cards", "bet", "profit/loss"]

2. game_log.csv: ["seed", "players", "rounds", "dealer_rule", "blackjack_pays", "decks", "penetration_rate", "dealer_balance", "shuffles"]

3. player_log.csv: ["player_id", "hands_played", "bet_size", "strategy", "final_balance"]

## Notes on interpretation

The results are based on simulated outcomes and not real world gameplay. The game is also played slightly differently around the world. For example, the simulator deals two cards to the dealer before players playout their hands, whereas some casinos only deal the second card after all players have finished their hands.  
The statistical tests assume independence of the sample points, which may not be given. Hands within a round of a single player are not strictly independent. Also dealing cards from a given shoe makes hands dependent. Therefore, there is also the option to draw cards randomly out of the deck. This, in turn, is unrealistic in a casino. 

## License

[MIT](https://choosealicense.com/licenses/mit/)
